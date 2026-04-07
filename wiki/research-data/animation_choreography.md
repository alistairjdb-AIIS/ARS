# Animation Choreography: Orchestrating Multiple Elements
**Date:** 2026-03-22
**Research method:** 16 web searches across 8 query domains, cross-referenced against IBM Carbon Design System, Material Design, GSAP documentation, Disney's 12 Principles, and CSS-Tricks technical articles
**Status:** Research synthesis. Implementation details are [VERIFIED] against source documentation. Design judgments are [LLM-ESTIMATED] unless tagged otherwise.
**Feeds:** Motion agent, design agent, any multi-element animation work on Pulse, calculators, or landing pages

---

## What This Document Is

Animation choreography is the coordination of multiple animated elements into a single cohesive sequence — not how one element moves, but how a group of elements moves together. The difference between a screen that feels alive and a screen that feels noisy is almost always choreography, not individual animation quality.

This document covers: stagger patterns, the conductor model, entrance/exit strategy, transition choreography, GSAP timeline structure, the breath pattern, and planning process.

---

## 1. Stagger Patterns Beyond Uniform Delay

Uniform stagger (each element delays by X ms) is the baseline. These are the named patterns beyond that.

### 1a. The Five Stagger Origin Patterns
Source: GSAP documentation + Motion.dev stagger API [VERIFIED]

| Pattern | `from` value | Behavior | When to use |
|---------|-------------|----------|-------------|
| Left-to-right (default) | `"start"` | First element animates first, last element last | Reading order reveals (text, lists) |
| Right-to-left | `"end"` | Last element first, works backward | Exits, undo feedback |
| Ripple from center | `"center"` | Middle element first, radiates outward simultaneously both ways | Drawing attention to a focal point (calculator result, key stat) |
| Ripple from edges | `"edges"` | Outer elements first, collapses toward center | Closing/focusing, gathering effect |
| Random-within-range | `"random"` | Unpredictable order, but respects timing constraints | Organic/alive feeling, particle-like reveals |

GSAP implementation reference:
```js
gsap.to(".card", {
  opacity: 1,
  stagger: {
    amount: 0.8,      // total time spread across all elements
    from: "center",   // "start" | "end" | "center" | "edges" | "random" | index number
    grid: "auto",     // auto-detect rows/columns from DOM layout
    axis: "x"         // focus on horizontal distance only, ignore vertical
  }
})
```

### 1b. Grouped Burst Pattern
[VERIFIED from IBM Carbon Design System + UX Collective]

Instead of staggering individual elements, stagger groups. Structure:
- Group A (structural/background) → animates first, all elements inside A are simultaneous
- Group B (content layer) → starts 80-120ms after A completes
- Group C (actions/CTAs) → starts after B

This avoids the "slideshow" problem where long individual staggers make the last card feel forgotten. Groups feel intentional; long individual staggers feel like slow loading.

Rule: keep stagger groups to 3-7 items. More than 7, the last item waits too long and the sequence loses coherence.

### 1c. Cascading vs Wave vs Simultaneous
[VERIFIED from multiple sources, synthesized]

| Mode | Description | Cognitive effect | Best for |
|------|-------------|-----------------|---------|
| Cascade | Each element starts after previous finishes | Sequential reading, high control | Long lists, step-by-step content |
| Wave (overlapping) | Each element starts before previous finishes | Fluid, connected motion | Card grids, icon sets, navigation |
| Grouped burst | Groups simultaneous, groups staggered from each other | Clean hierarchy without slow drags | Hero sections, result cards |
| Simultaneous | Everything at once | Chaotic, busy unless perfectly tuned | Avoid for 4+ elements |

The IBM Carbon Design System finding: "sequence the loading of page content — start with the most stable content (static, headers), end with the most important information (primary button, calculation result)." [VERIFIED] This maps directly to the grouped burst pattern applied to page load.

### 1d. Grid-Based Radial Stagger
[VERIFIED from GSAP grid stagger documentation]

When elements are in a 2D grid, stagger distance can be calculated from a center point across both axes simultaneously. The result is a ripple effect that radiates from whichever cell you specify as origin (by index or named position).

GSAP implementation: `grid: [rows, cols]` or `grid: "auto"` — GSAP uses `getBoundingClientRect()` to auto-calculate. Set `axis: null` to stagger on both X and Y simultaneously (true radial ripple).

This is the right pattern for: card grids on the calculators page, icon clusters, any 2D collection that should feel like it's "waking up."

### 1e. Timing Parameters
[VERIFIED from GSAP docs + Frontend Masters course + Aninix research]

| Parameter | Range | Effect |
|-----------|-------|--------|
| Stagger delay between items | 30-80ms | Feels cohesive and connected |
| Stagger delay between items | 80-200ms | Deliberate, counted reveals |
| Stagger delay between items | 200ms+ | Feels like loading, not animation |
| Stagger delay as % of duration | 30-70% of duration | Sweet spot for overlap feel |
| Individual element duration | 200-400ms (entrances) | Standard UI feel |
| Individual element duration | 150-250ms (exits) | Exit should always be faster than entrance |

Rule: exit animations should be faster than entrances. Enter at 300ms, exit at 200ms. [VERIFIED from Aninix UI animation guide]

---

## 2. The Conductor Model: One Element Leads, Others Follow

### 2a. The Core Principle
[VERIFIED: Disney's 12 Principles — "Follow Through and Overlapping Action" + IBM Design Language]

The conductor model comes directly from Disney's Principle 6: Follow Through and Overlapping Action. The rule is:

> Primary action leads. Everything else follows at defined offsets.

In a character: shoulder moves → arm follows → elbow follows → hand lags. The same logic applies to UI element groups.

In a UI element group:
- The most important element (the "lead") animates first and sets the rhythm
- Supporting elements (body) follow at 40-80ms offset from the lead
- Decorative or contextual elements (tail) follow at 80-150ms offset from the body

The cascade of offsets is what creates the sense of energy traveling through the interface, rather than elements being switched on simultaneously.

### 2b. How to Assign the Lead
[LLM-ESTIMATED from principles, not a documented rule]

Assign the conductor role to the element that answers: "What does the user need to orient to this screen first?"

In a calculator result:
- Lead: the number/result (anchors everything)
- Body: the interpretation text (what the number means)
- Tail: the actions/CTAs (what to do next)
- Decorative: background elements, accent lines

In a hero section:
- Lead: headline (not the logo, not the image)
- Body: subheadline + supporting text
- Tail: CTA button
- Decorative: background shapes, ambient elements

This order mirrors reading intent — not visual hierarchy, but task hierarchy.

### 2c. Overlapping vs Sequential Offsets
[VERIFIED from Overlapping Action principle + UX Collective]

Each follower should start before the leader finishes. Not:
- Lead completes → body starts → tail starts (sequential, robotic)

But:
- Lead is 60% through → body starts → at 60% of body → tail starts (overlapping, organic)

The overlapping feel comes from the animation durations being longer than the stagger delay. If your element duration is 300ms and your stagger is 80ms, elements are running simultaneously for 220ms — that overlap creates fluid, connected motion instead of a slideshow.

---

## 3. Entrance Choreography: Bringing 10+ Elements on Screen

### 3a. The Grouping Principle
[VERIFIED from IBM Carbon, Material Design, NNGroup animation duration research]

Never animate 10 elements as 10 individual staggers. Group them:

Step 1: Define groups by function (structural, content, action, decoration)
Step 2: Animate groups as units, not elements
Step 3: Stagger the groups from each other

Example — calculator page load:
1. **Structural layer** (nav, container outline): simultaneous, 150ms fade-in
2. **Content header** (headline, breadcrumb): starts 60ms after structural, 250ms ease-out
3. **Form elements** (inputs, labels): wave stagger within the group, 40ms between each, starts 80ms after header
4. **Result zone placeholder** (grayed, skeleton): appears with form, same timing
5. **Trust signals** (sources, disclaimer text): starts 100ms after form, 200ms fade

The user sees structure arrive → content arrive → interaction points arrive. Coherent, not chaotic.

### 3b. Direction Consistency
[VERIFIED from Material Design Shared Axis pattern + UX Choreography documentation]

Elements entering from the same direction create implied origin. Elements entering from different directions simultaneously create visual noise.

Rules:
- If content is being revealed (scroll, load), elements enter from below (moving upward into position)
- If content is contextually "behind" the current view, it enters from the left or right (shared axis)
- Background and hero elements may enter from slightly outside the frame; content elements enter from within the viewport (short travel distances, 10-30px max for UI)

Material Design's Shared Axis pattern: when navigating forward, content enters from the right and exits left. When going backward, content enters from the left and exits right. Direction encodes spatial relationship. [VERIFIED]

### 3c. The "Backdrop First" Rule
[VERIFIED from multiple sources including Aninix, IBM Carbon, UX Choreography]

Order: backdrop → container → content → actions.

Background elements animate first but slowly (they set the stage). Container shapes animate second. Content populates the container. Action elements (buttons, CTAs) arrive last because they require context before they're meaningful.

Breaking this order — showing actions before content, or animating foreground before background — feels disorienting because the user reaches for a CTA before understanding what it does.

---

## 4. Exit Choreography: Coordinated Departures

### 4a. The Three Exit Strategies
[VERIFIED from Aninix UI animation guide + UX Collective transition animations guide]

| Strategy | Description | When it works |
|----------|-------------|---------------|
| Reverse order (mirror entrance) | Last element to arrive, first to leave | When the user understands they're going backward or dismissing |
| Simultaneous | Everything fades/scales out at once | Fast transitions, when speed > continuity |
| Cascade outward | Center first → edges, or top → bottom | When content is being "replaced" by something new |

The key rule: exits should be faster than entrances. The user has already processed the content; they don't need to watch it leave carefully. Standard ratio: entrance = 300ms, exit = 200ms. For groups: entrance stagger = 50ms between elements, exit stagger = 25ms or eliminate entirely.

### 4b. What to Avoid
[LLM-ESTIMATED from observed patterns, not a cited rule]

Staggering exits in the same direction as entrances feels like the screen is slowly draining. It creates an incomplete feeling. If you stagger exits at all, reverse the order (last in, first out) or use simultaneous.

### 4c. Material Design's Fade Through Pattern
[VERIFIED from Material Design motion documentation]

For transitions where two screens have no strong spatial relationship: the exiting screen fades out and scales down slightly; the entering screen fades in and scales up. No directional stagger. The exit and entrance are coordinated in time — exit is ~60% complete before entrance begins. This prevents the simultaneous chaos of both screens being visible at full opacity.

---

## 5. Transition Choreography: Elements Rearranging During State Changes

### 5a. The FLIP Technique (Gold Standard)
[VERIFIED from Aerotwist blog (Paul Lewis, Google), CSS-Tricks, GSAP Flip plugin]

FLIP = First, Last, Invert, Play. This is the canonical technique for animating elements that change position or size during a state change (grid → list, sort, filter, expand/collapse).

Process:
1. **First:** Record current position of each element (`getBoundingClientRect()`)
2. **Last:** Apply the end-state DOM change instantaneously (the grid becomes a list, the sort reorders)
3. **Invert:** Apply a CSS transform to each element that puts it back at its "First" position visually, even though it's now in its "Last" DOM position
4. **Play:** Remove the transforms with a transition active — elements visually animate from First to Last

Why it performs: you're only animating `transform` and `opacity`, which run on the compositor thread at 60fps. You never animate `width`, `height`, `top`, `left`, or `grid-template-columns` directly. [VERIFIED]

GSAP's Flip plugin automates this process. The View Transition API (native browser) can also handle it for page-level transitions.

### 5b. Choreographing FLIP at Scale (Grid → List)
[VERIFIED from GSAP Flip plugin docs + animate-css-grid library]

When 12 cards rearrange simultaneously using FLIP, you get a visual swarm. To choreograph:
- Apply staggered FLIP timing: cards closer to their final position animate first; cards traveling further animate with a short delay
- Or: stagger the FLIP play-out by card index, shortest travel time first
- Or: group cards by column, animate column by column

The goal is that the eye can follow the rearrangement as a coherent directional flow, not as a random scatter.

### 5c. Material Design Container Transform
[VERIFIED from Material Design motion documentation]

When a card expands into a full view: the card's container smoothly transforms into the full-screen container. The card's content (title, image) moves into its new position within the expanded view. Elements not in the card (detail text, back button) fade in after the container has mostly settled.

Timing: container transform takes 300ms; new content fades in starting at 200ms (20ms before container settles). The slight overlap makes the expansion feel natural rather than two separate animations.

### 5d. Form → Result Transition
[LLM-ESTIMATED from Material Design principles, applied to calculator context]

This is specific to the calculator use case. When a user submits a form and results appear:

Option A (slide): Form slides up/out, result slides up/in from below. Suggests spatial continuity — results are "below" the form.
Option B (fade-through): Form fades and scales down 5%, result fades and scales up from 95%. Neutral spatial relationship.
Option C (morph): Form inputs condense into the result section (FLIP). The number you typed becomes the result. Strongest sense of causality — input becomes output.

Option C (morph) is the highest-trust transition for calculators. It makes the calculation feel real, not like the screen was replaced. [LLM-ESTIMATED — no direct citation for calculator-specific guidance]

---

## 6. GSAP Timeline Patterns: Professional Sequence Structure

### 6a. The Mental Model (Applies Even Without GSAP)
[VERIFIED from GSAP Timeline documentation + Noble Desktop tutorial]

A GSAP timeline is a container for tweens. The key insight: without a timeline, every animation needs a delay. With a timeline, animations position themselves relative to each other using the position parameter.

Position parameter syntax:
- `"+=0.2"` — start 0.2s after the previous tween ends (gap)
- `"-=0.2"` — start 0.2s before the previous tween ends (overlap)
- `"<"` — start at the same time as the previous tween (simultaneous)
- `">+0.1"` — start 0.1s after the previous tween starts (relative to start, not end)
- `"labelName"` — start at a named label point in the timeline

This is the conductor model implemented. The timeline is the score; tweens are the instruments; the position parameter is the conductor's cue.

### 6b. Nested Timelines: Modular Choreography
[VERIFIED from GSAP community forums + James Bateson GSAP timeline learnings]

For complex sequences, build sub-timelines for each logical group, then compose them into a master timeline.

```js
const heroEntrance = gsap.timeline()
heroEntrance.from(".headline", { y: 20, opacity: 0, duration: 0.4 })
heroEntrance.from(".subheadline", { y: 15, opacity: 0, duration: 0.3 }, "-=0.2")
heroEntrance.from(".cta", { y: 10, opacity: 0, duration: 0.25 }, "-=0.15")

const backgroundSettle = gsap.timeline()
backgroundSettle.from(".bg-shape", { scale: 1.05, opacity: 0, duration: 0.6 })

const master = gsap.timeline()
master.add(backgroundSettle)          // background first
master.add(heroEntrance, "-=0.3")     // hero entrance overlaps background settle
```

Benefits: each sub-timeline is independently testable, reusable, and can be controlled separately (pause, reverse, speed up) while remaining part of the master sequence.

### 6c. Callbacks as Choreography Anchors
[VERIFIED from GSAP Timeline documentation]

`onComplete`, `onStart`, and `onUpdate` callbacks let you trigger non-CSS events at specific points in the sequence:
- Fire a counter (number increments as the result section animates in)
- Trigger a sound at the moment the result appears
- Switch a state flag so secondary elements know when to begin

This is how complex "living" animations synchronize behavior (JS state) with visual animation (CSS/canvas).

### 6d. The Key Mental Model Takeaway (CSS-only applications)
[LLM-ESTIMATED — transferring GSAP mental model to CSS]

Even in pure CSS, use the GSAP mental model: think in terms of "what is the previous event, and how long after it does this element start?" Set `animation-delay` not as an absolute time value, but as the previous element's duration minus desired overlap. This makes the sequence robust if you change a duration — you change one number, the rest cascade correctly.

---

## 7. The Breath Pattern: A Living System

### 7a. What It Is
[VERIFIED from Animation Mentor breathing loop tutorial + AnimSchool blog + Codrops Frequency Breathwork project]

The breath pattern: multiple elements expand and contract together in a synchronized rhythm, creating the sense of a single living system rather than a collection of parts.

In character animation: ribcage expands → shoulders follow at slight offset → head lifts last. All are driven by the same underlying breath cycle but with cascading offsets that make it feel organic rather than mechanical.

In UI: the same principle applied to interface elements that pulse, glow, or scale rhythmically.

### 7b. Implementation Pattern
[VERIFIED from AnimSchool breathing principles + CSS breathing animation examples]

The breath pattern requires:
1. A master cycle duration (the "breath rate") — typically 3-5 seconds for calming, 1.5-2.5s for energetic
2. A primary element that drives the cycle (the chest)
3. Secondary elements offset by 10-20% of the cycle duration (the shoulders)
4. Tertiary elements offset by 20-40% of the cycle duration (the head, hands)
5. All elements use the same easing (typically ease-in-out) to suggest shared energy source

CSS example structure for a pulsing dot indicator:
```css
.dot-core     { animation: breathe 4s ease-in-out infinite; }
.dot-ring-1   { animation: breathe 4s ease-in-out infinite 0.4s; }  /* 10% offset */
.dot-ring-2   { animation: breathe 4s ease-in-out infinite 0.8s; }  /* 20% offset */
```

If all three had zero delay they would feel mechanical — a flashing light, not a living pulse.

### 7c. The Pulse Application (Specific to This Product)
[LLM-ESTIMATED — applied to HealthCalculators Pulse context]

The pulsing green dot on the Pulse product is the canonical place for this pattern. The dot-core and dot-ring-1 that already exist are the first two elements of a breath pattern. Adding a third, slower, outer ring with a 20-40% cycle offset would complete the "living system" feeling without adding visual noise.

The breath pattern is also applicable to: calculator result sections that "breathe" once after results appear (a single, slow scale pulse: 1.0 → 1.01 → 1.0 over 1.5s), suggesting the result is settled and alive.

### 7d. Differentiating Breath from Looping
[LLM-ESTIMATED]

Breathing implies a cycle with biological rhythm — variable slightly, never perfectly mechanical. To avoid a metronome feeling:
- Use `animation-timing-function: ease-in-out` (not linear)
- Slight asymmetry: inhale longer than exhale (inhale = 60% of cycle, exhale = 40%)
- Optional: add `animation-duration: calc(4s + var(--jitter))` with small CSS variable variation per element (0.1-0.3s range)

---

## 8. Planning Process: Storyboard → Timing Sheet → Implementation

### 8a. The Three-Phase Planning Process
[VERIFIED from Milanote motion graphics pre-production guide + Toon Boom timing chart documentation + story-boards.ai]

**Phase 1: Storyboard (visual intent)**
Identify keyframes — the major states the screen passes through. Not every intermediate frame, only the start state and end state of each meaningful animation event. Sketch or describe:
- What is on screen before the animation
- What triggers it
- What is on screen after it settles

**Phase 2: Timing Sheet (beat chart)**
Map each element group to a time axis. This is called a timing chart in traditional animation, a beat chart in motion graphics. Structure:

| Time (ms) | Element | Action | Duration | Easing |
|-----------|---------|--------|----------|--------|
| 0 | Background | fade in | 200ms | ease-out |
| 60 | Container | scale 0.98→1.0, fade in | 250ms | ease-out |
| 120 | Headline | y: 20→0, fade in | 350ms | ease-out |
| 200 | Subheadline | y: 15→0, fade in | 300ms | ease-out |
| 280 | CTA button | y: 10→0, fade in | 250ms | ease-out |

Reading the timing sheet tells you: does anything feel too late? Is anything competing for attention? Are the overlaps correct?

**Phase 3: Implementation**
Build in CSS variables or GSAP timeline using the timing sheet as the source of truth, not intuition. If you change a duration, update the sheet first, then the code.

### 8b. The Two Questions Before Any Sequence
[LLM-ESTIMATED from synthesis of all sources]

Before writing any animation:
1. What is the user trying to do at this moment? (Intent)
2. What element answers that intent most directly? (That element is the conductor/lead)

Everything else in the sequence exists to support the lead's arrival. If an animation doesn't support the lead's arrival, it's decorative. Decorative animations should enter last, at reduced prominence, and exit first.

### 8c. What a Timing Sheet Catches That Code Doesn't
[LLM-ESTIMATED]

- The 23rd element in a stagger starting at 1,150ms — visible only in the timing sheet, invisible when reading code
- Two unrelated elements accidentally animating simultaneously (conflicts show as vertical alignment in the sheet)
- Sequences where no element is clearly dominant (no conductor) — all elements start at the same delay offset, which means there's no lead

---

## Cross-Domain Synthesis: Five Principles That Appear Everywhere

These patterns appear in IBM Carbon, Material Design, Disney's 12 Principles, GSAP documentation, and UX research independently. That convergence makes them the closest thing to ground truth.

| Principle | Source domains | One-sentence rule |
|-----------|---------------|------------------|
| **Lead and follow** | Disney, GSAP, Material Design | One element leads; others follow at defined offsets |
| **Entrance slower than exit** | Aninix, NNGroup, UX Collective | Enter at full duration, exit at 60-70% of entrance duration |
| **Group before stagger** | IBM Carbon, Material Design, UX Collective | Stagger groups, not individual elements, above 4+ items |
| **Direction encodes meaning** | Material Design, IBM Carbon | Up = reveal, right = forward, left = back, down = dismiss |
| **Overlap creates connection** | Disney Overlapping Action, GSAP position parameter | Each element should start before the previous finishes |

---

## Falsifiability

Each major finding — what would disprove it:

- **Lead and follow improves perceived quality:** Would be disproved if A/B tests showed users rate simultaneous animations as equally or more natural. Only one study (NNGroup on animation duration) touches this indirectly; it does not test conductor vs simultaneous directly.
- **Exit faster than entrance:** Could be wrong for animations where exit is itself a meaningful narrative event (a long, deliberate exit can signal consequence). The rule holds for UI transitions; does not necessarily hold for storytelling sequences.
- **Group before stagger:** If users perceive individual-element staggers for 8+ items as more dynamic than grouped staggers, this rule breaks. No direct user test cited.
- **Direction encodes meaning:** This is a Material Design convention, not a universal principle. In right-to-left locales, directional meaning reverses.
- **The breath pattern creates "living" feel:** This is [LLM-ESTIMATED] applied from character animation to UI. Direct UI testing of breath patterns vs mechanical loops is not in the sources found.

---

## Uncertainty Flags

- [VERIFIED] markers indicate the finding came directly from named source documentation
- [LLM-ESTIMATED] markers indicate reasoning from principles, not direct citation
- GSAP-specific timing numbers are verified; CSS-only equivalents are estimated to be similar
- The form → result transition section (Section 5d) is entirely LLM-ESTIMATED; no direct citation exists for calculator-specific transition choreography
- The breath pattern applied to UI dot elements (Section 7c, 7d) is LLM-ESTIMATED from character animation principles

---

## Sources

- [Staggers — GSAP Docs](https://gsap.com/resources/getting-started/Staggers/)
- [GSAP Timeline Documentation](https://gsap.com/docs/v3/GSAP/Timeline/)
- [IBM Carbon Design System — Motion Choreography](https://carbondesignsystem.com/elements/motion/choreography/)
- [IBM Carbon Design System — Motion Overview](https://carbondesignsystem.com/elements/motion/overview/)
- [Material Design — Choreography](https://m1.material.io/motion/choreography.html)
- [Material Design — The Motion System](https://m2.material.io/design/motion/the-motion-system.html)
- [FLIP Your Animations — Paul Lewis, Aerotwist](https://aerotwist.com/blog/flip-your-animations/)
- [Animating Layouts with FLIP — CSS-Tricks](https://css-tricks.com/animating-layouts-with-the-flip-technique/)
- [GSAP Flip Plugin](https://gsap.com/docs/v3/Plugins/Flip/)
- [Animating Responsive Grid Layouts with GSAP Flip — Codrops](https://tympanus.net/codrops/2026/01/20/animating-responsive-grid-layout-transitions-with-gsap-flip/)
- [Stagger Animation — Motion.dev](https://motion.dev/docs/stagger)
- [Stagger Animation — Aninix Wiki](https://www.aninix.com/wiki/how-to-create-a-good-stagger-in-the-ui-animation)
- [Repeatable Staggered Animation Three Ways — CSS-Tricks](https://css-tricks.com/repeatable-staggered-animation-three-ways-sass-gsap-web-animations-api/)
- [Staggering Animations — CSS-Tricks](https://css-tricks.com/staggering-animations/)
- [Offset and Delay in Motion Design — SVGator](https://www.svgator.com/blog/offset-delay-motion-design/)
- [Disney's 12 Principles in UI — IxDF](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)
- [Disney's 12 Principles in UX Design — UX Collective](https://uxdesign.cc/disneys-12-principles-of-animation-exemplified-in-ux-design-5cc7e3dc3f75)
- [Follow Through and Overlapping Action — AnimatedVideos.co](https://animatedvideos.co/blog/follow-through-and-overlapping-in-animation/)
- [Animation Duration — NNGroup](https://www.nngroup.com/articles/animation-duration/)
- [Transition Animations: A Practical Guide — UX Collective](https://uxdesign.cc/transition-animations-a-practical-guide-5dba4d42f659)
- [UX Choreography — Failfast Design](https://www.failfast.design/services/ux-choreography)
- [Motion Design UX: Techniques & Choreography — Christina Paone, Medium](https://medium.com/@paonecreative_87456/motion-design-ux-techniques-choreography-de3931080308)
- [Motion Design: Intro to UX Choreography — UXPAMagazine](http://uxpamagazine.org/motion-design/)
- [Choreography — CSS Animations and Transitions — Frontend Masters](https://frontendmasters.com/courses/css-animations/choreography/)
- [View Transitions Staggering — Frontend Masters Blog](https://frontendmasters.com/blog/view-transitions-staggering/)
- [Animation Timing Chart — Business of Animation](https://businessofanimation.com/the-key-to-perfecting-your-animation-timing-chart/)
- [Timing and Transitions in Motion Storyboarding — story-boards.ai](https://www.story-boards.ai/content-hub/blog/understanding-timing-and-transitions-in-motion-graphics-storyboarding/)
- [How to Plan a Motion Graphics Project — Milanote](https://milanote.com/guide/motion-graphics-pre-production)
- [Breathing Life Into Your Animation — AnimSchool Blog](https://blog.animschool.edu/2024/11/15/breathing-life-into-your-animation/)
- [Frequency Breathwork: Translating Invisible Rhythm of Breath — Codrops](https://tympanus.net/codrops/2025/12/29/frequency-breathwork-translating-the-invisible-rhythm-of-breath-into-digital-form/)
- [Tutorial: Animate Natural Breathing Loops — Animation Mentor](https://www.animationmentor.com/blog/tutorial-animate-natural-breathing-loops/)
- [Rearrange/Animate CSS Grid with View Transition API — Bram.us](https://www.bram.us/2023/05/09/rearrange-animate-css-grid-layouts-with-the-view-transition-api/)
- [GSAP Timelines Tutorial — Noble Desktop](https://www.nobledesktop.com/learn/javascript/gsap-timelines-animating-multiple-elements-in-sequence)
- [7 Must-Know GSAP Animation Tips — Codrops](https://tympanus.net/codrops/2025/09/03/7-must-know-gsap-animation-tips-for-creative-developers/)
