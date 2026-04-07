# Blind A/B Test v24 — Labels (committed before render)

## Test Parameters
- **Register:** Photoreal human
- **Tools:** Runway Gen-4.5 (text-to-video) vs Kling AI (text-to-video)
- **Variable:** Cross-tool comparison with tool-optimized prompts (same intent, different syntax)
- **Brief:** Elderly woman sitting in a sun-filled kitchen, reading a handwritten letter. She pauses, looks up toward the window, and a faint smile forms. Morning light. 8 seconds.
- **Hypothesis:** Kling should produce better per-frame face quality (confirmed in prior tests). Runway Gen-4.5 text-to-video quality for photoreal humans is unknown — this is the first internal test.
- **New methodology:** Prompts are NOT identical. Each is written in the tool's native prompt dialect (force/physics prose for Runway, action/concrete for Kling). Same intent, different syntax. This follows the Prompt-A-Video research finding that identical prompts systematically disadvantage one tool.
- **Quality modifiers stripped:** No "cinematic," "photorealistic," "8K" — per research finding that these suppress motion.

## Mapping (hidden from operator until after pick)
- **Output A:** Kling AI
- **Output B:** Runway Gen-4.5

## Brief (shared intent — not a prompt)
An elderly woman (70s, white hair in a loose bun, reading glasses on nose, weathered hands with visible veins) sits at a wooden kitchen table. Morning sunlight streams through a window to her left. She's reading a handwritten letter. She pauses, looks up toward the window, and a faint smile crosses her face — the kind that comes with a memory. Warm but not saturated. Natural imperfections: age spots on hands, slight under-eye circles, asymmetric smile. Shot on medium close-up, soft natural light.

## Prompt A — Kling AI (action/timeline dialect)
A 75-year-old woman with white hair in a loose bun, reading glasses perched on her nose. Deep laugh lines around her eyes, age spots on her temples, slightly crooked smile. She wears a soft cream cardigan over a faded floral blouse. She sits at a worn wooden kitchen table, reading a handwritten letter held in weathered hands with visible veins.

0-4s: Her eyes move across the page, one finger tracing a line. Her lips press together softly, a quiet breath.

4-8s: She pauses. Looks up toward the window on her left. Morning sunlight catches fine white hairs at her temple. A faint asymmetric smile forms — slow, private, remembering something. Her eyes glisten slightly.

Soft window light from camera-left, gentle shadow falloff. Warm but restrained color grading. Visible pores on forehead. Fine facial hair catching the light. Shot on 35mm film, subtle grain.

## Prompt B — Runway Gen-4.5 (force/physics prose dialect)
An elderly woman with white hair pulled into a loose bun, reading glasses balanced on her nose. Deep laugh lines, age spots at her temples, a slightly crooked smile. Cream cardigan over faded floral blouse. She sits at a scarred wooden kitchen table holding a handwritten letter in weathered hands.

Her eyes track slowly across the page. One finger drags along a line of ink. She draws a quiet breath, lips pressing together.

Then she stops. Her gaze lifts toward the window. Morning light catches the fine white hairs at her temple. Something lands — a memory settling behind her eyes. A slow, lopsided smile pulls at one corner of her mouth.

Soft window light from the left. Warm but muted tones. Visible pores, fine peach fuzz on her cheeks, faint under-eye circles. 35mm film texture, subtle grain.
