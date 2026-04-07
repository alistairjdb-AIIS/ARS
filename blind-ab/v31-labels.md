# Test v31 — Baby Phoenix continuous story

## Test Parameters
- **Character:** Baby Phoenix (Nano Banana 2 reference image)
- **Tool:** Runway-hosted Veo 3.1 fast (image-to-video chaining, all clips)
- **Image gen:** Nano Banana 2 for opening frame
- **Technique:** Frame-chained continuous narrative, one environment family, script with foreshadowing

## The Scene (one continuous story)
A baby phoenix sits on a branch at the edge of a volcanic crater at sunrise. It tries to fly — flaps its wings hard, the small wing causes it to spin, it tumbles off the branch. Falls toward the warm volcanic rocks below. Catches itself mid-fall with a frantic burst of wing-flapping, hovering clumsily. Lands on a warm rock next to a volcanic vent. Steam rises around it. The phoenix's tail flame flickers brighter from the volcanic warmth. Emboldened, it tries again — runs along the crater rim, flapping hard, and this time lifts off. Wobbly, uneven, but flying. It rises above the crater as dawn breaks golden behind it. Its whole body glows with warm ember light.

## Clip Breakdown
### Clip 1 (8s): The attempt
Baby phoenix perched on a gnarled branch at the crater's edge. Sunrise warming the volcanic landscape. It spreads its wings — one noticeably smaller. Flaps hard. Spins. Tumbles off the branch.

### Clip 2 (8s): The save
Falling toward volcanic rocks. Frantic wing-flapping. Catches itself just above the ground, hovering clumsily. Lands on a warm rock. Steam rises from a nearby vent. Its tail flame flickers brighter from the volcanic heat. It looks up at where it fell from, determined.

### Clip 3 (8s): The flight
The phoenix runs along the crater rim, flapping hard. Lifts off — wobbly, uneven, but airborne. Rises above the crater edge as dawn breaks golden behind it. Its feathers glow with warm ember light. It lets out a triumphant chirp. Flying.

## Pipeline
1. Nano Banana 2 → opening frame (phoenix on branch, volcanic crater, sunrise)
2. Runway Veo 3.1 fast image-to-video → Clip 1
3. Extract last frame (lossless PNG)
4. Runway Veo 3.1 fast image-to-video → Clip 2
5. Extract last frame (lossless PNG)
6. Runway Veo 3.1 fast image-to-video → Clip 3
7. ffmpeg concat
