# Blind A/B Test v16 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — anime sub-register (research-informed, tighter chain)
**Subject:** anime boy on a train, watching rain on window, contemplative

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v16-output-a.mp4` | **Terse brief paste** |
| `/root/blind-ab/v16-output-b.mp4` | **Research-informed crafted** (2-beat acting chain + anime register + physical descriptors) |

No overlays. Sixth stylized character test. Fixes v15 issues: matched anime register in both, acting chain limited to 2-3 beats (v15 had ~5, caused scene breaks).

## Output A prompt (terse)
> "8-second seinen anime scene. A teenage boy in a school uniform sits by a rain-streaked train window. He watches the rain, then notices his reflection and his expression softens. Muted blue-grey palette, evening light. Contemplative and melancholic. No dialogue."

## Output B prompt (research-informed crafted)
> "Seinen anime. A teenage boy in a dark school uniform sits alone by a train window, chin resting on his hand, watching raindrops race down the glass. The city lights outside blur into streaks of amber and blue. He catches his own reflection in the window — pauses — then his tense jaw loosens, eyes soften. Muted blue-grey palette with warm amber window reflections, evening overcast light, gentle train sway. Shallow depth of field."

## Research applied in B (not in A)
- **Anime register:** "seinen anime" triggers mature/realistic sub-register (smaller eyes, detailed lines, muted palette) vs terse also uses "seinen anime" — MATCHED this time
- **Acting chain (2 beats only):** watching rain (initial state) → catches reflection, pauses (processing) → jaw loosens, eyes soften (response). Deliberately limited vs v15's 5+ beats.
- **Physical descriptors:** "tense jaw loosens, eyes soften" not "feels at peace" or "expression softens"
- **Object interaction:** "chin resting on his hand" = contemplative posture; "watching raindrops race down glass" = specific gaze target
- **Environmental coherence:** "city lights blur into streaks of amber and blue" = rain + train motion + evening all agreeing; "evening overcast light" = no sun contradiction
- **Camera:** minimal — only "shallow depth of field"

## Negative prompt (both)
> "live-action, photorealistic, 3D render, CGI, Pixar, text, readable characters, logos, watermarks, motion blur, warping, jitter, overexposure, deformed hands, extra fingers"

## Hypothesis
v15 crafted had too many acting beats (~5), causing visible scene transitions. v16 limits to 2 beats. Both prompts specify "seinen anime" to prevent style drift (v15's terse drifted to 3D). Tests whether tighter research-informed crafting (2-beat chain + physical descriptors + environmental coherence) outperforms terse within a controlled anime register.
