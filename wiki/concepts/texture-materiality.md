# Texture and Materiality

> Film grain, glassmorphism, noise layers, neumorphism, surface materials, and tactile digital surfaces. How visual texture communicates emotion, depth, and authenticity on flat screens.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### Film Grain: Character and Implementation

Film grain is silver halide crystal clusters from chemical development. Larger crystals = faster film stock = coarser grain. The randomness is physical, not algorithmic -- no two frames are identical. Digital gradients feel inert to the human visual system because perfect smoothness is a signal of artificiality. [VERIFIED -- fffuel.co, ibelick.com]

**Grain character by film format:**

| Format | Grain Size | Emotional Signal |
|--------|-----------|-----------------|
| Super 8 / 16mm | Very coarse, clumping | Urgent, gritty, underground |
| 35mm | Medium, consistent | Classic, authentic, crafted |
| 65mm / IMAX | Fine, barely visible | Epic, premium, expansive |
| Digital "clean" | None | Modern, cold, corporate |

[VERIFIED -- yelzkizi.org grain guide, premiumbeat.com]

**Three CSS grain implementations:**

1. **SVG feTurbulence (recommended):** Generates Perlin/fractal noise natively. `baseFrequency` 0.4-0.5 = coarse 16mm grain, 0.65-0.75 = medium 35mm, 0.85-1.0 = fine digital. `numOctaves` 1-2 = smoother, 3-4 = more organic. [VERIFIED -- css-tricks.com, freecodecamp.org, fffuel.co]

2. **CSS filter + pseudo-element overlay:** `::before` with noise image, controlled by `mix-blend-mode`. `overlay` preserves highlight and shadow grain. `multiply` = grain in light areas only. `screen` = grain in dark areas only. [VERIFIED -- ibelick.com]

3. **CSS animated grain:** Cycling through noise texture positions with `steps(1)` timing (discrete jumps, not smooth interpolation) matches how real film frames differ. [VERIFIED -- redstapler.co, Viget]

**Performance reality:** SVG feTurbulence is CPU-intensive, recalculates on every repaint. Counter-strategies: pre-render to raster PNG/WebP for static grain (eliminates runtime cost), limit animated grain to small surfaces, use Canvas for one-time render. [VERIFIED -- fffuel.co]

**Grain opacity as dial:**

| Opacity | Character | Use Case |
|---------|-----------|----------|
| 3-5% | Almost subliminal | Premium, polished |
| 6-10% | Visibly grainy, textured | Cinematic, authentic |
| 12-20% | Heavy grain, analog feel | Gritty, underground |
| 20%+ | Distressed, lo-fi | Intentional aesthetic only |

[THEORETICAL -- based on practitioner ranges from fffuel.co and ibelick.com]

### Glassmorphism

Blurs everything behind an element with `backdrop-filter: blur()`, layering translucency on top. NOT `filter: blur()` (which blurs the element itself). [VERIFIED -- modern-css.com, Josh W. Comeau]

**When it works:** (1) genuine depth behind the panel (solid color background = nothing to blur), (2) blur radius proportionate to element size (large panels 16-24px, small badges 6-10px), (3) used selectively (nav bars, floating cards, modal overlays), (4) implied light source via asymmetric border. [VERIFIED -- modern-css.com, sliderrevolution.com]

**When it fails:** Multiple glass panels stacking (blur compounds, content illegible), mobile low-end GPUs (backdrop-filter expensive), static background content (blur adds cost with no spatial benefit), insufficient text-to-background contrast, large layout containers instead of floating elements. [VERIFIED]

**Rule of thumb:** Maximum 1-2 glass elements visible at once. More = visual noise, not depth. [VERIFIED]

**The border is half the effect:** A 1px semi-transparent white border at top/left simulates edge catching light. Without this, the panel reads as a faded box, not a surface with thickness. Asymmetric border (brighter top-left, darker bottom-right) implies light from top-left. [THEORETICAL -- consistent with light direction principles]

**Apple's Liquid Glass (WWDC 2025):** Adds glossy surface reflections and lighting effects on top of basic blur, treating glass as a physical object responding to ambient light. [VERIFIED -- IxDF glassmorphism guide 2026]

### Surface Materials via CSS

**Brushed metal:** Repeating linear gradients for fine directional streaks + underlying gradient for tonal variation. Specular highlight simulated with `background-attachment: fixed` -- as user scrolls, gradient position stays viewport-locked, creating apparent specular movement. [VERIFIED -- simurai.com, css-tricks.com]

**Chrome/polished metal:** Multi-stop gradient with irregular intervals between light and dark values. Irregularity reads as reflection; even intervals read as stripes. Blend mode overlays (luminosity, overlay, hard-light) add complexity. [VERIFIED -- ibelick.com, eggradients.com]

**Paper:** Matte surface, slight warm/cream base tone, micro-texture via feTurbulence noise at 3-5% opacity. Pure white reads as screen, not paper. Torn edges via irregular polygon clip-path along bottom edge. [VERIFIED -- subframe.com]

**Fabric/textile:** Two overlapping repeating gradients at 90 degrees create a subtle grid that reads as woven texture at distance. [VERIFIED -- transparenttextures.com]

### Neumorphism

Simulates surface where elements are extruded from or pressed into background. Two shadows simultaneously from single implied light source: dark shadow toward bottom-right (away from light), light shadow toward top-left (lit face). Both shadows required -- removing either destroys the illusion. [VERIFIED -- css-tricks.com, LogRocket]

**Non-negotiable rules:** All neumorphic elements must share the same light angle (convention: top-left). Element and background must be same or nearly same color (shadows differentiate, not fill). [VERIFIED]

**Failure modes:** Low contrast inherent to the design (fails WCAG), dark backgrounds weaken the effect significantly, unclear interactive affordance (users cannot distinguish interactive from decorative). [VERIFIED -- bighuman.com, nngroup.com]

### Noise and Dithering

Digital gradients are mathematically perfect. Human vision evolved processing natural environments where perfect gradients don't exist. Adding controlled noise breaks the artificial signal. [VERIFIED -- maximeheckel.com, Wikipedia]

| Noise Type | Character | Aesthetic |
|-----------|-----------|-----------|
| Bayer (ordered) | Regular grid, geometric | Retro, pixel-art, lo-fi |
| Perlin | Organic, flowing randomness | Natural, cinematic, film grain |
| Fractal | Multi-scale complexity | Highly organic, cloud-like |
| White noise | Pure random, no structure | Static, harsh -- rarely desirable |

[VERIFIED -- Codrops Bayer dithering guide, maximeheckel.com]

Applying Perlin noise on top of a CSS gradient with `mix-blend-mode: overlay` disrupts the gradient's smooth transitions, making them appear to dissolve into each other -- dimensional rather than just tonal. [VERIFIED -- css-tricks.com, frontendmasters.com]

### Light Interaction: Three Types

Every surface responds to light in three simultaneous ways:

| Light Type | CSS Approximation | Where It Appears |
|-----------|-------------------|-----------------|
| Specular (direct) | Multi-stop gradient, highlight pseudo-element | Top-left edge, center of domed surfaces |
| Diffuse (scattered) | Base gradient with tonal variation | Across whole surface |
| Ambient occlusion | Dark shadow in corners/crevices | Under elements, where surfaces meet |

[VERIFIED -- archivinci.com, robbowen.digital]

**Three-layer box-shadow** (contact + near-field + far-field) is always more convincing than single-layer because it matches how real shadows behave: dark near the object, fading with distance. [VERIFIED -- devtoolbox.dedyn.io]

### Texture as Emotional Signal

Research from University of British Columbia: participants holding a rough board judged social interactions as more difficult than those holding a smooth board. Physical texture sensation activates the same neural pathways as visual texture. Limbic system processes texture signals before conscious analysis. [VERIFIED -- UBC study cited in downloadartwork.com, emkaan.com]

| Texture | Primary Emotion | Design Use Case |
|---------|----------------|-----------------|
| Smooth/polished | Calm, clarity | Premium tools, medical, finance |
| Rough/coarse | Grounded, resilient | Wellness, outdoor, craft |
| Grainy/gritty | Tension, urgency | Music, fashion, documentary |
| Matte/flat | Modern, serious | Tech, editorial, minimalist |
| Reflective/glossy | Aspirational, expansive | Luxury goods, high-end consumer |
| Soft/fabric | Warm, intimate | Health companions, mental wellness |

[VERIFIED -- downloadartwork.com, kpfilms.com, emkaan.com]

**Grain as authenticity signal:** Grain communicates "not manufactured" -- the visual signature of physical processes. In a context dominated by perfect digital rendering, grain functions as an authenticity marker. High-end brands, artisan products, and storytelling companies have reintroduced grain in 2025. [VERIFIED -- kryzalid.net, sellnship.in]

### The Uncanny Valley of Texture

As an interface approaches but doesn't achieve the fidelity of physical objects, it creates discomfort. Failure modes: too literal (calendar that looks like paper but scrolls digitally), inconsistent physics (shadows from two light sources), texture without function (leather on a button with no cultural analog), high effort at low resolution (wood-grain that pixelates on HiDPI). [VERIFIED -- cassidyjames.com]

### The 2025 Sweet Spot: Suggestion, Not Simulation

Current practitioner consensus: suggest, don't simulate. Three principles:

1. **Function follows texture** -- texture is credible only when behavior matches surface suggestion. Glass card that moves fluidly = glass. Glass card that snaps rigidly = not glass. [VERIFIED]

2. **One material per layer** -- mixing material metaphors in the same visual layer creates incoherence. Glass on metal on paper = three competing physical realities. [VERIFIED]

3. **Subtlety increases believability** -- 5% opacity grain overlay is more convincing than 20% because the viewer's imagination fills in the rest. Overdone texture announces "I am trying to look like something I am not." [VERIFIED -- justinmind.com, nngroup.com]

---

## Operational Rules

1. **When adding grain to any surface, start at 5% opacity and increase only if the context demands it** -- because subtlety increases believability, and overdone grain announces artificiality rather than authenticity.

2. **When using glassmorphism, limit to 1-2 glass elements visible simultaneously** -- because stacking glass layers compounds blur, degrades legibility, and collapses the depth hierarchy.

3. **When building any surface with implied light, maintain consistent light direction across all elements** -- because inconsistent light sources create physical impossibility that the brain registers as "wrong" even without conscious identification.

4. **When adding box-shadow for depth, always use 3 layers (contact + near + far)** -- because single-layer shadows read as flat decoration while three-layer shadows match real shadow behavior.

5. **When choosing texture for health/medical context, use smooth + subtle grain (5%) not rough/gritty** -- because smooth textures signal calm and clarity, while gritty textures signal tension and urgency, which is counterproductive in clinical contexts.

6. **When the grain must be animated, limit animated grain to small surfaces and pre-render to raster for large areas** -- because SVG feTurbulence recalculates on every repaint and is CPU-intensive at scale.

7. **When mixing material metaphors, use one material per depth layer maximum** -- because glass on metal on paper in the same layer creates three competing physical realities that destroy coherence.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/animation_texture_materiality.md` | Film grain implementations, glassmorphism, surface materials (metal/paper/fabric), neumorphism, noise/dithering, light interaction, texture-emotion psychology, uncanny valley, neo-skeuomorphism |

---

## Related Concepts

- [[particle-procedural-effects]] -- shares noise-generation techniques (feTurbulence, Perlin noise) with grain implementations
- [[squash-stretch-weight]] -- motion weight and visual texture weight work together to create coherent physical presence
- [[motion-curves-easing]] -- material behavior (glass fluidity, metal rigidity) must match the motion curves applied to that element

---

## Deep Reference

- **When** choosing SVG grain `baseFrequency` to match a specific film stock look → **read** `research-data/animation_texture_materiality.md` §1 (Film Grain) **for** the frequency-to-stock mapping (0.4-0.5 = coarse 16mm, 0.65-0.75 = medium 35mm, 0.85-1.0 = fine digital), `numOctaves` complexity control, and three CSS implementation methods (SVG feTurbulence, pseudo-element overlay at opacity 0.08, canvas noise)
- **When** deciding between neumorphism and glassmorphism for a UI element → **read** `research-data/animation_texture_materiality.md` §3-4 (Neumorphism, Glassmorphism) **for** the neumorphism dual-shadow formula (`light-shadow: -offset, dark-shadow: +offset`), glassmorphism backdrop-filter parameters (`blur(12-20px)`, `background: rgba(255,255,255,0.05-0.15)`), and the one-glass-element-per-view readability rule
- **When** choosing how much texture to apply and the result looks either too sterile or too heavy → **read** `research-data/animation_texture_materiality.md` §7 (Texture-Emotion Psychology) **for** the UBC rough-vs-smooth study findings, the "suggestion over simulation" principle, and the texture intensity spectrum from clinical-clean to tactile-rich with use-case mapping
- **When** implementing noise on CSS gradients to break banding → **read** `research-data/animation_texture_materiality.md` §5 (Noise and Dithering) **for** four noise types (Bayer/Perlin/Fractal/White) with aesthetic mapping, Perlin + `mix-blend-mode: overlay` gradient technique, and Bayer dithering for intentional retro/lo-fi aesthetic

---

## Open Questions

- UBC texture psychology study used physical boards, not screens -- transfer to digital visual texture is plausible but not proven
- "Suggestion over simulation" as the sweet spot is practitioner consensus, not user research consensus -- actual preference data on texture intensity is sparse
- Whether grain reduces trust in health/medical contexts (clean = clinical = trusted) has not been A/B tested
- Apple's Liquid Glass multi-layer system may disprove the "one glass element per view" rule -- if no UX degradation at scale, the rule needs updating
- CSS implementation performance varies by GPU, browser version, and element count -- verify against actual devices before shipping animated grain
