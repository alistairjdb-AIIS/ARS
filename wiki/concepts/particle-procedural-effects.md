# Particle and Procedural Effects

> Particle system taxonomy for web: the five-property model, emitter types, ambient vs reactive vs generative categories, Canvas/CSS/WebGL performance tiers, and implementation budgets for each device class.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### Full Taxonomy of Web Particle/Procedural Effects

Every particle effect falls into one of five categories. Knowing the category determines which tools to reach for. [VERIFIED -- sfx_particle_systems.md, jQuery Script, CSS Script, CSS-Tricks, Codrops]

| Category | Effect | Primary Tool | Complexity |
|----------|--------|--------------|------------|
| Ambient | Floating dust motes | Canvas / CSS | Low |
| Ambient | Soft bokeh circles | CSS radial-gradient | Low |
| Ambient | Gentle snow / petals | Canvas / CSS | Low |
| Ambient | Aurora / northern lights | CSS gradient layers | Medium |
| Atmospheric | Fog / haze | CSS gradient + blur | Low |
| Atmospheric | Smoke (rising) | CSS keyframes + SVG feTurbulence | Medium |
| Atmospheric | Volumetric light rays (god rays) | CSS conic-gradient + mask | Medium |
| Reactive | Cursor trail | Canvas | Low |
| Reactive | Click burst / sparks | Canvas | Low |
| Reactive | Completion fireworks | Canvas | Medium |
| Reactive | Magnetic repulsion field | Canvas / CSS | Medium |
| Generative | Flow field (Perlin noise) | Canvas + noise library | High |
| Generative | Noise-based clustering | Canvas | High |
| Generative | Chromata-style path tracing | Canvas | High |
| System | Particle network (connected dots) | Canvas | Medium |
| System | Physics particles with gravity | Canvas | Medium |
| System | WebGL mass particles | WebGL / Three.js | High |

### The Five-Property Particle Model

Every particle system shares the same core model, regardless of visual output. [VERIFIED -- multiple sources]

Each particle has: position (x, y), velocity (vx, vy), acceleration (gravity, wind -- added to velocity each frame), lifetime (max age), age (current age), opacity (derived from age/lifetime ratio, 1.0 at birth to 0.0 at death), size (can change over lifetime), color (can shift over lifetime).

**Each frame:** velocity += acceleration, position += velocity, age++, opacity = 1 - (age/lifetime), if age >= lifetime: remove particle.

### Emitter Types

| Emitter | Behavior | Use Case |
|---------|----------|----------|
| Point | All particles born at single (x,y) | Explosions, sparks, fireworks |
| Area | Particles born at random position within bounding box | Snow, dust, ambient systems |
| Edge | Particles born along a line or curve | Trailing effects, path-following |
| Volume | Particles born anywhere within a region | Fog, smoke fields |

[VERIFIED -- sfx_particle_systems.md]

### Physics Modifiers

| Modifier | Effect | Typical Range |
|----------|--------|--------------|
| Gravity | Downward acceleration each frame | vy += 0.05-0.3 per frame |
| Wind | Horizontal drift | vx += +/-0.01-0.1 per frame |
| Drag/damping | Velocity multiplied to simulate air resistance | velocity *= 0.95-0.99 |
| Turbulence | Perlin noise added to velocity each frame | Low amplitude, high frequency |
| Magnetic | Velocity redirected toward/away from point | Normalized direction vector |

[VERIFIED -- sfx_particle_systems.md]

### Opacity Decay Curves

Linear decay is the baseline. Curve it for visual character:

- **Linear:** flat fade -- `1 - (age/lifetime)`
- **Ease-out:** holds bright longer, snaps to invisible -- `pow(1 - (age/lifetime), 2)`
- **Ease-in:** dims immediately, barely visible at end -- `1 - pow(age/lifetime, 2)`
- **Bell:** brightest in middle (sparkle/glow) -- `sin(t * PI)`

[VERIFIED -- sfx_particle_systems.md]

### Ambient Particles

Ambient particles run continuously in background. Their job is depth, not feedback. Opacity 0.1-0.4 maximum. [VERIFIED]

**Dust motes:** Very slow velocity (vx, vy +/-0.1-0.3 px/frame), Perlin noise turbulence for organic path, opacity 0.15-0.35, soft circular shape. CSS can handle up to approximately 30 particles. Canvas for 100-300. [VERIFIED]

**Bokeh circles:** Out-of-focus light circles. Size 20-150px, opacity 0.1-0.5 (never opaque), blur radius 4-20px, warm neutral or site accent color at low saturation. Performance limit: 15-20 DOM bokeh elements maximum before measurable slowdown. For more, switch to canvas. [VERIFIED -- Una Kravets]

**Snow/petals:** Same as dust but larger, slower, with gravity. Critical: asymmetric animation timing prevents lock-step (randomize delay and duration per element). [VERIFIED]

### Reactive Particles

Reactive particles fire in response to user actions. Their job: confirm intent, reward completion, make interface feel alive. [VERIFIED]

**Cursor trail:** Particles spawn at cursor position each frame, fade over 40-80 frames. Use sparingly -- on the one element that rewards attention, not everywhere. [VERIFIED]

**Click burst:** 8-20 particles at click position with radial velocity (evenly spaced angle + random magnitude), gravity, opacity decay over approximately 60 frames. [VERIFIED]

**Completion fireworks:** 3-5 bursts at staggered positions, higher particle counts (20-40 per burst), more velocity, color variation, 2-3 second lifetime. [VERIFIED]

### Atmospheric Effects

**Fog/haze:** Pure CSS. Stack 2-4 absolutely-positioned gradient blob layers, animated at different speeds and paths. Different animation durations (12s, 18s, 25s) with opposite alternate directions produce convincingly organic fog without JS. [VERIFIED -- CSS fog animation libraries]

**Rising smoke:** Individual puffs scaling up + translating upward + opacity fading. Blur must increase as puff rises (simulates diffusion). Note: animating `filter: blur()` is not GPU-composited -- use sparingly. [VERIFIED, with performance caveat]

**God rays:** CSS conic-gradient for ray pattern + mask-image with radial-gradient for soft edges + slow rotation. `mix-blend-mode: screen` on rays layer makes them add light to whatever is underneath -- mandatory for realistic light-on-dark effects. [VERIFIED -- multiple CodePen examples, Robb Owen]

### Aurora/Northern Lights

Layered animated gradient blobs + hue-shifting. Pure CSS viable for hero backgrounds. Use large soft pseudo-elements with `filter: blur(80px)` and different animation durations. Critical: only animate `transform` and `opacity` -- animating background, filter, or background-position causes rasterization each frame. [VERIFIED -- Auroral library, Aceternity UI]

### Generative: Flow Fields

Perlin noise function `noise(x, y)` returns smooth continuous values. Unlike `Math.random()`, adjacent inputs return adjacent outputs -- looks organic. Add a third dimension `z` incrementing each frame for animation without discontinuities. [VERIFIED]

Flow field = grid of angle vectors, each driven by Perlin noise. Particles sample their grid cell, update velocity toward that angle. Visual output looks like smoke, fluid, or wind. Standard library: `simplex-noise` (npm, 2.4KB gzip). [VERIFIED]

### Canvas vs DOM vs WebGL Decision Table

| Scenario | Particle Count | Tool | Notes |
|----------|---------------|------|-------|
| Atmospheric bokeh | <20 | DOM (CSS) | Simplest, zero JS |
| Floating dust/snow | 20-100 | DOM or Canvas | CSS is zero-JS; Canvas more control |
| Ambient continuous | 100-500 | Canvas 2D | Single canvas, rAF loop |
| Interactive cursor/click | 50-200 burst | Canvas 2D | Pool particles to avoid GC |
| Dense flow field | 500-3000 | Canvas 2D | CPU matters; profile on mobile |
| Mass background | 3000-10000 | WebGL | Canvas 2D bottlenecks around 3k-5k |
| Physically simulated mass | 10000+ | WebGL + instancing | GPU geometry instancing |

[VERIFIED -- multiple benchmarks, WebGL Fundamentals, SVG Genie, Tapflare]

**Hard thresholds:**
- Canvas 2D: approximately 3k-5k simultaneous particles before frame drops below 60fps on mid-range hardware [VERIFIED]
- DOM: approximately 100-200 animated elements before DOM reflows cause jank [VERIFIED]

### Performance Engineering

**GPU compositing rule:** Only `transform` and `opacity` are GPU-composited. `filter: blur()`, `background`, `width`, `height`, `top`, `left`, `box-shadow` all trigger rasterization or layout. [VERIFIED -- Algolia Engineering, Motion.dev]

**will-change:** Promotes element to own compositor layer but wastes GPU memory if overused. Apply to the `<canvas>` element itself for particle systems, not to individual particles. [VERIFIED -- DEV Community]

**Delta-time normalization:** `delta / 16.67` ensures consistent particle speed on 30Hz, 60Hz, and 144Hz screens. Without this, 120Hz screens make particles move twice as fast. [VERIFIED]

**Particle pooling:** Allocating new objects every frame triggers garbage collection pauses. Pool pattern: pre-allocate array, set `active: false` to return to pool, never delete. [VERIFIED]

**OffscreenCanvas:** Move expensive particle computation to a Web Worker. Keeps main thread free for UI. Support: Chrome, Firefox, Safari 16.4+. [VERIFIED for API; support THEORETICAL -- check target audience]

### Performance Budget by Device

| Device Class | Safe Particle Count (Canvas 2D) |
|-------------|--------------------------------|
| Desktop (modern) | 2000-3000 |
| Mid-range laptop | 500-1000 |
| Mobile (flagship) | 200-500 |
| Mobile (mid-range) | 50-150, prefer CSS-only |

[THEORETICAL -- inferred from benchmark ranges, not hard benchmarks]

---

## Operational Rules

1. **When adding ambient particles, cap opacity at 0.4 and keep them in the background layer** -- because ambient particles serve depth, not attention; anything above 0.4 opacity competes with content.

2. **When particle count exceeds 100, switch from DOM to Canvas** -- because DOM reflows cause jank past approximately 200 animated elements, while Canvas handles thousands.

3. **When particle count exceeds 3000, switch from Canvas 2D to WebGL** -- because Canvas 2D bottlenecks at 3k-5k particles on mid-range hardware.

4. **When targeting mobile, cap Canvas 2D particles at 200-500 (flagship) or 50-150 (mid-range)** -- because thermal throttling and limited GPU memory make mobile the binding constraint.

5. **When using CSS-only particles (bokeh, dust), limit to 15-20 DOM elements** -- because 60 radial gradients is measurably slow, and CSS particles cannot be pooled.

6. **When building a Canvas particle loop, always normalize for delta-time** (`delta / 16.67`) -- because without normalization, 120Hz screens produce twice the particle velocity.

7. **When reactive particles fire on user action, pool pre-allocated particle objects** -- because runtime allocation triggers garbage collection pauses that produce visible stutters.

8. **When using fog/smoke CSS effects, only animate transform and opacity on the layers** -- because animating background, filter, or background-position triggers rasterization every frame.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/sfx_particle_systems.md` | Complete particle taxonomy, five-property model, ambient/reactive/generative patterns, Canvas/DOM/WebGL decision table, performance engineering, implementation recipes |

---

## Related Concepts

- [[texture-materiality]] — EXTENDS: film grain overlays share noise-generation techniques with particle systems (feTurbulence, Perlin noise)
- [[motion-curves-easing]] — DEPENDS_ON: particle opacity decay curves are easing functions applied to lifetime
- [[transitions-state-change]] — INFORMS: particle bursts can serve as transition punctuation (completion fireworks)
- [[progressive-disclosure-pacing]] — INFORMS: reactive particles confirm the beat drops in a pacing sequence

---

## Deep Reference

- **When** choosing between CSS, Canvas, and WebGL for a particle effect and need the performance ceiling per approach → **read** `research-data/sfx_particle_systems.md` §6 (Performance Engineering) **for** the Canvas/DOM/WebGL decision table with particle count thresholds (~30 CSS, 100-300 Canvas 2D, 10,000+ WebGL), OffscreenCanvas worker threading pattern, and requestAnimationFrame budget analysis
- **When** tuning particle opacity decay and the fade feels wrong (too abrupt or too lingering) → **read** `research-data/sfx_particle_systems.md` §2.4 (Opacity Decay Curves) **for** four JS decay formulas (linear, ease-out holds bright then snaps, ease-in dims immediately, bell curve for sparkle/glow) with exact `Math.pow` and `Math.sin` implementations
- **When** building a completion fireworks effect and need burst parameters → **read** `research-data/sfx_particle_systems.md` §4 (Reactive Particles) **for** click burst specs (8-20 particles, radial velocity, ~60 frame lifetime), fireworks specs (3-5 staggered bursts, 20-40 particles each, 2-3s lifetime), and the one-element-only restraint rule
- **When** adding atmospheric fog or smoke and need the physics modifiers → **read** `research-data/sfx_particle_systems.md` §2.3 (Physics Modifiers) **for** gravity (vy += 0.05-0.3/frame), wind (vx += 0.01-0.1/frame), drag (velocity *= 0.95-0.99), and Perlin noise turbulence parameter ranges

---

## Open Questions

- OffscreenCanvas browser support should be verified against specific target audience before depending on worker-based rendering
- Performance budgets by device are estimated ranges, not hard benchmarks -- profile on actual target devices
- Whether ambient particles improve perceived quality in health/medical contexts is untested (could read as frivolous)
- The `filter: blur()` performance cost for animated smoke effects needs per-device profiling -- it is not GPU-composited and can cause jank
