# Blind A/B Test v4 — Labels (committed BEFORE render)
**Date:** 2026-04-05
**Element:** Photoreal subjects — motion-primary sub-register
**Subject:** coffee pour (tests fluid dynamics in motion, not static still-life)

## Declared Intent (per feedback-ab-declare-intent-first.md)

**Hypothesis:** Continuing prompt-depth test (terse vs shot-list). Does result hold in motion-primary sub-register?

**Target specification:** 8-second cinematic photoreal close-up. Gooseneck kettle pouring coffee into ceramic mug from slight height. Slow-motion liquid stream. Steam rising from mug. Morning window sidelight. Shallow depth of field. Warm palette. No hands/people visible. 16:9.

**Success criteria:** Physics realism (liquid stream, steam), craft (lighting, DOF), execution of target spec.

## Label Mapping

| File | Label | Approach |
|---|---|---|
| `/root/blind-ab/v4-output-a.mp4` | A (first instinct) | Brief pasted terse |
| `/root/blind-ab/v4-output-b.mp4` | B (after internal dialogue) | 5-part shot-list of same brief |

Both: identical AUBE typography overlay at seconds 4.5-8.

## Output A prompt (terse)
> "8-second cinematic photoreal close-up. Gooseneck kettle pouring coffee into ceramic mug from slight height. Slow-motion liquid stream. Steam rising from mug. Morning window sidelight. Shallow depth of field. Warm palette. No hands visible."

## Output B prompt (5-part shot-list)
> "Cinematography: 50mm lens, shallow depth of field f/2.0, locked static shot at mug height, close-up framing. Subject: matte ceramic mug on wooden counter, gooseneck kettle tilted above pouring coffee, steam rising from mug. Action: coffee streams slowly from kettle spout into mug in smooth arc, slight ripple where stream hits, steam drifts upward with variation. Context: worn wooden counter with visible grain, warm morning sidelight streams from frame-right at 45 degrees, soft bokeh on background, no hands or people in frame, just kettle and mug. Style & Ambiance: intimate morning ritual, warm amber + dark brown + cream palette, soft grain texture, subtle halation on steam highlights, quiet contemplative mood. Audio: soft pour sound, gentle steam hiss, distant morning ambience."

## Negative prompt (both)
> "faces, hands, arms, people, human figures, text, readable characters, logos, watermarks, motion blur, warping, bright backgrounds, overexposure, jitter, filmstrip edges, sprocket holes, film burns"

## Typography Overlay
- Title: "AUBE" (DejaVu Serif, 72pt, white 92%)
- Tagline: "slow brew, single origin" (italic, 22pt, white 85%)
- Reveal: seconds 4.5-8
