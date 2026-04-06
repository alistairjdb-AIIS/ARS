# Blind A/B Test v13 — Labels (committed BEFORE render)
**Date:** 2026-04-06
**Element:** Stylized characters — 3D Pixar-style sub-register
**Subject:** small dented robot on a park bench feeding pigeons, warm afternoon, autumn leaves

## Label Mapping (RANDOMIZED)

| File | Approach |
|---|---|
| `/root/blind-ab/v13-output-a.mp4` | **5-part shot-list** (crafted) |
| `/root/blind-ab/v13-output-b.mp4` | **Terse brief paste** |

No overlays. Brief held constant within pair. Third stylized character test — shifts sub-register from anime to 3D/Pixar to test if crafted advantage is style-agnostic.

## Output A prompt (crafted)
> "Cinematography: slow dolly-in from medium-wide to medium close-up, slightly low angle looking up at bench, shallow depth of field with autumn trees softly blurred behind. Subject: small humanoid robot with a rounded dented metal body, mismatched bolts, one slightly flickering eye-light, seated on a worn wooden park bench with peeling green paint. Action: robot reaches into a small paper bag on the bench, pulls out a breadcrumb, and tosses it gently toward three pigeons on the ground — pigeons hop and peck, one flutters its wings briefly, robot tilts its head watching them with subtle mechanical whir. Context: quiet city park in late afternoon, golden hour light filtering through canopy of maple trees, orange and red leaves scattered on the ground and drifting slowly through the air, empty path behind the bench, distant park lamp. Style & Ambiance: 3D Pixar-style rendering, warm saturated autumn palette, gentle whimsical mood, slight melancholy in the robot's solitude contrasted with the pigeons' liveliness. Audio: soft wind rustling leaves, distant birds chirping, subtle mechanical servo sounds when robot moves, pigeon cooing, gentle ambient park atmosphere."

## Output B prompt (terse)
> "8-second 3D Pixar-style animated scene. A small dented robot sits on a park bench feeding breadcrumbs to pigeons. Warm golden hour afternoon light, autumn leaves on the ground and falling gently. Whimsical and slightly melancholic mood. Camera slowly moves closer. No dialogue."

## Negative prompt (both)
> "live-action, photorealistic, anime, hand-drawn, 2D, text, readable characters, logos, watermarks, motion blur, warping, jitter, overexposure, deformed hands, extra fingers, uncanny valley"

## Hypothesis
v11 (anime static) and v12 (anime motion) both favored crafted — environmental completeness was the deciding factor. v13 tests if this transfers to 3D/Pixar sub-register where the rendering pipeline is fundamentally different. If crafted wins again, the pattern is style-agnostic within stylized characters. If terse wins, the advantage may be anime-specific.
