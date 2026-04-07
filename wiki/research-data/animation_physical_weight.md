# Physical Weight and Mass in CSS/JS Animation
**Date:** 2026-03-22
**Research scope:** Disney 12 principles applied to web UI, spring physics parameters, stagger organics, weight-scaled easing curves, element-class motion rules, Web Animations API techniques
**Sources:** existing library (animation_12_principles.md, animation_motion_curves.md, animation_choreography.md) cross-referenced against targeted web searches on spring weight, stagger organics, NNGroup duration scaling, Framer Motion defaults, Motion.dev, GSAP stagger easing
**Prior art:** animation_motion_curves.md covers spring physics fundamentals and cubic-bezier math (2026-03-22). animation_12_principles.md covers all 12 Disney principles with CSS implementations (2026-03-22). animation_choreography.md covers stagger patterns and conductor model (2026-03-22). This document synthesizes those into the specific lens of perceived weight: how element class (heavy/medium/light) maps to spring constants, duration, easing, and stagger behavior.
**Claim tagging:** [VERIFIED] = from primary source or canonical documentation. [SECONDARY] = practitioner consensus, design system docs. [INFERRED] = reasoned from first principles; no direct citation.

---

## Table of Contents

1. Disney Principles → Web UI: The Four Weight-Relevant Principles
2. Spring Constants by Element Weight Class
3. Easing Curves by Weight Class (cubic-bezier values)
4. Duration Scaling by Element Size
5. Stagger: Organic vs Mechanical Timing
6. Heavy vs Light Element Motion Rules
7. Web Animations API and CSS Techniques
8. Implementation Reference (summary table)
9. Falsifiability
10. Shared Assumptions

---

## 1. Disney Principles That Map to Perceived Weight

Four of the 12 principles are directly load-bearing for weight simulation. The other eight contribute but are not weight-specific.

### 1a. Slow In and Slow Out

The foundational weight principle. Duration + easing curve together determine perceived mass.

**Physical ground truth:** Heavy objects accelerate and decelerate slowly. Light objects accelerate and decelerate quickly. This is Newton's second law (F = ma): for the same force, high mass = low acceleration.

**Web translation:**

| Weight | Slow-in behavior | Slow-out behavior | Result |
|--------|-----------------|-------------------|--------|
| Heavy | Long ease-in: slow initial acceleration | Long ease-out: slow final deceleration | Long total duration, most movement in middle |
| Medium | Moderate ease-in | Moderate ease-out | Standard UI feel, 250-400ms |
| Light | Short ease-in: jumps to speed quickly | Short ease-out: arrives abruptly or with spring snap | Short duration, overshoot feels natural |

**Keyframe spacing as weight signal** [VERIFIED — animation_12_principles.md line 795]:

```css
/* LIGHT: 60% of distance covered in first 20% of time */
@keyframes lightEnter {
  0%   { transform: translateY(20px); }
  20%  { transform: translateY(8px); }   /* covers 60% of distance early */
  60%  { transform: translateY(1.5px); }
  100% { transform: translateY(0); }
}

/* HEAVY: only 15% of distance in first 40% of time */
@keyframes heavyEnter {
  0%   { transform: translateY(40px); }
  40%  { transform: translateY(34px); }  /* barely moved — building momentum */
  70%  { transform: translateY(16px); }
  100% { transform: translateY(0); }
}
```

### 1b. Anticipation

A backward dip before the main action. Communicates that an element has mass — something with no mass changes direction instantly.

**Weight relationship:** The larger the anticipation dip, the heavier the element feels. A light badge might use 2% anticipation. A heavy modal might use 5%.

**CSS mechanism:** Negative y-values in cubic-bezier (`y1 < 0`) cause the property to briefly move backward before proceeding [VERIFIED — animation_motion_curves.md]:

```css
/* Light element: minimal anticipation — barely perceptible */
--anticipation-light: cubic-bezier(0.36, -0.1, 0.64, 1);

/* Heavy element: visible anticipation — you feel the weight gathering */
--anticipation-heavy: cubic-bezier(0.36, -0.3, 0.66, 1.3);
```

**Duration for anticipation phase** [VERIFIED — animation_12_principles.md line 184]:
- Anticipation phase: 15-30% of total animation duration
- Total animation duration including anticipation: add 20-30% to base duration
- Do not use on every element — reserve for primary/heavy elements only

### 1c. Follow-Through and Overlapping Action

Elements with mass do not stop instantly. They overshoot and return.

**The follow-through signal for weight:**
- Heavy elements: larger overshoot, slower return to rest
- Light elements: smaller overshoot, faster return, or no overshoot (snaps)

**Three mechanisms** [VERIFIED — animation_12_principles.md]:

1. **Cubic-bezier overshoot** (y2 > 1): Simplest. One smooth arc that exceeds target and returns.
   - Light: `cubic-bezier(0.34, 1.3, 0.64, 1)` — y2=1.3, subtle
   - Heavy: `cubic-bezier(0.34, 1.56, 0.64, 1)` — y2=1.56, more pronounced (counterintuitive — see Section 3 for why)

2. **Shadow delay** (secondary follow-through): The element stops but its drop-shadow continues to transition, arriving 30-60ms after:
   ```css
   .card {
     transition: transform 300ms ease-out,
                 filter 380ms ease-out 40ms; /* shadow lags = mass */
   }
   ```

3. **True spring** via `linear()`: Multiple direction reversals approximating real spring oscillation. Only achievable with CSS `linear()` or JS physics. [VERIFIED — animation_motion_curves.md Section 3]

### 1d. Secondary Action

A secondary action runs after the primary, reinforcing that the element has mass and the system responded.

**Weight application:** Heavy elements get more pronounced secondary actions. A modal appearing might cause a very faint background dimple-pulse. A small badge just fades in with no secondary.

**Rules** [VERIFIED — animation_12_principles.md line 763]:
- Secondary action starts 100-300ms AFTER primary
- Secondary opacity: maximum 15% of primary action's visual weight
- One secondary per primary. Never two.

---

## 2. Spring Constants by Element Weight Class

### The Physics Model

Three parameters govern spring feel [VERIFIED — animation_motion_curves.md Section 4]:

- **Stiffness (k):** How aggressively the spring pulls toward the target. High = snappy. Low = lazy.
- **Damping (c):** How much the oscillation is resisted. High = settles fast, no bounce. Low = oscillates multiple times.
- **Mass (m):** Virtual mass of the element. High = sluggish, takes time to accelerate. Low = responsive.

**Damping ratio** determines which regime the spring is in:
```
zeta = damping / (2 * sqrt(stiffness * mass))
zeta < 1 = underdamped (bouncy)
zeta = 1 = critically damped (clean, no bounce)
zeta > 1 = overdamped (sluggish)
```

### Weight Class Presets

These are calibrated for UI transitions on transform/opacity (GPU-safe). They are derived from Figma's named presets, Apple's SwiftUI recommendations, Motion.dev documentation, and Framer Motion defaults, cross-synthesized for the specific purpose of communicating element weight.

**[VERIFIED — Figma named presets from animation_motion_curves.md Section 4]**
**[VERIFIED — Framer Motion defaults: stiffness 100, damping 10, mass 1]**
**[INFERRED — weight-class mapping from first principles + Figma/Apple recommendations]**

| Element Class | Example Elements | Stiffness | Damping | Mass | Zeta (approx) | Character |
|--------------|-----------------|-----------|---------|------|----------------|-----------|
| Ultra-light | Tooltips, chip badges, count indicators | 400-500 | 28-35 | 0.6-0.8 | ~1.0 (critically damped) | Instant feel, no bounce |
| Light | Small buttons, icon animations, tab indicators | 300-380 | 22-28 | 0.8-1.0 | 0.8-1.0 | Snappy with subtle spring |
| Medium | Cards, list items, form panels | 180-250 | 18-22 | 1.0-1.2 | 0.7-0.9 | Natural, slightly bouncy |
| Heavy | Modals, drawers, hero sections | 100-150 | 15-20 | 1.5-2.0 | 0.6-0.8 | Deliberate, visible settle |
| Ultra-heavy | Full-page transitions, large overlays | 60-90 | 12-16 | 2.5-3.5 | 0.5-0.7 | Slow, weighty, consequential |

### Framer Motion / Motion.dev Syntax

```js
// Ultra-light (tooltip)
{ type: "spring", stiffness: 450, damping: 32, mass: 0.7 }

// Light (button, badge)
{ type: "spring", stiffness: 340, damping: 26, mass: 0.9 }

// Medium (card, list item)
{ type: "spring", stiffness: 220, damping: 20, mass: 1.1 }

// Heavy (modal, drawer)
{ type: "spring", stiffness: 120, damping: 17, mass: 1.8 }

// Ultra-heavy (page transition)
{ type: "spring", stiffness: 75, damping: 14, mass: 3.0 }
```

### Apple SwiftUI Equivalents [VERIFIED — Apple Developer docs via animation_motion_curves.md]

```swift
// Light
.spring(response: 0.25, dampingFraction: 0.9)

// Medium (Apple's default)
.spring(response: 0.55, dampingFraction: 0.825)

// Heavy
.spring(response: 0.85, dampingFraction: 0.75)
```

`response` = how quickly it tries to reach target (lower = faster = lighter feel)
`dampingFraction` = 1.0 is critically damped, lower = more bounce

### Figma Named Presets as Reference Points [VERIFIED — animation_motion_curves.md]

| Name | Stiffness | Damping | Mass | Maps to weight class |
|------|-----------|---------|------|---------------------|
| Gentle | 100 | 15 | 1 | Heavy |
| Quick | 300 | 20 | 1 | Light |
| Bouncy | 600 | 15 | 1 | Off-chart (exaggerated light) |
| Slow | 80 | 20 | 1 | Ultra-heavy |

---

## 3. Easing Curves by Weight Class (cubic-bezier)

When spring physics are not available (CSS-only, or simple transitions), cubic-bezier curves approximate weight. They cannot produce true oscillation but can produce a single overshoot arc.

**Key insight from existing research** [VERIFIED — animation_motion_curves.md Section 1]: y-values outside [0, 1] produce overshoot (y > 1) or anticipation (y < 0). This is the weight simulation mechanism in CSS.

### Weight Class Easing Map

| Weight Class | Entry curve | Exit curve | Duration (enter) | Duration (exit) |
|-------------|-------------|------------|------------------|-----------------|
| Ultra-light | `cubic-bezier(0.0, 0.0, 0.15, 1.0)` | `cubic-bezier(0.55, 0, 1, 0.45)` | 100-150ms | 80-120ms |
| Light | `cubic-bezier(0.0, 0.0, 0.3, 1.0)` | `cubic-bezier(0.4, 0, 1, 1)` | 150-220ms | 120-180ms |
| Medium | `cubic-bezier(0.16, 1, 0.3, 1)` | `cubic-bezier(0.5, 0, 0.75, 0)` | 250-350ms | 180-250ms |
| Heavy | `cubic-bezier(0.14, 0.0, 0.0, 1.0)` | `cubic-bezier(0.5, 0, 1, 0.5)` | 350-500ms | 250-350ms |
| Ultra-heavy | `cubic-bezier(0.45, 0.05, 0.55, 0.95)` | `cubic-bezier(0.55, 0.05, 0.55, 0.95)` | 500-700ms | 350-450ms |

**Note on heavy entry curve:** `cubic-bezier(0.14, 0.0, 0.0, 1.0)` has a very low x1 (0.14) meaning deceleration starts almost immediately. The element "lumbers in" — fast arrival, very long deceleration tail. This is the heavy-object signature: fast buildup to momentum (nature of gravity/inertia) but slow settling.

**Note on overshoot for heavy elements:** Counterintuitively, HEAVY objects in physical reality do overshoot when stopped by a spring — think of a car's suspension. If you want a modal to feel physically weighty, give it a slight spring overshoot on arrival (y2 slightly above 1.0). If you want it to feel rigid/formal, do not overshoot.

### CSS Custom Property System

```css
:root {
  /* Ultra-light: instant, no ceremony */
  --ease-enter-ultralight: cubic-bezier(0.0, 0.0, 0.15, 1.0);
  --ease-exit-ultralight:  cubic-bezier(0.55, 0, 1, 0.45);

  /* Light: snappy with subtle spring */
  --ease-enter-light:      cubic-bezier(0.0, 0.0, 0.3, 1.0);
  --ease-exit-light:       cubic-bezier(0.4, 0, 1, 1);
  --ease-spring-light:     cubic-bezier(0.34, 1.3, 0.64, 1); /* overshoot: 1.3 */

  /* Medium: standard UI — confident arrival */
  --ease-enter-medium:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-exit-medium:      cubic-bezier(0.5, 0, 0.75, 0);
  --ease-spring-medium:    cubic-bezier(0.34, 1.56, 0.64, 1); /* overshoot: 1.56 */

  /* Heavy: deliberate, lumbers in */
  --ease-enter-heavy:      cubic-bezier(0.14, 0.0, 0.0, 1.0);
  --ease-exit-heavy:       cubic-bezier(0.5, 0, 1, 0.5);

  /* Ultra-heavy: slow symmetric movement, consequential */
  --ease-enter-ultraheavy: cubic-bezier(0.45, 0.05, 0.55, 0.95);
  --ease-exit-ultraheavy:  cubic-bezier(0.55, 0.05, 0.55, 0.95);
}
```

---

## 4. Duration Scaling by Element Size

Duration communicates weight directly. NNGroup's research establishes the core rule [VERIFIED — NNGroup animation-duration article, referenced in search results]:

> Use longer durations when objects travel large distances or have dramatic changes in surface area. Use shorter durations for small changes. A UI animation sequence with larger elements looks better when it lasts longer.

### Duration Formula

No precise formula exists in the literature, but the pattern across Material Design, Apple HIG, and NNGroup converges on these approximate duration ranges [SECONDARY — cross-referenced from animation_motion_curves.md Section 5]:

| Element surface area (approx) | Element examples | Base entry duration | Base exit duration |
|-------------------------------|-----------------|--------------------|--------------------|
| <32px diameter / <1000px2 | Badge, indicator dot, small icon | 100-150ms | 80-100ms |
| 32-64px / 1000-4000px2 | Button, chip, tag | 150-220ms | 120-160ms |
| 64-200px / 4000-20000px2 | Card (compact), form field | 220-320ms | 160-240ms |
| 200-400px / 20000-80000px2 | Card (full), panel, tooltip | 280-400ms | 200-280ms |
| Full-screen / modal-sized | Drawer, modal, overlay | 350-500ms | 250-350ms |
| Page-level | Route transition, hero section | 400-600ms | 300-400ms |

**The exit rule holds at every level:** Exit is always faster than entry (60-70% of entry duration). The eye does not need to watch something leave — it needs to watch something arrive. [VERIFIED — animation_choreography.md, animation_12_principles.md Section 6]

### Distance-Based Duration Adjustment

Beyond surface area, travel distance also scales duration. Material Design's guidance [VERIFIED — animation_motion_curves.md Section 5]:

- Short 1-4: 50-200ms (micro-interactions, in-place state changes)
- Medium 1-4: 250-400ms (standard element transitions, most cards)
- Long 1-4: 450-600ms (page-level, elements crossing large viewport distance)

**Practical rule:** For every additional 100px of travel beyond 30px, add approximately 30-50ms to base duration. This is [INFERRED] from the Material Design duration token spacing, not a stated formula.

---

## 5. Stagger: Organic vs Mechanical

### The Mechanical Problem

Uniform stagger — every element delays by exactly X ms — creates a visible rhythm that reads as programmatic, not physical. It is the animation equivalent of a clock ticking: recognizably artificial.

### What Makes Stagger Organic

Three techniques, in order of impact:

**Technique 1: Apply an easing function to the delay distribution itself** [VERIFIED — Motion.dev stagger documentation, GSAP stagger `ease` property]

This is the least-known and most powerful technique. Instead of uniform spacing between element starts, the gaps themselves accelerate or decelerate.

```js
// GSAP: apply easing to the stagger distribution
gsap.to(".card", {
  opacity: 1,
  y: 0,
  stagger: {
    amount: 0.6,          // total spread across all elements
    ease: "power2.out"    // gaps start large, compress at end
  }
})

// Motion.dev: same concept
animate(".card",
  { opacity: 1, y: 0 },
  { delay: stagger(0.08, { ease: "easeOut" }) }
)
```

Result: first elements start with large gaps between them (feels like they're gathering), last elements arrive in quick succession (feels like they're landing together). Organic, not ticking.

**Technique 2: Vary individual element durations within the stagger** [INFERRED from overlapping action principle + GSAP documentation]

Instead of every element having the same 300ms duration, vary slightly (±10-20%). Light elements in the set can be slightly faster; heavy ones slightly slower. In a card grid, this reads as natural variation in material weight.

```js
cards.forEach((card, i) => {
  // Duration varies ±15% around the base
  const durationVariation = 0.85 + (Math.sin(i * 1.618) * 0.5 + 0.5) * 0.3;
  // Golden ratio (1.618) as index multiplier produces pseudo-organic, non-repeating variation
  card.style.transitionDuration = `${Math.round(280 * durationVariation)}ms`;
})
```

**Technique 3: Apply easing to the stagger delay using a sine distribution** [SECONDARY — Motion.dev, multiple practitioner sources]

```js
// Sine distribution: elements in the middle of a list start with slightly more delay
// than elements at the edges — creates a "breath" or wave through the list
function sineStagger(index, total, baseDelay) {
  const position = index / (total - 1); // 0 to 1
  const sineValue = Math.sin(position * Math.PI); // 0 → 1 → 0 arc
  return baseDelay * (1 + sineValue * 0.4); // 40% variation around base
}
```

### Mechanical Stagger vs Organic: Specific Thresholds

| Parameter | Mechanical (avoid) | Organic (target) |
|-----------|-------------------|-----------------|
| Delay between items | Exactly uniform (e.g., precisely 50ms each) | 30-80ms with easing distribution applied |
| Duration per item | Identical across all items | ±10-20% variation |
| Easing per item | Same easing on every item | Same curve family, slight variation on secondary elements |
| Max items before grouping | N/A | >7 items: switch from individual stagger to grouped burst |
| Stagger direction | Always left-to-right | Match reading order; radial from focal point for emphasis |

**The 30-80ms boundary** [VERIFIED — animation_choreography.md, multiple sources]:
- Below 30ms: gaps are imperceptible, might as well be simultaneous
- 30-80ms: cohesive, connected — feels like one system breathing
- 80-200ms: deliberate, counted — each element is its own moment
- Above 200ms: reads as page load, not animation

### Eased Delay Distribution Example (CSS-only fallback)

For CSS-only implementations where JS distribution is unavailable, use the "golden angle" approach to avoid visible repetition:

```css
/* 8-item list: delays approximating a power-out distribution */
.item:nth-child(1) { transition-delay: 0ms; }
.item:nth-child(2) { transition-delay: 45ms; }
.item:nth-child(3) { transition-delay: 85ms; }
.item:nth-child(4) { transition-delay: 120ms; }
.item:nth-child(5) { transition-delay: 150ms; }
.item:nth-child(6) { transition-delay: 175ms; }
.item:nth-child(7) { transition-delay: 195ms; }
.item:nth-child(8) { transition-delay: 210ms; }
/* Gaps shrink: 45, 40, 35, 30, 25, 20, 15 — power-out distribution */
/* Total spread: 210ms — any longer starts to feel like loading */
```

---

## 6. Heavy vs Light Element Motion Rules

These are element-class rules — a lookup table mapping element type to its motion contract.

### Rule Table

[INFERRED from spring parameter research, duration scaling, NNGroup duration research, animation_motion_curves.md emotional quality map, first principles of physics. Not verified against user testing.]

| Element | Weight Class | Entry duration | Entry easing | Overshoot | Stagger delay (in groups) | Secondary action |
|---------|-------------|---------------|--------------|-----------|--------------------------|-----------------|
| Tooltip | Ultra-light | 120ms | `cubic-bezier(0.0, 0.0, 0.15, 1.0)` | None | N/A | None |
| Badge / count chip | Ultra-light | 130ms | `cubic-bezier(0.34, 1.3, 0.64, 1)` | Subtle (1.3) | N/A | None |
| Icon button | Light | 150ms | `cubic-bezier(0.0, 0.0, 0.3, 1.0)` | None | N/A | Subtle scale pulse |
| Text label reveal | Light | 180ms | `cubic-bezier(0.0, 0.0, 0.3, 1.0)` | None | 30-50ms | None |
| Tab indicator | Light | 160ms | `cubic-bezier(0.0, 0.0, 0.15, 1.0)` | None | N/A | None |
| Chip / tag | Light | 180ms | `cubic-bezier(0.34, 1.3, 0.64, 1)` | Subtle (1.3) | 30-50ms | None |
| Form field | Medium | 220ms | `cubic-bezier(0.16, 1, 0.3, 1)` | None | 40-60ms | None |
| Compact card | Medium | 280ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Optional (1.3-1.4) | 50-70ms | Shadow settle |
| Full card | Medium-heavy | 320ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Optional (1.2) | 60-80ms | Shadow settle 40ms late |
| Sidebar panel | Heavy | 380ms | `cubic-bezier(0.14, 0.0, 0.0, 1.0)` | None (or 1.05) | N/A | Backdrop fade 60ms early |
| Modal | Heavy | 400ms | `cubic-bezier(0.14, 0.0, 0.0, 1.0)` | 1.03-1.05 | N/A | Backdrop, scrim |
| Bottom sheet | Heavy | 380ms | `cubic-bezier(0.14, 0.0, 0.0, 1.0)` | None | N/A | Backdrop |
| Drawer | Heavy | 420ms | `cubic-bezier(0.14, 0.0, 0.0, 1.0)` | None | N/A | Backdrop |
| Page transition | Ultra-heavy | 500ms | `cubic-bezier(0.45, 0.05, 0.55, 0.95)` | None | N/A | Background first |
| Hero section | Ultra-heavy | 550ms | `cubic-bezier(0.16, 1, 0.3, 1)` | None | 80-120ms groups | Grain/texture layer |

**The modal overshoot note:** A 1.03-1.05 overshoot on a modal makes it feel physically present — like something heavy that carries past its destination by a small amount. Without any overshoot, large modals feel like HTML rectangles appearing. The overshoot amount is tiny on screen (3-5% of the modal height) but perceptible as weight signal.

### Different Elements Moving Differently in the Same Scene

When cards and badges and a heading appear together, they should not all share the same spring:

```css
/* Heading: heavy, arrives with authority */
.section-heading {
  animation: 500ms cubic-bezier(0.14, 0.0, 0.0, 1.0) forwards headingIn;
}

/* Cards: medium weight, arrive in stagger */
.card {
  animation: 300ms cubic-bezier(0.16, 1, 0.3, 1) forwards cardIn;
  /* stagger via transition-delay */
}

/* Badges on cards: ultra-light, pop in after cards settle */
.badge {
  animation: 130ms cubic-bezier(0.34, 1.3, 0.64, 1) forwards badgeIn;
  animation-delay: calc(var(--card-delay) + 250ms); /* after card settles */
}
```

The heading lumbers in first. The cards cascade in with medium weight. The badges pop last, after cards are settled. Three weight classes, one scene, no uniform easing.

---

## 7. Web Animations API and CSS Techniques for Spring Motion

### Approach 1: CSS `linear()` (recommended for pure CSS springs)

[VERIFIED — animation_motion_curves.md Section 3, Chrome for Developers, Josh Comeau]

`linear()` is the CSS function that can approximate spring physics by providing 40+ data points describing the oscillation curve. Cubic-bezier cannot produce oscillation (only one smooth arc). `linear()` can.

**Browser support as of Mar 2026:** Chrome 113+, Firefox 112+, Edge 113+. Safari: No. Coverage ~88%.

```css
/* Spring bounce — light element (generated by tool) */
.badge-spring {
  transition: transform 400ms linear(
    0, 0.009, 0.035, 0.078, 0.138 15.4%,
    0.373, 0.654, 0.854, 0.968, 1.029,
    1.051 45.4%, 1.053, 1.038, 1.012 63.1%,
    0.990, 0.977, 0.971 73.3%, 0.973, 0.992,
    1.004, 1.008, 1.007, 1.002, 0.999, 1
  );
}

/* Fallback for Safari: cubic-bezier approximation */
@supports not (animation-timing-function: linear(0, 1)) {
  .badge-spring {
    transition: transform 400ms cubic-bezier(0.34, 1.3, 0.64, 1);
  }
}
```

**Generating `linear()` values:** Do not hand-write. Use:
- Jake Archibald's linear() generator: https://linear-easing-generator.netlify.app
- CSS Spring Easing Generator: https://www.kvin.me/css-springs

Input spring parameters (stiffness, damping, mass), get CSS output.

### Approach 2: Web Animations API (WAAPI) with JS spring solver

The WAAPI allows JavaScript to drive keyframe animations without CSS. For spring motion, use a JS spring solver to generate the keyframe array at runtime.

```js
// Spring solver — produces keyframes for WAAPI
function solveSpring(stiffness, damping, mass, precision = 40) {
  let position = 0, velocity = 0;
  const target = 1;
  const dt = 1 / precision;
  const keyframes = [];

  for (let i = 0; i <= precision; i++) {
    const force = -stiffness * (position - target);
    const dampingForce = -damping * velocity;
    const acceleration = (force + dampingForce) / mass;
    velocity += acceleration * dt;
    position += velocity * dt;
    keyframes.push({ transform: `translateY(${(1 - position) * 40}px)`, opacity: position });
  }

  return keyframes;
}

// Apply to element — heavy card
const keyframes = solveSpring(120, 17, 1.8); // heavy card params
element.animate(keyframes, {
  duration: 500,    // duration is separate from spring params in WAAPI
  fill: 'forwards',
  easing: 'linear' // keyframes already encode the curve
});
```

**Important limitation** [VERIFIED — web search results 2026-03-22]: CSS `transition` duration and spring physics are architecturally incompatible. In real spring physics, duration emerges from the physics (the spring settles when it settles). CSS requires a fixed duration. The WAAPI and `linear()` generator solve this by pre-computing the spring's time-to-settle and baking that as the animation duration.

### Approach 3: Framer Motion / Motion.dev (React and vanilla)

The simplest path for production. Spring parameters map directly to element weight class.

```js
// React (Framer Motion)
import { motion } from 'framer-motion';

// Heavy modal
<motion.div
  initial={{ y: 40, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  transition={{ type: "spring", stiffness: 120, damping: 17, mass: 1.8 }}
>

// Light badge
<motion.span
  initial={{ scale: 0.7, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: "spring", stiffness: 450, damping: 32, mass: 0.7 }}
>
```

```js
// Vanilla JS (Motion.dev)
import { animate, spring } from "motion";

// Medium card
animate(card, { y: [20, 0], opacity: [0, 1] }, {
  type: spring({ stiffness: 220, damping: 20, mass: 1.1 })
});
```

### Approach 4: CSS `transition` with cubic-bezier (Safari-safe fallback)

When `linear()` is not available, cubic-bezier approximates a single-bounce spring:

```css
/* Good enough for most UI contexts — one smooth arc with single overshoot */
.modal {
  transition: transform 420ms cubic-bezier(0.14, 0.0, 0.04, 1.03),
              opacity 320ms ease-out;
}

/* Note: cubic-bezier overshoot y2=1.03 adds only 3% overshoot — very subtle */
/* y2=1.56 (Framer's "playful" default) is for light elements, not heavy ones */
```

---

## 8. Implementation Reference

### Spring Constants Reference (complete table)

| Weight Class | Stiffness | Damping | Mass | Duration | Overshoot (y2) |
|-------------|-----------|---------|------|----------|-----------------|
| Ultra-light | 450 | 32 | 0.7 | 100-150ms | 1.3 |
| Light | 340 | 26 | 0.9 | 150-220ms | 1.3-1.4 |
| Medium | 220 | 20 | 1.1 | 250-350ms | 1.4-1.56 |
| Heavy | 120 | 17 | 1.8 | 350-500ms | 1.03-1.05 |
| Ultra-heavy | 75 | 14 | 3.0 | 500-700ms | None |

### Easing Curves (cubic-bezier) Reference

```css
/* By weight class */
--enter-ultralight: cubic-bezier(0.0, 0.0, 0.15, 1.0);   /* tooltip, indicator */
--enter-light:      cubic-bezier(0.0, 0.0, 0.3, 1.0);    /* button, chip */
--enter-medium:     cubic-bezier(0.16, 1, 0.3, 1);        /* card, panel */
--enter-heavy:      cubic-bezier(0.14, 0.0, 0.0, 1.0);   /* modal, drawer */
--enter-ultraheavy: cubic-bezier(0.45, 0.05, 0.55, 0.95); /* page transition */

/* Spring overshoot variants (single-bounce) */
--spring-subtle:    cubic-bezier(0.34, 1.3, 0.64, 1);    /* light elements */
--spring-medium:    cubic-bezier(0.34, 1.56, 0.64, 1);   /* medium elements */
--spring-heavy:     cubic-bezier(0.34, 1.05, 0.64, 1);   /* heavy elements, subtle */

/* Exits: always ease-in, faster than entrance */
--exit-light:       cubic-bezier(0.4, 0, 1, 1);
--exit-medium:      cubic-bezier(0.5, 0, 0.75, 0);
--exit-heavy:       cubic-bezier(0.5, 0, 1, 0.5);
```

### Duration Rules

| Scenario | Duration |
|----------|----------|
| Same element, small state change | 100-150ms |
| Small element entering | 120-180ms |
| Medium element entering | 250-350ms |
| Large element entering | 380-500ms |
| Page-level transition | 450-600ms |
| Any exit | 60-70% of corresponding entry duration |
| Stagger spread across 5-7 items | 150-300ms total |
| Secondary action delay after primary | 100-300ms |

---

## 9. Falsifiability

| Finding | What would disprove it |
|---------|----------------------|
| Heavier elements need longer durations | User testing showing users rate short-duration large-element animations as more natural than long-duration ones |
| Low stiffness + high mass = heavy feel | Spring physics is a mathematical model — the "feel" interpretation is [INFERRED]. User studies testing stiffness/mass vs perceived weight labels could disprove the mapping |
| Overshoot y2=1.03-1.05 adds weight signal for modals | A/B test showing users rate overshot modals as lighter or less authoritative than non-overshot modals |
| Easing on stagger delay produces organic feel vs uniform | User testing comparing eased-delay stagger vs uniform stagger on naturalness ratings |
| Exit should be 60-70% of entry duration | Contexts where slow exits are intentional (farewell states, consequence signaling) — the rule breaks for narrative sequences |
| `linear()` spring on `transform` has no performance cost vs cubic-bezier | Benchmarks showing measurable frame drop on low-end devices with complex `linear()` values |
| Heavy elements overshoot less than light elements | Physical counterexample: an underdamped heavy spring in real life oscillates more. The UI convention (heavy = less overshoot) is a DESIGN choice for authority/stability, not a physics fact |

The last point is a genuine tension worth flagging. In real spring physics, a heavy underdamped spring bounces more (harder to stop). In UI convention, heavy elements overshoot less because overshoot reads as playfulness, and heavy/authoritative elements (modals, drawers) should not feel playful. The design convention and physical reality go in opposite directions here for the underdamped case.

---

## 10. Shared Assumptions

1. **"Natural feel" transfers cross-culturally.** All sources assume that physics-based motion feels natural to all users. No cross-cultural evidence. [ASSUMED across all sources]

2. **Spring physics maps to perceived weight.** The claim that high mass + low stiffness reads as "heavy" to users is [INFERRED] from first principles. The physics model describes mechanical behavior; whether users perceive the intended weight class is not confirmed by user testing in the cited sources.

3. **GPU compositing removes performance concern.** All sources assume that animating transform/opacity is essentially free. This breaks at high layer counts, under memory pressure, or on thermal-throttled mobile devices.

4. **The overshoot-as-playfulness signal is stable.** If a product category normalizes heavy overshoot (like highly consumer-facing fitness apps), the convention may shift — overshoot could start to signal category/genre rather than element weight.

5. **Stagger delays below 200ms total are always preferred.** NNGroup data is from 2015-2019. As motion literacy increases and reduced-motion preferences grow, users may prefer faster or no staggers. Sunset condition: when reduced-motion usage exceeds 20% in analytics, reconsider stagger strategies.

---

## Sources

**Internal (existing research library):**
- `/root/healthcalculators-full/tools/research-data/animation_motion_curves.md` — spring physics fundamentals, cubic-bezier math, linear() implementation (2026-03-22)
- `/root/healthcalculators-full/tools/research-data/animation_12_principles.md` — all 12 Disney principles with CSS implementations (2026-03-22)
- `/root/healthcalculators-full/tools/research-data/animation_choreography.md` — stagger patterns, conductor model (2026-03-22)

**External:**
- [Executing UX Animations: Duration and Motion Characteristics — NNGroup](https://www.nngroup.com/articles/animation-duration/)
- [A Friendly Introduction to Spring Physics Animation in JavaScript — Josh W. Comeau](https://www.joshwcomeau.com/animation/a-friendly-introduction-to-spring-physics/)
- [Springs and Bounces in Native CSS — Josh W. Comeau](https://www.joshwcomeau.com/animation/linear-timing-function/)
- [Designing spring animations for the web — Felix Runquist](https://felixrunquist.com/posts/designing-spring-animations-for-the-web)
- [Effortless UI Spring Animations: A Two-Parameter Approach — kvin.me](https://www.kvin.me/posts/effortless-ui-spring-animations)
- [spring — JS and CSS spring generation — Motion.dev](https://motion.dev/docs/spring)
- [React transitions — Configure Motion animations — Motion.dev](https://motion.dev/docs/react-transitions)
- [stagger — Stagger the delay of multiple animations — Motion.dev](https://motion.dev/docs/stagger)
- [Staggers — GSAP Docs](https://gsap.com/resources/getting-started/Staggers/)
- [The physics behind spring animations — Maxime Heckel](https://blog.maximeheckel.com/posts/the-physics-behind-spring-animations/)
- [Understanding easing and cubic-bezier curves in CSS — Josh Collinsworth](https://joshcollinsworth.com/blog/easing-curves)
- [Easing functions — Motion.dev](https://motion.dev/docs/easing-functions)
- [Crafting Easing Curves for User Interfaces — Ryan Brownhill, Medium](https://medium.com/@ryan_brownhill/crafting-easing-curves-for-user-interfaces-34f39e1b4a43)
- [Framer Motion spring defaults — unpkg.com framer-motion types](https://unpkg.com/browse/framer-motion@3.6.1/types/types.d.ts)
- [Duration & Easing — Material Design 1](https://m1.material.io/motion/duration-easing.html)
- [The Subtle Power of Delay in Cascading Animation Timing — PapiRicoSF](https://papiricosf.com/cascading-animation-timing/)
- [Create complex animation curves in CSS with linear() — Chrome for Developers](https://developer.chrome.com/docs/css-ui/css-linear-easing-function)
- [spring() — Apple Developer SwiftUI](https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:))
- [Prototype easing and spring animations — Figma Help Center](https://help.figma.com/hc/en-us/articles/360051748654-Prototype-easing-and-spring-animations/)
