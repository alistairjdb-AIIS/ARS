# Blind A/B Test v20 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — Pixar × Pokémon hybrid
**Subject:** electric creature on mossy log, hears thunder, cheeks spark with excitement

## TEST DESIGN
Same as v19: both prompts are research-informed crafted. Variable is /animate pipeline.

## BIAS MITIGATION
- A/B assignment: A=/animate-designed, B=crafted-without-animate
- Presentation order: A-first, B-second (alternating from v19's B-first)
- Character description matched (yellow creature, red cheeks, pointed ears, lightning tail, mossy log, forest)
- Same model (Kling AI), same parameters

## Label Mapping

| File | Approach |
|---|---|
| `/root/blind-ab/v20-output-a.mp4` | **Research-crafted + /animate pipeline** |
| `/root/blind-ab/v20-output-b.mp4` | **Research-crafted WITHOUT /animate** |

## Output A prompt (/animate-designed)
> "3D Pixar-style animation. A small round-bodied yellow creature with red cheek patches, long pointed ears with black tips, and a lightning-bolt tail sits perfectly still on a mossy log in a quiet forest clearing. Fireflies drift. The creature's ears twitch — then slowly rotate upward. Distant thunder rumbles. The creature freezes, eyes wide, listening. A beat. Then a faint warm glow begins in its cheek patches, building, until tiny sparks dance across its face. Its whole body shivers with delight. Soft dappled forest light, shallow depth of field. No dialogue."

## Output B prompt (crafted without /animate)
> "3D Pixar-style animation. A small round-bodied yellow creature with red cheek patches, long pointed ears with black tips, and a lightning-bolt shaped tail sits on a mossy log in a forest clearing. It hears distant thunder — its ears perk up and rotate toward the sound. Its cheek patches begin to glow and crackle with tiny sparks. The creature's eyes widen with excitement, and it bounces on the log. Warm dappled sunlight through canopy, fireflies in the background. Shallow depth of field. No dialogue."

## What /animate changed
1. **Loading-heavy:** A opens with "sits perfectly still" + "fireflies drift" (quiet loading) vs B jumps to "hears thunder" by sentence 2
2. **Explicit hold:** "The creature freezes, eyes wide, listening. A beat." vs B has no pause
3. **Restrained payoff:** A: "a faint warm glow begins, building, until tiny sparks dance" (gradual) vs B: "begin to glow and crackle with tiny sparks" (immediate)
4. **Physical response:** A: "whole body shivers with delight" (involuntary, physical) vs B: "bounces on the log" (voluntary, action)
5. **No camera spec in either** (both learned from v13)

## Negative prompt (both)
> "live-action, photorealistic, anime, hand-drawn, text, watermarks, logos, deformed, extra limbs, uncanny valley"

## Hypothesis
Second /animate pipeline test. Tests whether the loading principle + restrained payoff + explicit hold produces measurably better output in a stylized (Pixar) register vs v19's photoreal register. If /animate wins again, the value is cross-register. N=2 if it wins, still directional.
