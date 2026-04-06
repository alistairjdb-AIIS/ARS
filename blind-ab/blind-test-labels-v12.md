# Blind A/B Test v12 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — anime sub-register
**Subject:** anime boy walking through rain-soaked Japanese street at night, umbrella, neon reflections

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v12-output-a.mp4` | **Terse brief paste** |
| `/root/blind-ab/v12-output-b.mp4` | **5-part shot-list** (crafted) |

No overlays. Brief held constant within pair. Second character test — tests motion (walking) vs v11 (static).

## Output A prompt (terse)
> "8-second anime-style scene. Boy walking through a rain-soaked Japanese street at night, holding a clear umbrella. Neon signs reflecting in puddles on the ground. Slow walk, camera tracking alongside. Moody blue and neon palette. No dialogue."

## Output B prompt (crafted)
> "Cinematography: medium tracking shot moving alongside character from left, eye-level, shallow depth of field with neon signs softly defocused behind. Subject: anime-style teenage boy, dark jacket with hood down, holding a clear umbrella, walking at a slow unhurried pace through a narrow Japanese street. Action: rain falls steadily on umbrella surface with visible droplet impacts, feet step through shallow puddles creating small ripple rings, neon reflections in wet pavement stretch and distort with each footstep, umbrella tilts slightly with walking rhythm. Context: nighttime, wet narrow street lined with small shops and izakayas, neon signage in Japanese casting colored light on wet surfaces, steam rising from a vent or grate, no other people visible, rain streaks visible in backlit neon glow. Style & Ambiance: hand-drawn anime aesthetic, moody blue-purple base palette with warm neon accents of pink and orange, melancholic solitude mood, rain as atmosphere not obstacle. Audio: steady rain on umbrella, soft footsteps in puddles, distant muffled music from a shop, faint city hum."

## Negative prompt (both)
> "live-action, photorealistic, 3D render, CGI, text, readable characters, logos, watermarks, motion blur, warping, jitter, overexposure, deformed hands, extra fingers"

## Hypothesis
v11 (static character) favored crafted — environmental completeness was the deciding factor. v12 tests if the same holds for character-in-motion where the crafted prompt specifies physical interactions (rain on umbrella, puddle ripples, neon distortion in water). If crafted wins again on "completeness," the pattern is strengthening.
