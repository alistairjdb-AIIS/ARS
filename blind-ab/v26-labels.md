# Blind A/B Test v26 — Labels (committed before render)

## Test Parameters
- **Register:** Pixar/3D — multi-shot character consistency
- **Tool:** Runway Gen-4 Turbo (image-to-video with reference)
- **Variable:** NOT a comparison test. This is a CAPABILITY test — can Runway maintain character identity across 3 different scenes from the same reference image?
- **Brief:** Same robot character from v25, placed in 3 different scenes with different actions and lighting. The test is whether the robot looks like the SAME character across all 3.
- **Reference image:** Generated via Recraft V4 from the v25 character description.
- **Success criteria:** Can the operator identify these as the same character across all 3 clips? Rate identity consistency 1-10.
- **Cost:** 3x Gen-4 Turbo clips at $0.05/s x 10s = $1.50 total

## Mapping
- **Output A:** Scene 1 — robot in junkyard (same as v25 brief, with reference image)
- **Output B:** Scene 2 — robot in a rainy city street at night
- **Output C:** Scene 3 — robot in a sunlit meadow

## Reference Image
Generated via Recraft V4. Prompt: Pixar-style 3D robot character — small spherical body, weathered silver plating, rust-orange patina patches, oversized bright blue LED eyes, stubby limbs, three-pronged claws. Standing on neutral gray background, full body visible, front-facing.

## Scene Prompts (Runway Gen-4 Turbo — force/physics prose, NO re-description of reference)

### Scene 1 — Junkyard discovery
The robot sits among rusted scrap metal. It spots a tiny yellow flower pushing through a crack. Its head tilts with a click, one claw reaches out — then pulls back. It cups both claws gently around the flower. Late afternoon golden light, warm dust in the air.

### Scene 2 — Rainy city night
The robot stands on a wet sidewalk under a flickering streetlamp. Rain bounces off its metal body. It looks up at the rain, then holds one claw out, catching droplets. Its LED eyes dim slightly, then brighten as a raindrop lands perfectly in its palm. Neon reflections in puddles. Cool blue-purple light.

### Scene 3 — Sunlit meadow
The robot walks through tall grass in a wide meadow. Butterflies circle its head. It swats gently at one, misses, stumbles. Catches its balance and watches the butterfly land on its claw. Freezes. Bright midday sun, lens flare, warm green and gold palette.
