# Recraft V4

> Design-grade image and vector generation platform with an OpenAI-compatible API, excelling at visual composition, typography in images, SVG output, and brand-consistent asset production across 6 model tiers.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Capabilities

#### 6 Model Tiers

| Model ID | Resolution | Time | Cost | Use Case |
|----------|-----------|------|------|----------|
| `recraftv4` | 1024x1024 | ~10s | $0.04 | Iteration, social media, web assets |
| `recraftv4_pro` | 2048x2048 | ~28s | $0.25 | Print-ready, large-format, final assets |
| `recraftv4_vector` | Scalable SVG | ~15s | $0.08 | Icons, logos, illustrations for web/app |
| `recraftv4_pro_vector` | High-detail SVG | ~45s | $0.30 | Complex vectors, fine geometric detail |
| `recraftv3` | 1024x1024 | varies | $0.04 | When you need style presets or editing |
| `recraftv3_vector` | Scalable SVG | varies | $0.08 | When you need style presets with vector |

**V3 still required for:** Image-to-image, inpainting, background replacement, style parameter, negative prompts, text_layout, artistic_level control. V4 does NOT support these editing endpoints. [VERIFIED]

**API architecture:**
- **Base URL:** `https://external.api.recraft.ai/v1`
- **Auth:** `Authorization: Bearer <token>`
- **OpenAI-compatible:** Use `openai` Python library with Recraft base_url [VERIFIED]
- **MCP Server:** Remote at `https://mcp.recraft.ai/mcp` -- 9 tools exposed, no local install [VERIFIED]

```python
from openai import OpenAI
client = OpenAI(base_url='https://external.api.recraft.ai/v1', api_key=RECRAFT_API_TOKEN)
response = client.images.generate(prompt='...', model='recraftv4')
```

#### Every API Endpoint

**Generation:**
- `POST /images/generations` -- Text to image/vector. Params: prompt (required), model, n (1-6), size, style (V3 only), style_id (V3 only), negative_prompt (V3 only), response_format (url|b64_json), text_layout (V3), controls [VERIFIED]
- `POST /images/explore` -- V4 only. Generates 8 diverse directions. Costs 2x per image ($0.08 for 8 images). [VERIFIED]
- `POST /images/explore/similar` -- From a previous generation. Params: source_image_id, similarity (1-5) [VERIFIED]

**Editing (V3 only):**
- `POST /images/imageToImage` -- image + prompt + strength (0-1). Max 5MB, 16MP, 4096px [VERIFIED]
- `POST /images/inpaint` -- image + mask (grayscale) + prompt [VERIFIED]
- `POST /images/replaceBackground` -- image + prompt [VERIFIED]
- `POST /images/generateBackground` -- image + mask + prompt [VERIFIED]
- `POST /images/eraseRegion` -- image + mask, no prompt needed [VERIFIED]

**Processing:**
- `POST /images/vectorize` -- Raster to SVG. $0.01 [VERIFIED]
- `POST /images/removeBackground` -- $0.01 [VERIFIED]
- `POST /images/crispUpscale` -- Preserves content. $0.004. Max 5MB, 4MP [VERIFIED]
- `POST /images/creativeUpscale` -- Regenerates detail. $0.25. Max 5MB, 16MP [VERIFIED]
- `POST /images/variateImage` -- Remix. $0.04 [VERIFIED]

**Style:**
- `POST /styles` -- Create from 1-5 reference images. Returns UUID. $0.04 [VERIFIED]

**Account:**
- `GET /users/me` -- Returns credits, email, id, name [VERIFIED]

#### The Controls Object

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

- `colors`: Array of preferred RGB values. Model incorporates but doesn't guarantee exact match. [VERIFIED]
- `background_color`: Specific background RGB [VERIFIED]
- `artistic_level`: 0-5, V3 only [VERIFIED]
- `no_text`: Boolean, V3 only [VERIFIED]

For strict brand compliance, specify colors in BOTH the controls parameter AND the prompt text. [VERIFIED]

#### Size / Aspect Ratios

14 supported ratios. Key sizes:

| Ratio | V4 Standard | V4 Pro |
|-------|------------|--------|
| 1:1 | 1024x1024 | 2048x2048 |
| 16:9 | 1344x768 | 2688x1536 |
| 9:16 | 768x1344 | 1536x2688 |
| 4:5 | 928x1152 | 1856x2304 |
| 3:2 | 1248x832 | 2496x1664 |

Use `9:16` for Instagram Reels, `1:1` for feed posts, `4:5` for Instagram portrait. [VERIFIED]

#### Output and Limits

- **Prompt length:** V4 = 10,000 characters; V3 = 1,000 characters [VERIFIED]
- **Export formats:** SVG, PNG, JPG, WebP, PDF, TIFF, Lottie [VERIFIED]
- **API default:** WebP for raster, SVG for vector [VERIFIED]
- **Rate limits:** 100 images/minute, 5/second max [VERIFIED]
- **URL expiry:** Generated images stored ~24 hours at URL (public, signed). Download immediately. [VERIFIED]
- **Credits:** $1.00 = 1,000 API units. Units do not expire. [VERIFIED]

### Prompt Patterns

#### Universal Prompt Structure (Global to Local) [VERIFIED]

1. Core concept (subject + scene type)
2. Background/environment context
3. Primary subject framing and pose
4. Physical attributes and identity details
5. Secondary subjects and spatial relationships
6. Lighting direction and behavior
7. Camera, depth, and contrast mechanics
8. Mood and compositional resolution

**Template:** `A [image style/medium] of [main content]. [Detailed description]. [Background description]. [Style description].`

#### Format-Specific Prompting

**Vector and Logo Design -- DO:**
- Name the graphic type (logo, icon set, symbol system, badge)
- Define shape logic and silhouette clarity
- Specify strict color palette by count ("two-color palette: deep navy and warm gold")
- Describe line discipline ("consistent 2px stroke weight", "bold outlines")
- State layout structure ("centered composition", "fits within a circle")
- Add technical constraints ("no gradients, no shadows, no texture")
- Emphasize "clean geometry", "flat illustration", "scalable"

**Vector and Logo Design -- DO NOT:**
- Use texture/material language (leather, fabric, grain)
- Describe lighting or atmospheric effects
- Use photographic terms (depth of field, bokeh)

**Social Media Graphics -- DO:**
- Specify typographic hierarchy ("65% oversized typography, 35% product imagery")
- Define color blocking logic
- State format ("Instagram story", "square feed post")
- Put exact text in quotation marks

**Photorealistic -- DO:**
- Lead with pose and framing before appearance
- Define lighting source direction explicitly
- Specify depth-of-field and contrast approach
- Use photographic vocabulary (lens choice, exposure, film grain)

#### Specificity Ladder

| Vague | Specific |
|-------|----------|
| blue background | deep saturated cobalt background |
| big headline | oversized tightly-kerned bold sans-serif headline |
| good lighting | soft directional editorial lighting from upper left |
| modern style | clean Swiss-style composition with mathematical grid alignment |
| professional look | editorial studio photography with neutral backdrop and controlled shadows |

#### Prompt Length Strategy [VERIFIED]

- **Short (1-2 sentences):** Exploring creative directions. Let V4's design taste lead.
- **Medium (3-5 sentences):** Known concepts needing specific execution.
- **Long (paragraph):** Precise art direction. Use full 8-layer structure.

V4 adapts: short prompts = model designs WITH you. Long prompts = model EXECUTES your architecture.

#### Text in Images [VERIFIED]

- V4 treats typography as structural, not overlay
- Short phrases and headlines render accurately
- Put exact text in quotation marks: `headline reading "SUMMER SALE"`
- Define typographic hierarchy: size, weight, position
- Specify typeface style: "bold condensed sans-serif"
- Single words and short phrases work well; longer text blocks degrade

### Operational Patterns

**V4 vs V4 Pro decision rule:**
- Social media (1080px delivery): V4 Standard. 1024px output is sufficient after minor scaling. [VERIFIED]
- Instagram Reels frames: V4 Standard at 9:16 (768x1344) + crisp upscale ($0.044 total) [VERIFIED]
- Print, large display, client deck hero: V4 Pro. 2048px native avoids upscale artifacts. [VERIFIED]
- Vector assets: V4 Vector for most work. V4 Pro Vector only for many fine details. [VERIFIED]

**V3 vs V4 workflow:**
For workflows requiring editing or style presets, generate with V4, then use V3 endpoints for refinement. Or generate everything via V4 prompting alone. [VERIFIED]

**Service reliability:**
Platform experienced multi-day outages (Feb 2025). Build fallback to Imagen 4 for time-critical work. [VERIFIED]

#### Style System

V4 does NOT support the `style` parameter. Style controlled entirely through prompt. [VERIFIED]

V3 has 95+ style presets across categories:
- **Photorealistic:** 21 styles (Natural light, Studio photo, HDR, Black & white, etc.)
- **Illustration:** 46 styles (Hand-drawn, Grain, Clay, Risograph, Pixel art, etc.)
- **Vector:** 23 styles (Line art, Linocut, Color blobs, etc.)
- **Emblem:** 5 styles (Prestige Emblem, Pop Graphic, etc.)

**Custom styles:** Upload 1-5 reference images to `POST /styles`. Returns UUID. Use `style_id` in V3 generation. $0.04 per creation. [VERIFIED]

### Quality Assessment

**Where Recraft V4 excels vs alternatives:**
- Design composition (rule of thirds, visual hierarchy, focal point, color harmony) -- superior to Imagen 4 [VERIFIED]
- Typography in images -- best-in-class, treats text as structural [VERIFIED]
- SVG output -- only model with true native SVG generation [VERIFIED]
- Brand consistency via controls parameter + style system [VERIFIED]
- API maturity (OpenAI-compatible, MCP server) [VERIFIED]

**Where Recraft V4 loses to alternatives:**
- Photorealism -- Imagen 4 superior for documentary/natural style [VERIFIED]
- Speed and cost -- Imagen 4 Fast is cheaper ($0.02 vs $0.04) and faster [VERIFIED]
- Literal prompt adherence -- Imagen 4 more faithful to prompt text [VERIFIED]

**Known failure modes:**
1. Dimension inconsistency -- output sizes occasionally drift [VERIFIED]
2. Complex multi-element scenes -- counting accuracy degrades past 4-5 objects [VERIFIED]
3. Editing via natural language frequently fails -- regenerate instead [VERIFIED]
4. Human figures -- warping around hands and complex poses [VERIFIED]
5. Fine text beyond headlines becomes illegible [VERIFIED]
6. Vector complexity ceiling -- excessive anchor points in complex scenes [VERIFIED]
7. Style consistency across batches without style parameter requires very consistent prompt language [VERIFIED]

### Recraft V4 vs Imagen 4 Decision Matrix

| Dimension | Recraft V4 | Imagen 4 |
|-----------|-----------|----------|
| Design composition | Superior | Adequate |
| Typography in images | Best-in-class | Good |
| Vector/SVG output | Native | None |
| Photorealism | Strong | Superior |
| Speed | 10-28s | Very fast |
| Cost | $0.04-$0.30 | $0.02-$0.04 |
| Brand consistency | Controls + styles | No equivalent |
| Prompt adherence | Aesthetic interpretation | More literal |

**Use Recraft V4 for:** SVG output, social media graphics with text, brand identity, illustrations, composition-critical work, color palette control

**Use Imagen 4 for:** Pure photorealism, high-volume generation, speed-critical work, natural environments, literal prompt adherence

**Complementary workflow:** Generate design assets with Recraft V4. Generate photographic elements with Imagen 4. Composite in post-production. [VERIFIED]

---

## Design Craft Principles (compiled from source)

### Reduction as Authority
Every Recraft prompt for professional output should include an explicit reduction constraint: "Maximum three colors", "Single focal element", "No decorative elements", "Clean background, generous whitespace." [VERIFIED from design research]

### Structure Before Surface
Describe STRUCTURE first (composition, layout, hierarchy), SURFACE second (color, texture, mood). Getting structure wrong makes all surface choices feel arbitrary. [VERIFIED from design research]

### Contrast Creates Hierarchy
Ensure at least TWO forms of contrast in every generation: size, color, weight, space, or detail contrast. [VERIFIED from design research]

### Constraint as Creative Engine
Add explicit constraints to prompts: limited colors, limited elements, single typeface. Constraints focus the model's design decisions and produce more distinctive output. [VERIFIED from design research]

---

## Operational Rules

- **When choosing a model tier,** use V4 Standard ($0.04) for web/social, V4 Pro ($0.25) for print/final, V4 Vector ($0.08) for SVG, because the 6.25x cost jump to Pro is only justified for resolution-critical final delivery. [VERIFIED]
- **When prompting V4,** lead with structure (composition, layout, hierarchy) then surface (color, texture, mood), because structural decisions constrain all subsequent surface decisions. [VERIFIED]
- **When generating brand assets,** pass brand colors in BOTH the controls parameter (as RGB arrays) AND in prompt text, because the controls parameter alone doesn't guarantee exact adherence. [VERIFIED]
- **When text must appear in the image,** put exact text in quotation marks and specify typographic hierarchy (size, weight, position), because V4 treats typography as structural but needs explicit instructions. [VERIFIED]
- **When needing editing capabilities,** use V3 endpoints (inpaint, image-to-image, background replacement), because V4 does not support editing operations. [VERIFIED]
- **When generating vector assets,** avoid all texture/material/lighting language and specify "clean geometry, flat illustration, scalable", because photographic vocabulary conflicts with vector generation. [VERIFIED]
- **When exploring creative directions,** use the Explore endpoint (8 diverse outputs for $0.08), because it costs 2x per image but produces diverse starting points. [VERIFIED]
- **When building brand-consistent series,** write one master prompt prefix encoding the brand system and reuse it across all calls with consistent controls, because small prompt variations cause noticeable style drift without the style parameter. [VERIFIED]
- **When time-critical work is at risk,** build fallback to Imagen 4, because Recraft has experienced multi-day outages. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `tools/research-data/recraft_v4_operational_reference.md` | Complete API reference, all endpoints, 6 model tiers, prompt engineering, V3 vs V4 capability split, controls object, style system, pricing, design craft principles, decision matrix vs Imagen 4, failure modes, operational checklists |
| `credentials.md` (memory) | Auth pattern, plan info, model naming |

---

## Related Concepts

- [[ideogram-3]] -- Ideogram specializes in text-in-image with 58 style presets; Recraft has better design composition and SVG but Ideogram has more style variety
- [[veo-3-1]] -- Recraft generates static frames that can serve as storyboards or reference images before Veo video generation
- [[elevenlabs]] -- Audio layer to pair with Recraft-generated visual assets
- [[kling-ai]] — INFORMS: Kling generates video from Recraft-produced static frames/thumbnails; Recraft provides the visual design layer that Kling's silent video output lacks

---

## Deep Reference

- **When** choosing between V3 and V4 models and need the capability split → **read** `research-data/recraft_v4_operational_reference.md` §2 (Models) **for** the 6-tier model table with exact pricing (V4 $0.04 standard, $0.25 pro, $0.08 vector, $0.30 pro_vector), resolution, timing, and the critical fact that V3 is still required for inpainting, image-to-image, style parameter, negative prompts, and `text_layout`
- **When** using the API and need the complete endpoint reference → **read** `research-data/recraft_v4_operational_reference.md` §3 (Every API Endpoint) **for** all generation endpoints (generations, explore, explore/similar), all editing endpoints (V3 only: imageToImage, inpaint, replaceBackground, eraseRegion), the `controls` object for V4 (colors, background_color), and the V4 Explore feature (8 diverse directions at 2x cost)
- **When** deciding between Recraft and Imagen 4 for a specific use case → **read** `research-data/recraft_v4_operational_reference.md` §(Decision Matrix vs Imagen 4) **for** the use-case comparison (Recraft wins on SVG, design composition, brand consistency; Imagen on photorealism), prompt engineering differences, and failure mode catalog

---

## Open Questions

- V4 style creation via API -- when will V4 support the `style` parameter? Currently prompt-only for V4 [THEORETICAL]
- V4 editing endpoints -- inpainting, image-to-image planned for V4? Currently V3-only [THEORETICAL]
- Lottie export -- documented as supported format but not tested via API [THEORETICAL]
- MCP server capabilities -- 9 tools exposed, exact tool list not fully documented here [THEORETICAL]
