# Behavioral Data Schema — Daily Nonogram

## Design Principles

1. **Log behavior, not inferences.** Record "player filled cell (3,5) after 892ms hesitation" — not "player was uncertain." Inference happens downstream.
2. **Two-tier capture.** Action events (every cell interaction) + pointer stream (sampled at 10Hz, not 60Hz — balances signal quality vs. storage).
3. **Errors shown immediately.** Cell flashes red on wrong fill. Captures error recovery, retry speed, persistence. Avoids early frustration.
4. **Stable outer schema, flexible inner payload.** Following OpenGameData pattern: fixed envelope fields + game-specific `event_data` JSON.
5. **Privacy-first.** No PII in event stream. Session IDs are opaque. IP addresses not stored in event data. Behavioral data is pseudonymous.

---

## Event Envelope (all events share this structure)

```json
{
  "session_id": "string — opaque UUID, generated per browser session",
  "user_id": "string — opaque UUID, persisted via localStorage (anonymous until account created)",
  "puzzle_id": "string — unique puzzle identifier (e.g., '2026-03-06')",
  "puzzle_difficulty": "string — 'easy' | 'medium' | 'hard'",
  "puzzle_size": "string — e.g., '10x10', '15x15'",
  "event_type": "string — event name (see catalog below)",
  "event_seq": "integer — ordinal position in session, monotonically increasing",
  "timestamp_ms": "integer — Unix epoch milliseconds (from performance.now() + offset for sub-ms precision)",
  "device_type": "string — 'mouse' | 'touch' | 'pen' (from PointerEvent.pointerType)",
  "viewport_width": "integer",
  "viewport_height": "integer",
  "event_data": "object — event-specific payload (see below)"
}
```

---

## Event Catalog

### 1. SESSION_START

Fires when player opens the game page.

```json
{
  "event_type": "SESSION_START",
  "event_data": {
    "referrer": "string — document.referrer (how they got here)",
    "user_agent": "string — navigator.userAgent",
    "timezone_offset_min": "integer — new Date().getTimezoneOffset()",
    "is_returning_user": "boolean — user_id existed in localStorage",
    "current_streak": "integer — consecutive days played",
    "total_puzzles_completed": "integer — lifetime count"
  }
}
```

**Signal:** Returning vs. new user segmentation. Timezone reveals geography for session-timing analysis (do they play at 9am or 11pm?). Streak length = engagement depth.

---

### 2. PUZZLE_START

Fires when the puzzle grid renders and becomes interactive.

```json
{
  "event_type": "PUZZLE_START",
  "event_data": {
    "puzzle_grid_rows": "integer",
    "puzzle_grid_cols": "integer",
    "total_filled_cells": "integer — ground truth count of cells that should be filled",
    "clue_complexity": "integer — sum of all clue group counts (higher = more constraint info available)"
  }
}
```

**Signal:** Baseline for all timing calculations. `clue_complexity` allows difficulty normalization across puzzles.

---

### 3. CELL_ACTION

Fires on every cell interaction (fill, mark-empty, erase). **This is the core behavioral event.**

```json
{
  "event_type": "CELL_ACTION",
  "event_data": {
    "action": "string — 'fill' | 'mark_x' | 'erase'",
    "row": "integer — 0-indexed",
    "col": "integer — 0-indexed",
    "previous_state": "string — 'empty' | 'filled' | 'marked_x'",
    "new_state": "string — 'empty' | 'filled' | 'marked_x'",
    "is_correct": "boolean — does new_state match ground truth? (null if erase)",
    "time_since_puzzle_start_ms": "integer",
    "time_since_last_action_ms": "integer — gap between this action and previous CELL_ACTION",
    "hover_duration_before_action_ms": "integer — time pointer was over this cell before committing action",
    "cells_filled_so_far": "integer — running count of filled cells",
    "cells_marked_so_far": "integer — running count of X-marked cells",
    "errors_so_far": "integer — cumulative error count in this session",
    "row_progress": "float — fraction of this row's filled cells correctly identified (0.0-1.0)",
    "col_progress": "float — fraction of this column's filled cells correctly identified (0.0-1.0)",
    "is_drag_action": "boolean — was this part of a click-drag sequence across multiple cells?"
  }
}
```

**Hypothesized signals and what would disprove them:**

| Derived metric | Hypothesized signal | Disproved if |
|---|---|---|
| `time_since_last_action_ms` distribution | Processing speed, deliberation style. Short + consistent = fast processor. Long + variable = deliberative/uncertain. | Distribution is random (no clustering) across players — would mean it's noise, not trait. |
| `hover_duration_before_action_ms` | Confidence/uncertainty per decision. Long hover = low confidence. | Hover duration doesn't correlate with `is_correct` — would mean hovering reflects motor habit, not cognitive state. |
| Sequence of (row, col) across actions | Solving strategy: row-first, column-first, corner-start, edge-in, or random. Systematic = high executive function. | All players show the same sequence — would mean the puzzle structure forces the order, not the player's strategy. |
| `errors_so_far` growth rate | Learning rate / error monitoring. Errors clustering early then dropping = fast learner. Errors distributed evenly = no learning. | Error rate correlates only with puzzle difficulty, not with any player-level trait — would mean it's a puzzle property, not a player property. |
| `erase` actions as fraction of total | Self-correction tendency. High erase rate + high final accuracy = strong metacognition. | Erase rate doesn't predict anything downstream — would mean it's mechanical (misclicks), not cognitive. |
| `is_drag_action` frequency | Confidence/commitment style. High drag usage = pattern-confident, batch-processing. Low = cell-by-cell deliberation. | Drag usage correlates only with device_type (mouse vs. touch) — would mean it's input-method artifact, not behavioral. |

---

### 4. ERROR_MADE

Fires when `CELL_ACTION` has `is_correct === false`. Captures error-specific context.

```json
{
  "event_type": "ERROR_MADE",
  "event_data": {
    "row": "integer",
    "col": "integer",
    "error_number": "integer — ordinal error in this session (1st, 2nd, 3rd...)",
    "time_since_puzzle_start_ms": "integer",
    "time_since_last_error_ms": "integer — null if first error",
    "action_that_caused_error": "string — 'fill' | 'mark_x'",
    "puzzle_completion_pct": "float — how far into the puzzle (0.0-1.0)",
    "was_in_completed_row": "boolean — was this row already fully deducible from clues?",
    "was_in_completed_col": "boolean — was this column already fully deducible?"
  }
}
```

**Signal:** Error timing reveals whether errors come from rushing (early, fast actions) or fatigue (late, after long session). `was_in_completed_row/col` distinguishes deduction errors (logically solvable but missed) from guessing errors (insufficient info).

---

### 5. ERROR_CORRECTED

Fires when a player erases or overwrites an incorrect cell with the correct value.

```json
{
  "event_type": "ERROR_CORRECTED",
  "event_data": {
    "row": "integer",
    "col": "integer",
    "error_number_corrected": "integer — which error (by ordinal) is being fixed",
    "time_since_error_ms": "integer — how long the error persisted before correction",
    "actions_between_error_and_correction": "integer — how many other cell actions happened in between",
    "correction_method": "string — 'immediate_erase' | 'delayed_erase' | 'overwrite'"
  }
}
```

**Signal:** `time_since_error_ms` and `actions_between_error_and_correction` reveal error monitoring style. Immediate correction = attentive/cautious. Delayed correction = either didn't notice or was focused elsewhere (different attentional strategy). `correction_method` distinguishes deliberate undo from overwriting mid-flow.

---

### 6. POINTER_SAMPLE

Fires at 10Hz (every 100ms) while pointer is over the puzzle grid. **High-volume event — stored separately or batched.**

```json
{
  "event_type": "POINTER_SAMPLE",
  "event_data": {
    "client_x": "integer",
    "client_y": "integer",
    "grid_row": "integer | null — row under pointer, null if between cells or on clues",
    "grid_col": "integer | null",
    "velocity_px_per_s": "float — pointer speed",
    "is_over_clue_area": "boolean — pointer is over row/column clue headers",
    "clue_row_or_col": "integer | null — which clue set is being examined"
  }
}
```

**Signal:** Pointer trajectory over the grid reveals scanning strategy (systematic row-by-row vs. jumping). `is_over_clue_area` + `clue_row_or_col` captures which clues the player consults and how often — proxy for analytical depth. Velocity changes near cell boundaries indicate hesitation.

**Storage note:** At 10Hz, a 5-minute session = ~3,000 events. At ~100 bytes each = ~300KB per session. Manageable but should be batched and compressed before transmission. Consider reducing to 5Hz if storage becomes a concern — the behavioral literature suggests 4-8Hz is sufficient for trajectory analysis.

---

### 7. CLUE_INTERACTION

Fires when player hovers over or taps a row/column clue header for >200ms (debounced to avoid noise).

```json
{
  "event_type": "CLUE_INTERACTION",
  "event_data": {
    "clue_type": "string — 'row' | 'col'",
    "clue_index": "integer — which row or column",
    "hover_duration_ms": "integer",
    "clue_values": "array[integer] — the clue numbers for this row/col",
    "row_or_col_completion_pct": "float — how solved is this row/col at time of hover"
  }
}
```

**Signal:** Which clues a player consults before acting reveals reasoning strategy. Re-consulting already-solved clues suggests verification behavior (high conscientiousness). Consulting unsolved clues before acting suggests planning. Players who rarely consult clues may be guessing or have strong working memory.

---

### 8. HINT_USED

Fires if a hint system is implemented and player uses it.

```json
{
  "event_type": "HINT_USED",
  "event_data": {
    "hint_type": "string — 'reveal_cell' | 'check_errors' | 'reveal_row'",
    "hint_number": "integer — ordinal hint usage (1st, 2nd...)",
    "time_since_puzzle_start_ms": "integer",
    "puzzle_completion_pct": "float",
    "time_since_last_action_ms": "integer — how long they hesitated before requesting help"
  }
}
```

**Signal:** Hint-seeking threshold (how stuck before asking for help) = frustration tolerance / independence. Earlier hint use at lower completion = lower persistence. Late hint use at high completion = "almost there" frustration.

---

### 9. PUZZLE_COMPLETE

Fires when all cells are correctly filled.

```json
{
  "event_type": "PUZZLE_COMPLETE",
  "event_data": {
    "solve_time_ms": "integer — total time from PUZZLE_START",
    "total_actions": "integer — total CELL_ACTION count",
    "total_errors": "integer",
    "total_hints": "integer",
    "total_erases": "integer",
    "actions_per_minute": "float",
    "error_rate": "float — errors / total_actions",
    "first_action_delay_ms": "integer — time from PUZZLE_START to first CELL_ACTION",
    "image_name": "string — what pixel-art image was revealed",
    "shared_result": "boolean — did player tap share button?"
  }
}
```

**Signal:** Session-level summary. `first_action_delay_ms` = initial deliberation (analytical vs. impulsive). `actions_per_minute` = processing speed. `shared_result` = social engagement tendency.

---

### 10. PUZZLE_ABANDON

Fires if player closes/navigates away before completing.

```json
{
  "event_type": "PUZZLE_ABANDON",
  "event_data": {
    "time_spent_ms": "integer",
    "puzzle_completion_pct": "float",
    "total_actions": "integer",
    "total_errors": "integer",
    "last_action_type": "string — what they were doing before leaving",
    "time_since_last_action_ms": "integer — idle time before abandonment",
    "abandon_method": "string — 'tab_close' | 'navigation' | 'idle_timeout'"
  }
}
```

**Signal:** When and why players quit. High completion + abandon = frustration at the end (possibly one stubborn cell). Low completion + fast abandon = difficulty mismatch or disinterest. `time_since_last_action_ms` before abandon = how long they stared before giving up (persistence).

---

### 11. STREAK_UPDATE

Fires on session start if the player has a streak history.

```json
{
  "event_type": "STREAK_UPDATE",
  "event_data": {
    "current_streak": "integer",
    "longest_streak": "integer",
    "streak_broken": "boolean — did they miss yesterday?",
    "days_since_last_play": "integer"
  }
}
```

**Signal:** Streak maintenance correlates with conscientiousness. Streak breaks followed by return = resilient engagement. Streak breaks followed by churn = streak-dependent (extrinsically motivated).

---

## Storage Architecture (recommendation)

| Event type | Volume per session | Storage tier |
|---|---|---|
| SESSION_START, PUZZLE_START, PUZZLE_COMPLETE, PUZZLE_ABANDON, STREAK_UPDATE | 1-3 each | Primary DB (PostgreSQL / SQLite) |
| CELL_ACTION, ERROR_MADE, ERROR_CORRECTED, CLUE_INTERACTION, HINT_USED | 50-300 per session | Primary DB, partitioned by date |
| POINTER_SAMPLE | 1,500-3,000 per session | Separate table or object storage (S3/R2). Batch-uploaded, compressed. |

**Estimated daily storage at 10K DAU:**
- Action events: ~10K sessions x ~200 events x ~200 bytes = ~400MB/day
- Pointer samples: ~10K sessions x ~2,500 events x ~100 bytes = ~2.5GB/day

Pointer samples are the bulk. Consider:
- Start at 5Hz instead of 10Hz (halves volume, still sufficient per literature)
- Only capture pointer data for a random 20% sample of sessions initially
- Compress with gzip before upload (~5:1 ratio on JSON)

---

## What This Schema Does NOT Capture (acknowledged gaps)

1. **Eye gaze.** Would reveal what players look at vs. interact with. Not capturable without webcam permission + eye tracking library. Out of scope for launch.
2. **True touch pressure.** Hardware support is inconsistent (force touch deprecated). Not reliable enough to build metrics on.
3. **Emotional state.** No physiological signals (heart rate, GSR). Behavioral proxies (speed changes, error spikes) are available but noisy.
4. **Multi-session learning curves.** This schema captures per-session behavior. Cross-session analysis (does the player improve over weeks?) requires a downstream analytics layer joining sessions by `user_id`.
5. **Social context.** We don't know if the player is alone, on a commute, in a meeting. `timezone_offset_min` and time-of-day are weak proxies.

---

## Validation Plan (post-launch)

The behavioral signals above are hypotheses. To validate:

1. **Internal consistency:** Do metrics derived from the same construct correlate? (e.g., does `hover_duration_before_action_ms` correlate with `first_action_delay_ms`? Both should reflect deliberation style.)
2. **Test-retest reliability:** Does the same player produce similar behavioral profiles across different puzzles on different days?
3. **Discriminant validity:** Do the metrics actually differentiate between players, or do all players look the same? (If variance is low, the signal is noise.)
4. **Predictive validity (bridge phase):** Do behavioral profiles predict bridge conversion? This is the ultimate test — only possible with Phase 2 data.

Minimum sample for meaningful validation: ~500 unique users completing 5+ puzzles each.
