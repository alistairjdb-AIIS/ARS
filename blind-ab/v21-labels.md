# Blind A/B Test v21 — Labels (committed before render)

## Test Parameters
- **Register:** Anime (Makoto Shinkai sub-register)
- **Tool:** Kling AI
- **Brief:** Young woman on train platform at dusk, watching departing train. Wind moves hair and scarf. 5-8s.
- **Variable:** First instinct (A) vs internal-dialogue-refined (B)
- **Hypothesis:** Internal dialogue will improve narrative coherence by questioning ambient assumptions in the first-instinct prompt.

## Mapping (hidden from operator until after pick)
- **Output A:** First instinct prompt
- **Output B:** After 5-whys internal dialogue

## Prompts

### Prompt A (first instinct)
Makoto Shinkai style anime, a young woman with dark hair stands alone on a rural train platform at dusk. A departing train's red tail lights glow in the distance. Wind catches her long navy scarf and loose strands of hair. She watches the train leave, one hand slightly raised as if she almost waved. Golden hour light filters through scattered clouds, casting long warm shadows across the wooden platform. Atmospheric dust particles catch the light. Soft ambient sounds of cicadas and distant rails.

### Prompt B (after internal dialogue)

**5-whys applied to Prompt A:**
1. WHY "golden hour" + "dusk"? These are different times. Dusk is post-sunset, golden hour is pre-sunset. Pick one. → Dusk only. Blue-purple sky, no golden light.
2. WHY "scattered clouds"? What do they add narratively? → Clouds at dusk create layered color gradients (pink/orange/purple). Keep but specify: "stratified clouds banding pink and deep blue."
3. WHY "one hand slightly raised"? This locks a specific pose that may not read well in 5s of video. → Loosen: "her fingers curl at her side, deciding whether to wave." Internal conflict, not frozen gesture.
4. WHY "atmospheric dust particles"? At dusk in a rural station, more likely: fireflies, or moths around the platform light. → Replace with: "a single moth circles the warm overhead platform lamp."
5. WHY cicadas? Cicadas are summer afternoon, not dusk. Dusk sounds: evening frogs, distant chime, or silence broken only by wind. → "Silence except wind and a distant crossing bell."

**Resulting prompt:**
Makoto Shinkai style anime, a young woman with dark hair stands alone on a rural train platform at dusk. Deep blue-purple sky with stratified clouds banding pink near the horizon. A departing train's red tail lights shrink into the distance along a single track. Wind catches her long navy scarf and loose strands of hair. She stares after the train, her fingers curling at her side, deciding whether to wave. A single moth circles the warm overhead platform lamp. Weathered wooden planks beneath her feet. Silence except wind and a distant crossing bell.
