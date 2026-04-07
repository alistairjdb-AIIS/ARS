# Ideogram 3.0: Operational Reference for AI-Driven Visual Text Production

Research date: April 3, 2026. Verified against official documentation and multiple independent sources.

**Consumer:** Agent producing visual content (social media graphics, title cards, infographics, typographic compositions, branded visuals). Every section answers: "How does knowing this change what I type into the API?"

---

## LAYER 1: TOOL MASTERY

---

### 1. API Capabilities — Complete Endpoint Reference

Base URL: `https://api.ideogram.ai`
Auth: Header `Api-Key: <key>`
Rate limit: 10 concurrent in-flight requests (default)
Format: `multipart/form-data` for all endpoints
Image URLs in responses expire — download immediately.

#### 1.1 Generate
```
POST /v1/ideogram-v3/generate
```

**Required:** `prompt` (string)

**Optional:**
| Parameter | Type | Default | Notes |
|---|---|---|---|
| `num_images` | integer | 1 | Number of images |
| `seed` | integer | random | For reproducibility |
| `aspect_ratio` | string | `1x1` | 15 options: 1x3, 3x1, 1x2, 2x1, 9x16, 16x9, 10x16, 16x10, 2x3, 3x2, 3x4, 4x3, 4x5, 5x4, 1x1 |
| `resolution` | string | auto | 70 exact resolutions from 512x1536 to 1536x512. Mutually exclusive with aspect_ratio |
| `rendering_speed` | string | `DEFAULT` | `FLASH`, `TURBO`, `DEFAULT`, `QUALITY` |
| `magic_prompt` | string | `AUTO` | `AUTO`, `ON`, `OFF` |
| `negative_prompt` | string | none | What to exclude |
| `style_type` | string | `AUTO` | `AUTO`, `GENERAL`, `REALISTIC`, `DESIGN`, `FICTION` |
| `style_preset` | string | none | 58 presets (see list below) |
| `style_codes` | array[string] | none | 8-char hex codes. Incompatible with style_reference_images and style_type |
| `color_palette` | object | none | Preset name (EMBER, FRESH, JUNGLE, MAGIC, MELON, MOSAIC, PASTEL, ULTRAMARINE) or custom hex colors with weights 0.05-1.0 |
| `style_reference_images` | array[binary] | none | Up to 10MB total. JPEG/PNG/WebP |
| `character_reference_images` | array[binary] | none | Currently 1 image max, 10MB. Special pricing |
| `character_reference_images_mask` | array[binary] | none | Grayscale mask matching character reference dimensions |

**Response (200):**
```json
{
  "created": "ISO 8601",
  "data": [{
    "url": "string|null",
    "prompt": "string (may differ from input if MagicPrompt active)",
    "resolution": "string",
    "upscaled_resolution": "string|null",
    "is_image_safe": true,
    "seed": 12345,
    "style_type": "GENERAL"
  }]
}
```

**Errors:** 400 (bad input), 401 (auth), 422 (safety fail), 429 (rate limit)

#### 1.2 Generate Transparent Background
```
POST /v1/ideogram-v3/generate-transparent
```
Same as Generate, plus:
- `upscale_factor`: `X1` (default), `X2`, `X4` — higher factors cost more
- System auto-selects maximum supported resolution at specified aspect ratio

**Use case for agent:** Generate logos, stickers, overlay text elements with transparent background for compositing.

#### 1.3 Edit (Inpainting)
```
POST /v1/ideogram-v3/edit
```
**Required:** `image` (binary, max 10MB), `mask` (binary, same size as image), `prompt`

Black mask regions = areas to edit. White regions = preserved.

All optional params from Generate available except aspect_ratio and resolution.

**Agent use case:** Fix text rendering errors. Generate image, if text misspelled, create mask over text area, re-edit with corrected prompt. This is the primary error correction workflow.

#### 1.4 Remix
```
POST /v1/ideogram-v3/remix
```
**Required:** `image` (binary), `prompt`

**Key unique parameter:** `image_weight` (integer, 0-100, default 50) — controls how much the input image influences output.

All optional params from Generate available. Input images auto-cropped to selected aspect_ratio.

**Agent use case:** Take a branded template/reference image, remix with new text content while preserving visual style. High image_weight (70-90) preserves layout; low (10-30) allows creative reinterpretation.

#### 1.5 Reframe (Outpainting)
```
POST /v1/ideogram-v3/reframe
```
**Required:** `image` (binary), `resolution` (target dimensions)

Optional: `num_images`, `seed`, `rendering_speed`, `style_preset`, `color_palette`, `style_codes`, `style_reference_images`

Note: No prompt parameter. No style_type. 69 target resolutions available.

**Agent use case:** Convert a 1:1 graphic to 9:16 for Stories/Reels or 16:9 for YouTube thumbnails.

#### 1.6 Replace Background
```
POST /v1/ideogram-v3/replace-background
```
**Required:** `image` (binary), `prompt` (describing new background)

Optional: `magic_prompt`, `num_images`, `seed`, `rendering_speed`, `style_preset`, `color_palette`, `style_codes`, `style_reference_images`

#### 1.7 Upscale
```
POST /upscale
```
Note: This is NOT under `/v1/ideogram-v3/` — it's a root-level endpoint.

**Required:** `image_request` (object with optional `prompt`), `image_file` (binary)

**Unique parameters:**
- `resemblance` (integer, default 50) — similarity to original
- `detail` (integer, default 50) — detail enhancement level
- `magic_prompt_option`: AUTO/ON/OFF
- No explicit upscale factor (2x/4x) — controlled via resemblance/detail

#### 1.8 Describe (Image-to-Text)
```
POST /describe
```
**Required:** `image_file` (binary)
**Optional:** `describe_model_version`: `V_2` or `V_3` (default V_3)

**Response:** `{ "descriptions": [{ "text": "string" }] }`

**Agent use case:** Analyze reference images to reverse-engineer effective prompts. Feed competitor visuals through Describe, then use output as prompt foundation.

---

### 2. Text Rendering — Core Capability Assessment

#### 2.1 Accuracy
- Latin text: ~90-95% accuracy on first generation
- Single words / 2-4 word phrases: highest reliability (95%+)
- Longer text (5+ words): accuracy drops, breaks increase
- Multi-line text with placement instructions: works but needs regeneration attempts
- Non-Latin scripts: significantly lower accuracy. Chinese/Arabic/Cyrillic often render incorrectly. Official docs acknowledge this.

#### 2.2 How to Specify Text
- **Quotation marks are mandatory.** Text intended for rendering MUST be in quotes within the prompt.
- Place quoted text EARLY in the prompt — Ideogram processes front-loaded tokens more reliably.
- Specify casing explicitly: "all caps", "title case", "lowercase" — reduces typos.
- Describe text location: "centered at top", "bottom third", "right side"
- Describe text style: "bold sans-serif", "elegant script", "rounded bauhaus style"

#### 2.3 Font Control
You CANNOT specify exact font names (no "use Helvetica"). You CAN describe:
- Weight: bold, ultra thin, light, heavy
- Category: sans-serif, serif, script, monospace
- Style descriptors: "rounded bauhaus style", "formal script with flourishes", "1960s hippie style", "art deco geometric"
- Size relative to composition: "large headline", "small subtitle text"

#### 2.4 What the Agent Should Know

**Reliable configurations:**
- Single headline, 1-4 words, placed at top or center
- Two text elements (headline + subtitle) with explicit placement
- Text on solid/simple backgrounds
- ALL CAPS text (fewer character-level errors)
- DESIGN style_type for any text-heavy graphic

**Unreliable configurations:**
- 3+ separate text blocks with specific placement
- Long sentences (8+ words) as a single text element
- Small text / fine print
- Text wrapping around objects
- Non-Latin characters
- Text that must exactly match a specific font

**Error correction workflow:**
1. Generate with text
2. If text has errors, use Edit endpoint with mask over text area
3. Re-prompt with corrected text
4. If still failing after 2 attempts, generate text-free version and composite text in post-processing

#### 2.5 Practical Character Limits
- Prompt limit: ~150-160 words / ~200 tokens
- Text within quotes: no hard character limit, but accuracy inversely proportional to length
- **Operational rule:** Keep quoted text under 20 characters per text block for >90% first-attempt accuracy. Under 10 characters for >95%.

---

### 3. Style References

#### 3.1 How It Works
Upload up to 3 reference images (10MB total). Ideogram extracts visual characteristics — color palette, texture, mood, composition style — and applies them to the generation.

Behind the scenes: draws from a library of 4.3 billion style presets to match reference aesthetics.

#### 3.2 Strength Control
No direct "style strength" slider in the API. Control indirectly:
- Through Remix: `image_weight` parameter (0-100) adjusts balance between reference and prompt
- Through prompt: removing style keywords when using references prevents conflicts
- Magic Prompt OFF recommended when using style references (prevents unwanted stylistic additions)

#### 3.3 Best Practices for Agent
- Choose reference images that share similar look/mood/aesthetic for unified results
- Mix diverse references intentionally when blending aesthetics
- Gradient-heavy reference images will shift overall color tone
- Turn Magic Prompt OFF when using style references
- Avoid style keywords in prompt when references are active — let the references speak
- Short, focused prompts yield best results with style references

#### 3.4 Style Codes (Alternative to References)
- 8-character hex codes from Ideogram's 4.3B preset library
- Generated automatically when using "Random" style
- Reusable across prompts for consistent visual style
- INCOMPATIBLE with style_reference_images and style_type — use one system or the other
- **Agent strategy:** When a generation looks right, extract its style code and save it for future use on similar content

---

### 4. Prompt Engineering — What the Best Users Do

#### 4.1 Optimal Prompt Structure
```
[Image summary]. [Main subject], [Text in quotes with placement], [Style/mood], [Composition/framing], [Technical details]
```

Concrete example for a social media quote card:
```
A modern motivational quote card with dark gradient background.
Bold white sans-serif text reading "START BEFORE YOU'RE READY" centered
in the upper third. Smaller text "— Rob Moore" below in thin serif.
Minimal geometric accent lines. Clean, professional, Instagram-ready.
```

#### 4.2 Rules That Change Output Quality

1. **Front-load the important parts.** Tokens beyond ~150 words get deprioritized or ignored.
2. **One subject, one style anchor, exact text in quotes, one placement instruction, one constraint.** This is the minimum effective prompt for text graphics.
3. **Use DESIGN style_type for all text-heavy work.** It treats text placement with visual hierarchy awareness.
4. **Natural sentences over keyword soup.** "A poster for a jazz concert with the title 'BLUE NOTE' in large art deco letters" beats "jazz poster, art deco, text, BLUE NOTE, large letters."
5. **Describe what you want, not what you don't want.** "Bald" not "no hair." Negative phrasing confuses the model. Use `negative_prompt` parameter for exclusions.
6. **Lock casing in quotes.** Write "SALE ENDS SUNDAY" not "Sale Ends Sunday" if you want all caps.
7. **Break multi-text layouts into explicit spatial chunks.** "Title 'SUMMER SALE' centered at top. Subtitle '50% OFF EVERYTHING' in smaller text below. Date 'June 1-15' at the bottom."

#### 4.3 Prompt Templates for Common Agent Tasks

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

**Infographic header:**
```
A professional infographic header. [Color scheme]. Bold headline reading
"[TITLE]" at top. [Icon/visual element description below]. Clean layout,
data-visualization style. style_type=DESIGN
```

**Branded visual with logo text:**
```
A [brand style] branded image. [Visual description]. Brand name
"[BRAND]" in [specific typography description] at [position].
[Tagline/subtitle]. Professional, polished. style_type=DESIGN
```

---

### 5. Magic Prompt — When to Use Each Setting

| Setting | What It Does | When to Use | When to Avoid |
|---|---|---|---|
| `AUTO` | Model decides enhancement level based on prompt length | General exploration, varied outputs | When you need exact control |
| `ON` | Enhances all generated images | Short/vague prompts that need enrichment | Precise text work, style references active |
| `OFF` | Uses your prompt exactly as written | **ALL text-heavy work**, style references, precise compositions | Never avoid this for text work |

**Operational rule for agent:** Default to `magic_prompt=OFF` for any generation where text accuracy matters. Magic Prompt adds creative details that can conflict with text placement, style references, and precise layout instructions.

When using Magic Prompt ON, the enhanced prompt is visible in the response's `prompt` field — useful for learning what details the model adds.

---

### 6. Style Types and Modes

#### 6.1 Style Types (style_type parameter)

| Type | Best For | Text Quality | Notes |
|---|---|---|---|
| `AUTO` | Let model decide | Variable | Not recommended for text work |
| `GENERAL` | Artistic, abstract, illustrations | Good | Versatile default |
| `REALISTIC` | Photography, product shots | Good for overlays | Best photorealism |
| `DESIGN` | **Graphics, typography, logos, marketing materials** | **Best** | **Default for all agent text work** |
| `FICTION` | Fantasy, sci-fi, stylized | Variable | Good for themed title cards |

Additional types available in responses (not settable via generate): `RENDER_3D`, `ANIME`

#### 6.2 Style Presets (58 options)
Grouped by utility for text-integrated visuals:

**Best for text-heavy work:**
ART_DECO, ART_POSTER, EDITORIAL, FLAT_ART, FLAT_VECTOR, GEO_MINIMALIST, HALFTONE_PRINT, MAGAZINE_EDITORIAL, MINIMAL_ILLUSTRATION, POP_ART, TRAVEL_POSTER, VINTAGE_POSTER

**Good for title cards / atmospheric:**
DRAMATIC_CINEMA, DARK_AURA, GOLDEN_HOUR, LONG_EXPOSURE, NIGHTLIFE, SPOTLIGHT_80S

**Risky for text (heavy stylization may distort letterforms):**
ABSTRACT_ORGANIC, ART_BRUT, BLURRY_MOTION, COLLAGE, CUBISM, DOUBLE_EXPOSURE, GRAFFITI_I, GRAFFITI_II, MIXED_MEDIA, PAINT_GESTURE, SURREAL_COLLAGE, WATERCOLOR, WEIRD

**Full list:** 80S_ILLUSTRATION, 90S_NOSTALGIA, ABSTRACT_ORGANIC, ANALOG_NOSTALGIA, ART_BRUT, ART_DECO, ART_POSTER, AURA, AVANT_GARDE, BAUHAUS, BLUEPRINT, BLURRY_MOTION, BRIGHT_ART, C4D_CARTOON, CHILDRENS_BOOK, COLLAGE, COLORING_BOOK_I, COLORING_BOOK_II, CUBISM, DARK_AURA, DOODLE, DOUBLE_EXPOSURE, DRAMATIC_CINEMA, EDITORIAL, EMOTIONAL_MINIMAL, ETHEREAL_PARTY, EXPIRED_FILM, FLAT_ART, FLAT_VECTOR, FOREST_REVERIE, GEO_MINIMALIST, GLASS_PRISM, GOLDEN_HOUR, GRAFFITI_I, GRAFFITI_II, HALFTONE_PRINT, HIGH_CONTRAST, HIPPIE_ERA, ICONIC, JAPANDI_FUSION, JAZZY, LONG_EXPOSURE, MAGAZINE_EDITORIAL, MINIMAL_ILLUSTRATION, MIXED_MEDIA, MONOCHROME, NIGHTLIFE, OIL_PAINTING, OLD_CARTOONS, PAINT_GESTURE, POP_ART, RETRO_ETCHING, RIVIERA_POP, SPOTLIGHT_80S, STYLIZED_RED, SURREAL_COLLAGE, TRAVEL_POSTER, VINTAGE_GEO, VINTAGE_POSTER, WATERCOLOR, WEIRD, WOODBLOCK_PRINT

---

### 7. Known Failure Modes

**Text failures:**
- Long text (8+ words) in a single block: letters merge, swap, or get garbled
- Multiple text blocks (3+) with specific positions: model conflates text locations
- Small text / fine print: illegible or misspelled
- Non-Latin scripts: frequently incorrect. Do not rely on Ideogram for Chinese, Arabic, Japanese, Cyrillic text.
- Text wrapping around curves or objects: unpredictable
- ALL CAPS text over 6 words: starts to break

**Visual failures:**
- Human faces at a distance: unnatural skin textures, proportions
- Hands and fingers: occasional distortion
- Subjects rendered too small in frame: insufficient detail

**Prompt failures:**
- Prompts > 150 words: later tokens ignored
- Negative phrasing in prompt body: model renders the thing you tried to exclude
- Vague/abstract concepts: unpredictable interpretation
- Single-word prompt changes: may have no visible effect

**Style failures:**
- Magic Prompt ON + style references: unintended style mutations
- style_codes + style_type or style_reference_images: parameter conflict (API error)
- Generic style descriptors ("modern", "artistic"): produce generic output

**Operational mitigations:**
1. Always generate 2-4 images (num_images=4) and pick the best text rendering
2. Use QUALITY rendering_speed for final output
3. Use TURBO for rapid iteration / text accuracy checks
4. Keep Edit endpoint ready as the text correction tool
5. For 3+ text elements, split across 2 generations and composite

---

### 8. Ideogram 3.0 vs. Google Imagen 4 — Where Each Wins

| Dimension | Ideogram 3.0 | Imagen 4 |
|---|---|---|
| **Text in decorative/stylized contexts** | Superior. Purpose-built text engine | Good but less stylistic range |
| **Text in photorealistic scenes** | Good | Superior. Typography treated as part of the photo |
| **Graphic design layouts** | Superior. DESIGN mode handles visual hierarchy | Adequate but not specialized |
| **Photorealism** | Good (REALISTIC mode) | Superior |
| **Style variety / presets** | Superior. 58 presets + 4.3B style codes | Limited style control |
| **Character consistency** | Has character reference feature | Not available |
| **Transparent backgrounds** | Native API support | Not available via standard API |
| **Non-Latin text** | Unreliable | Unreliable |
| **API flexibility** | More endpoints (edit, remix, reframe, replace-bg) | Simpler API |
| **Speed** | TURBO mode fast, QUALITY slow | Generally fast |
| **Cost** | ~$0.03-0.08 per image depending on tier | ~$0.03 per image via Vertex AI |

**Agent operational decision:**
- Use **Ideogram** for: text-heavy graphics, branded visuals, title cards, social media cards, infographics, typographic compositions, logo-type images, style-matched series
- Use **Imagen 4** for: photorealistic images, product photography, scene generation where text is secondary, when photorealism matters more than typography control
- Use **both** when: compositing a photorealistic Imagen 4 background with Ideogram-generated text overlay elements (generate text element with transparent background via Ideogram, composite onto Imagen scene)

---

### 9. Pricing and Rate Limits

**Official API (direct from Ideogram):**
- Generate (Default speed): ~$0.06 per image
- Generate (Turbo): ~$0.03 per image
- Generate (Quality): ~$0.08-0.10 per image
- Character reference generations: higher rate (exact multiplier not publicly documented)
- Upscale factors X2/X4: additional cost

Note: Pricing was difficult to pin down exactly. The official pricing page requires direct access. Multiple sources cite different numbers, likely reflecting pricing changes over time. The above represents the best cross-referenced estimates as of April 2026.

**Subscription credits (web UI):**
- Plus ($8/mo): Limited generations/month, Priority queue
- Pro ($20/mo): More generations, batch generation access
- Turbo uses 2 credits, Default 4 credits, Quality 6 credits per 4-image generation

**Rate limits:**
- Default: 10 concurrent in-flight requests
- No documented batch API for programmatic mass generation (batch generation is a web UI feature for Pro subscribers)

**Billing:**
- Pre-paid credit balance
- Auto-top-up: default minimum $10 threshold, $20 top-up amount
- All API keys on account share one billing plan
- Adjustable: minimum threshold > $2, top-up > $10

**Cost optimization for agent:**
1. Use TURBO for all iteration/testing (cheapest per image)
2. Generate 4 images per call (same API call cost, more options)
3. Switch to QUALITY only for final approved outputs
4. Save successful style_codes to avoid re-discovering styles
5. Use Describe endpoint to reverse-engineer competitor visuals instead of manual prompt iteration

---

## LAYER 2: CROSS-DOMAIN CRAFT KNOWLEDGE

### Typography in Visual Communication — Lessons from the Masters

---

### From Poster Design

#### Toulouse-Lautrec (1864-1901): Text and Image as One Organism

**Key insight:** Lautrec did not add text to images. He designed compositions where text and image were structurally inseparable.

**Techniques:**
- Typography incorporated directly into the composition as a design element, not added after
- Composition designed to guide the eye in circular motion around the page — text was a waypoint on this path
- Simplified forms, flat color areas, bold outlines — creating a visual language where letterforms and figures share the same graphic vocabulary
- Influence of Japanese prints: eliminated shadows, flattened space, used color as shape rather than light
- The text occupied the same spatial plane as the illustration — no sense of "layer on top of"

**Application to Ideogram prompts:**
- Describe text as part of the composition, not as an overlay: "A poster where the word 'MOULIN' is woven into the sweeping curves of a dancer's skirt" vs. "A dancer with text 'MOULIN' on top"
- Request flat color areas and bold outlines — this visual vocabulary naturally integrates text
- Use `style_preset=ART_POSTER` or `VINTAGE_POSTER` for Lautrec-influenced output

#### A.M. Cassandre (1901-1968): Geometry Unifies Image and Letter

**Key insight:** When letterforms and illustration share the same geometric logic, they become one visual system.

**Techniques:**
- Radically simplified forms into geometric volumes — cones, cylinders, planes
- Created custom typefaces (Bifur, Acier Noir, Peignot) where letterforms shared geometric DNA with his illustrations
- Used only capitals for large-scale legibility
- Type was not a separate element — it was integrated with the image as a unified concept
- Dubonnet series: first posters designed to be read from fast-moving vehicles (legibility at speed)
- Serial poster concept: related posters seen in rapid succession to build a complete idea

**Application to Ideogram prompts:**
- Describe geometric consistency: "Art deco poster with geometric letterforms matching the angular style of the illustration"
- Request "all caps" for display text — Cassandre's legibility principle
- For social media series, use same style_code across multiple generations for visual continuity (Cassandre's serial poster principle)
- Use `style_preset=ART_DECO` with `style_type=DESIGN`

#### Polish Poster School (1950s-1980s): Letters as Expressive Objects

**Key insight:** Typography can carry emotional content independent of the words' meaning. The shape of letters communicates before reading happens.

**Techniques:**
- Hand-drawn, uneven lettering integrated into illustrations
- Letters treated as expressive design elements, not information carriers
- Ambiguity and metaphor over literal illustration
- Bold typography mixed with painterly textures, abstract forms
- Each poster was unique — no templates, no systems, pure individual expression

**Application to Ideogram prompts:**
- For emotional/evocative title cards: "Hand-drawn expressive lettering that feels organic and emotional, with letters that bend and flow like the illustration around them"
- Use when you want text to FEEL something rather than just communicate information
- Works against Ideogram's default tendency toward clean typography — push for distortion and expression
- Best with `style_preset=ART_BRUT` or `PAINT_GESTURE`

#### Shepard Fairey (1970-present): Viral Visual Communication Formula

**Key insight:** Limited color + bold type + iconic image + single-word messaging = maximum memetic spread.

**The formula:**
- Limited palette (3-4 colors, typically including red/blue/white)
- High contrast stencil/screen-print aesthetic
- Single powerful word ("HOPE", "OBEY") — NOT a sentence
- Gotham typeface — geometric, authoritative, modern
- Three-quarters portrait view (face looking up and to the side = aspiration)
- Grassroots/street art aesthetic = democratic, accessible

**Application to Ideogram prompts:**
- "A bold propaganda-style poster with limited red, cream, and blue palette. Single word '[WORD]' in large geometric sans-serif at the bottom. High-contrast stencil aesthetic. Iconic, powerful."
- For maximum text impact: use SINGLE WORDS. Fairey proved one word hits harder than any sentence.
- Color palette parameter: custom with 3 hex colors at high weights
- `style_preset=POP_ART` or `ICONIC`

---

### From Editorial Design

#### Alexey Brodovitch (1898-1971): The Dance of Type and White Space

**Key insight:** White space is not empty — it is an active compositional force that gives typography room to breathe and creates visual rhythm.

**Techniques:**
- Revolutionized the double-page spread as a dynamic compositional field
- Crisp Bodoni typefaces + elegant white space + exquisite photographs = total composition
- Asymmetrical layouts that created movement and energy
- Full-page photography as emotional anchor, with typography as counterweight
- Each page designed as part of a sequence — pacing across spreads like music

**Application to Ideogram prompts:**
- Explicitly request white space: "with generous negative space around the text" or "asymmetrical layout with breathing room"
- The absence of visual elements is as important as their presence
- For title cards: "Elegant serif headline placed asymmetrically with large areas of clean space. Editorial quality."
- Use `style_preset=EDITORIAL` or `MAGAZINE_EDITORIAL`
- Aspect ratio 3:4 or 4:5 mimics editorial page proportions

#### Neville Brody (1957-present): Typography as Emotional Language

**Key insight:** Letters are not neutral carriers of meaning. They have coloring, rhythm, and expressive power independent of the words they form.

**Techniques:**
- Grid-breaking layouts that defied column structures
- Type pushed to extremes — squeezed into narrow columns, oversized, fragmented
- Created Arcadia typeface: boundary between legibility and expression
- Fuse project: type as art form, meaning through form independent of semantics
- Every page was a canvas for typographic experimentation

**Application to Ideogram prompts:**
- For bold/edgy content: "Experimental typography that pushes the boundaries of readability while remaining functional. Text feels energetic and unconventional."
- Brody proves you can distort letterforms significantly and maintain readability — useful for title cards where FEELING matters more than quick scanning
- `style_preset=AVANT_GARDE` or `BAUHAUS`
- Caution: Ideogram's text engine may fight against intentional distortion. Describe the EFFECT you want rather than requesting specific letter manipulations.

#### Magazine Cover Composition Rules

**Principles that apply directly to social media graphics:**
- Visual hierarchy path: eye goes to IMAGE first, then HEADLINE, then supporting text
- Lead element (text OR image) should dominate; the other supports
- Maximum 2-3 font families total
- Grid system keeps text aligned and balanced
- White space between text blocks prevents clustering
- Contrasting colors make text stand out from image
- Center-dominant compositions work best for thumbnail/cover contexts

**Application to Ideogram prompts:**
- Describe hierarchy explicitly: "Large bold headline dominates the top third, supporting text smaller in the bottom quarter, central image occupying the middle"
- Request specific contrast: "White text on dark background" or "Dark text with light halo effect"
- `style_type=DESIGN` respects these compositional rules better than other modes

---

### From Sign Painting and Lettering

#### Why Hand-Lettering Feels "Alive"

**Key insight:** The difference between typography (setting pre-made letters) and lettering (drawing letters) is the difference between mechanical reproduction and human gesture. People respond to the evidence of a human hand.

**What makes hand-lettering feel different:**
- Imperfection is signal of authenticity — slight variations in stroke weight, spacing, baseline
- Each letter is drawn for its specific context and neighbors — custom kerning, custom flourishes
- Physical process creates unique characteristics (brush texture, pen pressure variation)
- Permanence vs. disposability: hand-painted signs outlast and outweigh their disposable counterparts emotionally

**When to use typography vs. lettering aesthetic:**
- **Typography (clean fonts):** Corporate, professional, data-driven, trust/authority contexts
- **Lettering (drawn letters):** Personal, artisanal, emotional, authentic, story-driven contexts

**Application to Ideogram prompts:**
- For warm/authentic feel: "Hand-lettered text with natural brush strokes, slight imperfections that give it a human quality"
- For professional/clean: "Clean modern sans-serif typography, precise letter spacing, professional"
- Ideogram can produce both. The key is choosing which emotional register fits the content.
- Jessica Hische's principle: lettering fills the gap where typefaces are "close enough but not quite right" — when generic fonts would flatten the emotional content

---

### From Advertising

#### David Ogilvy: How the Eye Reads Ads

**Empirically verified reading order:**
1. Image (looked at first)
2. Headline
3. Caption
4. Body copy

**Ogilvy's rules that change how you design text-in-image:**
- Headlines below the image are read by 10% more people than headlines above (people scan downward)
- 5x more people read headlines than body copy — the headline IS the ad for 80% of viewers
- Serif fonts are easier to read than sans-serif in print
- ALL CAPS text is harder to read — people read it letter by letter instead of word-shape recognition
- Drop caps increase readership by 13%
- If the headline doesn't sell, 90% of the budget is wasted

**Application to Ideogram prompts:**
- Place key text below the main visual element when possible
- Make the headline THE message — don't bury meaning in body text that won't be read
- For readability: request sentence case over ALL CAPS for long text (reserve ALL CAPS for 1-3 word headlines)
- For infographics: request drop caps or oversized first letters

#### Bill Bernbach / "Think Small": Maximum Impact Through Minimum

**Key insight:** Negative space IS the message. What you don't fill speaks louder than what you do.

**The formula:**
- Mostly white/empty space — the eye has nowhere else to go
- Small subject in large field creates emphasis through isolation
- Fine-print text at bottom — reader must lean in, creating intimacy
- Lowercase headline ("think small") — the medium mirrors the message
- Photography replaced illustration — raw honesty over aspirational fantasy

**Application to Ideogram prompts:**
- "Minimal composition with vast white space. Small [subject] centered. Text '[HEADLINE]' in small, understated lowercase at the bottom. The emptiness IS the design."
- Counterintuitive: sometimes making text smaller makes it more powerful
- Not every social media graphic needs to scream — strategic quiet cuts through noise
- `style_preset=EMOTIONAL_MINIMAL` or `GEO_MINIMALIST`

#### Eye Movement Patterns (F-Pattern and Z-Pattern)

**F-Pattern (text-heavy content):**
1. Horizontal sweep across top
2. Shorter horizontal sweep slightly lower
3. Vertical scan down the left edge

**Z-Pattern (visual content with minimal text):**
1. Top-left to top-right (first scan)
2. Diagonal from top-right to bottom-left
3. Bottom-left to bottom-right (final scan)

**Application to Ideogram prompts:**
- For graphics with body text: place key information along F-pattern (top, left-aligned)
- For single-image graphics: place headline at top-left, CTA at bottom-right (Z-pattern endpoints)
- For Instagram (square): Z-pattern means "title top-left, action bottom-right"
- For Stories/Reels (9:16): F-pattern dominates — top-loaded content gets read

---

### From Film Title Design

#### Saul Bass (1920-1996): Typography Sets Emotional Tone

**Key insight:** Typography PREPARES the viewer emotionally. The shape, movement, and behavior of letters create an emotional state before the content is even consciously read.

**Techniques:**
- Simplified symbolic designs communicating film essence
- Sans-serif typography with rhythmic micro-movement
- Vertigo: spiral vortex pulling letters = disorientation, obsession
- Psycho: split text racing together and apart = fractured psyche
- Typography as kinetic gesture — written word becomes motion

**Application to title cards:**
- Describe the EMOTIONAL EFFECT of the typography, not just the words: "Text that fragments and separates, creating tension and unease" or "Typography that spirals inward, suggesting obsession"
- For Reels title cards: the first frame's typography tells viewers what emotion to expect
- Pair with appropriate style_presets: `DRAMATIC_CINEMA`, `DARK_AURA`, `MONOCHROME`

#### Kyle Cooper (1962-present): Distressed Typography Creates Feeling

**Key insight:** Imperfection in typography is a storytelling tool. Roughness, distortion, and analog artifacts communicate more than clean type ever could in certain emotional registers.

**Se7en techniques:**
- Typography hand-etched into scratchboard, then manipulated during film transfer
- Mixing handwritten text with Helvetica — the overlap creates anxiety
- Analog process over digital — natural inaccuracies were the point
- Jumpy frame changes + erratic motion + quavering type = the killer's own handwriting
- The typography WAS the character

**Application to title cards:**
- For dark/intense content: "Distressed, hand-scratched typography layered with clean sans-serif text, creating unease and tension. Raw, analog feel."
- The combination of clean + rough type creates productive tension
- `style_preset=GRAFFITI_I` or `DARK_AURA` with specific distress language in prompt

---

### From Calligraphy and Writing Systems

#### Arabic Calligraphy: Text as Sacred Art

**Key insight:** When text is treated as the primary art form rather than supplement to an image, it achieves a beauty that purely informational typography never reaches.

**Principles:**
- Balance between transmitting text and expressing its meaning through formal aesthetic code
- Evolution from bold/angular (Kufic) to flowing/elegant (Naskh) based on readability needs
- A single letter can develop into a decorative knot; an entire word can look like random brushstrokes
- "Purity of writing is purity of the soul" — the craft itself carries moral/spiritual weight
- Tools matter: the qalam (reed pen) creates depth and variation in each stroke

**Application:**
- The principle of text-as-primary-art applies to quote cards: make the typography THE visual, not decoration on a background
- Request "calligraphic" or "flowing script" styles for emotional/spiritual content
- The hierarchy: text first, decoration serves text — not the other way around

#### Chinese/Japanese Brush Calligraphy: Breath in Letters

**Key insight:** The universal principle across East Asian calligraphy is that letterforms carry the rhythm of the body that created them. Each stroke is a meditation — breath, body, and spirit aligned.

**Principles:**
- Balance, space, shape, form, and movement are the perceptual elements
- The relationship between filled (ink) and empty (white) space is the highest compositional art
- Each individual stroke is valued for its expressiveness — not just the finished character
- "Calligraphy is sheer life experienced through energy in motion registered as traces on silk or paper"

**Application:**
- When requesting calligraphic or brush-style text: emphasize the "breath" between elements
- "Characters with flowing brush energy, varying stroke weight that shows the rhythm of the hand"
- The filled/empty space principle is universal: always describe the relationship between text and surrounding space

#### Illuminated Manuscripts: Text as Visual Architecture

**Key insight:** Decoration serves navigation and comprehension, not just beauty. Every visual flourish helps the reader find their way through the content.

**Principles:**
- Decorated initials announce text divisions — they are wayfinding, not decoration
- Visual elaboration scales with importance: most important passages get most decoration
- Ruled lines formalize layout relationships between text, illuminations, borders
- Artist and patron collaborated on layout — the relationship between text and image was planned, not accidental

**Application:**
- For infographics and multi-section graphics: use decorative elements functionally, to signal hierarchy
- Larger/more elaborate treatment = more important information
- Every visual element should serve navigation, not just aesthetics
- Layout planning matters: describe the structural relationship before the decorative details

---

### From Psychology of Reading

#### Font Choice Affects Belief and Trust

**Errol Morris / NYT Experiment (2012):**
- 45,000 respondents saw same statement in 6 different fonts
- Baskerville (serif) increased agreement by ~1.5% over Helvetica (sans-serif)
- David Dunning (Cornell): Baskerville's "starchiness" — formality and gravitas — lends believability
- Statistically significant at massive sample size

**Broader research findings:**
- Serif fonts: trigger feelings of tradition, reliability, trustworthiness
- Sans-serif fonts: trigger feelings of modernity, openness, accessibility
- Slightly harder-to-read fonts improve memory retention (disfluency effect) — the brain pays more attention
- Eye-tracking + fMRI: different typefaces activate specific brain areas associated with emotion and trust

**Application:**
- For trust/authority content (health, finance, news): request serif-style typography
- For modern/accessible content (tech, lifestyle, social): request sans-serif
- For content that must be REMEMBERED: slightly unusual/challenging typography can help — but ONLY if the audience will actually engage with it
- In Ideogram: "formal serif typeface" vs. "modern clean sans-serif" in prompt

#### Readability vs. Legibility

**Legibility:** Can you distinguish individual characters? (e → c → o differentiation)
**Readability:** Can you smoothly scan and comprehend lines of text?

Good legibility contributes to readability, but they're not the same. A font can be perfectly legible character-by-character but have poor readability in blocks (bad line spacing, poor word spacing).

**Application:**
- For headlines (1-4 words): prioritize LEGIBILITY — individual character recognition at a glance
- For body text / longer text blocks: prioritize READABILITY — comfortable scanning
- For social media graphics, the HEADLINE is the only text most people will read — optimize for legibility
- In Ideogram: "large, highly legible headline" for short text; "readable body text with good spacing" for longer text

---

## CROSS-DOMAIN PATTERNS

### PATTERN 1: Text-Image Unity
**DOMAINS:** Toulouse-Lautrec (text woven into illustration), Cassandre (geometric DNA shared between letters and images), Polish Poster School (letters as illustration), Arabic calligraphy (text IS the art), illuminated manuscripts (decorated initials as both text and image)
**MECHANISM:** When text and image share the same visual language — same geometry, same color logic, same spatial rules — the viewer processes them as one composition rather than two competing layers. This reduces cognitive load and increases aesthetic coherence.
**APPLICATION:** In Ideogram prompts, describe text as PART of the visual composition rather than as an overlay. "A poster where bold geometric text 'JAZZ NIGHT' shares the angular shapes of the illustrated instruments" vs. "A jazz poster with text 'JAZZ NIGHT' on it." Use DESIGN style_type. Match described text style to described image style.
**FALSIFIABLE:** If eye-tracking studies showed that compositionally integrated text was read more slowly or less accurately than clearly separated text-on-image layouts, this principle would weaken. Evidence of reduced comprehension when text-image boundary is blurred would disprove universality.

### PATTERN 2: Negative Space as Active Element
**DOMAINS:** Brodovitch (white space as compositional force in editorial), Bernbach/"Think Small" (emptiness IS the message), Chinese/Japanese calligraphy (ink-to-white relationship as highest art), magazine cover design (breathing room between elements), Z/F-pattern reading (eyes need clear pathways through content)
**MECHANISM:** The human visual system uses contrast to establish hierarchy. Empty space around an element increases its perceived importance by isolation. Cluttered layouts create equal visual weight everywhere, which means nothing stands out. The brain processes spatial relationships before content — space tells the eye where to go.
**APPLICATION:** In Ideogram prompts, explicitly request negative space: "generous white space around the headline" or "minimal composition, the text floats in open space." For social media graphics, resist the urge to fill every pixel. The prompt template should include a space/breathing instruction. `style_preset=EMOTIONAL_MINIMAL` or `GEO_MINIMALIST` enforce this naturally.
**FALSIFIABLE:** If A/B tests showed that visually dense, fully-filled graphics consistently outperformed spacious layouts in engagement metrics (click-through, recall, sharing), this principle would need revision for the social media context specifically. Platform-specific norms may override the universal principle.

### PATTERN 3: Typography Carries Emotion Before Being Read
**DOMAINS:** Saul Bass (title sequences that create emotional state before content), Kyle Cooper (distressed typography as character expression), Neville Brody (type as emotional language), Polish Poster School (expressive letterforms), Chinese/Japanese calligraphy (breath and spirit in strokes), Errol Morris experiment (font affects belief)
**MECHANISM:** The visual form of letters is processed faster than their semantic content. Shape, weight, texture, and rhythm of letterforms trigger emotional associations (formal/casual, urgent/calm, trustworthy/playful) before the brain decodes the words. This is pre-attentive processing — it happens before conscious reading.
**APPLICATION:** Choose typography style based on the EMOTION you want the viewer to feel, not just the words you want them to read. "Heavy, bold, compressed type reading 'ACT NOW'" for urgency. "Light, elegant serif reading 'Take Your Time'" for calm. The font description in Ideogram prompts should be an emotional instruction, not a technical specification. Match type weight/style to content emotion.
**FALSIFIABLE:** If cognitive research demonstrated that typographic form had no measurable effect on emotional response or message interpretation (purely semantic processing), the emotional function of type would be an aesthetic assumption, not a communication principle.

### PATTERN 4: Single-Word Headlines Beat Sentences
**DOMAINS:** Shepard Fairey ("HOPE", "OBEY" — single words become cultural movements), Saul Bass (one-word film titles as graphic centerpieces), advertising research (Ogilvy: 5x more people read headlines than body copy), magazine covers (one dominant headline drives newsstand sales), social media (8-second attention spans, thumb-scroll behavior)
**MECHANISM:** A single word can be processed in a single fixation (one eye movement). A sentence requires multiple fixations and sequential processing. In fast-scanning contexts (streets, newsstands, social media feeds), the unit of communication that fits in one fixation wins. Additionally, a single word forces the viewer to complete the meaning — the participation creates stronger memory encoding.
**APPLICATION:** Default to the shortest possible text for Ideogram headline generations. One word is ideal, two-three acceptable, four is the upper bound for primary headlines. Longer messages go in subtitle text, which is deliberately smaller and subordinate. Prompt: "Single bold word '[WORD]' dominates the composition. Supporting text smaller below." This also aligns with Ideogram's text accuracy — fewer characters = higher reliability.
**FALSIFIABLE:** If data showed that multi-word headlines consistently produced higher recall/engagement than single words in thumb-scroll social media contexts, this principle would need platform-specific exceptions.

### PATTERN 5: Hierarchy Through Scale Differential
**DOMAINS:** Illuminated manuscripts (decorated initials scaled by importance), magazine design (headline > subhead > body text sizing), Ogilvy (drop caps increase readership 13%), Cassandre (all caps for large-scale legibility), film title design (title card size hierarchy), visual hierarchy research (size = first element noticed)
**MECHANISM:** The human visual system processes larger elements first (they occupy more foveal area during a fixation). Scale differences create an automatic reading order. When elements are similar in size, the eye has no path and wanders — or worse, focuses on the wrong element first. Hierarchy is not optional; if you don't create it deliberately, the viewer creates it randomly.
**APPLICATION:** In every Ideogram prompt with multiple text elements, describe explicit size relationships: "large bold headline, medium-weight subtitle at half the size, small attribution text at the bottom." Never describe two text elements as the same size unless you want them competing for attention. The scale ratio should be at least 2:1 between primary and secondary text. Use pixel-level resolution choices to ensure adequate space for hierarchy (1024x1024 minimum for two text levels, 1536-wide for three).
**FALSIFIABLE:** If research demonstrated that uniform-sized text elements in a composition achieved equal or better comprehension and recall than hierarchically scaled text, this would break. Uniformity-as-design-choice (some modernist work) does exist but is the exception that tests the rule.

### PATTERN 6: Constraint Amplifies Impact
**DOMAINS:** Fairey (3 colors only), Cassandre (geometric reduction to essentials), "Think Small" (mostly empty space), Saul Bass (simplified symbolic forms), Polish Poster School (ambiguity over explicit illustration), hand-lettering tradition (one sign, one message, one craft)
**MECHANISM:** When a designer reduces elements, the remaining elements carry more weight. The viewer's attention is a fixed resource — fewer elements means more attention per element. Additionally, constraint forces creative problem-solving that produces more original solutions than unlimited freedom. The brain finds constrained compositions easier to process (lower cognitive load = higher engagement).
**APPLICATION:** Limit Ideogram prompts to fewer elements rather than more. A graphic with 1 image + 1 headline + 1 color accent will almost always outperform one with 3 images + 4 text blocks + gradients + textures + borders. Use the color_palette parameter with 2-3 colors, not 8. Request "minimal" and "clean" compositions. The fewer elements you request, the more control Ideogram has over each one — and the better each one will render (especially text).
**FALSIFIABLE:** If maximalist, element-dense compositions consistently outperformed minimal ones in the agent's specific use cases (Instagram engagement, click-through, brand recall), this principle would need contextual qualification. Some audiences and platforms reward visual density.

---

## OPERATIONAL QUICK REFERENCE

### Default API Configuration for Text-Heavy Graphics
```python
{
    "prompt": "[structured prompt following templates above]",
    "style_type": "DESIGN",
    "magic_prompt": "OFF",
    "rendering_speed": "QUALITY",  # TURBO for iteration
    "num_images": 4,
    "aspect_ratio": "1x1",  # or 9x16 for Stories/Reels
    "negative_prompt": "blurry text, misspelled words, illegible, low quality"
}
```

### Text Accuracy Checklist (Before Sending to API)
1. Is all intended text in quotation marks?
2. Is text placed early in the prompt?
3. Is casing explicitly stated?
4. Is each text block under 20 characters?
5. Is placement described (top/center/bottom, left/right)?
6. Is `magic_prompt` set to `OFF`?
7. Is `style_type` set to `DESIGN`?
8. Am I generating 4 images for selection?

### Error Correction Pipeline
```
Generate (4 images) → Pick best text rendering → If errors exist:
  → Create mask over error region
  → Edit endpoint with corrected text in prompt
  → If still failing after 2 edit attempts:
    → Generate text-free version
    → Composite text via Remotion/canvas overlay
```

### When to Use Which Endpoint
| Task | Endpoint | Key Setting |
|---|---|---|
| New graphic from scratch | Generate | style_type=DESIGN |
| Fix text in existing image | Edit | mask over text, new prompt |
| Adapt image to new text/style | Remix | image_weight=50-70 |
| Change aspect ratio | Reframe | target resolution |
| Swap background | Replace Background | prompt describes new bg |
| Create overlay element | Generate Transparent | upscale_factor as needed |
| Enhance resolution | Upscale | resemblance=50, detail=50 |
| Reverse-engineer a prompt | Describe | describe_model_version=V_3 |

### Style Selection Decision Tree
```
Is text accuracy the #1 priority?
  YES → style_type=DESIGN, magic_prompt=OFF, no style_preset
  NO → Does this need photorealism?
    YES → style_type=REALISTIC
    NO → Does this need a specific artistic style?
      YES → Use appropriate style_preset from list
      NO → style_type=GENERAL or AUTO
```
