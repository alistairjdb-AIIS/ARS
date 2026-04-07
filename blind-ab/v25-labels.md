# Blind A/B Test v25 — Labels (committed before render)

## Test Parameters
- **Register:** Pixar/3D animation
- **Tools:** Runway Gen-4.5 (text-to-video) vs Kling AI (text-to-video)
- **Variable:** Cross-tool comparison with tool-optimized prompts (same intent, different syntax)
- **Brief:** A small round robot in a junkyard discovers a tiny flower growing between rusted metal. It tilts its head, gently reaches out with one claw, and pulls back — afraid of crushing it. Then it carefully cups both claws around the flower, shielding it. Late afternoon golden light.
- **Hypothesis:** Pixar/3D has the strongest model priors — both tools should perform well. The question is whether Runway's scene composition (A2D architecture strength) or Kling's motion quality (3D VAE strength) produces a more emotionally resonant Pixar scene.
- **Methodology:** Tool-optimized prompts. Quality modifiers stripped. Acting chain present. Camera minimal.

## Mapping (hidden from operator until after pick)
- **Output A:** Runway Gen-4.5
- **Output B:** Kling AI

## Brief (shared intent — not a prompt)
A small, round-bodied robot (friendly shape language — spherical head, stubby limbs, oversized round eyes with blue LED irises) sits in a vast, sunlit junkyard. Rusted car parts, old washing machines, tangled wires. It spots a tiny yellow flower growing through a crack in rusted sheet metal. It tilts its head (mechanical whir), reaches toward the flower with one three-pronged claw — then freezes and pulls back, afraid of crushing it. Processing beat: looks at its own claws, then back at the flower. Then gently cups both claws around the flower to shield it from the wind. Late afternoon golden light streaming through gaps in the scrap piles, dust motes in the air. 60-30-10: weathered silver body (60%), rust-orange patina patches (30%), bright blue LED eyes (10%).

## Prompt A — Runway Gen-4.5 (force/physics prose dialect)
Pixar-style 3D animation. A small spherical robot with a weathered silver body, rust-orange patches, and bright blue LED eyes sits among mountains of rusted scrap metal in a sunlit junkyard.

It spots a tiny yellow flower pushing through cracked metal. Its round head tilts with a soft mechanical click. One three-pronged claw extends toward the petals — then jerks back as if burned. It stares at its own claws. Too clumsy. Too heavy.

Then both claws reach out, slowly curving around the flower without touching it. Shielding it from the breeze.

Late afternoon light cuts through gaps in the scrap piles. Warm dust drifts through the beams.

## Prompt B — Kling AI (action/timeline dialect)
Pixar-style 3D animation. A small round-bodied robot with weathered silver plating, rust-orange patina patches, and oversized bright blue LED eyes. Stubby limbs, three-pronged claws. It sits in a vast sunlit junkyard surrounded by rusted car parts and tangled wires.

0-4s: The robot notices a tiny yellow flower growing through cracked sheet metal. Its spherical head tilts with a mechanical whir. One claw extends slowly toward the petals — then pulls back sharply. It looks down at its own claws, processing.

4-8s: Both claws reach out carefully, curving around the flower without touching it, cupping it gently. Shielding it from the wind. Its blue LED eyes brighten slightly.

Late afternoon golden light streaming through gaps in scrap piles. Warm dust motes drifting. Soft shadows.
