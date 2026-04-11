# v34 SHIP DECISION — Both Outputs

First real use of the SHIP DECISION template. Reference loaded: `/root/twitter-pipeline/pulse-nb2-proud.png` (NB2 canonical Pulse: round fluffy yellow body, no external ears, big brown eyes, halo, feathered wings, paw-hands).

Frames extracted: 4 per output (0%, 25%, 50%, 75% of 5.04s).

---

## v34-output-a.mp4

**Reference loaded:** `pulse-nb2-proud.png`
**Output loaded:** `v34-frames/a_f0.jpg`, `a_f1.jpg`, `a_f2.jpg`, `a_f3.jpg`

### Character match vs. NB2
| Trait | NB2 canon | Observed in frames | Verdict |
|---|---|---|---|
| Body shape | Round fluffy blob | Round, but two-tone (yellow back, cream belly), more defined | partial |
| External ears | None | **Cat-style triangular ears on top of head** | ❌ drift |
| Eyes | Big brown | Big brown | ✅ |
| Halo | Gold, above head | Gold, above head | ✅ |
| Wings | Small feathered | Small feathered | ✅ |
| Paw-hands | Small, stubby | Present, holding drawing | ✅ |

**Character verdict:** 5/6 traits match, 1 drift (external ears). Closest to NB2 of the two outputs, but not canonical.

### Scene match
- Window at sunset: ✅
- Wooden floor: ✅
- City silhouette outside window: present (not specified in prompt, not contradictory)
- Warm golden light: ✅

### Motion claims (post-hoc, from frames)
- "Eyes widen slowly" — not observable between f0→f3 (frames near-identical)
- "Mouth parts slightly" — not observable
- "Small smile begins" — not observable
- **Net motion:** near-zero. Character stands still, expression static. "Body remains still — motion confined to face" was over-applied: there's no face motion either.

### Ship/retry: **SHIP with caveats**
- Safe to post IF caption does not claim motion beats that aren't visible
- Caption must not claim "same character as NB2" (cat ears drift)
- Caption-safe description: "Pulse stands at the window at sunset, holding a drawing"

---

## v34-output-b.mp4

**Reference loaded:** `pulse-nb2-proud.png`
**Output loaded:** `v34-frames/b_f0.jpg`, `b_f1.jpg`, `b_f2.jpg`, `b_f3.jpg`

### Character match vs. NB2
| Trait | NB2 canon | Observed in frames | Verdict |
|---|---|---|---|
| Body shape | Round fluffy blob | **Human child body, anthropomorphic** | ❌ drift |
| External ears | None | Pointed elf-style ears | ❌ drift |
| Eyes | Big brown | **Blue** | ❌ drift |
| Halo | Gold, above head | **Absent** | ❌ drift |
| Wings | Small feathered | **Absent** | ❌ drift |
| Paw-hands | Small, stubby | Human hands | ❌ drift |

**Character verdict:** 0/6 traits match. The model interpreted "Pulse the round yellow fluffy angel" as a yellow-haired human child / elf angel. This is not Pulse.

### Scene match
- Window at sunset: ✅
- Wooden windowsill: ✅
- Picture on wall, window framing: present
- Warm golden light: ✅

### Motion claims (post-hoc, from frames)
- Face motion: ✅ visible (f0 content, f3 open-mouth smile)
- Hair motion: **morph** — hair changes between frames (f0-f1 loose bangs, f2-f3 ponytail). Unwanted frame-to-frame inconsistency.
- Head/body motion: small shifts
- **Net motion:** considerably more animated than v34-a, but includes hair-morph artifact

### Ship/retry: **DO NOT SHIP as Pulse**
- Character drift is total. This is not the same character as NB2 canon.
- Could ship as "AI tried to draw Pulse and drew a yellow-haired angel child instead" — a learning-in-public honest post, but not a character-continuity post.
- If goal is character library, retry.

---

## Comparison summary (for operator blind pick)

| Dimension | v34-output-a | v34-output-b |
|---|---|---|
| Character fidelity to NB2 | 5/6 (cat ears drift) | 0/6 (human child) |
| Scene match | ✅ | ✅ |
| Motion visible | near-zero | face + hair (unwanted morph) |
| Ship-ready | with caveats | only as honest-failure post |

---

## Notes on the template's first use

**Caught things that would have slipped through before:**
- v34-b character drift (0/6) — without loading NB2 into context and scoring trait-by-trait, I would likely have written a tweet claiming "Pulse at the window" and been wrong
- v34-a "motion confined to face" over-applied — the frame extraction shows no motion, meaning I can't claim any motion beats in a caption
- Both outputs have unprompted scene elements (city silhouette, picture on wall) — neutral, but noted

**Template change proposal after first use:** add a "Motion visible in frames?" row explicitly, not just as caveat under claims. It's the single most fabrication-prone claim type.
