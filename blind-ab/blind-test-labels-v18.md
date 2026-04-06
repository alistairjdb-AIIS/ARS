# Blind A/B Test v18 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Photoreal humans — first test
**Subject:** elderly man on a park bench, reads a letter, expression changes

## BIAS MITIGATION
- A/B assignment: B=crafted, A=terse (randomized)
- Presentation order: A-first, B-second (alternating from v17's B-first)
- Character description matched (elderly man, grey hair, weathered jacket, park bench)
- Acting chain limited to 2 beats
- No dialogue (avoids lip sync as confound — isolate visual quality first)

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v18-output-a.mp4` | **Terse brief paste** |
| `/root/blind-ab/v18-output-b.mp4` | **Research-informed crafted** (imperfection prompting + physical descriptors + film look + acting chain) |

No overlays. First photoreal human test. Tests whether research-informed crafting (imperfection prompting, physical descriptors, 85mm lens language, film grain, soft lighting) outperforms terse for human subjects.

## Output A prompt (terse)
> "8-second cinematic scene. An elderly man with grey hair and a weathered brown jacket sits on a park bench. He opens a letter, reads it, and his expression slowly changes from neutral to a gentle smile. Autumn park, soft afternoon light. Shot on 35mm film. No dialogue."

## Output B prompt (research-informed crafted)
> "Shot on 85mm lens, f/2.0, shallow depth of field, subtle handheld micro-shake. A man in his late seventies with thinning grey hair, deep laugh lines, age spots on his temples, and a slightly crooked nose sits on a weathered park bench. He wears a faded brown corduroy jacket with patched elbows. His weathered hands carefully unfold a letter — he squints at the handwriting, lips moving faintly. His brow furrows, then slowly softens. The corners of his mouth lift into an involuntary smile. His eyes glisten. Soft overcast afternoon light, autumn trees in background. Kodak Portra 400 film grain, natural skin texture with visible pores. No dialogue."

## Research applied in B (not in A)
- **Imperfection prompting:** "deep laugh lines, age spots on temples, slightly crooked nose, thinning grey hair" — breaks the AI face (photoreal research §4B)
- **Physical descriptors:** "brow furrows, then slowly softens, corners of mouth lift, eyes glisten" not "expression changes to a smile"
- **Acting chain (2 beats):** squints at handwriting, lips moving (initial state) → brow furrows then softens, mouth lifts, eyes glisten (emotional transition)
- **Film look:** "85mm lens, f/2.0, Kodak Portra 400 film grain, natural skin texture" — counters AI-clean aesthetic (research §3F)
- **Lighting:** "soft overcast afternoon light" — diffused light minimizes uncanny valley (research §3G)
- **Hands addressed:** "weathered hands carefully unfold a letter" — hands are doing ONE simple action, not complex manipulation (research §2B mitigation)
- **Object interaction with manner:** "carefully unfold" reveals character (gentle, reverent)
- **Camera:** minimal — only lens spec + shallow DOF + micro-shake (no camera choreography)

## Negative prompt (both)
> "anime, cartoon, 3D render, Pixar, illustration, text, watermarks, logos, perfect skin, airbrushed, overly smooth, plastic, uncanny valley, deformed hands, extra fingers"

## Hypothesis
First photoreal human test. Research identifies specific failure modes (AI face, dead eyes, hand artifacts, skin texture) and mitigations (imperfection prompting, film grain, soft lighting, medium shot). If research-informed crafted wins, the principles transfer from stylized characters to photoreal humans. If terse wins, Veo's photoreal human generation may be strong enough that the "AI face" mitigations aren't needed — or the mitigations don't work as theorized.
