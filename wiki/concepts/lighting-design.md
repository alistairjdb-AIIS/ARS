# Lighting Design

> Three-point lighting, key-to-fill ratios, color temperature, motivated lighting, shadow anatomy, and chiaroscuro — mapped from film cinematography to CSS box-shadow, radial-gradient, backdrop-filter, and dark UI design systems. Lighting is not decoration; it is the emotional register of the interface.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### Three-Point Lighting System

The standard illumination method in film, photography, video, and 3D rendering. Three distinct light sources, each with a specific role. [VERIFIED]

| Light | Position | Role | CSS Analog |
|-------|----------|------|-----------|
| Key light | 45 degrees to subject, primary side | Principal illuminator. Sets exposure, direction, mood. Casts dominant shadows. | `box-shadow: -8px 8px 24px rgba(0,0,0,0.6)` (offset = direction) |
| Fill light | Opposite side from key, lower angle | Reduces shadows from key. Softens contrast. Usually 50% or less of key brightness. | `box-shadow: 4px -2px 16px rgba(0,0,0,0.2)` (opposite offset, lower opacity) |
| Rim/back light | Behind subject, aimed at back | Creates bright edge outline. Separates subject from background. Adds depth. | `box-shadow: 0 0 12px 2px rgba(255,255,255,0.15)` or `border: 1px solid rgba(255,255,255,0.12)` |

The `box-shadow` offset direction is the light source position in reverse. If the light is above-left, the shadow falls below-right. The global light source must be consistent across all elements on a page. Mixing directions reads as incoherent. [VERIFIED]

### Key-to-Fill Ratio

The ratio between key and fill determines the scene's emotional register. [VERIFIED]

| Ratio | Name | Mood | UI Equivalent |
|-------|------|------|--------------|
| 1:1 | Flat | Bright, commercial, safe | High-key UI — equal shadow on all sides |
| 2:1 | Slight | Broadcast, clean | Standard card elevation |
| 4:1 | Moderate | Drama, narrative, presence | Hero sections, spotlight cards |
| 8:1+ | Heavy | Noir, mystery, intensity | Chiaroscuro UI — deep dark bg, single illuminated element |

In CSS terms: opacity ratio between key shadow and fill shadow. Key at `rgba(0,0,0,0.6)`, fill at `rgba(0,0,0,0.15)` = approximately 4:1. [VERIFIED]

### High-Key vs. Low-Key Lighting

**High-key:** Reduces contrast between shadows and highlights. Minimal shadow. Bright, flat, even. Multiple light sources eliminate shadow. Communicates: upbeat, safe, open, trustworthy. Fits: children's content, product shots, medical reference. [VERIFIED]

**Low-key:** High contrast between light and dark. Majority of scene in shadow. One dominant light source. Communicates: mystery, tension, drama, intensity. Fits: premium portfolio, cinematic UX, luxury brands. [VERIFIED]

**High-key UI:** White or light backgrounds, minimal shadow elevation (1-4dp), muted accent colors, readability optimized. [VERIFIED]

**Low-key UI:** Dark backgrounds (#121212, #0D0D0D — not pure #000000), strong spotlight behavior, glows as primary depth cue instead of shadows, high contrast accent colors (but desaturated to avoid saturation vibration against dark surfaces). [VERIFIED]

**When NOT to use low-key:** Accessibility contexts (dark mode needs 4.5:1 minimum contrast per WCAG), long-form reading (sustained text on dark = eye fatigue), medical/clinical content where trust and clarity are paramount over drama. [VERIFIED]

### Color Temperature as Emotional Control

Color temperature maps to time-of-day associations built through evolutionary exposure to natural light. These are hardwired, not learned. [VERIFIED]

| Temperature | Color | Emotion |
|-------------|-------|---------|
| 1800-2700K | Deep amber/orange | Intimacy, warmth, romance, urgency |
| 3000-3200K | Warm white/yellow | Comfort, nostalgia, relaxation |
| 4000-4500K | Neutral white | Neutral, productive, clinical |
| 5500-6500K | Cool white/blue-white | Alertness, focus, precision |
| 7000K+ | Blue | Isolation, sadness, futurism |

**The key rule:** "A warm glow makes audiences feel closer; a cool wash creates emotional distance." Applied to UI: warm = invitation, intimacy. Cool = precision, objectivity. [VERIFIED]

**CSS implementation** happens in three places: (1) Background toning (e.g., `#1A1208` for warm dark, `#080D12` for cool dark), (2) Glow color on accent elements via `box-shadow`, (3) CSS `filter` on images for color grading. [VERIFIED]

**Temperature mixing:** Warm foreground against cool background = subject feels human/present against cold world. Cool foreground, warm background = subject feels distant. This is a deliberate cinematographic technique. [VERIFIED]

### Motivated vs. Unmotivated Lighting

**Motivated lighting:** Light that has a logical source within the scene — a window, lamp, screen. The light is visible (a "practical") or implied by context. [VERIFIED]

**Unmotivated lighting:** Light that exists for the filmmaker's purposes but has no in-world source. Feels artificial when overdone. [VERIFIED]

**The immersion rule:** "To keep the audience engaged, keep all light motivated." Applied to UI: every glow, gradient, and highlight should have an implied or visible source. When the source is invisible and arbitrary, the design reads as decorative noise. When the source is implied (the result card is the light source illuminating the surrounding dark), the interface feels like a world with rules. [VERIFIED]

**The screen-as-practical pattern:** The calculator result card itself is the light source. Dark background receives glow from the card, implying the card emits light. CSS: the card has `box-shadow: 0 0 60px rgba(accent, 0.12), 0 0 120px rgba(accent, 0.06)` — ambient spill + far-field atmospheric fill. [THEORETICAL]

### Shadow Anatomy and Depth Hierarchy

A realistic shadow has two components: key shadow (directional, sharper, darker, small offset, higher opacity) and ambient shadow (non-directional, softer, lighter, zero offset, high blur, low opacity). Single-layer shadows read as flat/artificial. Two-layer reads as physically plausible. [VERIFIED]

| Elevation | box-shadow | Use |
|-----------|-----------|-----|
| 0 (flat) | none | Background, lowest layer |
| 1dp | `0 1px 3px rgba(0,0,0,0.3)` | Subtle separation |
| 4dp | `0 4px 12px rgba(0,0,0,0.4)` | Cards, containers |
| 8dp | `0 8px 24px rgba(0,0,0,0.5)` | Modals, focused panels |
| 24dp | `0 24px 60px rgba(0,0,0,0.6)` | Hero elements, maximum focus |

**Shadows on dark UIs:** The depth system inverts. Use GLOWS instead of shadows. Shadow on light background = element above surface (depth). Glow on dark background = element emitting light (energy). [THEORETICAL]

**`drop-shadow()` vs `box-shadow`:** `box-shadow` creates a rectangular shadow behind the bounding box. `filter: drop-shadow()` conforms to the actual shape (including transparency). For PNG icons, SVGs, and irregular shapes, `drop-shadow()` produces physically plausible results. [VERIFIED]

### Chiaroscuro: Extreme Contrast as Design Language

Originated in Renaissance painting (Leonardo, Rembrandt, Caravaggio). Entered cinema through German Expressionism and became the visual language of film noir. Uses a single hard light source; the image is about selecting what to reveal, not showing everything. [VERIFIED]

**Emotional effects:** Mystery, suspense, psychological intensity, moral ambiguity, introspection. Does NOT suggest safety, clinical precision, openness, or accessibility. [VERIFIED]

**Web equivalent:** Dark mode UI pattern. Near-black background (not pure black — #0D0D0D, #121212, or #1A1A1A). Single illuminated focal point. Everything else fades. Accent colors replace shadow as depth mechanism. [VERIFIED]

**Contrast tension:** High-contrast dark UIs use stark contrast for the focal element and deliberately low contrast for everything else. This is the opposite of accessibility-first design. Resolution: maintain WCAG 4.5:1 for primary text. Allow sub-4.5:1 for decorative/non-essential elements. [VERIFIED]

### The Golden Hour Look

Color temperature 2000-3000K (deep warm), soft directional light (low angle), long dramatic shadows, atmospheric haze. Communicates: warmth, ephemerality, nostalgia, "this moment matters." Does NOT communicate precision, clinical accuracy, or authority. [VERIFIED]

CSS: warm amber highlights via `radial-gradient` from bottom-center (horizon source), long directional shadows (low angle = long shadow offset), `filter: sepia(25%) saturate(130%) hue-rotate(-15deg)` for image grading. [VERIFIED]

### Dark Mode Design Patterns from Premium Health Apps

**Background color convergence across premium apps:** [VERIFIED]
- Pure black `#000000`: Apple Health (base layer) — clinical-premium on OLED
- Near-black `#0B0B0B`: WHOOP — austere, performance-focused
- Dark gray `#121212`-`#1C1C1E`: Strava, elevated surfaces — softer, approachable
- Dynamic: Oura — biometric-responsive, most differentiated

Pure black and near-black are premium signals. Mid-dark-gray reads as "we added dark mode" rather than "designed for dark." [VERIFIED]

**Glow, shadow, and depth on dark:** Elevation via slightly lighter surface color works. Subtle glow/bloom on data elements works. Drop shadows fail (invisible on dark). Pure inversion of light mode fails (wrong contrast ratios). Thin strokes and light-weight decorative elements disappear. [VERIFIED]

**Breathing room:** Dark mode requires 20-30% MORE padding/margin than light mode for equivalent readability. [VERIFIED]

**Pure black risk:** Users with astigmatism find light-text-on-pure-black harder to read due to halation (text appears to bloom/bleed). `#0B0B0B` mitigates this vs `#000000`. [VERIFIED]

---

## Operational Rules

1. **When placing shadows, maintain a single consistent global light source direction across all elements on the page.** If the key light is upper-left, ALL key shadows must fall lower-right. Mixed directions read as incoherent and break the illusion. [VERIFIED]

2. **When designing dark UI, use glows instead of shadows for depth.** Shadows are invisible on dark backgrounds. The depth system inverts: glow = energy/proximity, not shadow = elevation. [THEORETICAL]

3. **When implementing dark backgrounds, use near-black (#0B0B0B to #121212), never pure black (#000000).** Pure black kills perceived depth and causes halation for users with astigmatism. Exception: OLED displays where Apple uses true black for base layer with elevated surfaces at #1C1C1E. [VERIFIED]

4. **When every glow and gradient should have an implied light source.** Ask: "where is the light coming from?" If the answer is "nowhere," the element is unmotivated and reads as decoration. The screen-as-practical pattern (the result card IS the light source) creates motivated lighting. [VERIFIED]

5. **When using color temperature to set emotional register, match temperature to content purpose.** Cool (~5500-6500K equivalent) for clinical precision and data. Warm (~2700-3200K equivalent) for intimacy and human connection. The accent color IS the color temperature of the key light. [VERIFIED]

6. **When designing dark mode layouts, add 20-30% more spacing than the equivalent light mode layout.** Dark backgrounds amplify visual density. More breathing room is required for equivalent readability and premium feel. [VERIFIED]

7. **When using two-layer shadows for realism, always include both key (directional, sharp, darker) and ambient (omnidirectional, soft, lighter) components.** Single-layer shadows read as artificial. Two-layer reads as physically plausible. [VERIFIED]

8. **When encoding health signal valence, use copy and typography, not color.** Premium health apps (WHOOP, Oura, Apple) use color for identity or state, NOT binary good/bad. Binary green/red is the clinical/utilitarian pattern. It reads as medical software, not lifestyle product. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/cinematography_lighting_design.md` | Three-point lighting, key-to-fill ratios, high/low-key, color temperature, motivated lighting, shadows, chiaroscuro, golden hour, CSS implementations, decision framework |
| `research-data/dark_mode_health_ui_research.md` | Premium health app analysis (WHOOP, Oura, Apple, Strava), dark background convergence, accent color strategies, typography on dark, glow/shadow patterns, breathing room, accessibility |

---

## Related Concepts

- [[camera-language]] — Camera move sets the frame; lighting sets the mood within it
- [[color-narrative]] — Color temperature and lighting temperature overlap; warm/cool lighting is one axis of the color narrative arc
- [[visual-storytelling-mise-en-scene]] — Lighting is one of six mise-en-scene elements
- [[design-psychology-gestalt]] — Figure/ground separation depends on lighting and shadow; low-key UI is a figure/ground strategy

---

## Deep Reference

- **When** deciding key-to-fill ratio for a UI section and need to match mood → **read** `research-data/cinematography_lighting_design.md` §1 (Three-Point Lighting) **for** the ratio-to-mood table (1:1 = flat/commercial, 2:1 = broadcast, 4:1 = dramatic, 8:1+ = noir) with CSS `box-shadow` opacity equivalents for each ratio
- **When** choosing between high-key and low-key lighting for a dark-mode health UI → **read** `research-data/dark_mode_health_ui_research.md` (App-by-App Analysis) **for** exact hex values used by WHOOP (`#0B0B0B`), Oura, Apple Health, and Strava, their accent color strategies (WHOOP = single red, no green/red valence), typography-on-dark approaches, and why dark-by-default reads as premium
- **When** implementing CSS shadow that simulates a consistent light source → **read** `research-data/cinematography_lighting_design.md` §1 (CSS Mapping Rule) **for** the offset-direction reversal rule (light upper-left → shadow lower-right), the dual-shadow formula for key + fill, and the Material Design codification that requires global light source consistency across all elements
- **When** applying color temperature to set mood and need to choose between warm and cool → **read** `research-data/cinematography_lighting_design.md` §4 (Color Temperature) **for** the Kelvin-to-emotion mapping, golden hour as universal trust signal, cool blue as clinical/precision, and the CSS gradient technique that simulates color temperature shifts across the page

---

## Open Questions

- Whether the "consistency-of-light-source" rule is a cinematographer's concern or a measurable UX concern. If user testing shows users do not notice mixed shadow directions, the rule may be less critical for web than for film.
- Whether `backdrop-filter` performance drops on mobile at blur values above 8px, making the "atmospheric haze" technique not viable for performance-sensitive pages.
- Whether color temperature emotional associations differ across cultures. Warm = danger in some cultural contexts, cool = cleanliness vs. cold in others.
- Whether user testing would show dark-mode (low-key) UIs produce lower completion rates on medical calculators, falsifying the "clinical precision from dark" assumption.
- The 20-30% more spacing rule for dark mode comes from practitioner consensus; no controlled study with precise effect size was found.
