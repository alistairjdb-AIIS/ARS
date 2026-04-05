# Blind A/B Test v3 — Labels (committed BEFORE render)
**Date:** 2026-04-05
**Element:** Photoreal subjects (Element 1 of curriculum)
**New subject:** glass bottle of olive oil (introduces transparency + liquid refraction physics, not tested in ceramic bowl)

## Declared Intent (per feedback-ab-declare-intent-first.md)

**Hypothesis:** Does crafted shot-list prompting CONSISTENTLY beat terse prompting on photoreal subjects, or was v2's result subject-specific?

**Target specification:** 8-second cinematic photoreal still-life. Clear glass bottle of olive oil on polished marble surface. Warm morning window sidelight from frame-right at 45 degrees. Slow camera orbit ~20 degrees around bottle. Golden-green liquid visible through glass with light refraction. Shallow depth of field. Warm amber palette. Soft grain texture. 16:9.

**Success criteria:** Does B (crafted) better deliver the target spec than A (terse)? Judge: execution of brief, physics realism (liquid, glass refraction), lighting craft.

**Craft constraint from v2 lesson:** No "35mm film grain" terminology — replaced with "soft organic noise / subtle grain texture" to avoid literal filmstrip-edge artifacts.

## Label Mapping

| File | Label | Approach |
|---|---|---|
| `/root/blind-ab/v3-output-a.mp4` | **A (first instinct)** | Brief pasted terse |
| `/root/blind-ab/v3-output-b.mp4` | **B (after internal dialogue)** | Brief expanded into 5-part Veo shot-list, NO new subject elements |

Both: identical ORO typography overlay at seconds 4.5-8.

## Output A prompt (first instinct, terse)
> "8-second cinematic photoreal still-life. Clear glass bottle of olive oil on polished marble surface. Warm morning window sidelight from frame-right at 45 degrees. Slow camera orbit 20 degrees around bottle. Golden-green liquid visible through glass with light refraction. Shallow depth of field. Warm amber palette."

## Output B prompt (5-part shot-list of same brief)
> "Cinematography: 85mm lens, shallow depth of field f/2.0, slow camera orbit 20 degrees around subject, locked vertical at bottle mid-height. Subject: clear glass bottle of olive oil, slightly off-center, golden-green liquid visible through glass, subtle light refraction through bottle glass. Action: liquid shifts slowly as camera orbits, catching highlights at varying angles. Context: polished marble surface with subtle gray veining, warm morning light streams from frame-right window at 45 degrees, soft rim highlight on glass bottle edge, light refracts through liquid creating warm amber glow on marble beneath. Style & Ambiance: slow contemplative artisan luxury, warm amber + golden-green + muted marble palette, soft organic noise texture, subtle halation on glass highlights, quiet morning atmosphere. Audio: soft morning quiet, distant birdsong."

## Negative prompt (both, shared)
> "faces, hands, people, text, readable characters, logos, watermarks, motion blur, warping, morphing, bright backgrounds, overexposure, jitter, fast motion, busy frame, filmstrip edges, sprocket holes, film burns"

## Typography Overlay (identical on both)
- Title: "ORO" (DejaVu Serif, 72pt, white 92%)
- Tagline: "first pressing, single estate" (DejaVu Serif Italic, 22pt, white 85%)
- Reveal: seconds 4.5-8, fade-in
