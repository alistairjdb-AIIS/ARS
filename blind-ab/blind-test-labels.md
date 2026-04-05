# Blind A/B Test — Labels (committed BEFORE operator views)
**Date:** 2026-04-05
**Session task:** reaching Higgsfield Seedance 2.0 exemplar craft level via Veo 3.1

## Subject
8-second cinematic still-life: handmade ceramic bowl on oak surface, morning window light, 16:9, veo-3.1-fast-generate-preview.

## Label Mapping (the blind answer)

| File | Label | Approach |
|---|---|---|
| `/root/blind-ab/output-a.mp4` | **A (first instinct)** | Single-sentence minimal prompt, raw Veo output, no post-processing |
| `/root/blind-ab/output-b.mp4` | **B (after internal dialogue)** | Crafted 5-part shot-list prompt with explicit cinematography/lighting/camera/lens/audio language, Veo output + typographic brand overlay ("KAOLIN") composited via ffmpeg drawtext |

## Prompts (for post-reveal reference)

### Output A prompt
> "A handmade ceramic bowl on a wooden table with morning window light, 8 seconds, cinematic."

### Output B prompt
> "Slow dolly push-in toward a handmade clay-colored ceramic bowl sitting slightly off-center left on a weathered oak surface, 85mm lens, shallow depth of field. Warm morning sidelight enters from frame-right window at 45 degrees, casting soft golden glow across the bowl's surface and rim highlight while leaving the bowl's interior in deep contemplative shadow. Dust motes drift visibly in the diagonal light rays. Soft bokeh on wood grain texture in background. Steam rises slowly from bowl interior. Palette: warm beige, deep walnut brown, cream highlight, muted ochre. 35mm film grain throughout, slight halation on rim highlights, natural vignette. Subtle breath-like camera micro-movement. Quiet contemplative register. Audio: soft morning quiet, distant birdsong, faint kettle in distance."

## Protocol
1. This labels file committed to git BEFORE either video is rendered.
2. Both videos rendered.
3. Typography overlay applied to B only.
4. Operator views both blind, picks preferred.
5. Counter at `/root/.claude/projects/-root/memory/.blind-test-counter` reset to 0.
