# Test v30 — Continuous fox story, Google Veo 3.1 only

## Test Parameters
- **Register:** Pixar/3D — single continuous narrative
- **Tool:** Google Veo 3.1 fast ONLY (no Runway)
- **Variable:** Same story as v29 but with script fixes + all Google Veo (image-to-video confirmed working)
- **Script fixes from v29 feedback:**
  1. Butterflies visible in background of clip 2 (not spawning in clip 3)
  2. Extract frames at max quality (lossless PNG)
  3. Environment described consistently to reduce background breaks

## Pipeline
1. Google Veo 3.1 fast → Clip 1 (text-to-video with audio)
2. Extract last frame (lossless PNG)
3. Google Veo 3.1 fast → Clip 2 (image-to-video, with audio) — butterflies visible in background
4. Extract last frame (lossless PNG)
5. Google Veo 3.1 fast → Clip 3 (image-to-video, with audio) — butterflies already present, heart formation
6. ffmpeg concat
