# Transitions and State Change

> Screen transitions as a third state between two views: clip-path wipes, morph (FLIP) animations, the View Transitions API, glitch/distortion effects, parallax layers, and the principle that a transition transforms the traveler, not just transports them.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### The Generating Principle

A transition is not a gap between two states. It is a third state whose function is to transform the traveler, not just transport them. [VERIFIED -- cross_domain_pattern_synthesis.md, Generating Principle #4]

This means every transition technique carries meaning beyond "content A is now content B." The choice of clip-path vs morph vs dissolve vs hard cut is an editorial decision about what the state change means. [THEORETICAL -- synthesized from directing_editorial_pacing.md]

### Wipe Transitions: clip-path Animations

`clip-path` defines a visible region -- anything outside is hidden. Animating the clip shape creates content being "wiped on" or revealed. [VERIFIED -- MDN, CSS-Tricks, Emil Kowalski]

**Critical rule:** Both keyframes must use the same shape function. Animating `inset()` to `circle()` fails silently. [VERIFIED]

**Four wipe shapes:**

| Shape | Syntax | Best For |
|-------|--------|----------|
| `inset()` | `inset(top right bottom left)` | Directional wipes (up, down, left, right) |
| `circle()` | `circle(radius at cx cy)` | Circular reveal (spotlight, iris) |
| `ellipse()` | `ellipse(rx ry at cx cy)` | Asymmetric radial reveals |
| `polygon()` | `polygon(x1 y1, x2 y2, ...)` | Diagonal wipes, curtain splits, geometric reveals |

[VERIFIED -- sfx_screen_transitions.md]

**Core patterns:** Bottom-up reveal (most common for UI cards), left-to-right wipe (cinematic curtain), circular iris reveal (Apple keynote-style spotlight from center or corner), diagonal wipe (premium, less common), curtain split (two panels opening). [VERIFIED]

**Performance:** clip-path animates on the compositor thread -- no layout or paint. One of the cheapest visual effects in CSS. [VERIFIED]

**Easing for wipes:** Hard wipes: `steps(1)` for instant cut. Premium reveals: `cubic-bezier(0.77, 0, 0.175, 1)`. Organic wipes: `cubic-bezier(0.25, 0.46, 0.45, 0.94)`. [VERIFIED]

### Morph Transitions: FLIP Technique

FLIP = First, Last, Invert, Play. The gold standard for morphing DOM elements without animation libraries. Records starting position, applies end-state DOM change, applies inverse transform, then animates to identity. Only uses `transform` and `opacity` -- compositor thread at 60fps. [VERIFIED -- Paul Lewis/Aerotwist, CSS-Tricks, GSAP Flip plugin]

Works for: card to modal, thumbnail to full-screen, button to expanded panel. The shared element between states IS the statement -- it creates the cognitive message "this result came from your input." [VERIFIED]

### View Transitions API

The browser handles element-to-element morphing natively. Takes a screenshot of current state, your callback updates the DOM, takes screenshot of new state, animates between them. [VERIFIED -- MDN, Chrome DevRel]

**Same-document morph:** `document.startViewTransition(() => { updateDOM() })` [VERIFIED]

**Named element morph:** Assign the same `view-transition-name` to an element in old and new state. The browser morphs position, size, and content automatically. [VERIFIED]

**Cross-document transitions (MPA):** No JavaScript needed. `@view-transition { navigation: auto; }` on both pages. [VERIFIED]

**Browser support (2025):**

| Feature | Chrome | Edge | Safari | Firefox |
|---------|--------|------|--------|---------|
| Same-document | 111+ | 111+ | 18+ | 144+ |
| Cross-document (MPA) | 126+ | 126+ | 18.2+ | Not yet |
| `view-transition-class` | 125+ | 125+ | Not yet | Not yet |

Same-document transitions are Baseline Newly Available (October 14, 2025). [VERIFIED -- web.dev]

**Progressive enhancement pattern:**
```javascript
if (document.startViewTransition) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM(); // instant, still functional
}
```
[VERIFIED]

### SVG Path Morphing

When actual geometry must change (circle becoming rectangle, check becoming X), only SVG path morphing works. Both paths must have the same number of anchor points -- different counts produce jumps, not morphs. GSAP MorphSVG and Flubber handle incompatible paths. [VERIFIED]

### Mask Reveals

CSS `clip-path` for simple geometric reveals. SVG `<clipPath>` for complex shapes (stars, logos). SVG `<mask>` when gradient fade-outs, strokes, or luminance-based transparency are needed. CSS mask-image with gradient enables reveals that dissolve content from invisible to visible along a gradient edge. [VERIFIED]

### Glitch/Distortion Transitions

Three stacked pseudo-elements with different clip-path animations and color channel shifts. `steps(1)` timing function makes it look digital, not smooth. Random-looking patterns in clip-path inset values read as genuine corruption. [VERIFIED -- sfx_screen_transitions.md, Codrops, DEV Community]

Use as single-fire transition (`animation-iteration-count: 1`) with `animation-fill-mode: forwards`, resolving into clean state. Pair with View Transitions API: start glitch, start transition, cancel glitch at completion. [VERIFIED]

**When to use:** Entering from broken/confused state into clarity. "Failure to resolution" narrative. [THEORETICAL]

### Parallax Transitions

Multiple layers move at different rates, creating illusion of 3D space on 2D plane. Background slow (far), foreground fast (close). [VERIFIED]

**Modern CSS approach:** `animation-timeline: scroll()` -- no JavaScript. Supported Chrome 115+, Edge 115+, Safari 18+, Firefox partial 117+. [VERIFIED]

**Speed multipliers:** 0.1-0.3 = deep background, 0.4-0.6 = mid-ground, 0.7-0.9 = foreground. [VERIFIED]

### Zoom Transitions

Scaling into a detail that becomes the next scene. Used in Apple product demos (chip reveals, camera modules), data visualization (world map to city). Outgoing scene scales up and fades, incoming scales from small clip that expands. Zoom + clip combination creates "portal" effect. [VERIFIED -- sfx_screen_transitions.md, Codrops]

### Liquid Transitions

**Goo effect:** SVG filter with Gaussian blur + feColorMatrix. When two elements overlap, the filter fuses them into organic, fluid shapes. The `20 -10` alpha matrix values are the key control. [VERIFIED -- Codrops]

**Displacement map distortion:** feTurbulence generates Perlin noise, feDisplacementMap shifts each pixel by the noise values. Animating `baseFrequency` from 0 to peak to 0 creates a wave that rises and falls -- content ripples, then resolves. [VERIFIED -- MDN filter primitive docs, Codrops]

### Premium Demo Transition Patterns

Three universal rules from Apple, Stripe, Linear, Notion demos: [VERIFIED -- inferred from consistent patterns across multiple independent analyses]

1. **Transitions serve content, not themselves.** If the viewer notices the transition, it is too long or complex.
2. **Stagger by 80-120ms, not simultaneously.** Simultaneous group entry looks like a jump; staggered entry looks like flow.
3. **Enter fast, exit faster.** Enter duration approximately 1.5x exit duration.

### Decision Matrix

| Scenario | Technique | Duration |
|----------|----------|----------|
| Calculator result appears | clip-path inset, bottom-up | 0.6-0.8s |
| SPA route change with shared element | View Transitions API + view-transition-name | 0.3-0.4s |
| Card to full-screen modal | View Transitions API or FLIP | 0.4-0.5s |
| Section intro reveal | clip-path circle from corner or inset from bottom | 0.7-1.0s |
| Before/after comparison | Split curtain | 0.8s |
| Confusion to clarity state | Glitch (0.3s) then dissolve | 0.5s total |
| Brand film scene change | Zoom out + dissolve + zoom in | 1.2s |

[VERIFIED -- sfx_screen_transitions.md decision matrix]

---

## Operational Rules

1. **When transitioning between UI states with a shared element, use View Transitions API with named elements first, FLIP as fallback** -- because the browser handles the morph natively, the shared element creates perceived causality, and it is the most performant path.

2. **When a transition exceeds 0.8s in UI context, question whether it serves the content** -- because premium demos consistently keep transitions under 600ms, and longer transitions call attention to themselves rather than the content.

3. **When implementing clip-path wipes, always verify both keyframes use the same shape function** -- because mismatched functions (inset to circle) fail silently and produce no animation.

4. **When using glitch transitions, fire once and resolve to clean state** -- because looping glitch reads as broken interface, not intentional style; the narrative is corruption-to-clarity.

5. **When targeting broad browser support for morph transitions, implement progressive enhancement** -- because View Transitions API same-document is baseline, but MPA transitions and Safari support for advanced features remain incomplete.

6. **When choosing between dissolve, wipe, and morph, let the semantic relationship between states decide** -- because dissolve implies passage of time/dream-like connection, wipe implies location/time change, and morph implies "these are the same object across states."

7. **When using parallax, cap speed differential at 3 layers maximum** -- because more layers create visual complexity without additional depth perception, and mobile GPU budgets cannot sustain many parallax layers.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/sfx_screen_transitions.md` | clip-path wipes, FLIP, View Transitions API, glitch effects, parallax, zoom, liquid transitions, premium demo patterns |
| `research-data/animation_choreography.md` | FLIP technique details, Material Design Container Transform, direction consistency, exit choreography |

---

## Related Concepts

- [[choreography-stagger]] -- multi-element transitions use stagger patterns from choreography
- [[motion-curves-easing]] -- every transition technique consumes easing curves
- [[progressive-disclosure-pacing]] -- transitions serve the pacing of information revelation
- [[editorial-pacing-rhythm]] -- the choice of cut type (hard cut, dissolve, wipe, match cut) is an editorial decision

---

## Open Questions

- View Transitions API cross-document support in Firefox is "not yet" -- check caniuse before shipping MPA transitions
- clip-path compositor performance on Android mid-range devices needs real-device testing
- Apple/Stripe transition analysis is inferred from design community documentation, not official production specs
- The "80-120ms stagger" rule from premium demos is observational, not a published spec; could be wrong for 10+ element counts
- SVG feTurbulence + feDisplacementMap filter performance is GPU-dependent and can drop to 30fps on low-end devices
