# Texture and Materiality in Screen Design
**Date:** 2026-03-22
**Purpose:** Craft reference for making flat screens feel tactile, dimensional, and real. Feeds design agent and motion agent decisions.
**Method:** 8 targeted web searches across CSS-Tricks, FreeCodeCamp, Josh W. Comeau, ibelick.com, LogRocket, NNG, Kryzalid, IxDF, fffuel.co, Codrops, and design psychology literature.
**Source count:** 8 searches, 80+ result URLs crawled for content.
**Status:** Synthesized from primary sources. Evidence-tagged throughout.

---

## Evidence Tag Key
- [VERIFIED: source] — finding from a named primary source (research, institution, authoritative practitioner)
- [SECONDARY] — finding from practitioner sources, design publications, or industry consensus
- [ASSUMED] — logical inference, not directly observed or cited
- [CONTESTED] — finding where sources disagree or where the evidence is thin

---

## 1. Film Grain: The Full Spectrum

### What Film Grain Actually Is

Film grain is silver halide crystal clusters that remain after chemical development. Larger crystals = faster film stock = coarser grain. The randomness is physical, not algorithmic — no two frames are identical. This randomness is precisely what CSS tries to replicate, because pure digital "perfect" gradients feel inert to the human visual system. [SECONDARY: fffuel.co, ibelick.com]

### Grain Character by Film Format

| Format | Grain Size | Visual Quality | Emotional Signal |
|--------|-----------|----------------|-----------------|
| Super 8 / 16mm | Very coarse, clumping | Raw, unstable, documentary | Urgent, gritty, underground |
| 35mm | Medium, consistent | Cinematic, textured | Classic, authentic, crafted |
| 65mm / IMAX | Fine, barely visible | Luxurious, smooth | Epic, premium, expansive |
| Digital "clean" | None | Perfect, sterile | Modern, cold, corporate |

[SECONDARY: yelzkizi.org grain character guide, premiumbeat.com film grain download notes]

### The Three CSS Grain Implementations

**Method 1: SVG feTurbulence (recommended for most use cases)**

The `feTurbulence` filter generates Perlin or fractal noise natively in the browser. No external image needed.

```svg
<filter id="grain">
  <feTurbulence
    type="fractalNoise"
    baseFrequency="0.65"
    numOctaves="3"
    stitchTiles="stitch"
  />
  <feColorMatrix type="saturate" values="0"/>
</filter>
```

Applied as a CSS background via:
```css
background-image: url("data:image/svg+xml,...");
```

Key parameters and their effect on grain character:
- `baseFrequency` 0.4-0.5 = coarse 16mm-style grain
- `baseFrequency` 0.65-0.75 = medium 35mm-style grain
- `baseFrequency` 0.85-1.0 = fine digital grain
- `numOctaves` 1-2 = smoother, less complex noise
- `numOctaves` 3-4 = more complex, more organic

[VERIFIED: css-tricks.com grainy gradients, freecodecamp.org SVG grain guide, fffuel.co gggrain documentation]

**Method 2: CSS filter + pseudo-element overlay**

A `::before` or `::after` pseudo-element is positioned over the target with:
```css
.grainy::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("noise.svg");
  opacity: 0.08;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

The `mix-blend-mode` is load-bearing. `overlay` preserves both highlight and shadow grain. `multiply` makes grain only visible in light areas. `screen` makes it visible only in dark areas. [SECONDARY: ibelick.com grain technique]

**Method 3: CSS animation (animated grain)**

Film grain is never static — frames differ. Animated grain approaches this by cycling through a noise texture:

```css
@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-2%, -3%); }
  30% { transform: translate(3%, 2%); }
  50% { transform: translate(-1%, 4%); }
  70% { transform: translate(4%, -1%); }
  90% { transform: translate(-3%, 3%); }
}
.film-overlay {
  animation: grain 0.8s steps(1) infinite;
}
```

The `steps(1)` timing function is critical — it creates discrete jumps, not smooth interpolation, which matches how real film frames differ. [SECONDARY: redstapler.co CSS film grain, Viget film grain article]

Grained.js exposes this as a library with parameters: `animate`, `patternWidth`, `patternHeight`, `grainOpacity`, `grainDensity`, `grainWidth`, `grainHeight`. [SECONDARY: sarathsaleem/grained GitHub]

### Performance Reality

SVG feTurbulence is CPU-intensive because it recalculates on every repaint. Counter-strategies:
1. Pre-render to a raster PNG/WebP and use as a static background tile — eliminates runtime cost entirely
2. Limit animated grain to small surface areas, not full-page overlays
3. Canvas-based grain renders once rather than continuously — better for static grain than CSS filters [SECONDARY: fffuel.co performance notes]

### Grain Opacity as Dial

This is the most underused control. Opacity sets how strongly the grain reads:
- 3-5% opacity — almost subliminal, adds texture without visible noise (use for premium/polished)
- 6-10% opacity — visibly grainy, clearly textured (use for cinematic/authentic)
- 12-20% opacity — heavy grain, analog feel (use for gritty/underground)
- 20%+ opacity — distressed, lo-fi (intentional aesthetic choice only)

[ASSUMED: based on standard practitioner ranges from fffuel.co and ibelick.com recommendations]

---

## 2. Glass / Frosted Effects

### The Core Mechanic

Glassmorphism blurs everything behind the element, then layers translucency on top. The CSS property doing the work is `backdrop-filter: blur()`, NOT `filter: blur()`. The distinction matters: `filter` blurs the element itself; `backdrop-filter` blurs whatever is behind it.

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px); /* Safari */
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}
```

[VERIFIED: modern-css.com frosted glass, Josh W. Comeau backdrop-filter article]

### When It Works

Glassmorphism works when:
1. **There is genuine depth behind the panel.** If the background is a solid color, there is nothing to blur — the effect produces nothing. It requires layered content behind it.
2. **The blur radius is proportionate to the element size.** Large panels need more blur (16-24px). Small badges/pills need less (6-10px).
3. **Used selectively.** Best on: nav bars, floating cards, sidebars, modal overlays — components that sit above changing content.
4. **Light source is implied.** The border on the "lit" side of the panel should be brighter than the shadow side.

[SECONDARY: modern-css.com, sliderrevolution.com, theosoti.com]

### When It Fails

Overuse causes compounding degradation:
- If multiple glass panels stack, blur compounds and content behind becomes illegible
- On mobile low-end GPUs, backdrop-filter is expensive and causes jank
- If the panel's background content never changes (static), the blur adds visual cost with no spatial benefit
- When contrast between text and blurred background is insufficient — legibility collapses
- When used on large layout containers instead of floating UI elements — it breaks the visual hierarchy (everything seems at the same depth)

Apple's own Liquid Glass design language (WWDC 2025) adds **glossy surface reflections** and **lighting effects** on top of the basic blur, treating the glass as a physical object that responds to ambient light — not just a translucent layer. [SECONDARY: IxDF glassmorphism guide 2026]

**Rule of thumb:** Maximum 1-2 glass elements visible at once. More than 2 = visual noise, not depth.

### The Border Is Half the Effect

A 1px semi-transparent white border at the top/left edge of a glass panel simulates the edge catching light. Without this, the panel reads as just a blurry, faded box rather than a surface with thickness.

```css
border-top: 1px solid rgba(255, 255, 255, 0.3);
border-left: 1px solid rgba(255, 255, 255, 0.2);
border-bottom: 1px solid rgba(255, 255, 255, 0.05);
border-right: 1px solid rgba(255, 255, 255, 0.05);
```

This is the "thickness illusion" — the asymmetric border implies light hitting the glass from the top-left. [ASSUMED: consistent with light direction principles from neumorphism research]

---

## 3. Surface Materials via CSS

### Metal

Metal's defining properties: directional reflectivity (changes as you move), high specular highlight, anisotropic texture (brushed = linear streaks).

**Brushed metal via repeating gradients:**
```css
background:
  repeating-linear-gradient(
    90deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.03) 2px,
    rgba(255,255,255,0.03) 4px
  ),
  linear-gradient(
    180deg,
    #2a2a2a 0%,
    #3d3d3d 20%,
    #4a4a4a 40%,
    #3a3a3a 60%,
    #2d2d2d 80%,
    #1a1a1a 100%
  );
```

The repeating gradient creates fine horizontal streaks (brushed texture). The underlying gradient creates the tonal variation. [VERIFIED: simurai.com brushed metal technique, css-tricks.com brushed metal gradients]

**Specular highlight technique:**
The key insight is that a specular highlight changes position as the viewing angle changes. CSS can simulate this with `background-attachment: fixed` — as the user scrolls, the gradient position stays fixed to the viewport, making it appear to shift against the element. This is scroll-triggered specular movement without JavaScript. [SECONDARY: ibelick.com metallic effect, speckyboy.com metallic CSS]

**Chrome/polished metal multi-stop gradient:**
```css
background: linear-gradient(
  135deg,
  #c0c0c0 0%,
  #e8e8e8 15%,
  #a0a0a0 30%,
  #f5f5f5 45%,
  #888888 60%,
  #d0d0d0 75%,
  #999999 100%
);
```

The pattern of light → dark → light → dark at irregular intervals reads as reflection. The irregularity is important — even intervals look like stripes, not reflections. [SECONDARY: ibelick.com, eggradients.com metal gradient catalog]

Blend mode overlays using CSS blend modes (luminosity, overlay, hard-light) add complexity that multi-stop gradients alone can't achieve. [SECONDARY: speckyboy.com metallic CSS effects]

### Paper

Paper's defining properties: matte surface (no specular), slight warm/cream base tone, micro-texture (fiber structure), mild edge softness.

**Base approach:**
```css
.paper {
  background-color: #f5f0e8;
  background-image: url("paper-noise.svg");
  background-blend-mode: multiply;
}
```

Two complementary techniques:
1. SVG feTurbulence noise at 3-5% opacity as base texture — this is the "fiber" reading
2. A very slight off-white or warm beige base color — pure white reads as a screen, not paper

**Torn/rough edge illusion:**
```css
clip-path: polygon(
  0% 0%, 100% 0%, 100% 97%,
  98% 99%, 95% 97%, 92% 100%,
  89% 98%, 86% 100%, ...
);
```

Irregular clip-path values along the bottom edge simulate a torn sheet without any image. [SECONDARY: subframe.com CSS paper effects]

### Fabric/Textile

Fabric has woven structure — a perpendicular grid of threads at a scale smaller than the overall element. CSS approximation uses two overlapping repeating gradients at 90 degrees:

```css
background:
  repeating-linear-gradient(
    0deg,
    rgba(0,0,0,0.03) 0px,
    rgba(0,0,0,0.03) 1px,
    transparent 1px,
    transparent 4px
  ),
  repeating-linear-gradient(
    90deg,
    rgba(0,0,0,0.03) 0px,
    rgba(0,0,0,0.03) 1px,
    transparent 1px,
    transparent 4px
  );
```

This creates a subtle grid that reads at a distance as woven texture. [SECONDARY: transparenttextures.com technique analysis, ASSUMED: consistent with repeating gradient grid patterns]

---

## 4. Neumorphism: The Physics of Why It Works

### The Core Mechanic

Neumorphism (Soft UI) simulates a surface where elements are extruded from or pressed into the background. It works by casting two shadows simultaneously from a single implied light source:

```css
.raised-element {
  box-shadow:
    6px 6px 12px rgba(0, 0, 0, 0.15),   /* shadow toward bottom-right */
    -6px -6px 12px rgba(255, 255, 255, 0.7); /* highlight toward top-left */
}
```

The light source is top-left. The dark shadow falls toward bottom-right (away from light). The light shadow falls toward top-left (the lit face of the object). Both shadows are required — removing either one destroys the illusion. [VERIFIED: css-tricks.com neumorphism, LogRocket neumorphism CSS guide]

For an inset (pressed) element, the shadows invert:
```css
.pressed-element {
  box-shadow:
    inset 6px 6px 12px rgba(0, 0, 0, 0.15),
    inset -6px -6px 12px rgba(255, 255, 255, 0.7);
}
```

### Why Consistent Light Direction Is Non-Negotiable

If one element has a light source from top-left and another has it from top-right, the brain registers a physical impossibility. The depth illusion collapses because the scene becomes physically incoherent. The user may not consciously identify the problem, but the interface loses the quality of "believability."

All neumorphic elements on a page must share the same light angle. Convention: top-left is standard. [SECONDARY: neumorphism.io documentation, DEV community neumorphism examples]

### Color Matching Is Critical

The element and its background must be the same (or nearly the same) color. Neumorphism only works when the element appears to grow from the surface — it cannot work on top of a contrasting background. If the background is `#e0e0e0`, the element must also be `#e0e0e0`.

The shadows are what differentiate the element from the background, not the fill color. [VERIFIED: LogRocket neumorphism guide, css-tricks.com neumorphism]

### When Neumorphism Fails

**Accessibility:** Low contrast between the element and its background is inherent to the design. Light gray on light gray fails WCAG contrast ratios by definition. The effect requires softness — and softness means low contrast. There is no full fix for this within the style. Recent iterations (2025) use higher contrast shadow values and more vivid accent colors to improve accessibility while retaining the physical depth signal. [SECONDARY: bighuman.com neumorphism guide 2026, cccreative.design UI trends comparison]

**Dark backgrounds:** Dark neumorphism requires inverting the logic — the light shadow becomes a nearly-invisible detail. The effect weakens significantly at dark values. Some dark-mode neumorphism implementations use a slight color shift (desaturated warm tone) to replace the white highlight component.

**Interactive affordance:** Raised elements look pressable, but "flat" interactive elements do not. Users may not identify which elements are interactive vs decorative. [SECONDARY: bighuman.com]

---

## 5. Noise and Dithering: Controlled Randomness

### The Problem Being Solved

Digital rendering produces mathematically perfect gradients. Human vision evolved to process natural environments where perfect gradients do not exist — light scatters, surfaces vary, materials have micro-imperfections. A perfectly smooth gradient is a signal that something is artificial. Adding controlled noise breaks this signal.

Dithering originated as a technique to smooth visible color banding on displays with limited color depth. In modern web design, it is applied aesthetically — not to fix banding, but to create the impression of depth and materiality in gradients that are smooth enough not to band. [VERIFIED: blog.maximeheckel.com dithering article, Wikipedia dither, Codrops dithering shader 2025]

### Bayer Dithering vs Perlin Noise — The Difference

| Type | Character | Aesthetic |
|------|-----------|-----------|
| Bayer (ordered) | Regular grid pattern, geometric | Retro, pixel-art, lo-fi game aesthetic |
| Perlin noise | Organic, flowing randomness | Natural, cinematic, film grain |
| Fractal noise | Multi-scale complexity | Highly organic, cloud-like |
| White noise (random) | Pure random, no structure | Static, TV noise, harsh |

Perlin and fractal noise (via `feTurbulence`) produce the most natural film grain feel. Bayer dithering is deliberate retro. White noise is rarely desirable. [VERIFIED: Codrops Bayer dithering interactive guide 2025, maximeheckel.com dithering and retro shading]

### Applying Dithering to Gradients

The technique: apply Perlin noise on top of a CSS gradient with `mix-blend-mode: overlay` or `multiply`. The noise disrupts the gradient's smooth edges, making them appear to dissolve into each other rather than transition cleanly. The result is a gradient that reads as dimensional — it has surface variance, not just tonal variance.

```css
.gradient-with-dither {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
}
.gradient-with-dither::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("perlin-noise.svg");
  opacity: 0.06;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

[SECONDARY: css-tricks.com grainy gradients, frontendmasters.com grainy gradients]

---

## 6. Light Interaction: How Surfaces Should Respond

### The Three Types of Light Response

Every surface interacts with light in three ways simultaneously:

| Light Type | CSS Approximation | Where It Appears |
|------------|-------------------|-----------------|
| Specular (direct) | Multi-stop gradient, highlight pseudo-element | Top-left edge of raised elements, center of domed surfaces |
| Diffuse (scattered) | Base gradient with tonal variation | Across the whole surface |
| Ambient occlusion | Dark shadow in corners/crevices where surfaces meet | Under elements, in corners, where elements overlap |

[SECONDARY: archivinci.com ambient occlusion, robbowen.digital CSS blend mode shaders]

### Ambient Occlusion in CSS

Ambient occlusion (AO) is the darkening that occurs in corners, creases, and tight spaces where ambient light cannot reach. In 3D rendering it is computed. In CSS it is approximated with multiple layered shadows.

For text with AO depth:
```css
.text-with-ao {
  text-shadow:
    0 1px 0 rgba(0,0,0,0.4),
    0 2px 0 rgba(0,0,0,0.3),
    0 4px 4px rgba(0,0,0,0.2),
    0 8px 12px rgba(0,0,0,0.1);
}
```

Each shadow layer adds a component of the light diffusion. Tight shadows handle the sharp edge; soft distant shadows handle the ambient spread. [SECONDARY: freefrontend.com CSS text shadow effects, pixcode.io CSS shadow guide]

For elements (cards, buttons):
```css
.card-with-ao {
  box-shadow:
    0 1px 2px rgba(0,0,0,0.3),    /* contact shadow — tight */
    0 4px 8px rgba(0,0,0,0.15),   /* near field — diffusing */
    0 12px 24px rgba(0,0,0,0.08); /* far field — ambient spread */
}
```

The three-layer shadow is always more convincing than a single-layer shadow because it matches how real shadows behave: dark near the object, fading as distance increases. [SECONDARY: devtoolbox.dedyn.io CSS box-shadow guide]

### Specular Movement on Scroll

An underused technique: `background-attachment: fixed` locks a gradient to the viewport coordinate system rather than the element's coordinate system. As an element scrolls past a fixed gradient, the gradient appears to move across it — simulating how a specular highlight changes position as your viewing angle shifts.

```css
.metallic-surface {
  background-image: linear-gradient(
    135deg,
    transparent 40%,
    rgba(255,255,255,0.15) 50%,
    transparent 60%
  );
  background-attachment: fixed;
}
```

[SECONDARY: ibelick.com metallic effect]

---

## 7. Texture as Emotional Signal

### The Evidence Base

Research from the University of British Columbia found that participants holding a rough board judged social interactions as more difficult than participants holding a smooth board. The physical sensation of texture activates the same neural pathways as visual texture. The limbic system processes texture signals before conscious analysis. [VERIFIED: texture psychology research, UBC study as cited in downloadartwork.com and emkaan.com design psychology sources]

### The Texture-Emotion Map

| Texture | Primary Emotion | Secondary | Design Use Case |
|---------|----------------|-----------|-----------------|
| Smooth / polished | Calm, clarity, no threat | Precision, corporate | Premium tools, medical, finance |
| Rough / coarse | Grounded, resilient, authentic | Earthy, natural | Wellness, outdoor, craft |
| Grainy / gritty | Tension, urgency, psychological struggle | Raw, underground | Music, fashion, documentary |
| Matte / flat | Modern, serious, deliberate | Clean, focused | Tech, editorial, minimalist |
| Reflective / glossy | Aspirational, expansive | Luxurious, cold | Luxury goods, high-end consumer |
| Soft / fabric | Warm, intimate, personal | Approachable | Health companions, mental wellness |

[VERIFIED: downloadartwork.com texture psychology, kpfilms.com surface design psychology, emkaan.com material emotion research]

### Texture and Perceived Size

Smooth/reflective textures make spaces feel larger by bouncing light and creating visual expansion. Rough/matte textures create intimacy by absorbing light and visually compressing space. This applies to UI: a smooth dark gradient feels expansive; a grainy rough surface feels contained and close. [SECONDARY: kpfilms.com surface design impact]

### The Grain-Authenticity Signal

Grain specifically communicates "not manufactured" — it is the visual signature of physical processes (film, print, hand-made). In a context dominated by perfect digital rendering, grain functions as an authenticity marker. The signal: this was created by a person, not generated by a system.

This is why high-end brands, artisan products, and storytelling-oriented companies have reintroduced grain in 2025. It signals handcraft and intention, not technical limitation. [SECONDARY: kryzalid.net skeuomorphism 2025 comeback, sellnship.in real-world textures in digital design]

---

## 8. The Uncanny Valley of Texture

### Where the Valley Is

The original uncanny valley (Mori, 1970) describes how human-like robots cause discomfort as they approach-but-don't-reach human appearance. The same principle applies to digital texture: as an interface approaches-but-doesn't-achieve the fidelity of physical objects, it creates discomfort rather than immersion.

Specific failure modes:
- **Too literal:** A calendar that looks exactly like paper but scrolls digitally feels like a bad costume. The behavior is wrong for the appearance. [SECONDARY: cassidyjames.com uncanny valley curve]
- **Inconsistent physics:** Shadows from two different light sources on the same surface. Elements with different material behaviors in the same UI layer.
- **Texture without function:** Applying a leather texture to a button that should communicate "pressability" — but a leather button has no cultural analog. The texture confuses rather than cues.
- **High effort, low resolution:** A detailed wood-grain texture that pixelates on high-DPI screens. The attempt at realism reveals the limitation of the medium.

### The 2025 Sweet Spot: Suggestion, Not Simulation

The current consensus across practitioners in 2025 is **suggestion over simulation**. The goal is not to make a screen look like paper or glass — it is to evoke the emotional associations of those materials at low intensity.

This resolves as three principles:

**Principle 1: Function follows texture.** Texture is only credible when the element's behavior matches its surface suggestion. A glass card that moves fluidly when hovered = glass. A glass card that snaps rigidly = not glass.

**Principle 2: One material per layer.** Mixing material metaphors in the same visual layer creates incoherence. Glass panel on a metal background on a paper-textured page = three competing physical realities. One material per depth level.

**Principle 3: Subtlety increases believability.** Paradoxically, less texture reads as more real. A 5% opacity grain overlay is more convincing than 20% because the viewer's imagination fills in the rest. Overdone texture announces "I am trying to look like something I am not." [SECONDARY: justinmind.com skeuomorphic design guide, think.design skeuomorphic UX, nngroup.com skeuomorphism]

### Neo-Skeuomorphism 2025: The Current Synthesis

The term "neo-skeuomorphism" is now common in 2025 design discourse. It combines:
- **Modern flat behavior** (responsive, accessible, fast)
- **Physical material suggestion** (subtle shadows, surface texture, implied light source)
- **Purposeful texture** (applied only where it communicates interaction, hierarchy, or emotional tone)

Apple's Liquid Glass (WWDC 2025) is the highest-visibility example: blur + transparency + glossy surface reflection + lighting response. It is not flat, not aggressively skeuomorphic — it is material suggestion at a system level. [SECONDARY: IxDF glassmorphism 2026, cccreative.design neumorphism vs glassmorphism]

---

## Implementation Priority Stack

For our specific use case (dark health calculator interface, V25 design, cinematic tone):

| Priority | Technique | Implementation Effort | Emotional Return |
|----------|-----------|----------------------|-----------------|
| 1 | SVG grain overlay at 5-8% opacity | Low | HIGH — shifts from digital to cinematic immediately |
| 2 | Multi-layer box-shadow (3 layers) | Low | HIGH — makes cards feel physical not flat |
| 3 | Asymmetric border on glass panels | Low | MEDIUM — adds thickness illusion |
| 4 | Metal gradient on accent elements | Medium | MEDIUM — premium signal on specific elements |
| 5 | Animated grain on hero section | Medium | HIGH — cinematic quality for brand film feel |
| 6 | backdrop-filter blur on floating UI | Medium | MEDIUM — depth when layered content exists behind |
| 7 | Fixed-attachment specular on scroll | Low | MEDIUM — subtle material behavior on metal surfaces |
| 8 | feTurbulence parameter tuning per section | High | MEDIUM — grain character variation by page section |

---

## Falsifiability

| Finding | What Would Disprove It |
|---------|------------------------|
| "Grain reads as authenticity signal" | If A/B testing shows grain reduces trust scores in health/medical contexts (clean = clinical = trusted) |
| "5% grain opacity is more convincing than 20%" | If user testing shows higher opacity grain increases perceived quality in gritty/authentic brand contexts |
| "One glass element per view" | If Apple's Liquid Glass system (multi-layer glass) produces no UX degradation at scale |
| "Consistent light direction is required for believability" | If users cannot detect inconsistent light direction in neumorphic UIs without being primed to look |
| "Texture is processed before conscious analysis" | If neuroimaging studies fail to replicate the limbic system finding in digital (vs physical) texture contexts |

---

## Shared Assumptions to Flag

1. The research on physical texture psychology (UBC study) is assumed to transfer to visual/digital texture. The UBC study used physical boards, not screens. Transfer is plausible but not proven. [ASSUMED]

2. "Suggestion over simulation" as the 2025 sweet spot is practitioner consensus, not user research consensus. Actual user preference data on texture intensity in digital UI is sparse. [SECONDARY, not VERIFIED]

3. The CSS implementations documented here are drawn from practitioner sources and CSS specification behavior, not performance benchmarks. Real-world performance varies by GPU, browser version, and element count. [ASSUMED: verify against actual GPU performance budgets before shipping animated grain at scale]

---

## Sources

- [Grainy Gradients — CSS-Tricks](https://css-tricks.com/grainy-gradients/)
- [How to Create Grainy CSS Backgrounds Using SVG Filters — FreeCodeCamp](https://www.freecodecamp.org/news/grainy-css-backgrounds-using-svg-filters/)
- [gggrain: SVG Grainy Gradient Generator — fffuel.co](https://www.fffuel.co/gggrain/)
- [Create Grainy Backgrounds with CSS — ibelick.com](https://ibelick.com/blog/create-grainy-backgrounds-with-css)
- [Grainy Gradients — Frontend Masters Blog](https://frontendmasters.com/blog/grainy-gradients/)
- [Generating Animated Noise Texture — grained.js](https://sarathsaleem.github.io/grained/)
- [CSS Film Grain Effect — Red Stapler](https://redstapler.co/css-film-grain-effect/)
- [Creating a Film Grain Effect with CSS3 — Viget](https://www.viget.com/articles/film-grain-effect)
- [Next-level Frosted Glass with backdrop-filter — Josh W. Comeau](https://www.joshwcomeau.com/css/backdrop-filter/)
- [Glassmorphism — IxDF 2026](https://ixdf.org/literature/topics/glassmorphism)
- [What Is Glassmorphism — Ramotion Agency](https://www.ramotion.com/blog/what-is-glassmorphism/)
- [Creating a Metallic Effect with CSS — ibelick.com](https://ibelick.com/blog/creating-metallic-effect-with-css)
- [Brushed Metal — Simurai](https://simurai.com/lab/2011/08/21/brushed-metal)
- [Brushed Metal with CSS Gradients — CSS-Tricks](https://css-tricks.com/brushed-metal-with-css-gradients/)
- [Holograms, Light-Leaks and CSS-only Shaders — Robb Owen](https://robbowen.digital/wrote-about/css-blend-mode-shaders/)
- [Understanding Neumorphism in CSS — LogRocket](https://blog.logrocket.com/understanding-neumorphism-css/)
- [Neumorphism and CSS — CSS-Tricks](https://css-tricks.com/neumorphism-and-css/)
- [Neumorphism CSS Generator — neumorphism.io](https://neumorphism.io/)
- [What Is Neumorphism in UI Design — BigHuman 2026](https://www.bighuman.com/blog/neumorphism)
- [The Art of Dithering and Retro Shading for the Web — Maxime Heckel](https://blog.maximeheckel.com/posts/the-art-of-dithering-and-retro-shading-web/)
- [Interactive WebGL Backgrounds: Bayer Dithering — Codrops 2025](https://tympanus.net/codrops/2025/07/30/interactive-webgl-backgrounds-a-quick-guide-to-bayer-dithering/)
- [Building a Real-Time Dithering Shader — Codrops 2025](https://tympanus.net/codrops/2025/06/04/building-a-real-time-dithering-shader/)
- [Texture Psychology in Art — downloadartwork.com](https://www.downloadartwork.com/texture-psychology-art-mood/)
- [The Psychology of Texture: Surface Design Impacts Space — kpfilms.com](https://www.kpfilms.com/en/news-events/our-stories/the-psychology-of-texture-how-surface-design-impacts-space-perception)
- [The Power of Texture: Material Choices Affect Emotions — Emkaan](https://emkaan.com/the-power-of-texture-how-material-choices-affect-emotions)
- [Skeuomorphism: An Unexpected Comeback in 2025 — Kryzalid](https://kryzalid.net/en/web-marketing-blog/skeuomorphism-an-unexpected-comeback-in-2025/)
- [Skeuomorphism Returns: Real-World Textures in Digital Design — SellnShip](https://sellnship.in/skeuomorphism-returns-real-world-textures-in-digital-design/)
- [Skeuomorphism — Nielsen Norman Group](https://www.nngroup.com/articles/skeuomorphism/)
- [The Uncanny Valley Curve — Cassidy James](https://cassidyjames.com/blog/uncanny-valley-curve/)
- [Glassmorphism vs Claymorphism vs Skeuomorphism 2025 — Medium Bootcamp](https://medium.com/design-bootcamp/glassmorphism-vs-claymorphism-vs-skeuomorphism-2025-ui-design-guide-e639ff73b389)
- [UI Trends: Neumorphism vs Glassmorphism vs Neubrutalism — CCC Creative](https://www.cccreative.design/blogs/differences-in-ui-design-trends-neumorphism-glassmorphism-and-neubrutalism)
- [Design Trends 2025: Glassmorphism, Neumorphism — Contra](https://contra.com/p/PYkeMOc7-design-trends-2025-glassmorphism-neumorphism-and-styles-you-need-to-know)
- [CSS Paper Effects — Subframe](https://www.subframe.com/tips/css-paper-effect-examples)
- [Transparent Textures — transparenttextures.com](https://www.transparenttextures.com/)
- [CSS Box-Shadow Complete Guide — DevToolbox](https://devtoolbox.dedyn.io/blog/css-box-shadow-complete-guide)
- [What Are the Top Web Design Trends of 2025 — TBH Creative](https://www.tbhcreative.com/blog/web-design-trends-of-2025/)
