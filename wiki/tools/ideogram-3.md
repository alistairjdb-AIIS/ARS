# Ideogram 3.0

> Text-in-image generation specialist with 58 style presets, a color palette system, and dedicated DESIGN mode, purpose-built for typography-heavy graphics like title cards, social media quote cards, infographics, and branded visuals.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Capabilities

**Base URL:** `https://api.ideogram.ai`
**Auth:** `Api-Key: <key>`
**Rate limit:** 10 concurrent in-flight requests (default)
**Format:** `multipart/form-data` for all endpoints
**Image URLs expire** -- download immediately after generation [VERIFIED]

#### API Endpoints

**Generate:**
`POST /v1/ideogram-v3/generate`

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `prompt` | string | required | -- |
| `num_images` | integer | 1 | Generate multiple for text accuracy selection |
| `seed` | integer | random | Reproducibility |
| `aspect_ratio` | string | `1x1` | 15 options: 1x3, 3x1, 1x2, 2x1, 9x16, 16x9, 10x16, 16x10, 2x3, 3x2, 3x4, 4x3, 4x5, 5x4, 1x1 |
| `resolution` | string | auto | 70 exact resolutions. Mutually exclusive with aspect_ratio |
| `rendering_speed` | string | `DEFAULT` | `FLASH`, `TURBO`, `DEFAULT`, `QUALITY` |
| `magic_prompt` | string | `AUTO` | `AUTO`, `ON`, `OFF` |
| `negative_prompt` | string | none | What to exclude |
| `style_type` | string | `AUTO` | `AUTO`, `GENERAL`, `REALISTIC`, `DESIGN`, `FICTION` |
| `style_preset` | string | none | 58 presets |
| `style_codes` | array | none | 8-char hex codes. Incompatible with style_reference_images and style_type |
| `color_palette` | object | none | Preset name or custom hex with weights 0.05-1.0 |
| `style_reference_images` | array | none | Up to 10MB total. JPEG/PNG/WebP |
| `character_reference_images` | array | none | 1 image max, 10MB |

**Generate Transparent Background:**
`POST /v1/ideogram-v3/generate-transparent`
- Same as Generate plus `upscale_factor`: `X1`, `X2`, `X4`
- Use for logos, stickers, overlay text elements for compositing [VERIFIED]

**Edit (Inpainting):**
`POST /v1/ideogram-v3/edit`
- Required: `image` (binary, max 10MB), `mask` (binary, same size), `prompt`
- Black mask = areas to edit, white = preserved
- Primary text error correction workflow [VERIFIED]

**Remix:**
`POST /v1/ideogram-v3/remix`
- Key parameter: `image_weight` (0-100, default 50)
- High weight (70-90) preserves layout; low (10-30) allows creative reinterpretation [VERIFIED]

**Reframe (Outpainting):**
`POST /v1/ideogram-v3/reframe`
- Required: `image`, `resolution` (target dimensions)
- No prompt parameter. 69 target resolutions.
- Use to convert 1:1 to 9:16 for Stories/Reels [VERIFIED]

**Replace Background:**
`POST /v1/ideogram-v3/replace-background`
- Required: `image`, `prompt` (describing new background)

**Upscale:**
`POST /upscale` (root-level endpoint, NOT under /v1/ideogram-v3/)
- `resemblance` (default 50), `detail` (default 50)
- No explicit upscale factor -- controlled via resemblance/detail [VERIFIED]

**Describe (Image-to-Text):**
`POST /describe`
- `describe_model_version`: `V_2` or `V_3` (default V_3)
- Use to reverse-engineer effective prompts from reference images [VERIFIED]

#### Rendering Speed Tiers

| Speed | Cost | Use |
|-------|------|-----|
| FLASH | lowest | Rapid prototyping |
| TURBO | ~$0.03 | Iteration, text accuracy checks |
| DEFAULT | ~$0.06 | Standard generation |
| QUALITY | ~$0.08-0.10 | Final output [VERIFIED] |

#### Text Rendering Assessment [VERIFIED]

**Accuracy:**
- Latin text: ~90-95% on first generation
- Single words / 2-4 word phrases: 95%+ reliability
- 5+ words: accuracy drops
- Non-Latin scripts (Chinese/Arabic/Cyrillic): significantly lower, do not rely on

**How to specify text:**
- Quotation marks are MANDATORY around text to render
- Place quoted text EARLY in the prompt (front-loaded tokens processed more reliably)
- Specify casing explicitly ("all caps", "title case")
- Describe location ("centered at top", "bottom third")
- Describe style ("bold sans-serif", "elegant script")

**Practical character limits:**
- Prompt limit: ~150-160 words / ~200 tokens
- Under 20 characters per text block for >90% first-attempt accuracy
- Under 10 characters for >95% accuracy

**Font control:** Cannot specify exact font names. CAN describe: weight (bold, thin), category (sans-serif, serif, script), style descriptors ("rounded bauhaus style", "art deco geometric"), size relative to composition.

#### Multi-Panel Composition Limitation [TESTED — session 37]

**Ideogram 3.0 is NOT suitable for multi-panel comics or layouts with 3+ text blocks.** Tested decisively on a 6-panel comic format (FACT LAB #01): all 4 variants produced garbled text, broken grid layouts, and repeated panels. The model conflates text positions when multiple text blocks compete for placement.

- **1-2 text blocks with specific positions:** Works well (quote cards, title cards, posters)
- **3+ text blocks with specific positions:** Model conflates locations, text bleeds across panels, grid structure breaks
- **6-panel comic grid:** Complete failure — panels repeat, text garbles, grid collapses

**Use Recraft V4 for multi-panel static compositions** — won 3/3 on the same briefs where Ideogram failed. [TESTED]

#### The magic_prompt Parameter [VERIFIED]

| Setting | What It Does | When to Use |
|---------|-------------|-------------|
| `AUTO` | Model decides enhancement | General exploration |
| `ON` | Enhances all prompts | Short/vague prompts needing enrichment |
| `OFF` | Uses prompt exactly as written | ALL text-heavy work, style references, precise compositions |

**Rule:** Default to `magic_prompt=OFF` for any generation where text accuracy matters. Magic Prompt adds details that conflict with text placement and style references. When ON, the enhanced prompt is visible in the response's `prompt` field.

#### Style Types [VERIFIED]

| Type | Best For | Text Quality |
|------|----------|-------------|
| `AUTO` | Let model decide | Variable |
| `GENERAL` | Artistic, abstract, illustrations | Good |
| `REALISTIC` | Photography, product shots | Good for overlays |
| `DESIGN` | **Graphics, typography, logos, marketing** | **Best** |
| `FICTION` | Fantasy, sci-fi, stylized | Variable |

#### 58 Style Presets [VERIFIED]

**Best for text-heavy work:** ART_DECO, ART_POSTER, EDITORIAL, FLAT_ART, FLAT_VECTOR, GEO_MINIMALIST, HALFTONE_PRINT, MAGAZINE_EDITORIAL, MINIMAL_ILLUSTRATION, POP_ART, TRAVEL_POSTER, VINTAGE_POSTER

**Good for title cards / atmospheric:** DRAMATIC_CINEMA, DARK_AURA, GOLDEN_HOUR, LONG_EXPOSURE, NIGHTLIFE, SPOTLIGHT_80S

**Risky for text (heavy stylization distorts letterforms):** ABSTRACT_ORGANIC, ART_BRUT, BLURRY_MOTION, COLLAGE, CUBISM, DOUBLE_EXPOSURE, GRAFFITI_I, GRAFFITI_II, MIXED_MEDIA, PAINT_GESTURE, SURREAL_COLLAGE, WATERCOLOR, WEIRD

**Full list (58):** 80S_ILLUSTRATION, 90S_NOSTALGIA, ABSTRACT_ORGANIC, ANALOG_NOSTALGIA, ART_BRUT, ART_DECO, ART_POSTER, AURA, AVANT_GARDE, BAUHAUS, BLUEPRINT, BLURRY_MOTION, BRIGHT_ART, C4D_CARTOON, CHILDRENS_BOOK, COLLAGE, COLORING_BOOK_I, COLORING_BOOK_II, CUBISM, DARK_AURA, DOODLE, DOUBLE_EXPOSURE, DRAMATIC_CINEMA, EDITORIAL, EMOTIONAL_MINIMAL, ETHEREAL_PARTY, EXPIRED_FILM, FLAT_ART, FLAT_VECTOR, FOREST_REVERIE, GEO_MINIMALIST, GLASS_PRISM, GOLDEN_HOUR, GRAFFITI_I, GRAFFITI_II, HALFTONE_PRINT, HIGH_CONTRAST, HIPPIE_ERA, ICONIC, JAPANDI_FUSION, JAZZY, LONG_EXPOSURE, MAGAZINE_EDITORIAL, MINIMAL_ILLUSTRATION, MIXED_MEDIA, MONOCHROME, NIGHTLIFE, OIL_PAINTING, OLD_CARTOONS, PAINT_GESTURE, POP_ART, RETRO_ETCHING, RIVIERA_POP, SPOTLIGHT_80S, STYLIZED_RED, SURREAL_COLLAGE, TRAVEL_POSTER, VINTAGE_GEO, VINTAGE_POSTER, WATERCOLOR, WEIRD, WOODBLOCK_PRINT

#### Color Palette System [VERIFIED]

**Preset palettes:** EMBER, FRESH, JUNGLE, MAGIC, MELON, MOSAIC, PASTEL, ULTRAMARINE

**Custom palettes:** Array of hex colors with weights (0.05-1.0)

#### Style References [VERIFIED]

- Upload up to 3 reference images (10MB total)
- Draws from library of 4.3 billion style presets to match reference
- No direct "style strength" slider -- control indirectly through Remix `image_weight` or prompt specificity
- Magic Prompt OFF recommended when using style references
- Avoid style keywords in prompt when references are active

**Style codes:** 8-character hex codes from the 4.3B preset library. Reusable across prompts. Incompatible with style_reference_images and style_type -- use one system or the other.

### Prompt Patterns

#### Optimal Prompt Structure [VERIFIED]

```
[Image summary]. [Main subject], [Text in quotes with placement],
[Style/mood], [Composition/framing], [Technical details]
```

#### Rules That Change Output Quality [VERIFIED]

1. **Front-load important parts.** Tokens beyond ~150 words get deprioritized.
2. **Minimum effective prompt:** One subject, one style anchor, exact text in quotes, one placement instruction, one constraint.
3. **Use DESIGN style_type for all text-heavy work.**
4. **Natural sentences over keyword soup.** "A poster for a jazz concert with the title 'BLUE NOTE' in large art deco letters" beats "jazz poster, art deco, text, BLUE NOTE, large letters."
5. **Describe what you want, not what you don't.** Use negative_prompt parameter for exclusions.
6. **Lock casing in quotes.** Write "SALE ENDS SUNDAY" not "Sale Ends Sunday" if you want all caps.
7. **Break multi-text layouts into explicit spatial chunks.**

#### Prompt Templates

**Social media quote card:**
```
A [mood] quote card. [Background description]. Bold [font style] text
reading "[HEADLINE]" [placement]. [Secondary text description].
[Format: clean/minimal/branded]. style_type=DESIGN
```

**Title card for Reels:**
```
A cinematic title card with [background description]. Large [font style]
text reading "[TITLE]" centered. [Mood/atmosphere]. [Aspect: 9x16].
style_type=DESIGN, rendering_speed=QUALITY
```

**Branded visual with logo text:**
```
A [brand style] branded image. [Visual description]. Brand name
"[BRAND]" in [specific typography description] at [position].
[Tagline/subtitle]. Professional, polished. style_type=DESIGN
```

### Operational Patterns

**Default API configuration for text-heavy graphics:**
```python
{
    "prompt": "[structured prompt]",
    "style_type": "DESIGN",
    "magic_prompt": "OFF",
    "rendering_speed": "QUALITY",
    "num_images": 4,
    "aspect_ratio": "1x1",
    "negative_prompt": "blurry text, misspelled words, illegible, low quality"
}
```

**Error correction pipeline:**
1. Generate 4 images --> pick best text rendering
2. If text has errors --> create mask over text area --> Edit endpoint with corrected prompt
3. If still failing after 2 edit attempts --> generate text-free version --> composite text in post-processing

**Style selection decision tree:**
- Text accuracy is #1 priority? --> `style_type=DESIGN`, `magic_prompt=OFF`, no style_preset
- Need photorealism? --> `style_type=REALISTIC`
- Need specific artistic style? --> Use appropriate style_preset
- Otherwise? --> `style_type=GENERAL` or `AUTO`

**Cost optimization:**
1. Use TURBO for all iteration/testing (cheapest)
2. Generate 4 images per call (more options, same call)
3. Switch to QUALITY only for final approved outputs
4. Save successful style_codes for reuse
5. Use Describe endpoint to reverse-engineer competitor visuals

### Quality Assessment

**Where Ideogram 3.0 excels vs alternatives:**
- Text in decorative/stylized contexts -- superior to Imagen 4 [VERIFIED]
- Graphic design layouts with DESIGN mode [VERIFIED]
- Style variety: 58 presets + 4.3B style codes [VERIFIED]
- Character consistency via character reference feature [VERIFIED]
- Transparent background generation (native API) [VERIFIED]
- Edit/Remix/Reframe/Replace-background flexibility [VERIFIED]

**Where Ideogram 3.0 loses to alternatives:**
- Photorealism -- Imagen 4 superior [VERIFIED]
- Text in photorealistic scenes -- Imagen 4 better [VERIFIED]
- Non-Latin text -- unreliable (both Ideogram and Imagen) [VERIFIED]

**Known failure modes:**
- Long text (8+ words single block): letters merge, swap, garble [VERIFIED]
- Multiple text blocks (3+) with specific positions: model conflates locations [VERIFIED]
- **Multi-panel comic pages (6+ text blocks at grid positions): decisively fails** — session 37 test (comic-v1 FACT LAB, 6-panel 2x3 grid, 4 variants via `num_images=4` + QUALITY) produced garbled text ("WCH TEAD ECHAIN FOL", "SPAL AROM", "Eadmer med"), broken grids (1+2+3 layout instead of 2x3), repeated panels ("EACH ARM THINKS" rendered 3x in same page), and character drift across panels. All 4 variants unshippable. **Not recommended for multi-panel sequential art** — use NB2 (Gemini 3.1 Flash Image) or Recraft V4 for comic format. Ideogram stays in the toolbox for single-piece typography: quote cards, title cards, social posters, infographics. [VERIFIED — comic-v1 session 37]
- Small text / fine print: illegible or misspelled [VERIFIED]
- Non-Latin scripts: frequently incorrect [VERIFIED]
- Human faces at distance: unnatural proportions [VERIFIED]
- Hands and fingers: occasional distortion [VERIFIED]
- Prompts > 150 words: later tokens ignored [VERIFIED]
- Magic Prompt ON + style references: unintended style mutations [VERIFIED]
- style_codes + style_type or style_reference_images: parameter conflict (API error) [VERIFIED]

---

## Typography Craft Principles (compiled from source)

### Text-Image Unity [VERIFIED from research]
Describe text as PART of the visual composition, not as an overlay. "A poster where bold geometric text 'JAZZ NIGHT' shares the angular shapes of the illustrated instruments" beats "A jazz poster with text 'JAZZ NIGHT' on it."

### Negative Space as Active Element [VERIFIED from research]
Explicitly request negative space: "generous white space around the headline." Resist the urge to fill every pixel. `style_preset=EMOTIONAL_MINIMAL` or `GEO_MINIMALIST` enforce this.

### Single-Word Headlines Beat Sentences [VERIFIED from research]
One word per fixation. Default to the shortest possible text: 1 word ideal, 2-3 acceptable, 4 is the upper bound. This also aligns with Ideogram's text accuracy (fewer characters = higher reliability).

### Typography Carries Emotion Before Being Read [VERIFIED from research]
Choose typography style based on emotion, not information. "Heavy, bold, compressed type reading 'ACT NOW'" for urgency. "Light, elegant serif reading 'Take Your Time'" for calm. Font description should be an emotional instruction.

### Hierarchy Through Scale Differential [VERIFIED from research]
Describe explicit size relationships: "large bold headline, medium-weight subtitle at half the size, small attribution at bottom." Scale ratio at least 2:1 between primary and secondary text.

---

## Operational Rules

- **When generating text-heavy graphics,** always set `style_type=DESIGN` and `magic_prompt=OFF`, because DESIGN mode treats text placement with hierarchy awareness and magic_prompt adds details that conflict with precise text. [VERIFIED]
- **When text accuracy matters,** generate 4 images (`num_images=4`) and pick the best text rendering, because first-attempt accuracy is 90-95% for Latin text. [VERIFIED]
- **When text has errors,** use the Edit endpoint with a mask over the text area before regenerating from scratch, because targeted inpainting is faster and cheaper than full regeneration. [VERIFIED]
- **When quoted text must appear,** keep it under 20 characters per block for >90% accuracy and under 10 for >95%, because accuracy is inversely proportional to text length. [VERIFIED]
- **When placing text in the prompt,** put quoted text EARLY (before style/composition details), because front-loaded tokens are processed more reliably. [VERIFIED]
- **When using style references,** set `magic_prompt=OFF` and avoid style keywords in the prompt, because Magic Prompt + references cause unintended style mutations. [VERIFIED]
- **When iterating,** use TURBO rendering speed (~$0.03), because QUALITY (~$0.08-0.10) is 2-3x more expensive and only needed for final output. [VERIFIED]
- **When maintaining visual consistency across a series,** save successful `style_codes` and reuse them, because style codes from the 4.3B preset library are stable and reusable. [VERIFIED]
- **When needing 3+ text elements,** split across 2 generations and composite, because the model conflates text locations beyond 2 blocks. [VERIFIED]
- **When compositing with photorealistic backgrounds,** generate text elements via Generate Transparent endpoint and composite onto Imagen 4 scenes, because Ideogram excels at text while Imagen excels at photorealism. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `tools/research-data/ideogram_3_visual_text_research.md` | Complete API reference, all endpoints, text rendering assessment, style presets (58), magic_prompt behavior, prompt engineering, typography craft from poster/editorial/advertising masters, failure modes, pricing, Ideogram vs Imagen comparison |
| `credentials.md` (memory) | Auth pattern, plan info, key settings guidance |

---

## Related Concepts

- [[recraft-v4]] — CONTRASTS: Recraft has better design composition and native SVG; Ideogram has more style presets and stronger text rendering accuracy
- [[veo-3-1]] — INFORMS: Ideogram generates title cards and text overlays for Veo video content
- [[elevenlabs]] — INFORMS: audio layer to pair with Ideogram-generated visual cards

---

## Deep Reference

- **When** generating text-in-image and need the key settings that prevent magic_prompt from rewriting your typography → **read** `research-data/ideogram_3_visual_text_research.md` §(API Reference) **for** `magic_prompt: OFF` as mandatory for text work, `style_type: DESIGN` for consistent graphic output, the 15 aspect ratio options, 70 exact resolution options, and the 4 rendering speed tiers (FLASH/TURBO/DEFAULT/QUALITY) with cost tradeoffs
- **When** choosing a style preset and need the full list of 58 options → **read** `research-data/ideogram_3_visual_text_research.md` §(Style Presets) **for** the complete preset catalog organized by category, incompatibility rules (style_codes vs style_reference_images vs style_type), and the color palette system (8 named presets: EMBER, FRESH, JUNGLE, MAGIC, MELON, MOSAIC, PASTEL, ULTRAMARINE, plus custom hex with weights 0.05-1.0)
- **When** designing title cards or social media graphics with typography and need craft principles → **read** `research-data/ideogram_3_visual_text_research.md` §(Typography Craft) **for** poster/editorial/advertising typography principles adapted to AI text generation, failure modes (text bleeding, character substitution, kerning issues), and the prompting patterns that produce reliable multi-line text

---

## Open Questions

- Exact pricing for character reference generations -- higher rate not publicly documented [THEORETICAL]
- Non-Latin script improvement roadmap -- currently unreliable for CJK, Arabic, Cyrillic [VERIFIED as limitation]
- Batch API for programmatic mass generation -- only available as web UI feature for Pro subscribers [VERIFIED]
- Style code discovery -- codes generated automatically with "Random" style but no search/browse API [THEORETICAL]
