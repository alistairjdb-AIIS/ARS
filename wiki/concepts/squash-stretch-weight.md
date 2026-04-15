# Squash, Stretch, and Weight

> How element mass maps to spring constants, easing curves, duration, and squash/stretch ratios in web UI and video prompting. The most fundamental animation principle applied to digital surfaces.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 3 raw files, 0 memory files

---

## Core Findings

### Squash and Stretch Fundamentals

The most fundamental of Disney's 12 Principles. An object's volume stays constant -- when it squashes (compresses on one axis) it must stretch on the perpendicular axis. This communicates mass, flexibility, and physical properties. [VERIFIED -- Thomas & Johnston, "The Illusion of Life" 1981, confirmed via cssanimation.rocks, IxDF, Animation Mentor]

Without squash and stretch, UI elements feel weightless and incorporeal -- flat rectangles moving in 2D space. With it, elements feel like they have physical mass and respond to forces. The difference between a button press that feels like clicking a wooden block vs. pressing a real physical button. [VERIFIED -- IxDF, UX Collective]

**Volume preservation rule:** If scaleY drops by 0.08, scaleX should rise by approximately 0.05-0.06. The axes do not need to be perfectly reciprocal, but the visual impression of constant volume must hold. [THEORETICAL -- derived from Disney principle, calibration values are practitioner consensus]

### Calibration by Context

| Context | Squash/Stretch Differential | Character |
|---------|---------------------------|-----------|
| Subtle UI (professional) | 2-4% | Barely perceptible, keeps it corporate |
| Standard UI (consumer) | 4-8% | Responsive, feels bouncy |
| Playful UI (celebration) | 8-14% | Confident spring, energetic |
| Cartoonish (milestone only) | 15%+ | Only for success/celebration states |

[THEORETICAL -- derived from principle + practitioner ranges in animation_12_principles.md]

### CSS Implementation Patterns

**Button press (tactile feedback):**
```css
.button:active {
  transform: scaleX(1.04) scaleY(0.94);
  transition: transform 80ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```
[VERIFIED -- cssanimation.rocks, multiple CSS sources]

**Number counter reveal (value impact):**
```css
@keyframes countReveal {
  0%   { transform: scaleX(0.85) scaleY(1.2); opacity: 0; }
  60%  { transform: scaleX(1.04) scaleY(0.96); opacity: 1; }
  80%  { transform: scaleX(0.98) scaleY(1.01); }
  100% { transform: scaleX(1) scaleY(1); }
}
```
[VERIFIED -- animation_12_principles.md]

### Weight Classes and Their Motion Signatures

Element weight determines spring constants, easing curves, duration, and overshoot behavior. Five weight classes cover all UI elements. [VERIFIED -- Figma presets, Apple SwiftUI, Framer Motion defaults; weight-class mapping THEORETICAL]

| Weight Class | Examples | Stiffness | Damping | Mass | Duration (entry) | Overshoot (y2) |
|-------------|----------|-----------|---------|------|-----------------|----------------|
| Ultra-light | Tooltips, badges, count indicators | 400-500 | 28-35 | 0.6-0.8 | 100-150ms | 1.3 |
| Light | Small buttons, icons, tab indicators | 300-380 | 22-28 | 0.8-1.0 | 150-220ms | 1.3-1.4 |
| Medium | Cards, list items, form panels | 180-250 | 18-22 | 1.0-1.2 | 250-350ms | 1.4-1.56 |
| Heavy | Modals, drawers, hero sections | 100-150 | 15-20 | 1.5-2.0 | 350-500ms | 1.03-1.05 |
| Ultra-heavy | Full-page transitions, large overlays | 60-90 | 12-16 | 2.5-3.5 | 500-700ms | None |

### The Four Weight-Relevant Disney Principles

**1. Slow In and Slow Out** -- Duration + easing curve together determine perceived mass. Heavy objects accelerate and decelerate slowly (Newton's F=ma). Light objects snap. [VERIFIED -- animation_12_principles.md, animation_physical_weight.md]

**2. Anticipation** -- A backward dip before the main action. The larger the anticipation, the heavier the element feels. Light badge: 2% anticipation. Heavy modal: 5%. Negative y-values in cubic-bezier (y1 < 0) produce the backward movement. Anticipation phase should be 15-30% of total animation duration. [VERIFIED -- animation_12_principles.md, animation_motion_curves.md]

**3. Follow-Through and Overlapping Action** -- Elements with mass do not stop instantly. They overshoot and return. Heavy elements: larger overshoot, slower return. Light elements: smaller overshoot or snap. Three CSS mechanisms: cubic-bezier overshoot (y2 > 1), shadow delay (secondary follow-through 30-60ms late), true spring via linear(). [VERIFIED -- animation_12_principles.md]

**4. Secondary Action** -- Heavy elements get more pronounced secondary actions. A modal might cause a faint background dimple-pulse. A badge just fades in. Rules: secondary starts 100-300ms after primary, maximum 15% of primary's visual weight, one secondary per primary maximum. [VERIFIED -- IxDF, Ripplix]

### The Overshoot Paradox

In real spring physics, a heavy underdamped spring bounces MORE (harder to stop). In UI convention, heavy elements overshoot LESS because overshoot reads as playfulness, and heavy/authoritative elements should not feel playful. The design convention and physical reality go in opposite directions for the underdamped case. [VERIFIED -- animation_physical_weight.md Section 9]

This is a genuine design choice, not a physics fact. A modal with 1.03-1.05 overshoot feels physically present (something heavy carried past its destination). With 1.56 overshoot it would feel consumer/playful. [VERIFIED -- multiple sources]

### Keyframe Spacing as Weight Signal

Within a fixed duration, the distribution of keyframes communicates weight independently of easing curves. [VERIFIED -- animation_12_principles.md, animation_physical_weight.md]

**Light object:** 60% of distance covered in first 20% of time. Fast start, gentle drift to rest.
**Heavy object:** Only 15% of distance covered in first 40% of time. Slow buildup, most movement in the middle, long deceleration tail.

### Duration as Weight Communication

Duration communicates weight directly. Longer = heavier, more consequential. Shorter = lighter, more responsive. [VERIFIED -- NNGroup animation-duration research]

| Element Surface Area | Examples | Entry Duration | Exit Duration |
|---------------------|----------|---------------|--------------|
| <32px diameter | Badge, indicator dot | 100-150ms | 80-100ms |
| 32-64px | Button, chip, tag | 150-220ms | 120-160ms |
| 64-200px | Compact card, form field | 220-320ms | 160-240ms |
| 200-400px | Full card, panel | 280-400ms | 200-280ms |
| Full-screen | Drawer, modal, overlay | 350-500ms | 250-350ms |
| Page-level | Route transition, hero | 400-600ms | 300-400ms |

**The exit rule:** Exit is always 60-70% of entry duration. The eye needs to watch something arrive, not leave. [VERIFIED -- NNGroup, animation_choreography.md]

**Distance adjustment:** For every additional 100px of travel beyond 30px, add approximately 30-50ms to base duration. [THEORETICAL -- inferred from Material Design duration token spacing]

---

## Operational Rules

1. **When assigning motion to any UI element, classify its weight first** (ultra-light through ultra-heavy), then derive all parameters from the weight class table -- because inconsistent weight signals within a scene destroy the illusion of physical coherence.

2. **When a button is pressed, apply squash (scaleY 0.94-0.97) and stretch (scaleX 1.02-1.04) at 60-120ms** -- because uniform scaling communicates "resize" not "impact," and volume must appear preserved.

3. **When heavy elements (modals, drawers) enter, use overshoot of 1.03-1.05 maximum** -- because larger overshoot reads as playful, contradicting the authoritative signal heavy elements need to convey.

4. **When light elements (badges, chips) enter, allow overshoot of 1.3-1.4** -- because light elements should feel snappy and energetic, and the spring communicates responsiveness.

5. **When elements exit, use 60-70% of the entry duration and ease-in curves** -- because the user has already processed the content and does not need to watch it leave carefully.

6. **When revealing a result number, use a deliberate count-up with ease-in-out at 1200-1800ms for significant numbers** -- because slow timing communicates weight and precision in medical/health contexts.

7. **When different element weight classes appear in the same scene, each must use its own spring/easing parameters** -- because uniform easing across weight classes makes everything feel like the same material, destroying the weight hierarchy.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/animation_12_principles.md` | Squash/stretch mechanics, anticipation, follow-through, timing, exaggeration calibration |
| `research-data/animation_physical_weight.md` | Weight class presets, spring constants, easing curves by weight, duration scaling, organic stagger |
| `research-data/animation_motion_curves.md` | Cubic-bezier math, spring physics equation, overshoot mechanism, emotion-to-curve mapping |

---

## Related Concepts

- [[motion-curves-easing]] — DEPENDS_ON: the mathematical foundation for all weight-class curves
- [[choreography-stagger]] — INFORMS: how multiple weighted elements coordinate in sequence
- [[progressive-disclosure-pacing]] — INFORMS: timing and staging of reveals builds on weight principles
- [[texture-materiality]] — EXTENDS: visual weight signals (shadows, depth) complement motion weight

---

## Deep Reference

- **When** writing Framer Motion or SwiftUI spring code and need exact stiffness/damping/mass values for a weight class → **read** `research-data/animation_physical_weight.md` §2 (Spring Constants by Element Weight Class) **for** copy-paste Framer Motion syntax per weight class (e.g., tooltip: `stiffness: 450, damping: 32, mass: 0.7`), Apple SwiftUI `.spring(response:dampingFraction:)` equivalents, and Figma named preset mapping (Gentle=Heavy, Quick=Light, Bouncy=off-chart, Slow=Ultra-heavy)
- **When** deciding how much overshoot (y2) a heavy modal vs a light badge should have → **read** `research-data/animation_physical_weight.md` §9 (The Overshoot Paradox) **for** why the physics-correct answer (heavy bounces more) is wrong for UI convention, with the exact y2 values that maintain authority (1.03-1.05 for heavy) vs playfulness (1.3-1.56 for light)
- **When** building a card press or number counter reveal and need exact scaleX/scaleY keyframe values → **read** `research-data/animation_12_principles.md` §1 (Squash and Stretch) **for** three CSS implementation recipes with exact keyframe percentages, cubic-bezier values, and duration per interaction type
- **When** deciding if a 200px-travel animation should be 300ms or 500ms → **read** `research-data/animation_physical_weight.md` §4 (Duration Scaling) **for** the distance adjustment formula (+30-50ms per 100px beyond 30px) and the secondary action timing rules (start 100-300ms after primary, max 15% visual weight)

---

## Open Questions

- The overshoot paradox (physics says heavy bounces more, UI convention says less) has not been A/B tested -- the convention may be wrong for certain contexts
- Cross-cultural validity of "natural feel" from physics-based motion is assumed, not tested
- Whether stagger delays below 200ms total are always preferred may shift as reduced-motion preference usage grows (sunset condition: when reduced-motion exceeds 20% in analytics)
- The spring-to-weight mapping is inferred from first principles, not confirmed by user testing directly measuring perceived weight
