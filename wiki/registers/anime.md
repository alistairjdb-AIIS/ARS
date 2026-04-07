# Anime Visual Register (R01)

> The anime register encompasses Japanese animation visual language adapted for AI video generation — characterized by stylized eye designs, color-as-mood encoding, static-to-movement contrast, and distinct sub-registers (shonen, shojo, seinen, etc.) that each require specific prompt triggers to avoid generic "anime style" output.

**Confidence:** HIGH (crafted beats terse 3-0 in blind A/B; research-informed prompting confirmed)
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 1 memory file

---

## Core Findings

### Sub-Registers / Taxonomy

Eye design is the #1 register signal. Specifying eye style often triggers the broader register automatically. [VERIFIED — character_design_acting_research + cartoon_animation_styles_research converge]

| Sub-Register | Eye Style | Line Weight | Color Palette | Prompt Triggers |
|---|---|---|---|---|
| **Shonen** | Sharp, angular, intense | Bold, sharp lines | High saturation, bold | `"shonen anime, bold sharp lines, dynamic pose, intense eyes"` |
| **Seinen** | Smaller, realistic | Detailed, fine | Muted, restrained | `"seinen anime, realistic proportions, muted palette, fine detail"` |
| **Shojo** | Very large, sparkling | Thin, delicate | Soft pastels | `"shojo anime, large sparkling eyes, delicate lines, soft pastels"` |
| **Slice-of-Life** | Natural, proportionate | Clean, medium | Muted, warm, naturalistic | `"slice-of-life anime, natural proportions, muted warm palette"` |
| **Moe** | Oversized, round, sparkling | Soft, rounded | Candy pastels | `"moe anime, large round sparkling eyes, soft features, pastel colors"` |

**Director/studio anchors provide stronger specificity than sub-register names alone:** [VERIFIED — multiple sources converge]

| Anchor | Best For | Key Prompt Elements |
|---|---|---|
| **Makoto Shinkai** | Atmospheric, romantic | Volumetric clouds, god rays, golden hour, lens flare, rain detail |
| **Studio Ghibli** | Pastoral, whimsical | Watercolor warmth, hand-painted backgrounds, lived-in environments, wind through grass |
| **Cyberpunk anime** | Urban, night, neon | Neon-soaked streets, rain through neon, vertical density, steam, wet reflections |
| **Violet Evergarden** | Beautiful naturalistic | Soft golden natural light, delicate bloom |

**Era-specific triggers differentiate further:** [THEORETICAL]
- `"retro anime screencap, cel-shaded, VHS color palette"` = 90s aesthetic
- `"Makoto Shinkai style, dramatic sky, volumetric lighting"` = modern photorealistic-background
- `"Studio Ghibli style, soft watercolor warmth, hand-painted backgrounds"` = painterly

### Prompting Patterns

**Color as emotional grammar** — anime uses color shifts to encode mood, not just represent physical light. The same room can be warm orange (happy) or desaturated blue-grey (sad). [VERIFIED — character_design_acting_research]

| Mood | Prompt Language |
|---|---|
| Melancholic | `"desaturated blue-violet palette, cool color grading, muted highlights"` |
| Energetic | `"warm orange-gold color grading, high saturation, vibrant warm tones"` |
| Serene | `"soft pastel green palette, gentle white highlights, low contrast"` |
| Nostalgic | `"warm amber color grading, slightly faded tones, nostalgic golden light"` |
| Magical | `"mystical purple palette with cyan accents, glowing highlights"` |

**Shadow color rule:** Anime shadows are never black. Use `"colored shadows, blue-tinted shadow areas, no pure black shadows."` [VERIFIED]

**Lighting toolkit reliability** (from character_design_acting_research):

| Technique | Reliability | Prompt Language |
|---|---|---|
| Rim lighting | VERY HIGH | `"rim lighting, edge light on character, bright outline glow"` |
| Dramatic backlighting | VERY HIGH | `"dramatic backlighting, character silhouette against bright light"` |
| Neon on wet surfaces | VERY HIGH | `"neon reflections on wet pavement, colored light in puddles"` |
| Anime glow/bloom | HIGH | `"soft bloom on skin, gentle glow effect, warm bloom lighting"` |
| Dappled light (komorebi) | HIGH | `"sunlight filtering through tree canopy, dappled light and shadow"` |

**Framing grammar** — anime favors static compositions with cuts, not continuous camera movement. A held shot that suddenly moves is more "anime" than smooth tracking. [VERIFIED]

| Convention | Prompt Language |
|---|---|
| Dramatic low angle | `"low angle shot, camera looking up, dramatic perspective, imposing"` |
| Contemplative wide | `"extreme wide shot, character small in frame, vast landscape"` |
| Pillow shot (cutaway) | `"static wide shot of [environmental detail], held composition, no character"` |
| Half-face shadow | `"split lighting, one side illuminated one side dark"` |

**Acting-chain specificity matters more than camera specification:** [TESTED — v14 confirmed] Be the acting director, not the DP. Spend prompt tokens on stimulus-processing-response sequences, physical-descriptor emotions, and movement quality. Keep camera to 1-2 simple descriptors max.

**Beat count limit:** ~5 acting beats in 8 seconds causes visible scene transitions / fluidity breaks. Limit to 2-3 beats max. [TESTED — v15]

### A/B Test Results

**Anime sub-register: Crafted 3-0 over Terse (decisive).** [TESTED]

| Test | Subject | Result | Key Finding |
|---|---|---|---|
| v11 | Anime static | Crafted won (pre-research) | Style specificity matters even before acting-chain research |
| v12 | Anime motion | Crafted won (pre-research) | Motion quality improves with crafted prompts |
| v16 | Anime train | Research-crafted won (post-research) | Initial impression favored terse, but full quality + coherence analysis reversed it |
| v15 | Anime field | Inconclusive | Style drift confound — terse went 3D (demonstrates the 3D-drift failure mode) |

**Cross-register finding:** Research-crafted prompting wins 5-1 across all stylized characters (v11-v17), with anime being the strongest signal at 3-0. [TESTED]

**Narrative coherence reinforced in anime (v16):** Physically incoherent moments lose to coherent outputs even when flashier. [TESTED — see [[narrative-coherence]]]

### Known Failure Modes

**Style drift to 3D:** AI video models are biased toward photorealism and 3D rendering. A prompt for "anime" may produce 3D-rendered characters with anime proportions. [VERIFIED — observed in v15 where terse prompt drifted to 3D]
- Mitigation: Use supporting descriptors incompatible with 3D: `"flat colors, cel-shaded, 2D animation, hand-drawn look"`
- Stronger mitigation: Reference image workflow (generate anime still first, feed to video model)

**"Anime style" alone produces generic results.** Must specify the sub-register (shonen, seinen, etc.) or director anchor (Shinkai, Ghibli). [VERIFIED]

**Motion limitations — what does NOT translate to AI video:** [VERIFIED]
- Smear frames, impact frame insertion, framerate modulation — these are editing/post techniques, not generation
- Speed line overlays — inconsistent rendering

**Motion that DOES work:** [VERIFIED]
- Wind-on-hair/clothing
- Slow pans across detailed scenes
- Stillness-to-movement contrast (signature anime technique)
- `"Character standing still, hair flowing in wind, clothes rippling"` renders reliably

**Face priors vs body drift:** Anime has strong face priors (large eyes, simplified features) but body proportions can drift. [VERIFIED — character_design_acting_research]

**Temporal coherence:** Error accumulation follows power law; quality drops 3-7 seconds then plateaus. Shorter clips (3-4s) chain better than 8s for complex motion. [VERIFIED]

### Tool Selection

**Veo 3.1** is the primary tool for anime generation. Strong style preservation from reference images. The reference image workflow (generate anime still in target sub-register first, then feed to Veo) is the most reliable method. [VERIFIED]

**WAN 2.2** reportedly maintains flat-shaded style better than Kling for 2D anime consistency. [VERIFIED — community report]

**Kling AI** has not been systematically tested for anime. [UNKNOWN]

---

## Operational Rules

1. **Never use "anime style" alone.** Always specify sub-register (shonen, seinen, shojo, slice-of-life, moe) or director/studio anchor. [VERIFIED — generic produces generic]
2. **Spend prompt tokens on acting chains, not camera choreography.** Stimulus-processing-response sequences with physical descriptors improve output. Camera over-specification hurts. [TESTED — v14]
3. **Limit to 2-3 acting beats per 8-second clip.** More causes scene transitions and fluidity breaks. [TESTED — v15]
4. **Use color as mood, not just description.** Specify the emotional color grade, not just what colors objects are. [VERIFIED]
5. **Front-load character description before environment.** Models weight earlier tokens more heavily. [VERIFIED — Google official docs]
6. **Optimal prompt length: 150-300 characters.** Below 100 = generic. Above 400 = model prioritizes unpredictably. [VERIFIED — Veo official guide]
7. **For consistency across shots:** Repeat character description verbatim. Even small wording changes cause drift. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `character_design_acting_research.md` | Anime sub-register taxonomy, color grammar, lighting toolkit, framing conventions, motion patterns, Veo character patterns, acting chain methodology |
| `project-curriculum-elements.md` | A/B test results (v11-v17 scores), sub-register win patterns (anime 3-0), beat-count finding, narrative coherence reinforcement |
| `feedback-character-prompt-specificity.md` | Acting-chain vs camera-choreography finding, "be the director not the DP" rule, restraint principle |

---

## Related Concepts

- [[cartoon-western]] — Adjacent register; style drift between anime and Western cartoon is a documented failure mode
- [[pixar-3d]] — 3D drift risk from anime prompts; Pixar/3D has strongest model priors
- [[photoreal]] — Narrative coherence principle applies across registers including anime
- [[character-design-prompting]] — Acting chain specificity (stimulus-processing-response)

---

## Deep Reference

- **When** prompting for a specific anime sub-register (shonen vs shojo vs seinen) and the output is generic → **read** `research-data/character_design_acting_research.md` [SOURCE FORMAT: conversation JSON — search for "anime sub-register" and "anime visual language"] **for** sub-register taxonomy with visual characteristics, color grammar per register (shonen = high saturation primary, seinen = muted earth tones), lighting toolkit, and specific prompt triggers that activate each sub-register
- **When** the output drifts to 3D/Pixar instead of 2D anime → **read** `memory/project-curriculum-elements.md` §(Element 3 — Stylized characters) **for** the v15 style drift confound, the finding that "animated" prompts can drift toward 3D training data, and the beat-count limit (~5 acting beats in 8s causes visible scene transitions)
- **When** writing an acting chain for an anime character and need to calibrate specificity level → **read** `memory/feedback-character-prompt-specificity.md` (full file) **for** the v14 evidence that acting-chain specificity helps but camera choreography hurts, the "be the acting director, not the DP" rule, and why restraint in camera specification lets models choose better anime-specific composition

---

## Open Questions

- Does naming a specific anime director (e.g., "Shinkai style") outperform describing the visual features in Veo video generation? (Tested in image models, not systematically in video) [THEORETICAL]
- Can Kling AI produce anime-register output? No data. [UNKNOWN]
- Does the 3-0 crafted advantage in anime hold at higher N? Current sample is small but decisive. [TESTED at N=3, needs more N]
- Do era-specific triggers ("90s anime screencap" vs "modern anime") produce meaningfully different video outputs? [THEORETICAL]
