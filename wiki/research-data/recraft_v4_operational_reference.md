# Recraft V4 Operational Reference

Consumer: Agent generating visual design output (Reels graphics, brand identity, social media assets, icons, illustrations, infographics, design-system components).
Decision: When to use Recraft vs Imagen 4, which model tier, how to prompt, what to avoid.
Last verified: 2026-04-03

---

## LAYER 1: TOOL MASTERY

### 1. API Architecture

**Base URL:** `https://external.api.recraft.ai/v1`
**Auth:** `Authorization: Bearer RECRAFT_API_TOKEN`
**OpenAI-compatible:** Use `openai` Python library with Recraft base_url.
**MCP Server:** Remote at `https://mcp.recraft.ai/mcp` -- no local install needed. 9 tools exposed.

```python
from openai import OpenAI
client = OpenAI(base_url='https://external.api.recraft.ai/v1', api_key=RECRAFT_API_TOKEN)
response = client.images.generate(prompt='...', model='recraftv4')
```

### 2. Models (April 2026)

| Model ID | Resolution | Time | Cost | Use Case |
|----------|-----------|------|------|----------|
| `recraftv4` | 1024x1024 | ~10s | $0.04 | Iteration, social media, web assets |
| `recraftv4_pro` | 2048x2048 | ~28s | $0.25 | Print-ready, large-format, final assets |
| `recraftv4_vector` | Scalable SVG | ~15s | $0.08 | Icons, logos, illustrations for web/app |
| `recraftv4_pro_vector` | High-detail SVG | ~45s | $0.30 | Complex vectors, fine geometric detail |
| `recraftv3` | 1024x1024 | varies | $0.04 | When you need style presets or editing |
| `recraftv3_vector` | Scalable SVG | varies | $0.08 | When you need style presets with vector |

**V3 still required for:** Image-to-image, inpainting, background replacement, style parameter, negative prompts, text_layout, artistic_level control. V4 does NOT support these editing endpoints yet.

### 3. Every API Endpoint

**Generation:**
- `POST /images/generations` -- Text to image/vector. Params: prompt (required), model, n (1-6), size, style (V2/V3 only), style_id (V2/V3 only), negative_prompt (V2/V3), response_format (url|b64_json), text_layout (V3), controls.
- `POST /images/explore` -- V4 only. Generates 8 diverse directions. Costs 2x per image (16 credits for 8 images). Params: prompt, model, size, response_format, controls.
- `POST /images/explore/similar` -- From a previous generation. Params: source_image_id (required), similarity (1-5, required), response_format.

**Editing (V3 only):**
- `POST /images/imageToImage` -- Requires image file + prompt + strength (0-1). <5MB, <16MP, <4096px.
- `POST /images/inpaint` -- Requires image + mask (grayscale) + prompt.
- `POST /images/replaceBackground` -- Requires image + prompt.
- `POST /images/generateBackground` -- Requires image + mask + prompt.
- `POST /images/eraseRegion` -- Requires image + mask. No prompt needed.

**Processing:**
- `POST /images/vectorize` -- Raster to SVG. $0.01. Options: svg_compression (on|off), limit_num_shapes (on|off), max_num_shapes.
- `POST /images/removeBackground` -- $0.01.
- `POST /images/crispUpscale` -- Preserves content. $0.004. <5MB, <4MP.
- `POST /images/creativeUpscale` -- Regenerates detail. $0.25. <5MB, <16MP.
- `POST /images/variateImage` -- Remix. $0.04. Params: image, size (required), n, random_seed, image_format (png|webp).

**Style:**
- `POST /styles` -- Create from 1-5 reference images. Params: style (any|realistic_image|digital_illustration|vector_illustration|icon), files. Returns UUID. $0.04.

**Account:**
- `GET /users/me` -- Returns credits, email, id, name.

### 4. The Controls Object (applies to generation endpoints)

```json
{
  "controls": {
    "colors": [
      {"rgb": [0, 82, 147]},
      {"rgb": [255, 200, 50]}
    ],
    "background_color": {"rgb": [255, 255, 255]},
    "artistic_level": 3,
    "no_text": true
  }
}
```

- `colors`: Array of preferred RGB values. Model incorporates these into the output palette.
- `background_color`: Specific background RGB.
- `artistic_level`: 0-5, V3 only. Higher = more artistic interpretation.
- `no_text`: Boolean, V3 only. Suppresses text layouts.

**Operational note:** Convert hex to RGB before sending. #0052FF becomes [0, 82, 255].

### 5. Size/Aspect Ratios

14 supported ratios for all models:

| Ratio | V4 Standard | V4 Pro |
|-------|------------|--------|
| 1:1 | 1024x1024 | 2048x2048 |
| 4:3 | 1152x896 | 2304x1792 |
| 3:4 | 896x1152 | 1792x2304 |
| 16:9 | 1344x768 | 2688x1536 |
| 9:16 | 768x1344 | 1536x2688 |
| 3:2 | 1248x832 | 2496x1664 |
| 2:3 | 832x1248 | 1664x2496 |
| 5:4 | 1152x928 | 2304x1856 |
| 4:5 | 928x1152 | 1856x2304 |
| 21:9 | 1568x672 | 3136x1344 |
| 9:21 | 672x1568 | 1344x3136 |
| 3:1 | 1728x576 | 3456x1152 |
| 1:3 | 576x1728 | 1152x3456 |
| 2:1 | 1440x720 | 2880x1440 |

Use `size: "9:16"` for Instagram Reels frames, `size: "1:1"` for feed posts, `size: "4:5"` for Instagram portrait.

### 6. Prompt Length Limits

- V4 (all variants): **10,000 characters**
- V3/V2: 1,000 characters

### 7. Output Formats & Rate Limits

**Export formats:** SVG, PNG, JPG, WebP, PDF, TIFF, Lottie (animation-ready).
**API default:** WebP for raster, SVG for vector. Use `response_format: "b64_json"` for inline base64.

- 100 images/minute, 5/second max
- Generated images stored ~24 hours at URL (public, signed)
- Plan for immediate download after generation

### 8. Style System

**V4 models do NOT support the `style` parameter.** Style is controlled entirely through the prompt for V4.

**V3 style presets available (for V3 endpoints):**
- Photorealistic: 21 styles (Photorealism, Enterprise, Natural light, Studio photo, HDR, Hard flash, Motion blur, Black & white, Evening light, Faded Nostalgia, Forest life, Mystic Naturalism, Natural Tones, Organic Calm, Real-Life Glow, Retro Realism, Retro Snapshot, Urban Drama, Village Realism, Warm Folk, Product photo)
- Illustration: 46 styles (Illustration, Hand-drawn, Grain, Bold Sketch, Pencil sketch, Retro Pop, Clay, Risograph, Color engraving, Pixel art, Antiquarian, Bold fantasy, Child book, Cover, Crosshatch, Digital engraving, Expressionism, Freehand details, Grain 2.0, Graphic intensity, Hard Comics, Long shadow, Modern Folk, Multicolor, Neon Calm, Noir, Nostalgic pastel, Outline details, Pastel gradient, Pastel sketch, Pop art, Pop renaissance, Street art, Tablet sketch, Urban Glow, Urban sketching, Young adult book, Young adult book 2, Seamless Digital)
- Vector: 23 styles (Vector art, Line art, Linocut, Color blobs, Engraving, Bold stroke, Chemistry, Colored stencil, Cosmics, Cutout, Depressive, Editorial, Emotional flat, Marker outline, Mosaic, Naivector, Roundish flat, Segmented Colors, Sharp contrast, Thin, Vector Photo, Vivid shapes, Seamless Vector)
- Emblem: 5 styles (Prestige Emblem, Pop Graphic, Stamp, Punk Graphic, Vintage Emblem)

**Custom styles via API:** Upload 1-5 reference images to `POST /styles` with a base style category. Returns a style UUID. Use `style_id` parameter in V3 generation. $0.04 per style creation.

**Studio style features (not fully API-exposed):**
- Style remixing: combine up to 5 styles with weighted blending
- Two modeling modes: "Style Essentials" (textures, colors, atmosphere) and "Style and Composition" (includes layout, camera angle)
- Style prompts can be layered on top of reference images

### 9. V4 Features NOT YET Supported

- Style creation (via API `style` parameter -- use prompt instead)
- Prompt-based editing (image-to-image, inpainting -- use V3 for these)
- Image sets
- Artistic level control
- Negative prompts
- Text layout positioning

**Operational implication:** For workflows requiring editing or style presets, generate with V4, then use V3 endpoints for refinement. Or generate everything via V4 prompting alone.

---

### 10. Pricing Strategy

**$1.00 = 1,000 API units. Units do not expire.**

| Operation | Cost | When Worth It |
|-----------|------|---------------|
| V4 Standard | $0.04 | Default for iteration, exploration, web-resolution assets |
| V4 Pro | $0.25 | Final deliverables, print, client-facing where resolution matters. 6.25x cost. |
| V4 Vector | $0.08 | Icons, logos, web illustrations, anything that needs SVG |
| V4 Pro Vector | $0.30 | Complex vector illustrations, detailed brand assets |
| Explore (V4) | $0.08/set | Creative direction exploration (8 diverse outputs for $0.08 total) |
| Style creation | $0.04 | Once per brand -- reusable across all V3 generations |
| Vectorize raster | $0.01 | Converting existing rasters to SVG |
| Remove BG | $0.01 | Asset isolation |
| Crisp upscale | $0.004 | Scaling up without regeneration |
| Creative upscale | $0.25 | When you need regenerated fine detail at higher res |
| Erase region | $0.002 | Cheapest editing operation |

**Decision rule for V4 vs V4 Pro:**
- Social media (1080px delivery): V4 Standard. The 1024px output is sufficient after minor scaling.
- Instagram Reels frames: V4 Standard at 9:16 (768x1344) -- adequate for 1080x1920 with crisp upscale ($0.044 total).
- Print, large display, client deck hero: V4 Pro. The 2048px native resolution avoids upscale artifacts.
- Vector assets: V4 Vector for most work. V4 Pro Vector only for illustrations with many fine details where path precision matters.

---

## LAYER 1B: PROMPT ENGINEERING FOR RECRAFT V4

### Universal Prompt Structure (Global to Local)

```
1. Core concept (subject + scene type)
2. Background/environment context
3. Primary subject framing and pose
4. Physical attributes and identity details
5. Secondary subjects and spatial relationships
6. Lighting direction and behavior
7. Camera, depth, and contrast mechanics
8. Mood and compositional resolution
```

**Template:** `A [image style/medium] of [main content]. [Detailed description of main content]. [Background description]. [Style description].`

### Format-Specific Prompting

**Vector & Logo Design -- DO:**
- Name the graphic type explicitly (logo, icon set, symbol system, badge)
- Define shape logic and silhouette clarity
- Specify strict color palette by count ("two-color palette: deep navy and warm gold")
- Describe line discipline ("consistent 2px stroke weight", "bold outlines")
- State layout structure ("centered composition", "fits within a circle")
- Add technical constraints ("no gradients, no shadows, no texture")
- Emphasize "clean geometry", "flat illustration", "scalable"

**Vector & Logo Design -- DO NOT:**
- Use texture/material language (leather, fabric, grain)
- Describe lighting or atmospheric effects
- Use photographic terms (depth of field, bokeh)
- Leave spatial relationships implied

**Social Media Graphics -- DO:**
- Specify typographic hierarchy explicitly ("65% oversized typography, 35% product imagery")
- Define color blocking logic
- State format ("Instagram story", "square feed post")
- Describe contrast mechanics between layers
- Put exact text in quotation marks

**Illustration -- DO:**
- Lead with drawing style (anime, painterly, editorial, flat)
- Describe line behavior (clean, irregular, bold, thin)
- Define color logic as a system, not individual colors
- Specify surface treatment (flat color, watercolor wash, grain texture)

**Photorealistic -- DO:**
- Lead with pose and framing before appearance
- Define lighting source direction explicitly ("soft directional from upper left")
- Specify depth-of-field and contrast approach
- Use photographic vocabulary (lens choice, exposure, film grain)

### Specificity Ladder

These produce better results than vague equivalents:

| Vague | Specific |
|-------|----------|
| blue background | deep saturated cobalt background |
| big headline | oversized tightly-kerned bold sans-serif headline |
| good lighting | soft directional editorial lighting from upper left |
| modern style | clean Swiss-style composition with mathematical grid alignment |
| professional look | editorial studio photography with neutral backdrop and controlled shadows |

### Prompt Length Strategy

- **Short (interpretive):** When exploring creative directions. Let V4's design taste lead. 1-2 sentences.
- **Medium (guided):** For known concepts needing specific execution. 3-5 sentences covering subject + composition + style.
- **Long (architectural):** For precise art direction matching a brief. Use full 8-layer structure. Paragraph-length.

V4 adapts: short prompts = model designs WITH you. Long prompts = model EXECUTES your architecture.

### Text in Images

- V4 treats typography as structural, not overlay
- Short phrases, headlines, labels render accurately
- Put exact text in quotation marks: `headline reading "SUMMER SALE"`
- Define typographic hierarchy: size, weight, position
- Specify typeface style: "bold condensed sans-serif", "elegant thin serif"
- V4 handles single words and short phrases well; longer text blocks degrade

### Color Control via API

Pass exact brand colors in the `controls` parameter:
```json
{
  "controls": {
    "colors": [
      {"rgb": [0, 82, 147]},
      {"rgb": [255, 200, 50]},
      {"rgb": [30, 30, 30]}
    ],
    "background_color": {"rgb": [255, 255, 255]}
  }
}
```

Colors function as "preferred palette" -- the model incorporates them but doesn't guarantee every pixel matches. For strict brand compliance, specify colors in BOTH the controls parameter AND the prompt text.

### Known Failure Modes

1. **Dimension inconsistency:** Specified sizes occasionally drift after generation. Always verify output dimensions.
2. **Complex multi-element scenes:** Counting accuracy degrades past 4-5 distinct objects. Specify exact counts and relative positions.
3. **Editing via natural language:** Simple editing requests (remove this, adjust that) frequently fail. Regenerate rather than edit.
4. **Human figures:** Warping artifacts around hands and complex poses. May require regeneration.
5. **Fine text beyond headlines:** Paragraphs of text become illegible. Limit to headlines, labels, single words.
6. **Vector complexity ceiling:** Very complex scenes produce excessive anchor points requiring cleanup. Keep vector prompts structurally simple.
7. **Style consistency across batches:** Without the style parameter (unavailable in V4), prompt-only style control requires very consistent prompt language. Small prompt variations cause noticeable style drift.
8. **Service reliability:** Platform has experienced multi-day outages (Feb 2025). Build fallback to Imagen 4 for time-critical work.

---

## RECRAFT V4 vs IMAGEN 4: DECISION MATRIX

| Dimension | Recraft V4 | Imagen 4 |
|-----------|-----------|----------|
| **Design composition** | Superior. Understands rule of thirds, visual hierarchy, focal point placement, color harmony. | Adequate but not design-native. |
| **Typography in images** | Best-in-class. Treats text as structural element. Accurate short phrases. | Good text rendering, more literal placement. |
| **Vector/SVG output** | Native. Only model with true SVG generation. | None. Raster only. |
| **Photorealism** | Strong, editorial/fashion-forward aesthetic. | Superior for documentary/natural photorealism. Better atmospheric perspective, distance rendering, environmental physics. |
| **Speed** | 10-28s depending on tier. | Imagen 4 Fast extremely quick, up to 2K natively. |
| **Cost** | $0.04-$0.30 per image. | $0.02-$0.04 (Fast tier). |
| **Brand consistency** | Controls parameter for colors + style system. | No equivalent style system. |
| **Product photography** | Good, design-forward composition. | Superior for literal product documentation. |
| **Prompt adherence** | Strong for design intent; interprets aesthetically. | More literal/faithful to prompt text. |
| **API maturity** | OpenAI-compatible, MCP server, well-documented. | Google Cloud API, broadly integrated. |

**When to use Recraft V4:**
- Anything requiring SVG output
- Social media graphics with text
- Brand identity work (logos, icons, design systems)
- Illustrations with specific design aesthetic
- When composition and visual hierarchy matter more than photorealism
- When you need to control exact color palette

**When to use Imagen 4:**
- Pure photorealism (product photography, documentary style)
- High-volume generation where cost matters ($0.02 vs $0.04)
- Speed-critical generation (Imagen 4 Fast)
- Natural environments, atmospheric scenes
- When literal prompt adherence matters more than design interpretation

**Complementary workflow:** Generate design assets (layouts, graphics, icons, illustrations) with Recraft V4. Generate photographic elements (hero images, product shots, environmental backgrounds) with Imagen 4. Composite in post-production.

---

## LAYER 2: VISUAL DESIGN CRAFT KNOWLEDGE

### Principles from the Masters

#### Paul Rand (IBM, ABC, UPS)
**Core insight:** Design exists to solve problems and communicate, not to decorate. Every element must serve a clear purpose.

- Simplicity and geometry are the language of timelessness and universality
- A logo's principal role is to identify. Simplicity is its means.
- Qualities that matter: distinctiveness, visibility, adaptability, memorability, universality, timelessness
- Wit and humor create human connection (UPS package on escutcheon = funny + memorable)
- Challenge every element: if it doesn't serve a function, remove it
- Wrong to borrow a visual device without understanding why the original succeeded

**Prompt application:** When generating logos/icons, prompt for "clear purpose" and "minimal elements." Add "every element serves a function" as a design constraint. Avoid decorative flourishes. Specify: "no ornamental elements, no unnecessary detail, every shape communicates meaning."

#### Massimo Vignelli (NYC Subway, American Airlines)
**Core insight:** Design begins with architecture (grids, proportion, hierarchy), not aesthetics. Restraint creates authority.

- "One typeface is enough" -- used only 6 families across his entire career
- The grid is like underwear: you wear it, but it's not to be exposed
- Design is a moral discipline requiring self-sacrifice
- American Airlines identity lasted 46 years without a redesign -- because the underlying system was sound
- Typographic decisions serve communication, never decoration

**Prompt application:** For brand systems and layouts, prompt for "grid-based composition", "strict typographic hierarchy", "mathematical proportion." Limit font references: "single typeface family, varying only in weight and size." Describe "restrained color palette, maximum three colors."

#### Josef Muller-Brockmann (Swiss Style)
**Core insight:** Mathematical harmony in layout creates trust. The grid is an invisible framework for alignment decisions.

- Proportional relationships based on mathematical ratios create visual harmony
- The designer is an objective communicator, not an artist
- Rhythm, harmony, geometric compositions as structural tools
- Grid divides space into consistent units -- creates order that feels trustworthy

**Prompt application:** For infographics and information design, prompt for "Swiss-style layout", "mathematical grid alignment", "objective communication", "clear hierarchy through scale and position." Use: "geometric composition, modular grid, consistent spacing units."

#### Saul Bass (Movie Posters, AT&T)
**Core insight:** Reduction is power. Complex ideas communicated through minimal visual elements.

- Minimalist collage cutouts with bold, simple color
- Communicate story at a glance through symbolic design
- Influenced by Bauhaus: clean geometric forms serving clear purpose
- Connection as the single idea (AT&T globe = connection)

**Prompt application:** When generating conceptual graphics or visual metaphors, prompt for "single dominant visual symbol", "bold color, maximum three tones", "communicate [concept] through one geometric form." Use: "reductive design, symbolic representation, Saul Bass style simplification."

#### David Carson (Ray Gun)
**Core insight:** Intentional rule-breaking creates energy. The mess IS the message -- but only when it's deliberate.

- Breaking the grid works ONLY when you know the grid
- Visual chaos as emotional tone, not decoration
- Form as content: the layout IS the communication
- Instinct over instruction, but only after mastering fundamentals
- The Zapf Dingbats interview: if content doesn't deserve attention, the design should say so

**Prompt application:** For high-energy social content (Reels hooks, music/culture posts), can prompt for "experimental typography", "overlapping elements", "intentional asymmetry", "grunge aesthetic with purpose." BUT: only break rules after establishing the base rule first. Don't default to chaos.

### Typography Principles

#### Robert Bringhurst (Elements of Typographic Style)
- Typography exists to honor content
- Readability comes from rhythm, proportion, and harmony
- Type choices, kerning, leading, and margins all serve the text
- Five centuries of typographic knowledge codified into principles

#### Erik Spiekermann
- Typography IS brand voice -- a typeface creates a "visual voice"
- Letters need breathing room; smaller type needs MORE spacing
- Custom typefaces create uniqueness and build trust
- Warmth of Univers depends on context -- no font is inherently cold or warm

#### Type Pairing Rules
1. **Contrast, not conflict:** Pair serif body with sans-serif header (classic, almost impossible to get wrong)
2. **Shared skeleton:** Look for similar x-height and proportions even when overall appearance differs
3. **Clear hierarchy:** Different weights create reading order (heavy headline, light body)
4. **Limit selection:** 2-3 fonts maximum. More = clutter and distrust
5. **Same era or design logic:** Typefaces from the same designer or movement pair naturally

**Prompt application:** When specifying typography in Recraft prompts, name specific type styles rather than font names: "bold condensed sans-serif headline with elegant light serif body text." Specify the relationship: "typographic hierarchy with headline at 3x body size." For brand assets: "single type family, weight variation only."

### Color Theory (Albers + Itten)

#### Josef Albers (Interaction of Color)
- No color exists in isolation -- every color changes based on its neighbors
- Simultaneous contrast: adjacent colors alter each other's perceived hue, value, and saturation
- Complementary colors placed together increase vibrancy
- The same color appears different depending on surrounding context

#### Johannes Itten (Seven Contrasts)
1. **Hue:** Different hues side by side (red vs blue)
2. **Light-dark:** Tonal value differences
3. **Cold-warm:** Warm colors advance, cool colors recede
4. **Complementary:** Wheel opposites intensify each other
5. **Saturation:** Pure vs. muted creates emphasis
6. **Extension:** Balance through proportion (small bright area vs large muted area)
7. **Simultaneous:** Eye generates complement of what it sees

**Prompt application:** When specifying colors in the controls parameter AND prompt:
- Use complementary pairs for maximum vibrancy (important element in warm color, background in cool)
- Use extension contrast for hierarchy: small area of saturated accent color against large area of muted tone
- Describe color relationships, not just colors: "warm accent against cool neutral background" is more effective than listing colors
- For brand palettes, specify the ROLE each color plays: "primary brand blue as headline, warm gold as accent, neutral gray as body"

### Composition & Space

#### Rule of Thirds / Golden Ratio
**Evidence assessment:** Mixed. Rule of thirds is a simplification that sometimes produces generic results. Golden ratio has limited empirical support but produces more natural-feeling asymmetry than strict thirds. Both are starting points, not laws.

**What actually works:** Intentional asymmetry with clear focal point. The key insight is TENSION -- placing the subject slightly off-center creates visual interest. Dead center can work for logos and icons (stability), but for dynamic compositions (social media, Reels frames), off-center placement creates energy.

#### Ma (Japanese Negative Space)
- Emptiness is active, not leftover
- In Western design, space is what remains after placing elements
- In Japanese design, space IS the structure
- A single element floating in whitespace creates tension, focus, breathing room
- Less information, higher status perception

**Prompt application:** For premium/luxury brand assets, explicitly prompt for "generous negative space", "breathing room around primary element", "clean empty background occupying at least 40% of composition." For social media graphics, "bold subject against expansive clean background" produces more professional output than filling every inch.

### Information Design (Tufte)

#### Edward Tufte
- **Data-ink ratio:** Maximize the ink that communicates data. Remove everything else.
- **Chartjunk:** 3D effects, decorative hatching, unnecessary gridlines, gratuitous icons all reduce clarity
- "Above all else, show data"
- "Graphics do not become attractive through addition of ornamental hatching and false perspective"

**Prompt application:** For infographics and data visualization:
- Prompt for "clean data visualization, minimal decoration"
- "Information-first design, no chartjunk"
- "Flat, clean bars/lines with direct labels, no 3D effects"
- Specify "high data-ink ratio" as a design constraint
- For icon sets accompanying data: "simple, functional icons that communicate meaning at 16x16px"

### Brand Identity Systems

#### What Makes Systems Work (Bierut, Scher, Pentagram)
- Brand identity is "a world of associations accrued over time" (Bierut)
- "Words have meaning. Type has spirit." (Scher)
- The Mastercard overlapping circles work because they're a SYSTEM, not a logo
- The Public Theater identity fused high and low into new visual language
- Every touchpoint reinforces the same core visual idea

#### Design Systems vs Style Guides
- **Style guide:** Static reference document. Visual standards for colors, typography, spacing. Human interprets and implements.
- **Design system:** Living framework with coded components, behavioral patterns, interaction rules. Machine implements directly.
- **Why agents need systems, not guides:** An AI agent needs RULES (if brand = X, then colors = [a,b,c], typography = Y, spacing = Z grid). Style guides describe taste; design systems describe logic.

**Prompt application:** For brand consistency across generations:
1. Create a Recraft custom style from 3-5 brand reference images (via V3 `POST /styles`)
2. Define a reusable prompt PREFIX that encodes the brand system: "Brand visual system: primary blue #0052FF, secondary warm gray #E8E4E0, typography bold geometric sans-serif, clean grid layout, generous whitespace, no decorative elements."
3. Append the specific asset request after the prefix
4. Use the `controls.colors` parameter with exact brand RGB values on EVERY generation
5. This reusable prefix + consistent controls parameter = pseudo-design-system for the agent

---

## CROSS-DOMAIN PATTERNS

### PATTERN: Reduction as Authority

**DOMAINS:**
- Paul Rand: "simplicity and restraint" in logos (IBM stripes = 3 elements total)
- Saul Bass: movie posters communicated via single symbolic image
- Vignelli: 6 typefaces across entire career
- Tufte: maximize data-ink, erase everything else
- Japanese Ma: emptiness IS the structure
- Muller-Brockmann: grid as invisible framework, not decorative element

**MECHANISM:** The human visual system processes fewer elements faster and assigns higher confidence to each. Removal of noise increases signal clarity. In design contexts, fewer elements signal intentionality ("they chose this carefully") while crowded compositions signal uncertainty ("they couldn't decide what matters"). This maps to psychological research on choice overload and cognitive fluency.

**APPLICATION:** Every Recraft prompt for professional output should include an explicit reduction constraint. Examples:
- "Maximum three colors"
- "Single focal element"
- "No decorative elements that don't serve communication"
- "Clean background, generous whitespace"
- For vector: "simplified geometry, minimal anchor points, clean paths"

**FALSIFIABLE:** Would be disproved if maximalist designs (many elements, full-bleed color, multiple competing focal points) consistently outperformed minimal designs in professional contexts (brand trust, information comprehension, conversion). David Carson's work challenges this for youth/counterculture audiences, suggesting the pattern is context-dependent rather than universal. Test: generate maximalist vs reductive versions of the same brief and measure which the client/audience prefers.

---

### PATTERN: Structure Before Surface

**DOMAINS:**
- Vignelli: "Design begins with architecture, not aesthetics"
- Muller-Brockmann: mathematical grid as foundation before any visual element
- Bringhurst: rhythm, proportion, and harmony as typographic architecture
- Tufte: data structure determines visualization, not the reverse
- Brand systems: coded components (structure) over visual guidelines (surface)

**MECHANISM:** Structural decisions (grid, hierarchy, proportion, spacing) constrain all subsequent surface decisions (color, texture, style). Getting structure wrong makes all surface choices feel arbitrary. Getting structure right makes even mediocre surface choices feel intentional. This is why Vignelli's work with limited typefaces feels authoritative -- the structure carries it.

**APPLICATION:** In Recraft prompts, describe STRUCTURE first, SURFACE second:
1. Layout and composition ("centered, grid-based, asymmetric thirds")
2. Hierarchy ("headline dominates, supporting text at 40% scale")
3. Spatial relationships ("logo top-left, text block center-right, CTA bottom")
4. THEN: color, texture, style, mood

For the agent's workflow: always establish the structural prompt skeleton before adding aesthetic modifiers.

**FALSIFIABLE:** Would be disproved if prompts describing only surface qualities (colors, textures, mood) consistently produced better-composed outputs than prompts leading with structural description. Could test by generating identical concepts with structure-first vs surface-first prompt ordering.

---

### PATTERN: Contrast Creates Hierarchy

**DOMAINS:**
- Itten: seven types of color contrast as compositional tools
- Albers: adjacent colors change each other (simultaneous contrast)
- Bringhurst/Spiekermann: typographic weight contrast creates reading order
- Type pairing: contrast between serif/sans-serif creates visual interest
- Tufte: data-ink contrast separates signal from noise
- Visual hierarchy research: size, color, position create attention order

**MECHANISM:** The human visual system is a difference detector. We see EDGES (where one thing ends and another begins) more readily than fields. Contrast IS information -- it tells the viewer where to look, what's important, and how elements relate. Without contrast, everything is equivalent (visual entropy). With too much contrast, everything screams (visual chaos). Design is the calibration of contrast.

**APPLICATION:** In every Recraft generation, ensure at least TWO forms of contrast are specified:
- Size contrast: "oversized headline against small body text"
- Color contrast: "bright accent color against neutral background"
- Weight contrast: "bold primary element, light supporting elements"
- Space contrast: "dense information cluster with generous surrounding whitespace"
- Detail contrast: "detailed focal element against simplified background"

In the `controls` parameter, use colors that create deliberate contrast pairs, not random palettes.

**FALSIFIABLE:** Would be disproved if designs with uniform element treatment (no size/color/weight variation) performed equally well in comprehension and engagement tests. Unlikely for information design; possibly true for certain fine art or meditative contexts.

---

### PATTERN: Constraint as Creative Engine

**DOMAINS:**
- Vignelli: 6 typefaces forced inventive use of weight, size, spacing
- Rand: "every element must serve a purpose" as creative constraint
- Swiss Style: rigid grid produced immense variety within structure
- Type pairing: "max 2-3 fonts" produces more harmonious results than unlimited choice
- Color: limited palettes (3-5 colors) produce more cohesive results than unlimited color

**MECHANISM:** Constraints reduce the solution space, forcing creativity into invention WITHIN bounds rather than exploration ACROSS bounds. Unlimited options produce decision fatigue and bland averaging. Tight constraints produce distinctive solutions because the designer must find unexpected uses for limited tools. This is the paradox of creative freedom: less choice, more invention.

**APPLICATION:** Always add explicit constraints to Recraft prompts:
- "Using only [brand palette colors]"
- "No more than three visual elements"
- "Single typeface family"
- "Monochrome with one accent color"
- "Geometric shapes only, no organic forms"

These constraints do not limit quality -- they focus the model's design decisions and produce more distinctive output than open-ended prompts.

**FALSIFIABLE:** Would be disproved if unconstrained prompts ("make something cool") consistently produced more distinctive, professional output than constrained prompts. Empirically, the opposite holds: unconstrained AI generation produces generic averaging of training data.

---

### PATTERN: Intentionality Signals Quality

**DOMAINS:**
- Rand: challenged students to justify every element in their compositions
- Carson: chaos works only when it's deliberate ("the mess was the point")
- Ma: emptiness is active and deliberate, not leftover
- Spiekermann: type spacing is a deliberate decision reflecting care
- Tufte: every ink mark should represent data -- nothing incidental
- Bierut: brand identity is "associations accrued over time" through consistent choice

**MECHANISM:** Viewers unconsciously evaluate whether design choices appear deliberate or accidental. Deliberate choices signal competence, care, and authority. Accidental-looking choices signal carelessness or confusion. This is why AI-generated design often feels "off" -- the choices appear random rather than intentional. The difference between "designed" and "decorated" is whether each element appears CHOSEN or ACCUMULATED.

**APPLICATION:** This is the most important pattern for AI-generated design. The agent must make Recraft outputs feel intentional by:
1. Never using defaults -- always specify composition, color, typography, spacing
2. Describing WHY elements are placed where they are: "headline centered for stability" or "subject at left third for dynamic movement"
3. Using consistent design logic across related assets (same grid, same palette, same type style)
4. Reviewing output against the brief: does every element serve the communication goal?
5. Eliminating elements that appear random: if something in the output doesn't serve the purpose, regenerate with explicit exclusion

**FALSIFIABLE:** Would be disproved if viewers could not distinguish between deliberately-designed and randomly-generated compositions. Eye-tracking and preference studies consistently show viewers prefer and trust intentional-looking design. However, "intentional" is culturally mediated -- what reads as deliberate in Swiss design differs from what reads as deliberate in punk design.

---

## OPERATIONAL CHECKLISTS

### Before Every Recraft Generation

1. **Choose model:** V4 (iteration), V4 Pro (final), V4 Vector (SVG), V4 Pro Vector (complex SVG)
2. **Set size:** Match the delivery format (9:16 for Reels, 1:1 for feed, 4:5 for Instagram portrait)
3. **Set colors:** Pass brand palette in controls parameter as RGB arrays
4. **Structure prompt:** Lead with structure (composition, layout, hierarchy), then surface (color, texture, mood)
5. **Add constraints:** Limit colors, elements, fonts in prompt text
6. **Specify text exactly:** Quotation marks around any text that must appear in the image
7. **Add reduction language:** "clean", "minimal", "no decorative elements", "generous whitespace"

### For Brand-Consistent Series

1. Write one master prompt prefix encoding the brand system
2. Set controls parameter with brand RGB values (reuse across all calls)
3. If V3: create custom style from brand references (one-time $0.04)
4. Use identical structural language across all prompts in the series
5. Vary only the specific content/subject per generation
6. Review each output against previous outputs for visual drift

### For Vector Assets

1. Use `recraftv4_vector` (or `recraftv4_pro_vector` for complex work)
2. Prompt structure: name graphic type > shape logic > color count > line discipline > layout > constraints
3. Avoid all texture/material/lighting language
4. Include: "clean geometry", "flat illustration", "scalable", "no gradients"
5. Specify exact color palette in both prompt and controls
6. Verify SVG output in a vector editor before delivery
7. For icons: ensure consistency by keeping identical prompt structure, varying only the subject

### For Social Media Graphics

1. V4 Standard for web delivery, V4 Pro only if also using for print
2. Size: match platform (9:16, 1:1, 4:5)
3. Typographic hierarchy in prompt: specify headline > subhead > body > CTA
4. Color contrast: ensure text is readable against background
5. Specify layout: "bold headline occupying top 40%, imagery in center 40%, CTA at bottom 20%"
6. Include "social media graphic" or "Instagram post" in prompt for format awareness
7. Review text legibility at delivery size (1080px width for Instagram)
