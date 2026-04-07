# Blind A/B Test v29 — Labels (committed before render)

## Test Parameters
- **Register:** Pixar/3D — single continuous narrative
- **Variable:** NOT a comparison test. This is a capability test — can frame-chained generation produce one continuous story in one environment?
- **Character:** Fox kit from v14 (round-bodied, warm orange fur, cream chest, bright amber eyes)
- **Hypothesis:** Writing one continuous scene in one environment + frame-chaining should produce a cohesive story. Previous tests failed because they used different environments, not because of technical limitations.

## The Scene (one continuous story, one environment family)

The fox kit sits by a mossy forest stream, playing with the water. A blue butterfly drifts in and lands on its nose. The fox goes cross-eyed, then the butterfly lifts off and flies away. The fox chases it through the forest. The butterfly leads the fox to a sunlit clearing where dozens of butterflies rest on wildflowers. As the fox arrives, all the butterflies lift off together and swirl into the shape of a heart in the golden light. The fox sits and watches, wide-eyed.

## Scene Breakdown (frame-chained, same environment family)

### Clip 1 (text-to-video, 8s): Discovery
Fox kit by forest stream, paw dabbling in water. Blue butterfly drifts in, lands on its nose. Fox freezes, crosses eyes trying to look at it. Butterfly lifts off.

### Clip 2 (image-to-video from Clip 1 last frame, 8s): The Chase
Fox leaps up and chases the butterfly through dappled forest. Running between trees, leaping over roots. Butterfly stays just ahead. Same forest, continuous motion.

### Clip 3 (image-to-video from Clip 2 last frame, 8s): The Revelation
Fox follows butterfly into a sunlit clearing filled with wildflowers. Dozens of butterflies rest on the flowers. As the fox arrives, they all lift off and swirl upward, forming a heart shape in the golden light. Fox sits, wide-eyed, watching.

## Pipeline
1. Google Veo 3.1 fast → Clip 1 (text-to-video with audio)
2. Extract last frame of Clip 1
3. Runway Veo 3.1 fast → Clip 2 (image-to-video from last frame, with audio)
4. Extract last frame of Clip 2
5. Runway Veo 3.1 fast → Clip 3 (image-to-video from last frame, with audio)
6. ffmpeg → concatenate
