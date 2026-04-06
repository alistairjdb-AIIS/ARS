# Blind A/B Test v11 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — anime sub-register
**Subject:** anime young woman on rooftop at dusk, wind in hair, city skyline, contemplative

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v11-output-a.mp4` | **5-part shot-list** (crafted) |
| `/root/blind-ab/v11-output-b.mp4` | **Terse brief paste** |

No overlays. Brief held constant within pair. First character generation test.

## Output A prompt (crafted)
> "Cinematography: medium shot, slow push-in from waist-level, shallow depth of field with city skyline softly defocused. Subject: anime-style young woman, dark hair past shoulders, casual clothes, sitting on concrete rooftop edge, legs dangling over the side. Action: wind blows through her hair with irregular gusts, loose strands drift across her face, she gazes toward the horizon without moving, fabric of her jacket shifts slightly in breeze. Context: golden hour dusk, warm orange-pink sky fading to deep blue above, city skyline silhouetted in mid-ground, rooftop has weathered concrete texture with a few scattered items behind her, warm rim light from setting sun on her hair and shoulder edges. Style & Ambiance: hand-drawn anime aesthetic with visible line work, warm sunset + cool shadow palette, contemplative solitude mood, Makoto Shinkai-inspired atmospheric lighting. Audio: soft rooftop wind, distant city hum, faint wind chime."

## Output B prompt (terse)
> "8-second anime-style scene. Young woman sitting on a rooftop edge at dusk, legs dangling, wind blowing through her dark hair. City skyline in the background. She gazes at the horizon, contemplative. Warm sunset palette. Slow camera push-in. No dialogue."

## Negative prompt (both)
> "live-action, photorealistic, 3D render, CGI, text, readable characters, logos, watermarks, motion blur, warping, jitter, overexposure, deformed hands, extra fingers"

## Hypothesis
Prompt-depth was retired as a causal variable for photoreal (proxy for narrative coherence). This test checks if that finding transfers to stylized characters. If crafted wins, it may be because character rendering benefits more from physical specificity than landscapes do. If terse wins or ties, transfer confirmed.
