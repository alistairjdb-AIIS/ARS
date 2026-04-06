# Blind A/B Test v22 — Labels (committed before render)

## Test Parameters
- **Register:** Anime (Makoto Shinkai sub-register)
- **Tool:** Runway gen4.5 (FIRST USE — also testing tool quality vs Kling v21)
- **Brief:** Same scene as v21 — young woman on train platform at dusk, watching departing train. 5s.
- **Variable:** v21's winning hand-crafted prompt (A) vs /animate pipeline-designed prompt (B)
- **Hypothesis:** /animate's restraint-based approach will produce a more narratively coherent output by letting the model populate ambiance, while the hand-crafted prompt's environmental richness may overwhelm gen4.5's capacity.
- **Secondary test:** Runway gen4.5 quality on anime content (first data point).

## Mapping (hidden from operator until after pick)
- **Output A:** v21's winning prompt (hand-crafted first instinct, unchanged)
- **Output B:** /animate pipeline prompt (acting-chain + restraint)

## Prompts

### Prompt A (v21 winner, hand-crafted)
Makoto Shinkai style anime, a young woman with dark hair stands alone on a rural train platform at dusk. A departing trains red tail lights glow in the distance. Wind catches her long navy scarf and loose strands of hair. She watches the train leave, one hand slightly raised as if she almost waved. Golden hour light filters through scattered clouds, casting long warm shadows across the wooden platform. Atmospheric dust particles catch the light. Soft ambient sounds of cicadas and distant rails.

### Prompt B (/animate pipeline — acting chain + restraint)
Makoto Shinkai anime. Rural train platform, autumn dusk. Deep blue-purple sky fading to amber at the horizon. A young woman with dark hair stands still as a departing train's red lights shrink down the single track. Wind pulls her navy scarf sideways. She was about to wave but didn't — her hand lowers slowly back to her side. A single warm lamp overhead. Cool air. The platform is empty except for her.
