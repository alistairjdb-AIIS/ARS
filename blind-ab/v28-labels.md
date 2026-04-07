# Blind A/B Test v28 — Labels (committed before render)

## Test Parameters
- **Register:** Pixar/3D — 3-scene narrative with inter-scene fluidity
- **Variable:** Frame-chained Veo 3.1 (image-to-video, last frame → next scene) vs v27 Pipeline B (Veo standalone, no chaining)
- **Hypothesis:** Frame-chaining should create visual continuity between scenes — the last frame of scene N becomes the first frame of scene N+1, forcing the model to bridge environments rather than generating from scratch. This should make the sequence feel like one story instead of 3 disconnected clips.
- **Tool:** Veo 3.1 fast via Runway API (image-to-video with audio)

## Mapping (hidden from operator until after pick)
- **Output A:** Frame-chained Veo 3.1 (new — sequential generation, each scene starts from previous scene's last frame)
- **Output B:** v27 Pipeline B (Veo standalone — already generated, 3 independent clips composited)

## Pipeline (frame-chaining)
1. Veo 3.1 text-to-video → Scene 1 (junkyard, with audio)
2. Extract last frame of Scene 1
3. Veo 3.1 image-to-video → Scene 2 (last frame as input, rainy city, with audio)
4. Extract last frame of Scene 2
5. Veo 3.1 image-to-video → Scene 3 (last frame as input, meadow, with audio)
6. ffmpeg → concatenate

## Scene Prompts (same story as v27, Veo-native dialect)

### Scene 1 (text-to-video)
3D animated style. A small round-bodied robot with weathered silver plating, rust-orange patina patches, oversized bright blue LED eyes, stubby limbs, three-pronged claws, and a small antenna on top.

The robot sits alone in a vast junkyard at dawn. It notices a tiny yellow flower growing through cracked metal. Its head tilts with a mechanical whir. One claw reaches toward the petals — then pulls back gently. Both claws cup around the flower, shielding it.

Warm golden dawn light through gaps in scrap piles. Dust motes drifting. Soft shadows on rusted metal.

Audio: metallic creaking, wind through scrap, soft mechanical whir, warm ambient hum.

### Scene 2 (image-to-video, from Scene 1 last frame)
The same robot now stands on a wet city sidewalk under a flickering streetlamp at night. Rain bounces off its metal body. It looks up at the rain, holds one claw out to catch droplets. Its LED eyes dim then brighten as a raindrop lands in its palm.

Cool blue-purple neon light. Wet pavement reflections. Rain streaks in lamplight.

Audio: rain on metal and pavement, distant traffic, streetlamp buzz, soft electronic chime when eyes brighten.

### Scene 3 (image-to-video, from Scene 2 last frame)
The same robot walks through tall grass in a wide meadow at golden hour. Butterflies circle its head. It swats at one, misses, stumbles. Catches its balance. A butterfly lands on its outstretched claw. It freezes perfectly still.

Bright golden sunlight, lens flare, warm green and gold. Grass swaying.

Audio: wind through grass, insects, birdsong, gentle mechanical whir as it freezes.
