# Cinematography Lighting Design for Web/Screen
**Date:** 2026-03-22
**Research method:** 8 web searches across cinematography, CSS implementation, and UI design sources
**Purpose:** Feed design agent and motion agent. Every principle must map to a CSS/animation implementation.

---

## Evidence Tags

[VERIFIED] = confirmed across 2+ independent sources
[SOURCE] = single source, not yet corroborated
[LLM-ESTIMATED] = reasoned from principles, no direct source
[ASSUMED] = inference from analogous domain

---

## 1. Three-Point Lighting — The Foundational System

### The Film System [VERIFIED]

Three-point lighting is the standard illumination method in film, photography, video, and 3D rendering. It uses three distinct light sources, each with a specific role.

| Light | Position | Role | CSS Analog |
|-------|----------|------|-----------|
| Key light | 45 degrees to subject, primary side | Principal illuminator. Sets overall exposure, direction, and mood. Casts the dominant shadows. | `box-shadow: -8px 8px 24px rgba(0,0,0,0.6)` (offset = direction) |
| Fill light | Opposite side from key, lower angle | Reduces or eliminates shadows from key. Softens contrast. Usually 50% or less of key brightness. | `box-shadow: 4px -2px 16px rgba(0,0,0,0.2)` (opposite offset, lower opacity) |
| Rim/back light | Behind subject, aimed at back of head/shoulders | Creates bright edge outline. Separates subject from background. Adds depth and three-dimensionality. | `box-shadow: 0 0 12px 2px rgba(255,255,255,0.15)` (inset=false, spread, low opacity) or `border: 1px solid rgba(255,255,255,0.12)` |

### The CSS Mapping Rule [LLM-ESTIMATED]

The `box-shadow` offset direction is the light source position in reverse. If the light is above-left, the shadow falls below-right:

```css
/* Light source: upper-left (natural, neutral) */
box-shadow:
  8px 12px 32px rgba(0,0,0,0.5),   /* key shadow — dark, directional */
  -4px -4px 16px rgba(0,0,0,0.15); /* fill — opposite, much softer */
```

The global light source must be consistent across all elements on a page. Material Design codifies this: key lights create directional shadows, ambient light creates soft omnidirectional shadows. Mixing directions reads as incoherent. [VERIFIED — multiple CSS shadow sources]

### Key-to-Fill Ratio [VERIFIED]

The ratio between key and fill determines the scene's feel:

| Ratio | Name | Mood | UI Equivalent |
|-------|------|------|--------------|
| 1:1 | Flat | Bright, commercial, safe | High-key UI — equal shadow on all sides |
| 2:1 | Slight | Broadcast, interview, clean | Standard card elevation |
| 4:1 | Moderate | Drama, narrative, presence | Hero sections, spotlight cards |
| 8:1+ | Heavy | Noir, mystery, intensity | Chiaroscuro UI — deep dark bg, single illuminated element |

In CSS terms: `box-shadow` opacity ratio between the key shadow and fill shadow. Key at `rgba(0,0,0,0.6)`, fill at `rgba(0,0,0,0.15)` = ~4:1 ratio.

---

## 2. High-Key vs Low-Key Lighting — When to Use Each

### Definitions [VERIFIED]

**High-key lighting:** Reduces contrast between shadows and highlights. Minimal shadow. Bright, flat, even. Often multiple light sources from different angles to eliminate shadow.

**Low-key lighting:** High contrast between light and dark areas. Majority of the scene is in shadow. One dominant light source. Deep, dramatic, selective.

### Emotional Register [VERIFIED]

| Approach | Emotions | Content Fit | Examples |
|----------|----------|-------------|---------|
| High-key | Upbeat, safe, open, clean, trustworthy | Commercials, children's content, interviews, product shots, "truth" | Duolingo, kids apps, food brands, medical reference |
| Low-key | Mystery, tension, drama, sensuality, intensity, noir | Thriller, noir, cinematic, luxury, horror, documentary | Netflix hero, Spotify, premium portfolio sites |

### UI Translation [VERIFIED + LLM-ESTIMATED]

**High-key UI:**
- White or very light backgrounds
- Minimal shadow elevation (1-4dp in Material Design)
- Accent colors are muted or pastels
- No strong directional lighting
- Readability optimized — nothing hidden

**Low-key UI:**
- Dark backgrounds (#121212, #0D0D0D — not pure #000000)
- Strong spotlight behavior: key elements are bright, surroundings are dark
- Glows as the primary depth cue (not shadows)
- High contrast accent colors (but desaturated — avoid saturation vibration against dark surfaces)
- Information reveals progressively from dark

**The V25 calculator design is low-key.** Full-viewport dark background, content emerging from darkness, green accent glow as the sole focus signal. This is a cinematographic choice, not just a color preference.

### When NOT to Use Low-Key [VERIFIED]

- Accessibility contexts: dark mode needs 4.5:1 contrast ratio minimum (WCAG) — low-key can fail this
- Long-form reading (sustained text on dark = eye fatigue)
- Medical/clinical content where trust and clarity are paramount over drama

---

## 3. Color Temperature as Emotional Control

### The Physics/Psychology Link [VERIFIED]

Color temperature is measured in Kelvin (K). The human brain maps temperature to time-of-day associations built through evolutionary exposure to natural light. These are not learned associations — they are hardwired.

| Temperature | Color | Association | Emotion |
|-------------|-------|-------------|---------|
| 1800-2700K | Deep amber/orange | Firelight, candle, sunset | Intimacy, warmth, romance, danger, urgency |
| 3000-3200K | Warm white/yellow | Incandescent, golden hour | Comfort, nostalgia, relaxation, home |
| 4000-4500K | Neutral white | Midday sun, office | Neutral, productive, clinical neutrality |
| 5500-6500K | Cool white/blue-white | Overcast sky, daylight | Alertness, focus, precision, clinical |
| 7000K+ | Blue | Moonlight, underwater, cold | Isolation, sadness, tension, futurism |

### The Key Rule [VERIFIED]

"A warm glow makes audiences feel closer to characters; a cool wash creates emotional distance."

Applied to UI: warm temperature = invitation, intimacy, closeness with the product. Cool temperature = precision, objectivity, clinical distance.

**The teal accent in V25 sits at the cool-neutral boundary (~5000K equivalent).** This is intentional: health data needs clinical trust, not fireplace intimacy. Purple (IVF) sits slightly cooler, implying precision and medical authority. If you wanted warmth (BMI validation mode), shift to amber (#F59E0B range).

### CSS Implementation [VERIFIED — derived from search results]

Color temperature control happens in three places:

**1. Background toning:**
```css
/* Warm dark (3200K feel — intimate, human) */
background-color: #1A1208;

/* Neutral dark (4500K feel — balanced) */
background-color: #121212;

/* Cool dark (6500K feel — clinical, digital) */
background-color: #080D12;
```

**2. Glow color on accent elements:**
```css
/* Warm accent (amber/firelight) */
box-shadow: 0 0 24px rgba(245, 158, 11, 0.4);

/* Cool accent (teal/clinical) */
box-shadow: 0 0 24px rgba(20, 184, 166, 0.35);

/* Cold accent (blue/futurist) */
box-shadow: 0 0 24px rgba(59, 130, 246, 0.3);
```

**3. CSS color-filter on images (for color grading existing assets):**
```css
/* Warm grade */
filter: sepia(20%) saturate(110%) hue-rotate(-10deg);

/* Cool grade */
filter: saturate(90%) hue-rotate(10deg) brightness(0.95);
```

### Temperature Mixing [VERIFIED — cinematography principle]

Professional cinematography uses temperature contrast deliberately. Warm foreground subject, cool background = subject feels human/present against cold world. Cool foreground, warm background = subject feels distant, isolated.

In UI: warm foreground element (the calculator result card) against cool dark background = the result feels personal, the system feels precise. This is what V25 achieves — dark cool background, warm result output.

---

## 4. Motivated vs Unmotivated Lighting

### Definitions [VERIFIED]

**Motivated lighting:** Light that has a logical source within the scene. The audience (or user) can explain where the light comes from. A window. A lamp. A screen. A phone. A candle. The light is either visible (a "practical") or implied by context.

**Practical light:** A light source visible within the frame itself — a lamp, a computer screen, a TV, a candle. Cinematographers often boost practicals (hide LED panels inside fixtures) to achieve the look without practical power levels.

**Unmotivated lighting:** Light that exists for the cinematographer's purposes but has no in-world source. The subject is lit beautifully but there is no lamp, no window, no explanation. Feels artificial when overdone.

### The Immersion Rule [VERIFIED]

"To keep the audience engaged in the story rather than wondering where the light is coming from, keep all light motivated."

Applied to UI: every glow, gradient, and highlight should have an implied or visible source. When the source is invisible and arbitrary, the design reads as decorative noise. When the source is implied (the calculator result panel is the light source, illuminating the surrounding dark), the interface feels like a world with rules.

### CSS Motivated Lighting [LLM-ESTIMATED from principles]

**The screen-as-practical pattern:**

The calculator result card itself is the light source. Dark background receives glow from the card, implying the card is emitting light:

```css
.result-card {
  background: rgba(20, 184, 166, 0.08);
  border: 1px solid rgba(20, 184, 166, 0.25);
  /* The card emits the glow — it IS the practical */
  box-shadow:
    0 0 60px rgba(20, 184, 166, 0.12),  /* ambient spill from card */
    0 0 120px rgba(20, 184, 166, 0.06); /* far-field atmospheric fill */
}
```

**The window-as-source pattern:**

The top of the viewport is the light source (implied: skylight, ceiling light). Content fades lighter toward the top edge:

```css
.page-background {
  background: radial-gradient(
    ellipse 80% 50% at 50% -10%,   /* source: above center, off-screen */
    rgba(20, 184, 166, 0.08) 0%,
    transparent 70%
  ),
  #0D0D0D;
}
```

**Unmotivated (avoid):**

Random glows that don't correspond to any on-screen element. Background blob that exists in the middle of a section with no implied source.

---

## 5. Shadows — Depth, Drama, and Hierarchy

### How Shadows Create Depth [VERIFIED]

Shadows create the illusion of Z-axis depth on a 2D screen. Elements that cast shadows appear closer to the viewer. Elements receiving shadows appear further away. This is how Material Design's elevation system works: higher elevation = bigger, softer, more diffuse shadow.

The key insight: attention gravitates toward elements closest to us. Elevated elements with strong shadows pull attention. This is functional hierarchy, not decoration.

### Shadow Anatomy [VERIFIED — CSS sources]

A realistic shadow has two components:

**Key shadow:** Directional, sharper, darker. Caused by the dominant point light source. Small offset, lower blur, higher opacity.

**Ambient shadow:** Non-directional, softer, lighter. Caused by scattered ambient light. Zero or minimal offset, high blur, low opacity.

```css
/* Realistic two-layer shadow (key + ambient) */
box-shadow:
  0 4px 6px rgba(0, 0, 0, 0.4),    /* key shadow: directional, sharp */
  0 12px 40px rgba(0, 0, 0, 0.2);  /* ambient shadow: soft, diffuse */
```

Single-layer shadows read as flat/artificial. Two-layer reads as physically plausible.

### Hierarchy Through Shadow Scale [VERIFIED]

| Elevation | box-shadow | Use |
|-----------|-----------|-----|
| 0 (flat) | none | Background, lowest layer |
| 1dp | `0 1px 3px rgba(0,0,0,0.3)` | Subtle separation |
| 4dp | `0 4px 12px rgba(0,0,0,0.4)` | Cards, containers |
| 8dp | `0 8px 24px rgba(0,0,0,0.5)` | Modals, focused panels |
| 24dp | `0 24px 60px rgba(0,0,0,0.6)` | Hero elements, maximum focus |

### Shadows on Dark UIs [LLM-ESTIMATED]

On dark backgrounds, shadows become invisible (dark on dark). The depth system inverts: use GLOWS instead of shadows.

- Shadow on light background = element above surface (depth)
- Glow on dark background = element emitting light (energy)

```css
/* Light mode elevation (shadow) */
.card-light { box-shadow: 0 8px 24px rgba(0,0,0,0.15); }

/* Dark mode elevation (glow) */
.card-dark { box-shadow: 0 0 24px rgba(20,184,166,0.15); }
```

### The `drop-shadow()` Filter vs `box-shadow` [VERIFIED]

`box-shadow` creates a rectangular shadow behind the element's bounding box. `filter: drop-shadow()` creates a shadow that conforms to the actual shape of the element (including transparency). For PNG icons, SVGs, and irregular shapes, `drop-shadow()` produces physically plausible results where `box-shadow` does not.

---

## 6. Chiaroscuro — Extreme Contrast as Design Language

### The Origin [VERIFIED]

Chiaroscuro (Italian: chiaro = light, scuro = dark) originated in Renaissance painting — Leonardo da Vinci, Rembrandt, Caravaggio. It describes extreme contrast between illuminated areas and deep shadow. It entered cinema through German Expressionism and became the defining visual language of film noir.

The technique uses a single hard light source, letting half the subject fade into shadow. The image is not about showing everything — it is about selecting what to reveal.

### Emotional Effects [VERIFIED]

Chiaroscuro inherently suggests:
- Mystery, suspense, danger
- Psychological intensity
- Moral ambiguity
- Introspection
- The hidden

It does NOT suggest:
- Safety
- Clinical precision
- Openness
- Accessibility

### Web Equivalent [VERIFIED — dark mode UI research]

The dark mode UI pattern is the closest web analog to chiaroscuro. Key characteristics:

1. Background: near-black but not pure black. Pure black (#000000) kills perceived depth. Use #0D0D0D, #121212, or #1A1A1A.
2. A single illuminated focal point — the hero element, the result card, the CTA.
3. Everything else fades. Navigation is low-contrast. Secondary elements are barely visible.
4. Accent colors replace shadow as the depth mechanism.

**The Netflix homepage is cinematic chiaroscuro.** Dark background. Hero image pops with maximum contrast. Everything else recedes. Your eye has no choice.

### Contrast Ratio in Chiaroscuro UI [VERIFIED]

High-contrast dark UIs use stark contrast for the focal element and deliberately low contrast for everything else. This is the opposite of accessibility-first design (which seeks consistent contrast). The two goals are in tension.

Resolution: maintain WCAG 4.5:1 for primary text. Allow sub-4.5:1 for decorative/non-essential elements (navigation, dividers, labels). The calculator result text must be readable. The page chrome can fade.

### CSS Implementation [LLM-ESTIMATED from principles]

```css
/* Chiaroscuro dark page: everything recedes except the focal element */

body {
  background: #0D0D0D;
}

/* Secondary elements: barely present */
nav a {
  color: rgba(255,255,255,0.35);  /* Very low contrast: decorative, recedes */
}

/* Primary focal element: emerges from dark */
.result-card {
  color: #FFFFFF;               /* Full contrast */
  background: rgba(20,184,166,0.10);
  border: 1px solid rgba(20,184,166,0.3);
  box-shadow: 0 0 80px rgba(20,184,166,0.15);
}

/* The gradient vignette — darkness deepens at edges, lightens toward center */
.page-background::before {
  content: '';
  position: fixed;
  inset: 0;
  background: radial-gradient(
    ellipse 60% 60% at 50% 40%,
    transparent 0%,
    rgba(0,0,0,0.4) 100%
  );
  pointer-events: none;
  z-index: 0;
}
```

---

## 7. Practical CSS Implementations

### A. Radial-Gradient as Spotlight [VERIFIED — CSS search results]

A radial-gradient simulates a focused light source hitting a surface from above or at an angle.

```css
/* Static spotlight: top-center source, fades to dark */
.hero {
  background:
    radial-gradient(
      ellipse 70% 40% at 50% 0%,       /* source: top-center, off-screen */
      rgba(20,184,166,0.12) 0%,
      transparent 70%
    ),
    #0D0D0D;
}

/* Interactive spotlight: follows mouse via CSS custom properties */
.spotlight-container {
  background-image: radial-gradient(
    circle 300px at var(--x, 50%) var(--y, 50%),
    rgba(255,255,255,0.08) 0%,
    transparent 100%
  );
}
/* JS: element.style.setProperty('--x', e.clientX + 'px') */
```

### B. Box-Shadow as Key Light [VERIFIED — CSS sources]

Key light in CSS = the primary `box-shadow`. The offset direction must be consistent with the page's implied light source. If the light is above-left, all key shadows fall below-right.

```css
/* Page light source: upper-left (reads as natural/safe) */
.card {
  box-shadow:
    6px 10px 24px rgba(0,0,0,0.5),   /* key shadow: lower-right */
    -2px -2px 12px rgba(0,0,0,0.1);  /* fill: opposite, very subtle */
}

/* Page light source: directly above (formal, balanced) */
.card {
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}

/* Dark mode: glow replaces shadow */
.card-dark {
  box-shadow:
    0 0 24px rgba(20,184,166,0.2),   /* ambient glow */
    0 0 8px rgba(20,184,166,0.4);    /* tight glow = proximity to source */
}
```

### C. Backdrop-Filter as Atmospheric Haze [VERIFIED — CSS sources]

`backdrop-filter: blur()` simulates depth-of-field haze and atmospheric blur. Elements behind a blurred layer appear distant, creating a perception of physical depth layers.

The key effect: heavy blur makes the background color bleed through as ambient light. Combine with a semi-transparent background to achieve a "frosted glass" or "atmospheric fog" layer.

```css
/* Frosted glass panel — foreground element, background recedes into haze */
.glass-card {
  background: rgba(13, 13, 13, 0.7);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  border: 1px solid rgba(255,255,255,0.06);
}

/* Progressive fog: deepens toward bottom (depth receding) */
.fog-layer {
  position: absolute;
  inset: 0;
  mask: linear-gradient(to bottom, transparent 0%, black 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  pointer-events: none;
}
```

Performance note: `backdrop-filter` is GPU-accelerated in all modern browsers. Safe to use. Include `-webkit-` prefix for Safari.

### D. Rim Light / Edge Glow in CSS [VERIFIED + LLM-ESTIMATED]

Rim light separates subjects from backgrounds. In CSS, it is typically implemented as a border glow or a tight outer box-shadow:

```css
/* Rim light via border + box-shadow */
.rim-lit-card {
  border: 1px solid rgba(20,184,166,0.4);    /* the physical edge glow */
  box-shadow:
    0 0 0 1px rgba(20,184,166,0.1),           /* halo just outside border */
    inset 0 0 0 1px rgba(20,184,166,0.05);   /* inner edge — the backlight spilling inward */
}

/* Animated rim pulse (for key elements) */
@keyframes rim-pulse {
  0%, 100% { box-shadow: 0 0 0 1px rgba(20,184,166,0.2); }
  50%       { box-shadow: 0 0 0 3px rgba(20,184,166,0.4); }
}
.pulsing-dot {
  animation: rim-pulse 2s ease-in-out infinite;
}
```

---

## 8. The Golden Hour Look

### What It Is [VERIFIED]

Golden hour (also "magic hour" in cinematography) is the first and last hour of sunlight. The sun is near the horizon, light travels through more atmosphere, and blue wavelengths scatter out. What remains: amber, orange, gold.

Characteristics:
- Color temperature: 2000-3000K (deep warm)
- Soft, directional light (low angle)
- Long, dramatic shadows
- High contrast between lit and shadowed areas
- Atmospheric haze/glow

### Emotional Signal [VERIFIED]

Golden hour communicates: warmth, ephemerality, nostalgia, beauty, the human, the emotional. Cinematographers use it for romance, revelation, homecoming, triumph. It is the light of "this moment matters."

It does NOT communicate: precision, clinical accuracy, data, authority.

### CSS Approximation [VERIFIED — color palette sources + LLM-ESTIMATED implementation]

The golden hour look uses three elements: warm amber highlights, long directional shadows (low angle = long shadow), and atmospheric softness.

```css
/* Golden hour hero background */
.golden-hero {
  background:
    /* The horizon glow — low, warm, atmospheric */
    radial-gradient(
      ellipse 100% 60% at 50% 100%,      /* source: horizon (bottom-center) */
      rgba(245,158,11,0.25) 0%,           /* #F59E0B = amber-400 */
      rgba(239,68,68,0.08) 40%,           /* edge of warm zone: slight red */
      transparent 70%
    ),
    /* Deep sky gradient */
    linear-gradient(
      to bottom,
      #0D1117 0%,                         /* deep dark at top */
      #1A0E08 100%                        /* dark amber tone at bottom */
    );
}

/* Golden hour card toning */
.golden-card {
  background: rgba(245,158,11,0.06);
  border: 1px solid rgba(245,158,11,0.2);
  box-shadow:
    0 16px 64px rgba(245,158,11,0.12),   /* warm ambient */
    0 4px 16px rgba(0,0,0,0.4);          /* key shadow (directional, low angle) */
}

/* CSS color grading (applied to images) */
.golden-image {
  filter: sepia(25%) saturate(130%) hue-rotate(-15deg) brightness(1.05);
}
```

**Golden hour color palette:**

| Role | Color | Hex |
|------|-------|-----|
| Primary glow | Amber | #F59E0B |
| Secondary | Orange | #F97316 |
| Deep shadows | Dark amber-brown | #1A0E08 |
| Highlight | Pale gold | #FDE68A |
| Atmospheric haze | Warm gray | rgba(245,158,11,0.08) |

---

## 9. Synthesis — The Design Decision Framework

### Which Lighting System to Use [LLM-ESTIMATED from combined principles]

| Design Goal | Lighting System | CSS Implementation |
|-------------|----------------|-------------------|
| Clinical trust, data precision | High-key + cool temperature | Light bg, minimal shadow, cool accent |
| Focused attention, drama | Low-key + single spotlight | Dark bg, radial-gradient source, chiaroscuro |
| Warmth, invitation, personal | Low-key + warm temperature | Dark amber bg, warm glow accent |
| Separation/depth without drama | Three-point, balanced ratio | Layered box-shadow with fill |
| Interactive moment | Motivated (cursor = light source) | radial-gradient on pointermove |
| Atmospheric immersion | Backdrop-filter haze | Layered backdrop-filter blur |
| Element identity/separation | Rim light | Border + outer box-shadow glow |

### The V25 Calculator Design in Lighting Terms [LLM-ESTIMATED]

V25 uses low-key lighting with a motivated light source (the result card itself emits light) and rim lighting on the primary element to separate it from the dark background. The key light is the accent glow. There is no fill light — the surrounding dark stays dark. This is chiaroscuro — not decorative, functional. It says: THIS is the one thing that matters.

The accent color (teal, purple, coral) is the color temperature of the key light. It sets the emotional register per calculator.

### What Would Disprove These Mappings [Falsifiability]

- If user testing shows dark-mode (low-key) UIs produce lower completion rates on medical calculators, the "clinical precision from dark" assumption is wrong. Medical content may require high-key (clinical white) to communicate safety.
- If the consistency-of-light-source rule is relaxed and users do not notice mixed shadow directions, the "global light source" principle may be a cinematographer's concern, not a UX concern.
- If color temperature emotional associations differ across cultures (warm = danger in some contexts, cool = cleanliness vs cold in others), the temperature-emotion map may not be universal.
- If `backdrop-filter` performance drops on mobile at blur values above 8px, the "atmospheric haze" technique is not viable for performance-sensitive pages.

---

## Sources

- [Three-Point Lighting: Key, Fill & Rim Lighting — StudioBinder](https://www.studiobinder.com/blog/three-point-lighting-setup/)
- [Three-point lighting — Wikipedia](https://en.wikipedia.org/wiki/Three-point_lighting)
- [What is a Rim Light — StudioBinder](https://www.studiobinder.com/blog/what-is-a-rim-light-photography-definition/)
- [Chiaroscuro Lighting in Film — No Film School](https://nofilmschool.com/chiaroscuro-lighting)
- [Chiaroscuro Lighting — Artlist Blog](https://artlist.io/blog/chiaroscuro-lighting/)
- [What is Chiaroscuro — StudioBinder](https://www.studiobinder.com/blog/what-is-chiaroscuro-definition-examples/)
- [Chiaroscuro — Wikipedia](https://en.wikipedia.org/wiki/Chiaroscuro)
- [Warm vs Cool Lighting Psychology — Skope Entertainment](https://skopemag.com/2025/04/15/warm-vs-cool-lighting-in-stage-design-key-differences-uses-psychology)
- [Color Temperature in Filmmaking — DpDiaries](https://dpdiaries.com/lighting/understanding-color-temperature-in-filmmaking-a-guide-to-white-balance/)
- [High-Key vs Low-Key Lighting — Artlist](https://artlist.io/blog/high-key-lighting-vs-low-key-lighting/)
- [High-Key and Low-Key Photography — FD Photo Studio](https://www.fdphotostudio.com/high-key-and-low-key-photography-lighting-mood-and-when-to-use/)
- [What is Low-Key Lighting — Videomaker](https://www.videomaker.com/how-to/lighting/lighting-design/what-is-low-key-lighting-and-why-should-you-use-it/)
- [What is Motivated Lighting — StudioBinder](https://www.studiobinder.com/blog/what-is-motivated-lighting-in-film/)
- [Motivated Lighting — No Film School](https://nofilmschool.com/motivated-lighting)
- [What is Practical Lighting — StudioBinder](https://www.studiobinder.com/blog/what-is-practical-lighting-in-film/)
- [CSS Spotlight Effect — Frontend Masters](https://frontendmasters.com/blog/css-spotlight-effect/)
- [Creating Glow Effects with CSS — Coder's Block](https://codersblock.com/blog/creating-glow-effects-with-css/)
- [Five Ways to Create Light Effects with CSS — OpenReplay](https://blog.openreplay.com/five-ways-to-create-light-effects-with-css/)
- [Designing Beautiful Shadows in CSS — Josh W. Comeau](https://www.joshwcomeau.com/css/designing-shadows/)
- [Mastering CSS Box Shadow — Silphium Design](https://silphiumdesign.com/css-box-shadow-simulating-real-light-shadow/)
- [Getting Deep Into Shadows — CSS-Tricks](https://css-tricks.com/getting-deep-into-shadows/)
- [Dark Mode UI Best Practices — Toptal](https://www.toptal.com/designers/ui/dark-ui-design)
- [Dark Mode UI Design — LogRocket](https://blog.logrocket.com/ux-design/dark-mode-ui-design-best-practices-and-examples/)
- [backdrop-filter — MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter)
- [Using CSS backdrop-filter — CSS-Tricks](https://css-tricks.com/using-css-backdrop-filter-for-ui-effects/)
- [Next-level frosted glass — Josh W. Comeau](https://www.joshwcomeau.com/css/backdrop-filter/)
- [Golden Hour Gradient — icolorpalette](https://icolorpalette.com/gradients/golden-hour)
- [Golden Hour Photography — Adobe](https://www.adobe.com/creativecloud/photography/technique/golden-hour.html)
- [Rim Lighting — Beverly Boy Productions](https://beverlyboy.com/filmmaking/what-is-rim-light-in-cinematography/)
- [Rim Light — NFI](https://www.nfi.edu/rim-light/)
- [Mastering Motivated Lighting — Number Analytics](https://www.numberanalytics.com/blog/motivated-lighting-cinematography-ultimate-guide)
