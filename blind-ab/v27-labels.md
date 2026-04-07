# Blind A/B Test v27 — Labels (committed before render)

## Test Parameters
- **Register:** Pixar/3D — multi-scene narrative sequence
- **Variable:** Multi-tool stitched pipeline vs Veo-only pipeline
- **Hypothesis:** Multi-tool pipeline (Recraft → Runway → ElevenLabs → ffmpeg) should win on character consistency. Veo-only should win on per-clip audio-visual coherence. The question is which produces a better END-TO-END narrative sequence.
- **This is a PIPELINE test, not a single-clip test.** The deliverable is a 3-scene composite, not individual clips.

## Mapping (hidden from operator until after pick)
- **Output A:** Multi-tool pipeline (Runway video + ElevenLabs SFX + ffmpeg composite)
- **Output B:** Veo 3.1 only (joint audio+video, 3 clips composited via ffmpeg)

## Story (shared brief — 3 scenes, same robot character)
A small Pixar-style robot explores the world alone. Three moments from its day:

**Scene 1 — Junkyard discovery (dawn)**
The robot sits among rusted scrap metal. It spots a tiny yellow flower pushing through a crack. Its head tilts, one claw reaches out — then pulls back, afraid. It gently cups both claws around the flower. Warm golden light, dust in the air.
Audio: metallic creaking, wind through scrap, a soft mechanical whir when it tilts.

**Scene 2 — Rainy city night**
The robot stands on a wet sidewalk under a flickering streetlamp. Rain bounces off its body. It looks up, holds one claw out to catch droplets. Its eyes brighten when a drop lands in its palm.
Audio: rain on metal, distant traffic, streetlamp buzz, a soft electronic chime when its eyes brighten.

**Scene 3 — Sunlit meadow (golden hour)**
The robot walks through tall grass. Butterflies circle it. It swats at one, misses, stumbles. Catches its balance and watches a butterfly land on its claw. Freezes.
Audio: wind through grass, insects, birdsong, a gentle mechanical whir as it freezes.

## Pipeline A — Multi-tool (Runway + ElevenLabs + ffmpeg)
1. Video: Runway Gen-4 Turbo clips from v26 (already generated, character-locked via reference image)
2. Audio: ElevenLabs Sound Effects API — generate SFX per scene
3. Composite: ffmpeg — merge audio onto video, concatenate 3 scenes with 1s crossfade

## Pipeline B — Veo 3.1 only
1. Video+Audio: Veo 3.1 standard model — 3 separate generations with audio prompts embedded
2. Composite: ffmpeg — concatenate 3 scenes with 1s crossfade
3. Character consistency: text-only (same character description repeated verbatim)

## Cost comparison
- Pipeline A: $1.50 (Runway, already spent) + ~$0.10 (ElevenLabs SFX) = ~$1.60
- Pipeline B: 3 × $3.20 (Veo standard, 8s) = $9.60
- Pipeline B (fast): 3 × $1.20 (Veo fast, 8s) = $3.60
Using Veo fast to keep costs reasonable.
