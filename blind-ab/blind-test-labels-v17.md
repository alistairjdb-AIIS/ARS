# Blind A/B Test v17 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — classic cartoon sub-register (Golden Age / Looney Tunes-adjacent)
**Subject:** orange tabby cat sneaking up on a sleeping bulldog, steps on tail, freezes in terror

## BIAS MITIGATION
- A/B assignment: A=crafted, B=terse (randomized)
- **Presentation order randomized:** Video links will be shown B-first, A-second (reversing the default order to counter detected B-position bias from prior 5 tests)
- Character description matched in both prompts (orange tabby cat, brown bulldog)
- Both prompts specify same sub-register ("classic cartoon animation, thick black outlines, flat cel colors")
- Acting chain limited to 2 beats (learned from v15)

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v17-output-a.mp4` | **Research-informed crafted** (2-beat acting chain + cartoon register + physical descriptors) |
| `/root/blind-ab/v17-output-b.mp4` | **Terse brief paste** |

No overlays. Seventh stylized character test. First cartoon sub-register test. Tests research-informed crafting in a register maximally different from anime and Pixar.

## Output A prompt (research-informed crafted)
> "Classic cartoon animation, thick black outlines, flat cel colors, painted background. An orange tabby cat tiptoes on exaggerated pointed feet toward a sleeping brown bulldog on a porch. The cat's body stretches tall and thin with each careful step, eyes darting nervously. Its paw lands squarely on the bulldog's tail — the cat freezes mid-step, eyes going wide, every hair standing on end. The bulldog's one eye cracks open. Bright saturated colors, exaggerated squash-and-stretch motion, hand-drawn 2D animation."

## Output B prompt (terse)
> "8-second classic cartoon animation scene with thick black outlines and flat cel colors. An orange tabby cat sneaks up on a sleeping brown bulldog on a porch. The cat accidentally steps on the bulldog's tail and freezes in terror. Bright colors, exaggerated cartoon motion, hand-drawn 2D style. No dialogue."

## Research applied in A (not in B)
- **Cartoon register specifics:** "painted background" (research: Golden Age uses watercolor/gouache BGs distinct from characters)
- **Acting chain (2 beats):** tiptoeing (initial state) → paw lands on tail, freezes, eyes go wide, hair stands on end (reaction). Bulldog's eye opening = cliffhanger beat.
- **Physical descriptors:** "body stretches tall and thin with each careful step" (cartoon motion principle: stretch during motion), "eyes darting nervously" (not "looks nervous"), "every hair standing on end" (physical fear response)
- **Movement quality:** "tiptoes on exaggerated pointed feet" = cartoon sneaking convention; "freezes mid-step" = the cartoon "take" setup
- **Camera:** none specified (let Veo choose)

## Negative prompt (both)
> "live-action, photorealistic, 3D render, CGI, Pixar, anime, text, readable characters, logos, watermarks, gradient shading, realistic lighting"

## Hypothesis
First cartoon register test. Both prompts lock the style (thick outlines, flat cel colors, hand-drawn 2D) to prevent drift. Research-informed crafted adds cartoon-specific motion language (stretch, tiptoe, freeze, hair standing) and 2-beat acting chain. If crafted wins, the acting-chain advantage extends beyond anime/Pixar to cartoon. If terse wins, Veo's cartoon rendering may be strong enough autonomously (consistent with Pixar pattern).
