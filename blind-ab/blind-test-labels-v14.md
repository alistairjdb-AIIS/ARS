# Blind A/B Test v14 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — 3D Pixar-style sub-register (research-informed)
**Subject:** small fox kit by a forest stream, butterfly lands on its nose

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v14-output-a.mp4` | **Terse brief paste** |
| `/root/blind-ab/v14-output-b.mp4` | **Research-informed crafted** (acting chain + shape language + 60-30-10 color + physical descriptors) |

No overlays. Fourth stylized character test. First test applying character design & acting research. Tests whether research-informed crafting outperforms terse on Pixar-style characters (where terse won v13 without research).

## Output A prompt (terse)
> "8-second 3D Pixar-style animated scene. A small fox kit sits by a forest stream. A butterfly lands on its nose. The fox goes cross-eyed trying to look at it. Warm dappled sunlight through trees. Whimsical and charming. No dialogue."

## Output B prompt (research-informed crafted)
> "3D Pixar-style. Medium close-up, soft dappled light through canopy. A small round-bodied fox kit — warm orange fur, cream chest and ear tips, bright amber eyes — sits by a mossy forest stream, one paw dabbling in the water. Its ears perk up. A blue butterfly drifts into frame. The fox freezes, then slowly crosses its eyes as the butterfly settles on its nose. Its whiskers twitch. A tiny smile spreads. Warm golden hour, shallow depth of field."

## Research applied in B (not in A)
- **Shape language:** "round-bodied" encodes friendly/cute via circular shapes
- **Color hierarchy:** orange dominant, cream secondary, amber accent (60-30-10)
- **Acting chain:** dabbling (initial state) → ears perk (stimulus) → freezes (processing) → crosses eyes (response) → whiskers twitch, smile (secondary response)
- **Movement quality:** "slowly crosses" = gentle personality
- **Physical descriptors over labels:** "ears perk up, whiskers twitch, tiny smile spreads" not "looks curious then happy"
- **Object interaction with manner:** "one paw dabbling in water" reveals playful personality
- **Environment limited:** 3 elements (stream, canopy, golden hour) — front-loaded character

## Negative prompt (both)
> "live-action, photorealistic, anime, hand-drawn, 2D, text, readable characters, logos, watermarks, motion blur, warping, jitter, overexposure, deformed hands, extra fingers, uncanny valley"

## Hypothesis
v13 terse won because crafted over-constrained camera and lacked acting/expression depth. v14's research-informed crafted encodes acting chain, shape language, color hierarchy, and physical-descriptor emotion — all absent from v13's crafted prompt. If B wins, research findings have measurable prompt-level impact. If A (terse) wins again, Veo's own character choices may simply be better than human specification for Pixar-style.
