# Blind A/B Test v19 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Photoreal humans — /animate pipeline test
**Subject:** young woman in coffee shop receives text message, expression shifts

## TEST DESIGN
This is NOT a terse-vs-crafted test. BOTH prompts are research-informed crafted. The variable is whether the /animate design thinking pipeline (FEEL/CONVERGENCE/VISUAL + cross-domain principles) adds measurable value on top of research-informed crafting.

## BIAS MITIGATION
- A/B assignment: A=/animate-designed, B=crafted-without-animate
- Presentation order: B-first, A-second (alternating from v18)
- Character description matched (dark curly hair, freckles, cream sweater, coffee shop, rain)
- Same model (Kling AI), same parameters

## Label Mapping

| File | Approach |
|---|---|
| `/root/blind-ab/v19-output-a.mp4` | **Research-crafted + /animate pipeline** (FEEL/CONVERGENCE/VISUAL, loading principle, cross-domain synthesis) |
| `/root/blind-ab/v19-output-b.mp4` | **Research-crafted WITHOUT /animate** (research applied directly to prompt, no design thinking framework) |

## Output A prompt (/animate-designed)
> "A woman in her late twenties with dark curly hair tucked behind one ear, light freckles, warm brown eyes, sits alone in a window seat of a quiet coffee shop. She wears an oversized cream knit sweater. Rain traces lines down the glass beside her. She cradles a ceramic mug in both hands, steam curling, watching the rain — still, unhurried. Her phone buzzes once on the wooden table. She glances down. Her hands lower the mug slowly. She picks up the phone. Her brow draws together — she reads, lips barely moving. A beat. Then something shifts — her brow releases, her eyes soften, and the smallest smile pulls at the corner of her mouth before she can stop it. Soft overcast window light, shallow depth of field, Kodak Portra 400 grain. No dialogue."

## Output B prompt (crafted without /animate)
> "A woman in her late twenties with dark curly hair, light freckles across her nose, and warm brown eyes sits in a window seat of a quiet coffee shop. She wears an oversized cream knit sweater, hands wrapped around a ceramic mug. Her phone buzzes on the table. She glances down — her lips part slightly, eyebrows lift. She sets the mug down slowly, picks up the phone with both hands, and a slow disbelieving smile spreads across her face. Soft window light from camera-left, steam rising from the mug, rain-streaked glass behind her. Kodak Portra 400, natural skin texture. No dialogue."

## What /animate changed (the test variable)
1. **Loading-heavy structure** — 60% of A's prompt is pre-phone-buzz stillness vs ~30% in B
2. **Explicit hold** — "A beat." in A; no explicit pause in B
3. **Restraint on payoff** — A: "smallest smile pulls at the corner of her mouth before she can stop it" vs B: "slow disbelieving smile spreads across her face"
4. **Sensory loading details** — A: "Rain traces lines down the glass," "steam curling, watching the rain — still, unhurried"
5. **No lens language** — A removed "85mm, f/2.0" that B includes (v13 learning applied)
6. **Principles applied** — Tension/Resolution (#10), Rhythm/Pacing (#5), Tempo/Rate (#15 "the hold is the loudest moment"), Revelation (#3, Spielberg: reaction > spectacle)

## Negative prompt (both)
> "anime, cartoon, 3D render, Pixar, illustration, text, watermarks, logos, perfect skin, airbrushed, overly smooth, plastic, deformed hands, extra fingers"

## Hypothesis
Both prompts are research-informed crafted. The variable is whether /animate's structured design thinking (FEEL/CONVERGENCE/VISUAL + cross-domain principles + loading principle) produces measurably better output than direct research application alone. If A wins, the /animate pipeline adds value and should be enforced. If B wins (or tie), /animate is overhead without measurable output improvement.
