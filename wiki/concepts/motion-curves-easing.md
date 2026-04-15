# Motion Curves and Easing

> The mathematical foundation for all animation timing: cubic-bezier coordinate geometry, spring physics differential equations, CSS linear() for complex curves, brand-specific motion systems, and the mapping from emotion to curve parameters.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### Cubic-Bezier: The Four-Point Model

A cubic Bezier curve is defined by four points: P0 = (0,0) always, P3 = (1,1) always, P1 = (x1,y1) and P2 = (x2,y2) as control points. CSS syntax: `cubic-bezier(x1, y1, x2, y2)`. [VERIFIED -- MDN, CSS-Tricks, Maxime Heckel]

The curve starts at P0 moving toward P1, arrives at P3 from the direction of P2. P1 and P2 are directional attractors, NOT points the curve passes through. [VERIFIED -- MDN]

**Coordinate rules:**
- x1, x2: restricted to [0, 1] -- controls WHEN acceleration/deceleration happens (time axis)
- y1, y2: any value, including outside [0, 1] -- controls HOW FAR the property moves (displacement axis)
- y > 1 = property overshoots its final value, then settles back (spring feeling)
- y < 0 = property briefly moves backward before proceeding (anticipation)

[VERIFIED -- MDN, mathematical fact]

**P1 controls start behavior:** High x1 = long slow start. Low x1 = immediate acceleration. High y1 = fast start. y1 < 0 = anticipation dip. [VERIFIED]

**P2 controls end behavior:** Low x2 = deceleration begins early (long glide). High x2 = deceleration starts late (fast to end). y2 > 1 = overshoot. Low y2 = hard brake. [VERIFIED]

### Standard Presets Decoded

| Name | cubic-bezier | Character |
|------|-------------|-----------|
| `linear` | (0, 0, 1, 1) | Mechanical, robotic. No natural feel. |
| `ease` | (0.25, 0.1, 0.25, 1) | Browser default. Acceptable but generic. |
| `ease-in` | (0.42, 0, 1, 1) | Slow start, full-speed exit. Launch feeling. |
| `ease-out` | (0, 0, 0.58, 1) | Fast entry, gentle landing. Most natural for UI. |
| `ease-in-out` | (0.42, 0, 0.58, 1) | Symmetric S-curve. Formal, balanced. |

**Why ease-out dominates UI:** Objects entering from off-screen arrive at full velocity and decelerate to rest. This matches physical intuition -- a dropped object decelerates on landing, not before. [VERIFIED -- MDN, CSS-Tricks]

### Emotion-to-Curve Mapping

The x-axis controls TIMING, the y-axis controls DISPLACEMENT. Combined with duration, these produce emotional qualities. [VERIFIED for physics principles; emotional mapping THEORETICAL -- inferred from first principles]

| Emotion | Curve | Duration | Key Mechanism |
|---------|-------|----------|--------------|
| Confident | `cubic-bezier(0.16, 1, 0.3, 1)` | 150-200ms | Strong ease-out, clean stop, no overshoot |
| Gentle/Careful | `cubic-bezier(0.45, 0.05, 0.55, 0.95)` | 400-600ms | Symmetric ease-in-out, no rush |
| Playful | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 250-350ms | y2=1.56 causes single subtle overshoot |
| Hesitant | `cubic-bezier(0.5, 0, 0.75, 0)` | 350-450ms | High x1 delays acceleration |
| Snappy/Tense | `cubic-bezier(0.25, 0, 0.3, 1)` | 80-150ms | Fast off the line, no bounce |
| Solemn/Weighted | `cubic-bezier(0.4, 0, 1, 1)` | 300-500ms | Strong ease-in, gravity-like |
| Anticipation | `cubic-bezier(0.36, 0, 0.66, -0.56)` | Medium | Negative y creates backward dip |

**Two variables that override everything:** (1) Duration beats curve shape -- a gentle curve at 50ms feels snappy. (2) Context beats curve -- the same ease-out on a notification feels informative, on an error state feels nonchalant. [VERIFIED -- animation_motion_curves.md]

### CSS linear(): The New Frontier

`linear()` interpolates between multiple discrete points, approximating any arbitrary curve including spring, bounce, and elastic motion that cubic-bezier mathematically cannot represent. [VERIFIED -- MDN, Chrome Developers, Josh Comeau]

Cubic-bezier has no mechanism for oscillation, multiple direction reversals, or asymmetric acceleration after overshoot. `linear()` with 40+ data points enables all of these. [VERIFIED -- mathematical limitation of cubic-bezier]

**Browser support (March 2026):** Chrome 113+, Edge 113+, Firefox 112+. Safari: No. Overall approximately 88%. [VERIFIED -- Smashing Magazine Oct 2025, MDN]

**Fallback strategy:** Use cubic-bezier with similar character as baseline, `linear()` spring as progressive enhancement. [VERIFIED]

**Performance:** `linear()` does NOT affect GPU compositability. The property being animated is the entire performance story, not the easing function. `linear()` with 100 points on `transform` = GPU-composited, smooth. `ease-out` on `width` = layout-triggering, janky. [VERIFIED -- LogRocket, Josh Comeau]

### Spring Physics: Stiffness, Damping, Mass

Spring motion follows Hooke's Law + damping: `F = -kx - cv` where k = stiffness, x = displacement, c = damping coefficient, v = velocity. [VERIFIED -- Maxime Heckel, Josh Comeau, Figma, Apple Developer docs, Popmotion]

**Three parameters:**
- Stiffness (k): high = snaps to target fast; low = slow to move
- Damping (c): high = settles fast, no bounce; low = oscillates many times
- Mass (m): high = slow to respond (heavy); low = quick to respond (light)

**Damping ratio determines regime:**
```
zeta = damping / (2 * sqrt(stiffness * mass))
zeta < 1: underdamped (bouncy)
zeta = 1: critically damped (clean, no bounce)
zeta > 1: overdamped (sluggish)
```
[VERIFIED -- physics, confirmed in Maxime Heckel, Apple docs]

**Emotional quality of spring configurations:**

| Configuration | Quality | Use |
|--------------|---------|-----|
| High stiffness + high damping | Snappy, decisive | Button press, micro-interaction |
| High stiffness + low damping | Tense, agitated | Alert/warning appearance |
| Low stiffness + high damping | Gentle, careful | Modal open, tooltip |
| Medium stiffness + medium damping | Pleasant, natural | Default for most transitions |
| High mass + any | Heavy, consequential | Full-page transitions, hero reveals |
| Low mass + any | Light, responsive | Tags, chips, small elements |

[VERIFIED -- animation_motion_curves.md, Figma docs]

### Brand-Specific Motion Systems

Motion curves can be as distinctive as a typeface. A brand's motion signature is defined by: default curve type, overshoot allowance, duration range, and rule-breaking moments. [VERIFIED -- IBM Carbon, Slack; THEORETICAL for Stripe/Vercel/Linear]

**Material Design 3:** Cubic-bezier tokens. Standard `(0.2, 0, 0, 1)`, Standard accelerate `(0.3, 0, 1, 1)`, Standard decelerate `(0, 0, 0, 1)`, Emphasized (two-phase spring approximation). Duration tokens from 50ms (Short 1) to 600ms (Long 4). [VERIFIED -- Material UI source, MDN]

**Apple HIG:** Spring-first philosophy. Default `spring(response: 0.55, dampingFraction: 0.825)`. Duration emerges from spring parameters, not explicit tokens. Never exceed 0.4 bounce for standard UI. [VERIFIED -- Apple Developer docs, WWDC23]

**IBM Carbon:** Two official curves -- Productive `(0.2, 0, 0.38, 0.9)` for task-oriented interactions, Expressive `(0.4, 0.14, 0.3, 1)` for editorial/branding moments. Most explicit motion-to-intent system of any major design system. [VERIFIED -- Carbon documentation]

**Key philosophical disagreement:** MD3 uses spatial metaphor (direction encodes information hierarchy). Apple uses physics metaphor (elements have weight and spring properties). Both agree on purposeful over decorative motion. [VERIFIED -- inferred from official documentation framing]

### Motion Personality System

A motion personality is 3-5 easing curves covering all UI states in a product: enter, exit, state change, emphasis, micro. Combined with 3 duration tokens (fast 100-150ms, default 200-300ms, slow 400-600ms) and one explicit rule-breaking escape valve. [THEORETICAL -- synthesized from IBM Carbon, Slack, Material Design approaches]

### Performance: GPU vs Layout

Only `transform` and `opacity` run on the GPU compositor thread. Everything else (width, height, padding, margin, left, top, background-color, box-shadow) triggers layout or paint on the main thread. [VERIFIED -- Smashing Magazine, Chrome Developers, MDN]

- 60fps = 16.7ms per frame budget
- Composited animations: 0-2ms of that budget
- Layout-triggering animations: 10-16ms, leaving no room

Easing function complexity has no meaningful performance cost difference. [VERIFIED -- LogRocket, Josh Comeau]

`will-change` promotes element to its own compositor layer but increases VRAM consumption. Apply before animation, remove after. Do not apply globally. [VERIFIED -- multiple sources]

---

## Operational Rules

1. **When choosing between ease-in and ease-out, default to ease-out for entries and ease-in for exits** -- because ease-out matches physical intuition of objects decelerating on arrival, and ease-in matches committed departure.

2. **When targeting Safari, always provide a cubic-bezier fallback for linear() springs** -- because Safari does not support linear() as of March 2026, and the 12% unsupported browsers include a significant iOS user base.

3. **When building a brand motion system, define exactly 3-5 semantic curve roles (enter, exit, state-change, emphasis, micro) with explicit curves for each** -- because unconstrained curve invention across a product creates inconsistent motion character.

4. **When animating any property other than transform and opacity, treat it as a performance red flag** -- because all other properties trigger layout or paint, which can consume the entire 16.7ms frame budget.

5. **When duration and curve conflict on emotional read, trust duration first** -- because a gentle curve at 50ms feels snappy regardless of curve shape; duration is the dominant variable.

6. **When spring physics are needed but JS libraries are unavailable, use CSS linear() with 40+ data points generated by Jake Archibald's linear-easing-generator** -- because hand-authoring spring curves is impractical and cubic-bezier cannot produce oscillation.

7. **When a modal or heavy element needs spring feel, keep overshoot y2 at 1.03-1.05** -- because larger overshoot values read as playful, contradicting the authority signal heavy elements require.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/animation_motion_curves.md` | Cubic-bezier math, spring physics, emotion-to-curve map, linear(), brand motion systems, performance |
| `research-data/animation_physical_weight.md` | Weight-class easing tables, duration scaling, spring constants by element class |

---

## Related Concepts

- [[squash-stretch-weight]] — INFORMS: weight classes consume the curves defined here
- [[choreography-stagger]] — INFORMS: stagger timing uses these curves for organic delay distribution
- [[transitions-state-change]] — INFORMS: transitions consume these easing functions
- [[editorial-pacing-rhythm]] — INFORMS: rhythm emerges from curve x duration interactions
- [[texture-materiality]] — INFORMS: material behavior (glass fluidity, metal rigidity) must match the motion curves applied to that element; texture and easing must agree on physical weight
- [[particle-procedural-effects]] — INFORMS: particle systems consume easing curves for birth/death opacity fades, velocity damping, and size-over-lifetime progressions that determine whether particles feel organic or mechanical
- [[progressive-disclosure-pacing]] — INFORMS: progressive disclosure sequences depend on easing curves to set the emotional character of each reveal, beat drop, and dimming transition

---

## Deep Reference

- **When** deciding whether to use CSS `linear()` or cubic-bezier for a spring animation → **read** `research-data/animation_motion_curves.md` §3 (CSS linear()) **for** the mathematical limitation that makes cubic-bezier incapable of oscillation, a ready-made 40-point spring data array, Safari support status (No as of Mar 2026 = ~12% gap), and the progressive-enhancement fallback strategy
- **When** a transition feels wrong and you need to diagnose whether it's stiffness, damping, or mass → **read** `research-data/animation_motion_curves.md` §4 (Spring Physics) **for** the damping ratio formula (`zeta = c / (2*sqrt(k*m))`), regime definitions (underdamped/critically damped/overdamped), and how each parameter independently changes feel (high stiffness + low damping = tense; low stiffness + high damping = gentle)
- **When** defining motion tokens for a new brand and choosing between Material Design's spatial approach vs Apple's physics approach → **read** `research-data/animation_motion_curves.md` §5-6 **for** MD3's exact duration tokens (Short 1 = 50ms through Long 4 = 600ms), Apple's default `.spring(response: 0.55, dampingFraction: 0.825)`, IBM Carbon's two-curve system (Productive vs Expressive with exact cubic-bezier values), and the philosophical disagreement that determines which approach fits
- **When** an animation stutters and you suspect a performance issue → **read** `research-data/animation_motion_curves.md` §8 (Performance) **for** the safe-to-animate property list (only `transform` and `opacity` are GPU-composited), the 16.7ms frame budget breakdown, and why `will-change` solves one problem but creates VRAM pressure

---

## Open Questions

- Safari linear() support is a critical gap for spring-dependent motion systems -- check caniuse before every production deployment
- Whether "natural feel" from physics-based curves is culturally universal (assumed, not tested cross-culturally)
- The emotion-to-curve mappings are inferred from physics principles and source descriptions, not directly measured on users
- GPU compositing assumption ("transform + opacity = free") breaks at high layer counts, under VRAM pressure, or on thermally throttled mobile devices
