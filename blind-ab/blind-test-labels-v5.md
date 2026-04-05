# Blind A/B Test v5 — Labels (committed BEFORE render)
**Date:** 2026-04-05
**Element:** Photoreal subjects — environment sub-register (NEW, first test in this sub-register)
**Subject:** morning café/bakery interior at dawn, empty room

## Declared Intent (per feedback-ab-declare-intent-first.md)

**Hypothesis:** Continuing prompt-depth test (terse vs 5-part shot-list). Does the outcome hold in environment sub-register? (tally so far: terse 2, crafted 1, N=3 → this makes N=4; operator threshold = N=5)

**Target specification:** 8s cinematic photoreal interior. Morning café/bakery at dawn, empty room, warm light streaming through windows, wooden tables and chairs, counter in background, slow camera push-in through doorway. Warm palette. 16:9. No people.

**Success criteria:** spatial depth, light behaviour (dust motes, window beams), material authenticity (wood grain, worn textures), architectural detail, execution of target spec.

## Label Mapping (RANDOMIZED — breaks v2/v3/v4 pattern where A was always terse)

| File | Approach |
|---|---|
| `/root/blind-ab/v5-output-a.mp4` | **5-part shot-list** of the brief |
| `/root/blind-ab/v5-output-b.mp4` | **Terse brief paste** |

Both: identical PASSAGE typography overlay at seconds 4.5–8.

## Output A prompt (5-part shot-list)
> "Cinematography: wide lens, slow dolly push-in through open doorway, natural depth of field, establishing shot framing. Subject: empty café/bakery interior at dawn, wooden tables and chairs arranged in room, counter visible in background, window on side wall. Action: camera pushes slowly through doorway into room, dust motes drift visibly through light beams, a window curtain shifts slightly, otherwise stillness. Context: warm golden light streaming through windows at low morning angle, wood grain textures on tables and floor with irregular wear, architectural detail visible (exposed beam or brick), no people in frame. Style & Ambiance: intimate first-light stillness, warm amber + honey wood + cream palette, soft directional shadows, contemplative quiet mood, natural imperfection in surfaces. Audio: distant bird call, soft wood creak, faint room tone."

## Output B prompt (terse)
> "8-second cinematic photoreal interior. Morning café/bakery at dawn, empty room, warm light streaming through windows, wooden tables and chairs, counter in background, slow camera push-in through doorway. Warm palette. No people."

## Negative prompt (both, identical to v4)
> "faces, hands, arms, people, human figures, text, readable characters, logos, watermarks, motion blur, warping, bright backgrounds, overexposure, jitter, filmstrip edges, sprocket holes, film burns"

## Typography Overlay
- Title: "PASSAGE" (DejaVu Serif, 72pt, white 92%)
- Tagline: "open at first light" (italic, 22pt, white 85%)
- Reveal: seconds 4.5–8
