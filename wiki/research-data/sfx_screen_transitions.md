# Screen Transitions & Visual Effects Research
## The Craft of Making One State Flow Into Another Cinematically

**Date:** 2026-03-22
**Researcher:** Claude (Sonnet 4.6)
**Method:** 14 targeted web searches across MDN, Chrome DevRel, CSS-Tricks, Codrops, Smashing Magazine, GSAP docs, and SVG/filter references.
**Use case context:** Product demo animations, brand film sequences, calculator state transitions, Pulse onboarding flows.
**Prior context read:** brand_film_motion_techniques_v1.md, scroll_animation_research.md (both checked — this file covers distinct territory: the moment of state change, not ongoing scroll or video generation)

---

## Uncertainty Flags

- Apple and Stripe transition descriptions are inferred from editorial analysis and secondhand study — no official technique breakdowns exist. [ASSUMED — consistent across multiple independent analysis sources]
- Browser support figures sourced from caniuse + Chrome DevRel blog, cross-referenced against MDN. [VERIFIED at search time — check before shipping]
- CSS code patterns are synthesized from MDN, CSS-Tricks, and Codrops documentation. [SECONDARY — verify against MDN before implementation]
- GSAP ScrollTrigger zoom-layer technique described from Codrops article (Oct 2025) — specific keyframe values not available without WebFetch. [DIRECTIONAL]
- SVG filter liquid/displacement technique confirmed from Codrops Morphing Page Transition repo + MDN filter primitive docs. [VERIFIED from two independent sources]

---

## Section 1 — Wipe Transitions: clip-path Animations

### 1.1 What clip-path Does

`clip-path` defines a visible region on an element. Anything outside the clip is hidden. Animating the clip shape over time creates the illusion of content being "wiped on" or "revealed."

The critical rule: **you must use the same shape function in every keyframe.** Animating `inset()` to `circle()` fails. Both keyframes must be `inset()` or both must be `polygon()`.

### 1.2 The Four Wipe Shapes

| Shape Function | Syntax | Best For |
|---|---|---|
| `inset()` | `inset(top right bottom left)` | Directional wipes (up, down, left, right) |
| `circle()` | `circle(radius at cx cy)` | Circular reveal from a point (spotlight, iris) |
| `ellipse()` | `ellipse(rx ry at cx cy)` | Asymmetric radial reveals |
| `polygon()` | `polygon(x1 y1, x2 y2, ...)` | Diagonal wipes, curtain splits, geometric reveals |

### 1.3 Core Wipe Patterns (code-level)

**Bottom-up reveal (most common for UI cards):**
```css
.reveal {
  clip-path: inset(100% 0 0 0); /* fully hidden: top clipped */
  animation: wipe-up 0.8s cubic-bezier(0.77, 0, 0.175, 1) forwards;
}
@keyframes wipe-up {
  from { clip-path: inset(100% 0 0 0); }
  to   { clip-path: inset(0% 0 0 0); }
}
```

**Left-to-right wipe (cinematic curtain):**
```css
@keyframes wipe-right {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0% 0 0); }
}
```

**Circular iris reveal (Apple keynote-style spotlight):**
```css
@keyframes iris-open {
  from { clip-path: circle(0% at 50% 50%); }
  to   { clip-path: circle(150% at 50% 50%); } /* 150% ensures full coverage at all aspect ratios */
}
```
Variant: iris from corner (more dramatic)
```css
from { clip-path: circle(0% at 0% 0%); }
to   { clip-path: circle(200% at 0% 0%); }
```

**Diagonal wipe (premium, less common):**
```css
@keyframes diagonal-wipe {
  from { clip-path: polygon(0 0, 0 0, 0 100%, 0 100%); }
  to   { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
}
```

**Curtain split (two panels opening):**
Use two overlay elements (left half, right half), both inset to center from their respective sides:
```css
.curtain-left  { clip-path: inset(0 50% 0 0); animation: curtain-left 0.9s ease forwards; }
.curtain-right { clip-path: inset(0 0 0 50%); animation: curtain-right 0.9s ease forwards; }
@keyframes curtain-left  { to { clip-path: inset(0 100% 0 0); } }
@keyframes curtain-right { to { clip-path: inset(0 0 0 100%); } }
```

### 1.4 Performance Notes

clip-path animates on the compositor thread — no layout or paint. It is one of the cheapest visual effects in CSS. `overflow: clip` on the parent prevents overdraw artifacts at polygon corners. The `-webkit-clip-path` vendor prefix is still needed for older Safari.

### 1.5 Easing for Wipes

- Hard wipes (0-duration feel): `steps(1)` — instant cut with shaped edges
- Premium reveals: `cubic-bezier(0.77, 0, 0.175, 1)` — slow start, fast through, controlled stop
- Organic wipes: `cubic-bezier(0.25, 0.46, 0.45, 0.94)` — ease-out variant, feels physical

---

## Section 2 — Morph Transitions: Element A Becomes Element B

### 2.1 The Principle

Morphing gives visual continuity to a state change where the content itself changes — a button becomes a modal, a card expands to full-screen, an icon transitions to a label. The eye follows the shared geometry. No cut — the viewer understands the new state is the same object.

### 2.2 CSS/DOM Morph (FLIP Technique)

**FLIP = First, Last, Invert, Play.** The only correct way to morph DOM elements without JavaScript animation libraries.

```javascript
// First: record starting position
const first = el.getBoundingClientRect();

// Last: apply final class/state
el.classList.add('expanded');
const last = el.getBoundingClientRect();

// Invert: calculate difference, apply as transform so element appears at original position
const dx = first.left - last.left;
const dy = first.top - last.top;
const dw = first.width / last.width;
const dh = first.height / last.height;
el.style.transform = `translate(${dx}px, ${dy}px) scale(${dw}, ${dh})`;
el.style.transformOrigin = 'top left';

// Play: animate transform back to identity
el.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
requestAnimationFrame(() => {
  el.style.transform = '';
});
```

This works for: card → modal, thumbnail → full-screen, small button → expanded panel.

### 2.3 View Transitions API — Native Browser Morph (2025)

The View Transitions API handles element-to-element morphing natively in modern browsers with zero manual FLIP math.

**How it works:**
1. Browser takes a screenshot of the current state
2. Your callback updates the DOM to the new state
3. Browser takes a screenshot of the new state
4. Browser animates between the two screenshots using CSS animations

**Same-document morph (SPA-style):**
```javascript
document.startViewTransition(() => {
  // Make your DOM changes here
  modal.classList.add('visible');
  card.classList.add('hidden');
});
```

**Named element morph (key feature):**
Assign the same `view-transition-name` to an element in the old state and the new state. The browser morphs position, size, and content between them automatically:
```css
/* On the card (old state) */
.card-thumbnail {
  view-transition-name: hero-image;
}

/* On the modal (new state) */
.modal-hero {
  view-transition-name: hero-image;
}
```

**Customizing the morph animation:**
```css
/* Override default cross-fade with custom keyframes */
::view-transition-old(hero-image) {
  animation: fade-out 0.3s ease forwards;
}
::view-transition-new(hero-image) {
  animation: scale-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
```

**Cross-document transitions (MPA — no JavaScript needed):**
```css
/* Add to BOTH the leaving page and the arriving page */
@view-transition {
  navigation: auto;
}

/* On elements that persist between pages */
.nav-logo { view-transition-name: site-logo; }
```

### 2.4 Browser Support (verified 2025)

| Feature | Chrome | Edge | Safari | Firefox |
|---|---|---|---|---|
| Same-document transitions | 111+ | 111+ | 18+ | 144+ |
| Cross-document (MPA) | 126+ | 126+ | 18.2+ | Not yet |
| `view-transition-class` | 125+ | 125+ | Not yet | Not yet |
| `view-transition-types` | 125+ | 125+ | Not yet | Not yet |

Same-document transitions are now **Baseline Newly Available** (October 14, 2025) — meaning all three major browser engines support them.

### 2.5 SVG Path Morphing (Shape A → Shape B)

When the transition requires actual geometry to change — a circle becoming a rectangle, a check becoming an X — only SVG path morphing can do it.

**Constraint:** Both paths must have the same number of anchor points. Different point counts = jump, not morph.

**With GSAP MorphSVG:**
```javascript
gsap.to('#shape-a', {
  morphSVG: '#shape-b',
  duration: 0.6,
  ease: 'power2.inOut'
});
```

**With Flubber (handles incompatible paths by interpolating):**
```javascript
import { interpolate } from 'flubber';
const interpolator = interpolate(pathA, pathB);
// Returns function(t) => SVG path string for 0 <= t <= 1
```

**With SMIL (native SVG, no library, limited browser support):**
```html
<path d="M10,10 L90,10 L90,90 L10,90">
  <animate attributeName="d"
    from="M10,10 L90,10 L90,90 L10,90"
    to="M50,10 L90,50 L50,90 L10,50"
    dur="0.5s" fill="freeze" />
</path>
```

---

## Section 3 — Mask Reveals: Shaped Windows Over Content

### 3.1 clipPath vs mask — When to Use Which

| | `clip-path` (CSS) | `<clipPath>` (SVG) | `<mask>` (SVG) |
|---|---|---|---|
| Shape control | Basic shapes + polygon | Arbitrary SVG shapes | Arbitrary SVG + gradients |
| Stroke support | No | No | Yes |
| Gradient support | No | No | Yes |
| Complexity | Low | Medium | High |
| Performance | Compositor thread | Good | Good |

**Rule:** Use CSS `clip-path` for simple geometric reveals. Use SVG `<clipPath>` for complex shapes (stars, logos, custom paths). Use SVG `<mask>` when you need gradient fade-outs, strokes, or luminance-based transparency.

### 3.2 SVG clipPath Animated Reveal

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="reveal-mask">
      <rect id="mask-rect" x="0" y="-100%" width="100%" height="100%" />
    </clipPath>
  </defs>
</svg>

<div class="content" style="clip-path: url(#reveal-mask)">
  <!-- revealed content -->
</div>
```
```javascript
// Animate the mask rect downward to reveal content
gsap.to('#mask-rect', { y: '100%', duration: 0.8, ease: 'power2.out' });
```

### 3.3 Shaped Mask Reveal (logo, circle, custom path)

Codrops approach: animate the SVG path `d` attribute inside a `<clipPath>`. The clip shape morphs while the content behind it becomes visible:

```html
<clipPath id="shape-reveal">
  <path id="reveal-path" d="M 50 50 L 50 50 L 50 50 Z" /> <!-- collapsed -->
</clipPath>
```
Animate the path from collapsed triangle to full coverage — content inside the clip region appears to be "drawn" by the shape.

### 3.4 CSS Mask (gradient fade-in from edge)

`mask-image` and `mask-composite` give gradient-based reveals that `clip-path` cannot:

```css
.reveal {
  mask-image: linear-gradient(to right, transparent 0%, black 100%);
  mask-size: 200% 100%;
  mask-position: 100% 0;
  transition: mask-position 0.8s ease;
}
.reveal.active {
  mask-position: 0% 0;
}
```
This slides the gradient from right to left, making content appear to materialize from an invisible-to-visible gradient.

---

## Section 4 — View Transitions API: The Recommended Path for Web UIs

See Section 2.3 and 2.4 for full code. Summary of when to use it vs alternatives:

| Scenario | Best Tool |
|---|---|
| SPA route change with shared element morph | View Transitions API + `view-transition-name` |
| MPA navigation with persistent nav/logo | View Transitions API + `@view-transition` rule |
| Card expands to modal (same page) | View Transitions API OR FLIP |
| Complex multi-element choreography | GSAP + View Transitions API combined |
| Need to support Safari < 18 / Firefox < 144 | FLIP + CSS transition fallback |
| Shape changes (not just position/size) | SVG morphing (GSAP MorphSVG or Flubber) |

**Progressive enhancement pattern:**
```javascript
if (document.startViewTransition) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM(); // instant, no transition — still functional
}
```

---

## Section 5 — Glitch/Distortion Transitions

### 5.1 What It Is

Glitch simulates digital corruption: chromatic aberration (RGB channels splitting), scan-line artifacts, random clip jumps, step-function timing. Used as a transition into a scene (corruption resolves into clarity) or as a state-change punctuation (something breaks, something new appears).

**When to use it in health/Pulse context:** Entering from a broken/confused state into clarity. "System failure → Pulse fixes it." Before/after framing.

### 5.2 The Core Technique

Three stacked pseudo-elements, each with different clip-path animation and color channel shift:

```html
<div class="glitch" data-text="YOUR TEXT">YOUR TEXT</div>
```

```css
.glitch {
  position: relative;
}
.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
.glitch::before {
  color: #ff0000;
  left: 2px;
  text-shadow: -2px 0 cyan;
  animation: glitch-1 0.4s steps(1) infinite;
}
.glitch::after {
  color: #00ffff;
  left: -2px;
  text-shadow: 2px 0 red;
  animation: glitch-2 0.4s steps(1) infinite reverse;
}
@keyframes glitch-1 {
  0%   { clip-path: inset(20% 0 60% 0); transform: translate(-2px, 0); }
  20%  { clip-path: inset(70% 0 5% 0);  transform: translate(2px, 0); }
  40%  { clip-path: inset(40% 0 30% 0); transform: translate(0, 0); }
  60%  { clip-path: inset(10% 0 80% 0); transform: translate(-2px, 2px); }
  80%  { clip-path: inset(55% 0 15% 0); transform: translate(2px, -2px); }
  100% { clip-path: inset(20% 0 60% 0); transform: translate(-2px, 0); }
}
@keyframes glitch-2 { /* offset variant of glitch-1 */ ... }
```

The `steps(1)` timing function is what makes it look digital, not smooth. The values inside `clip-path: inset()` should be randomized across keyframes — random-looking patterns read as genuine corruption.

### 5.3 Glitch as a Transition (not just a loop)

Use `animation-iteration-count: 1` + `animation-fill-mode: forwards` to trigger glitch once, then resolve cleanly. Pair with View Transitions API: start the glitch, start the view transition, cancel the glitch at transition completion.

```javascript
el.classList.add('glitching');
document.startViewTransition(() => {
  updateDOM();
}).ready.then(() => {
  el.classList.remove('glitching');
});
```

### 5.4 Image Glitch (for screen/frame transitions)

Three-image stack technique: same image three times, each animated independently with different clip-path offsets:

```css
.glitch-layer-1 { animation: glitch-strip 0.3s steps(1) 3; animation-delay: 0s; }
.glitch-layer-2 { animation: glitch-strip 0.3s steps(1) 3; animation-delay: 0.05s; mix-blend-mode: screen; }
.glitch-layer-3 { animation: glitch-strip 0.3s steps(1) 3; animation-delay: 0.1s;  mix-blend-mode: multiply; }
```

---

## Section 6 — Parallax Transitions: Layers at Different Speeds

### 6.1 The Principle

Parallax uses depth-of-field as a metaphor. Background moves slow (far away), foreground moves fast (close). The speed differential creates the illusion of 3D space on a 2D plane. In transitions, it means: multiple layers of content move at different rates as the "camera" moves between states.

### 6.2 CSS-Only Parallax (Scroll-Driven, 2025 approach)

The modern approach uses `animation-timeline: scroll()` — no JavaScript:

```css
@keyframes parallax-bg {
  from { transform: translateY(0); }
  to   { transform: translateY(-30%); } /* slower movement */
}
@keyframes parallax-fg {
  from { transform: translateY(0); }
  to   { transform: translateY(-80%); } /* faster movement */
}

.background { animation: parallax-bg linear; animation-timeline: scroll(); }
.foreground { animation: parallax-fg linear; animation-timeline: scroll(); }
```

Supported: Chrome 115+, Edge 115+, Safari 18+. Firefox partial (117+).

### 6.3 JavaScript Parallax (highest compatibility, precise control)

```javascript
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  document.querySelector('.bg').style.transform = `translateY(${scrollY * 0.3}px)`;
  document.querySelector('.mg').style.transform = `translateY(${scrollY * 0.5}px)`;
  document.querySelector('.fg').style.transform = `translateY(${scrollY * 0.7}px)`;
}, { passive: true });
```
Speed multipliers: 0.1–0.3 = deep background, 0.4–0.6 = mid-ground, 0.7–0.9 = foreground.

### 6.4 GSAP Parallax Transition (between scenes, not just scroll)

To parallax-transition between two full-screen sections on a button click or scroll snap:

```javascript
const tl = gsap.timeline();
tl.to('.scene-1-bg', { y: '-20%', duration: 1 })
  .to('.scene-1-fg', { y: '-60%', duration: 1 }, '<')
  .from('.scene-2-bg', { y: '20%', duration: 1 }, '<0.2')
  .from('.scene-2-fg', { y: '60%', duration: 1 }, '<');
```

The result: scene 1 layers drift away at different speeds, scene 2 layers drift in from opposite directions at different speeds. Feels like moving through physical space.

---

## Section 7 — Zoom Transitions: Scaling Into a Detail That Becomes the Next Scene

### 7.1 The Cinematic Logic

Zoom transitions are used in film to say: "the thing we just showed you in wide shot — we're going closer, and what you'll find there is the next story." Used extensively in Apple product demos (zoom into the chip, the camera module, the screen), in data visualization (zoom from world map into a city), and in brand films.

### 7.2 CSS Scale Zoom (simplest version)

```css
.zoom-enter {
  transform: scale(0.8);
  opacity: 0;
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.4s ease;
}
.zoom-enter.active {
  transform: scale(1);
  opacity: 1;
}

/* Outgoing: zoom away as departing scene */
.zoom-exit.active {
  transform: scale(1.15);
  opacity: 0;
  transition: transform 0.5s ease-in, opacity 0.3s ease-in;
}
```

### 7.3 GSAP ScrollTrigger Zoom-Through (Codrops, Oct 2025)

Layered zoom creates a Z-axis tunnel effect: each layer scales from a smaller starting value as you scroll, giving the impression you're flying through depth planes.

Architecture:
- N image layers, each slightly smaller than the last (scale stagger: 1.0, 0.9, 0.8...)
- ScrollTrigger scales each layer back to 1.0 on scroll, with a staggered offset
- Optional: blur layers start slightly blurred and sharpen as they reach scale(1)

```javascript
const layers = gsap.utils.toArray('.depth-layer');
layers.forEach((layer, i) => {
  gsap.from(layer, {
    scale: 0.7 + (i * 0.05), // each layer starts slightly larger
    filter: 'blur(4px)',
    scrollTrigger: {
      trigger: '.zoom-scene',
      start: 'top bottom',
      end: 'bottom top',
      scrub: 1,
    },
    delay: i * 0.08,
  });
});
```

### 7.4 Zoom + Clip Combination (zoom into a portal)

Zoom transition plus circular clip creates a "portal" effect — the circular reveal expands as the scale increases:

```javascript
const tl = gsap.timeline({ paused: true });
tl.to('.scene-outgoing', {
  scale: 2,
  opacity: 0,
  duration: 0.8,
  ease: 'power2.in'
});
tl.fromTo('.scene-incoming',
  { clipPath: 'circle(5% at 50% 50%)', scale: 1.5 },
  { clipPath: 'circle(150% at 50% 50%)', scale: 1, duration: 0.8, ease: 'power2.out' },
  '<0.2' // slight overlap
);
```

---

## Section 8 — Liquid Transitions

### 8.1 The Goo Effect (CSS filter trick)

The "liquid" merge effect uses an SVG filter applied to a container. When two elements overlap, the filter fuses them into an organic, fluid shape.

```html
<svg class="goo-filter" aria-hidden="true">
  <filter id="goo">
    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
    <feColorMatrix in="blur" mode="matrix"
      values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 20 -10"
      result="goo" />
    <feBlend in="SourceGraphic" in2="goo" />
  </filter>
</svg>

<div class="container" style="filter: url(#goo)">
  <div class="blob-a"></div>
  <div class="blob-b"></div>
</div>
```

**How it works:** Gaussian blur expands the elements into soft, overlapping blobs. The `feColorMatrix` applies a contrast-like operation that crushes the alpha channel — areas of overlap above a threshold become fully opaque, creating the merged liquid shape. Areas below threshold become transparent.

The `20 -10` values in the matrix are the key: multiply alpha by 20, subtract 10. Increase the multiplier for sharper edges; decrease for softer merging.

### 8.2 SVG Displacement Map for Liquid Distortion

For a ripple/liquid warp that distorts content during a transition:

```html
<svg class="displacement-filter" aria-hidden="true">
  <filter id="liquid-distort">
    <feTurbulence type="turbulence" baseFrequency="0.015" numOctaves="2"
      result="turbulence" seed="2">
      <animate attributeName="baseFrequency"
        dur="0.6s" values="0;0.04;0" repeatCount="1" />
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" in2="turbulence"
      scale="30" xChannelSelector="R" yChannelSelector="G" />
  </filter>
</svg>

<div class="transitioning-content" style="filter: url(#liquid-distort)">
  <!-- content that should appear to liquify during transition -->
</div>
```

**How it works:**
- `feTurbulence` generates Perlin noise — a field of random displacement values
- `feDisplacementMap` uses that noise to shift each pixel of the source element
- `baseFrequency` controls the scale of distortion (lower = larger waves)
- Animating `baseFrequency` from 0 to peak to 0 creates a wave that rises and falls — the content appears to ripple, then resolve

The `<animate>` on `baseFrequency` fires once (`repeatCount="1"`) — the distortion blooms and subsides. Trigger this on state change by cloning the SVG element (forces animation restart in most browsers).

### 8.3 SVG Path Morphing Liquid Transition (Codrops method)

An SVG path element positioned between two content panels morphs from one state to another as the transition plays. The path is styled as a wave/blob shape that connects the panels during the transition and then collapses.

Library: anime.js for path morphing. The Codrops Morphing Page Transition repo demonstrates this pattern.

Key states:
1. Initial: SVG path is flat horizontal line (invisible)
2. Mid-transition: Path bulges into a fluid wave (visible, covers seam between panels)
3. Final: Path collapses back to flat on the other side

---

## Section 9 — How Premium Product Demos Handle Transitions

### 9.1 Apple Keynote/Product Demo Patterns

[ASSUMED — inferred from multiple independent editorial analysis sources, no official Apple production docs]

**Techniques observed consistently across Apple demos:**

| Transition Type | Where Used | Effect |
|---|---|---|
| **Fade through black/white** | Between product categories | Clean separation, resets visual attention |
| **Screen-into-screen reveal** | Showing device UI | Device appears, then screen "lights up" — staged reveal, not simultaneous |
| **Iris close from black** | Scene endings | `circle(0% at 50% 50%)` equivalent — classic cinematic close |
| **Zoom into component** | Chip/camera reveals | Starts on full device, pushes into hardware detail — macro transition |
| **Feature card wipe-on** | Spec lists | Cards slide in bottom-up in rapid succession, staggered by ~80ms |
| **Dissolve (cross-fade)** | Color variants, angle changes | Simplest tool for same-subject different-state |
| **Perspective shift** | Device rotation demos | Subtle 3D transform, `perspective` + `rotateY`, not a hard cut |

**What Apple never does:**
- Glitch effects (off-brand — implies malfunction)
- Parallax complexity (too noisy — distracts from product)
- Long transitions (>0.8s) — every transition is under 600ms in product demos

### 9.2 Stripe Demo Patterns

[ASSUMED — inferred from design community analysis, not Stripe official docs]

Stripe Sessions 2025 product keynote: the brand language centers on data flowing and connecting, not appearing.

**Stripe-specific patterns:**
- **Line drawing reveals:** SVG paths drawn on scroll/time — the infrastructure literally draws itself
- **Card glide-in from right:** Payment/product cards enter from the right edge, settle into grid position
- **Number count-up during reveal:** The number animates from 0 → value simultaneously with the element appearing — not separate sequences
- **Subtle morph on hover:** Interactive elements expand slightly (1.02–1.04 scale), border-radius changes

### 9.3 The 3 Universal Rules from Premium Demos

Distilled from consistent patterns across Apple, Stripe, Linear, Notion product demos:

1. **Transitions serve content, not themselves.** The viewer should not think about the transition. If they notice it, it's too long or too complex.
2. **Stagger by ~80-120ms, not simultaneously.** A group of elements entering together looks like a jump. Staggered entry looks like flow.
3. **Enter fast, exit faster.** Entering elements take longer to settle (establishing presence). Exiting elements disappear quickly (don't delay the next thing). Ratio: enter duration ≈ 1.5x exit duration.

---

## Section 10 — Decision Matrix: Which Technique for Which Scenario

| Scenario | Recommended Technique | Duration | Notes |
|---|---|---|---|
| Calculator result appears | clip-path inset, bottom-up | 0.6–0.8s | Stagger multiple result rows |
| Screen A → Screen B (same page) | View Transitions API + cross-fade | 0.3–0.4s | Fastest, native, cleanest |
| Card → Full-screen modal | View Transitions API + named element morph | 0.4–0.5s | Requires `view-transition-name` |
| Section intro reveal | clip-path circle from corner OR inset from bottom | 0.7–1.0s | Use for hero sections only |
| Before/after comparison | Split curtain (two inset elements) | 0.8s | Both halves animate outward |
| State: confusion → clarity | Glitch (0.3s) → dissolve into clean state | 0.5s total | Glitch first, then resolve |
| Scene change in brand film | Zoom out + dissolve + zoom in | 1.2s | Film rhythm, not UI rhythm |
| Product feature reveal | Iris reveal (circle from center) | 0.5s | Works for spotlight framing |
| Data visualization entry | Number count-up + element stagger | 1.5–2.5s | Slower — data needs time |
| Page-to-page navigation | Cross-document View Transitions API | 0.3s | Zero JS needed |

---

## Falsifiability

- If View Transitions API cross-document support ships in Firefox stable before this date, the "Firefox Not yet" entries in Section 2.4 are outdated. Check caniuse before shipping.
- If clip-path performance degrades on Android mid-range devices (GPU memory constraints), the "compositor thread" claim in Section 1.4 is incomplete — test on real devices.
- Apple/Stripe transition analysis is inferred from design community documentation. If official production specs surface, verify specific durations and easing curves against that data.
- The "80-120ms stagger" rule in Section 9.3 is directional — derived from observational analysis, not a published spec. Could be wrong for larger element counts (e.g., 10+ items might need shorter stagger to avoid feeling slow).
- SVG `feTurbulence` + `feDisplacementMap` filter performance is GPU-dependent. On low-end devices it can drop to 30fps. Do not use for any animation that plays continuously.

---

## What We Might Be Missing

1. **Three.js / WebGL transitions** — GPU-rendered fragment shader transitions (pixel dissolve, burn, wave distortion) are used by high-budget sites (Awwwards winners). Not documented here because they require WebGL knowledge and exceed our current stack.
2. **Canvas-based transitions** — Some premium demos use HTML Canvas for pixel-level control. Not documented here.
3. **GSAP's SplitText + MorphSVG combo** — Letter-level SVG morphing (text transforms into a shape) is a documented technique not covered here. Research if needed for Pulse brand typography.
4. **CSS Houdini** — `@property` with `animation-timeline` enables custom interpolatable CSS variables. Could unlock animated clip-path via scroll without JavaScript. Still not universally supported.
5. **Reduced motion accessibility** — All transitions should respect `prefers-reduced-motion`. Not covered in this file. See MDN for the standard pattern.

---

## Sources

- [View Transition API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)
- [What's new in view transitions (2025 update) — Chrome for Developers](https://developer.chrome.com/blog/view-transitions-in-2025)
- [Smooth transitions with the View Transition API — Chrome for Developers](https://developer.chrome.com/docs/web-platform/view-transitions/)
- [Same-document view transitions Baseline Newly available — web.dev](https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available)
- [View Transitions API (single-document) — caniuse](https://caniuse.com/view-transitions)
- [Animating with Clip-Path — CSS-Tricks](https://css-tricks.com/animating-with-clip-path/)
- [The Magic of Clip Path — Emil Kowalski](https://emilkowal.ski/ui/the-magic-of-clip-path)
- [How to Animate clip-path for Smooth Transitions — CSS3 Shapes](https://css3shapes.com/how-to-animate-clip-path-for-smooth-transitions/)
- [Animating clip paths on scroll with @property in CSS — utilitybend](https://utilitybend.com/blog/animating-clip-paths-on-scroll-with-at-property-in-css/)
- [CSS Glitch Effect — Codrops](https://tympanus.net/codrops/2017/12/21/css-glitch-effect/)
- [How to create Pure CSS Glitch Animation — DEV Community](https://dev.to/kerthin/how-to-create-pure-css-glitch-animation-for-images-and-svg-ojl)
- [CSS Glitch Effect — muffinman.io](https://muffinman.io/blog/css-image-glitch/)
- [Building a Layered Zoom Scroll Effect with GSAP ScrollSmoother and ScrollTrigger — Codrops](https://tympanus.net/codrops/2025/10/29/building-a-layered-zoom-scroll-effect-with-gsap-scrollsmoother-and-scrolltrigger/)
- [Morphing Page Transition — Codrops](https://tympanus.net/codrops/2017/08/08/morphing-page-transition/)
- [GitHub: codrops/MorphingPageTransition](https://github.com/codrops/MorphingPageTransition)
- [SVG Mask Transitions on Scroll with GSAP and ScrollTrigger — Codrops](https://tympanus.net/codrops/2026/03/11/svg-mask-transitions-on-scroll-with-gsap-and-scrolltrigger/)
- [SVG Morphing Animations — SVGenius](https://svgenius.design/blog/svg-morphing-animations-transform-one-shape-into-another)
- [SVG path morphing — Motion.dev](https://motion.dev/tutorials/js-svg-path-morphing)
- [feTurbulence — MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence)
- [feDisplacementMap — MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feDisplacementMap)
- [SVG Filter Effects: Creating Texture with feTurbulence — Codrops](https://tympanus.net/codrops/2019/02/19/svg-filter-effects-creating-texture-with-feturbulence/)
- [Bringing Back Parallax With Scroll-Driven CSS Animations — CSS-Tricks](https://css-tricks.com/bringing-back-parallax-with-scroll-driven-css-animations/)
- [The best way to create a parallax effect in 2026 — builder.io](https://www.builder.io/blog/parallax-scrolling-effect)
- [Smashing Animations Part 2: CSS Masking — Smashing Magazine](https://www.smashingmagazine.com/2025/05/smashing-animations-part-2-css-masking-add-extra-dimension/)
- [SVG Masks and clipPaths — Motion Tricks](https://www.motiontricks.com/svg-masks-and-clippaths/)
- [Shape Morphing — CSS-Tricks](https://css-tricks.com/books/greatest-css-tricks/shape-morphing/)
- [Morphing Arbitrary Paths in SVG — minus-ze.ro](https://minus-ze.ro/posts/morphing-arbitrary-paths-in-svg/)
