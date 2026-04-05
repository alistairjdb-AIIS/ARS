# Blind A/B Test v2 — Labels (committed BEFORE render)
**Date:** 2026-04-05
**Fix applied:** both prompts target IDENTICAL brief. Only prompt-craft-depth varies.
**Also fixed:** typography overlay applied to BOTH (not just B), holding that variable constant too.

## Shared Brief (both outputs target this exact description)
8-second cinematic still-life. Handmade ceramic bowl on weathered oak surface. Morning window sidelight from frame-right at 45 degrees. Slow camera push-in. Steam rising from bowl interior, drifting in the sidelight. Warm palette. 16:9.

## Label Mapping

| File | Label | Approach |
|---|---|---|
| `/root/blind-ab/v2-output-a.mp4` | **A (first instinct)** | Brief pasted terse as single-paragraph prompt |
| `/root/blind-ab/v2-output-b.mp4` | **B (after internal dialogue)** | Brief expanded into 5-part Veo shot-list (cinematography + subject + action + context + style & ambiance) — NO new subject elements added |

Both get identical KAOLIN typography overlay (serif title + italic tagline, seconds 4.5-8, ffmpeg drawtext).

## Output A prompt (first instinct — terse paste)
> "8-second cinematic still-life. Handmade ceramic bowl on weathered oak surface. Morning window sidelight from frame-right at 45 degrees. Slow camera push-in. Steam rising from bowl interior, drifting in the sidelight. Warm palette."

## Output B prompt (after internal dialogue — 5-part shot-list of same brief)
> "Cinematography: 85mm lens, shallow depth of field f/2.0, slow dolly push-in 15%, locked horizontal at table height. Subject: handmade ceramic bowl, slightly off-center left composition. Action: steam rises from bowl interior, drifting slowly in the light beam. Context: weathered oak surface with visible grain, warm morning sidelight streams from frame-right window at 45 degrees, soft rim highlight on bowl, long shadow across oak. Style & Ambiance: slow contemplative artisan luxury, warm beige + honey-oak + cream palette, 35mm film grain, slight halation on rim highlights, quiet morning atmosphere. Audio: soft morning quiet, distant birdsong."

## Negative prompt (both)
> "faces, hands, people, text, readable characters, logos, watermarks, motion blur, warping, morphing, bright backgrounds, overexposure, jitter, fast motion, busy frame"

## What This Test Answers
Does prompt-craft-depth (terse vs shot-list) produce measurably better execution of the SAME brief, controlling for subject specification and post-processing?

## Protocol
1. Labels committed to git BEFORE render.
2. Both videos generated with Veo 3.1 Fast.
3. Identical typography overlay applied to both.
4. Operator picks preferred blind.
5. Counter reset to 0.
