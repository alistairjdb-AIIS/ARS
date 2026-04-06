# Blind A/B Test v23 — Labels (committed before render)

## Test Parameters
- **Register:** Anime (generic anime style — no Shinkai due to Runway moderation, kept consistent)
- **Tool:** Kling AI v1-6
- **Brief:** Same scene as v21/v22 — person on train platform at dusk, departing train. 5s.
- **Variable:** Hand-crafted prompt (A) vs /animate pipeline prompt (B) — same prompts as v22 but on Kling
- **Hypothesis:** Kling should produce higher quality anime than Runway gen4.5 (v22 finding). /animate pipeline should still win if restraint helps on Kling too.
- **Cross-tool comparison:** v22 (Runway) vs v23 (Kling), same prompts.

## Mapping (hidden from operator until after pick)
- **Output A:** Hand-crafted (rich environmental detail)
- **Output B:** /animate pipeline (acting chain + restraint)

## Prompts (identical to v22)

### Prompt A (hand-crafted)
Anime style illustration. A person with dark hair stands alone on a rural train platform at dusk. A departing trains red tail lights glow in the distance. Wind catches their long navy scarf and loose strands of hair. They watch the train leave, one hand slightly raised. Golden light filters through scattered clouds, casting warm shadows across the wooden platform. Atmospheric dust particles catch the light.

### Prompt B (/animate pipeline — acting chain + restraint)
Anime style illustration. Rural train platform, autumn dusk. Deep blue-purple sky fading to amber at the horizon. A person with dark hair stands still as a departing trains red lights shrink down the single track. Wind pulls their navy scarf sideways. Their hand lowers slowly back to their side. A single warm lamp overhead. Cool air. The platform is empty except for them.
