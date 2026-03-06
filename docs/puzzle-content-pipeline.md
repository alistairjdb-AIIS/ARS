# Puzzle Content Pipeline — Daily Nonogram

## Grid Sizes (DECIDED)

| Size | Role | Target Solve Time | Available at Launch |
|---|---|---|---|
| **5x5** | Tutorial only | 1-2 min | Yes — 5 tutorial puzzles, not daily |
| **10x10** | Daily puzzle | 5-8 min | Yes — primary daily format |
| **15x15** | Stretch goal / weekly bonus | 10-20 min | No — add post-launch if retention supports longer sessions |

**Rationale:**
- 10x10 is the industry minimum for a satisfying daily puzzle (confirmed by Pixelogic, Solitaire.org, SolitaireParadise all using 10x10 as their smallest serious daily).
- 5x5 is too trivial for daily play but useful for onboarding first-time nonogram players.
- 15x15 targets 10-20 min sessions — outside our 3-8 min target. Add later as an optional "weekly challenge" or unlockable.
- Every site offering multiple sizes per day (Solitaire.org, SolitaireParadise) started with 10x10 as the base.

---

## Difficulty Calibration

### Constraint: All puzzles must be line-solvable

No guessing. No backtracking. A sweep-based solver must fully solve every published puzzle. This is non-negotiable for casual players and is the industry standard (Pixelogic, puzzle-nonograms.com, Japanese newspaper nonograms all enforce this).

### Difficulty metric: Sweep count

Following Batenburg & Kosters (2012), difficulty within line-solvable puzzles = number of alternating H-SWEEP + V-SWEEP passes required by SIMPLE-SOLVER.

| Difficulty | Sweep Count (10x10) | Fill Ratio | Clue Groups/Line |
|---|---|---|---|
| Easy | 2-4 sweeps | 55-70% | 1-2 groups |
| Medium | 4-7 sweeps | 45-60% | 2-3 groups |
| Hard | 7-12 sweeps | 35-55% | 2-4 groups |

### Daily difficulty curve

- **Days 1-7:** Easy only (onboarding period, retain new players)
- **Days 8-30:** Mix of easy and medium (player has built habit)
- **Days 31+:** Rotate easy/medium/hard across the week (e.g., Mon=easy, Wed=medium, Fri=hard)

### Additional calibration rules

1. **Avoid lines with 5+ clue groups in 10x10** — clue reading becomes tedious for casual players.
2. **Avoid fully symmetric images for medium/hard** — symmetry halves the solving work once recognized. Use symmetry only for easy puzzles.
3. **First-action availability:** Easy puzzles should have at least 2-3 fully determinable lines on first pass (the player can immediately fill something without scanning all clues).

---

## Image Sourcing Strategy

### Phase 1: Launch pipeline (0-6 months)

**Primary source: Twemoji SVG rasterization**
- Twemoji (Twitter's open-source emoji set): CC-BY 4.0 license. ~3,600 emoji as SVG.
- Google Noto Emoji: Apache 2.0 license. Alternative source.
- Pipeline: SVG → render to canvas at 64x64 → grayscale → binary threshold → downsample to 10x10 → cleanup isolated pixels → solver validation.
- Estimated yield after filtering for recognizability + unique solution + line-solvability: **300-500 usable puzzles** from ~3,600 emoji.
- Categories covered: animals, food, vehicles, nature, objects, sports, weather, flags — broad thematic variety.

**Secondary source: OpenGameArt CC0 16x16 sprites**
- Kyrise's RPG Icon Pack (hundreds of items), CC0 gem/currency icons, misc icon packs.
- Already at near-target resolution. Downsample from 16x16 → 10x10 with threshold.
- Estimated yield: **100-200 usable puzzles** (skews toward RPG items — swords, potions, gems).

**Tertiary: Hand-drawn originals**
- For seasonal/holiday content (Christmas tree, pumpkin, snowflake, heart).
- Budget: 2-5 per month, hand-crafted at 10x10 in a pixel editor.
- These are the highest quality and most recognizable. Use for marquee daily puzzles.

### Phase 2: Scaling (6+ months)

- **AI-assisted generation** via PixelLab or Retro Diffusion → generate at 32x32 → downsample → validate → curate.
- **Community creation** once DAU > 5,000: add puzzle editor, accept submissions with automated solver validation and editorial review. Following Nonograms Katana's model.

### What NOT to do

- Do not rely on general AI (DALL-E, Midjourney, standard Stable Diffusion) at 10x10 resolution. They don't understand pixel grid structure at this scale.
- Do not use procedural generation for daily puzzles. Procedural shapes are semantically unrecognizable — the image reveal moment is the engagement hook.
- Do not skip the solvability validator. Any image can fail uniqueness or line-solvability when converted. Validation is mandatory on every puzzle.

---

## Puzzle Data Format

```json
{
  "id": "2026-03-06",
  "title": "Apple",
  "category": "food",
  "difficulty": "easy",
  "grid_size": [10, 10],
  "fill_ratio": 0.58,
  "sweep_count": 3,
  "solution": [
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,0,0,0,0]
  ],
  "row_clues": [[4],[6],[8],[8],[10],[10],[8],[8],[6],[2]],
  "col_clues": [[2,2],[2,2],[7],[8],[9],[9],[8],[7],[2,2],[2,2]],
  "source": "twemoji",
  "source_license": "CC-BY-4.0",
  "image_colors": {
    "filled": "#E74C3C",
    "background": "#FFFFFF"
  },
  "created_at": "2026-03-01T00:00:00Z"
}
```

**Notes:**
- `solution` is the ground truth grid (1=filled, 0=empty). Never sent to client until puzzle is solved or abandoned.
- `row_clues` and `col_clues` are derived from solution at generation time and sent to client.
- `image_colors` allows the reveal to show the original emoji color instead of just black/white — makes the reveal more satisfying.
- `sweep_count` is computed by the solver at generation time for difficulty classification.

---

## Generation Pipeline (automated)

```
1. INPUT: Source image (SVG emoji, 16x16 sprite, or hand-drawn)
         ↓
2. RENDER: Draw to canvas at 64x64 (or native resolution)
         ↓
3. GRAYSCALE: Convert to grayscale
         ↓
4. THRESHOLD: Apply binary threshold (configurable, default 0.5)
         ↓
5. DOWNSAMPLE: Resize to 10x10 using area averaging + re-threshold
         ↓
6. CLEANUP: Remove isolated single pixels (noise from downsampling)
         ↓
7. COMPUTE CLUES: Derive row_clues and col_clues from binary grid
         ↓
8. VALIDATE UNIQUENESS: Run constraint solver — does this clue set
   have exactly one solution? If NO → discard or adjust threshold.
         ↓
9. VALIDATE LINE-SOLVABILITY: Run SIMPLE-SOLVER (alternating sweeps).
   Does it solve completely? If NO → discard (puzzle requires guessing).
         ↓
10. COMPUTE DIFFICULTY: Count sweep passes. Classify easy/medium/hard.
         ↓
11. HUMAN REVIEW: Is the image recognizable at 10x10? Does the reveal
    feel satisfying? Would a player say "oh, it's an apple"?
    If NO → discard.
         ↓
12. OUTPUT: Puzzle JSON file, categorized and tagged.
```

**Expected yield rates (estimated, not measured — must validate with real pipeline):**

| Step | Estimated pass rate |
|---|---|
| Uniqueness check | ~60-70% of images produce unique solutions at 10x10 |
| Line-solvability check | ~85-95% of uniquely solvable puzzles are line-solvable at 10x10 |
| Human recognizability review | ~50-70% of validated puzzles have recognizable images |
| **Overall yield** | **~25-45% of input images become publishable puzzles** |

---

## Content Runway

| Milestone | Puzzles needed | Source |
|---|---|---|
| **Tutorial** | 5 (5x5 only) | Hand-crafted |
| **Alpha/testing** | 30 | Twemoji pipeline |
| **Launch** | 90 minimum (3 months buffer) | Twemoji + OpenGameArt |
| **Comfortable buffer** | 180 (6 months) | All Phase 1 sources |
| **Year 1 total** | 365+ | Phase 1 + Phase 2 scaling |

**Content velocity requirement:** 1 puzzle/day sustained. With a 180-puzzle buffer, you have 6 months of runway before the pipeline must be producing at steady-state.

**Thematic variety target:** Minimum 8 categories with 10+ puzzles each before launch. Categories: animals, food, objects, nature, vehicles, weather, sports, symbols/shapes. This prevents visible repetition in the first month.

---

## Tools Required (to build before/alongside the game)

1. **Solver/validator script** (JS or Python)
   - Input: binary grid or clue set
   - Output: unique solution? line-solvable? sweep count?
   - Open-source starting points: HandsomeOne/Nonogram, ThomasR/nonogram-solver
   - This is the most critical pipeline tool. Build or adapt first.

2. **Image-to-puzzle converter** (JS or Python)
   - Input: image file (SVG, PNG)
   - Output: binary grid at target resolution + clue set
   - Steps 1-7 of the pipeline above
   - Straightforward image processing — Canvas API or Pillow/PIL

3. **Batch processor**
   - Input: directory of source images
   - Output: validated puzzle JSON files + rejection log
   - Runs converter → solver → classifier in sequence
   - Reports yield rate and category distribution

4. **Puzzle preview tool** (browser-based)
   - Renders puzzle grid with clues for human review
   - Shows the solved image alongside the clue-only view
   - Accept/reject buttons for curation
   - Optional: difficulty override (human can reclassify)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Yield rate lower than estimated | Not enough puzzles for launch | Start pipeline early. If yield is <20%, switch to 15x15 where images are more recognizable. |
| 10x10 images not recognizable enough | Weak reveal moment, low share rate | Test with 5 users before committing. If recognition rate <60%, move to 15x15 (accept longer sessions). |
| Solver implementation takes too long | Blocks entire pipeline | Use existing open-source solver (HandsomeOne/Nonogram). Don't build from scratch. |
| Twemoji color emoji don't threshold well to B&W | Many discards at step 4 | Experiment with multiple threshold values (0.3, 0.4, 0.5, 0.6). Some emoji may need per-image threshold tuning. |
| Content exhaustion after 6 months | Churn spike | Begin Phase 2 (AI + community) by month 3, before buffer runs out. |

---

## Self-Critique

**Falsifiability:** The yield rate estimates (25-45% of input images become puzzles) are derived from reasoning about the pipeline steps, not from running the actual pipeline. The real yield could be much lower if Twemoji designs at 10x10 are mostly unrecognizable blobs. **Test this within the first week of pipeline development** by processing 50 emoji manually and measuring actual pass rates.

**Shared assumption:** This entire pipeline assumes black-and-white (binary) nonograms. Color nonograms (multiple fill colors per puzzle) are a different category with different solvability constraints and richer images at smaller sizes. If 10x10 B&W recognition proves too low, color nonograms are an alternative that preserves the grid size while dramatically improving image quality. Trade-off: color nonograms are harder to solve and more complex to build.

**Alternative interpretation:** The emoji rasterization approach may produce puzzles that feel "generated" rather than "crafted." If players notice that every puzzle is a downscaled emoji, it could undermine the reveal moment. Mitigation: mix sources (emoji + sprites + hand-drawn) and avoid including the emoji name in the puzzle title until after reveal.
