# Disney's 12 Principles of Animation — Web UI Craft Reference

**Date:** 2026-03-22
**Sources:** 16 searches across cssanimation.rocks, IxDF, UX Collective, Smashing Magazine, CSS-Tricks, MDN, Josh W. Comeau, Tobias Ahlin, Nielsen Norman Group, Animation Mentor, NN/G, codepen examples
**Purpose:** Deep craft reference for `/motion` agent and design agent. Implementation-ready CSS/JS. Not surface-level.
**Claim tagging:** [VERIFIED] = from primary source documentation or canonical reference. [ASSUMED] = inferred from principle, not directly stated in source.

---

## Background

Frank Thomas and Ollie Johnston (Disney animators, 9 Old Men) published these principles in 1981 in "The Illusion of Life: Disney Animation." The principles describe how to make motion feel physically believable and emotionally resonant. They are craft principles, not style rules.

The web translation: CSS/JS animation has the same job as a Disney animator. The question is always "does this motion communicate weight, intent, and emotion?" If not, it fails — regardless of technical correctness.

**One rule for web application:** Every animation must have a mechanical reason AND an emotional reason. The mechanical reason is usability (confirms action, shows state). The emotional reason is feeling (delight, weight, precision). Animations that have only one of these feel either sterile or gratuitous.

---

## Pre-Flight Note on Performance

Before any implementation: only animate GPU-composited properties without triggering layout. [VERIFIED — MDN, Smashing Magazine]

**Safe to animate (no layout reflow):**
- `transform` (translate, scale, rotate, skew)
- `opacity`
- `filter` (use sparingly — can be expensive)
- `clip-path` (modern browsers)

**Expensive — avoid animating:**
- `width`, `height`, `margin`, `padding`, `top`, `left` (triggers layout)
- `box-shadow` (triggers paint) — use `filter: drop-shadow()` instead [VERIFIED — CSS-Tricks]
- `background-color` alone (triggers paint)

**Accessibility — always include:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 1. Squash and Stretch

### The Principle

The most fundamental of all 12. An object's volume stays constant — when it squashes (compresses on one axis) it must stretch on the perpendicular axis. This communicates mass, flexibility, and physical properties. A rubber ball squashes on impact and stretches during fast movement. A rigid metal ball does neither.

**Why it matters for UI:** Without squash and stretch, UI elements feel weightless and incorporeal — like flat rectangles moving in 2D space. With it, elements feel like they have physical mass and respond to forces. The difference between a button press that feels like clicking a wooden block vs. a button press that feels like pressing a real physical button.

### What it looks like MISSING

A button that simply changes background color on click. Or an element that scales uniformly (both axes together) — that is scaling, not squash and stretch. Uniform scale communicates "resize," not "impact."

### What it looks like PRESENT

A button that squashes vertically (scaleY: 0.92) and simultaneously expands horizontally (scaleX: 1.05) on press — like a real button being physically depressed. A notification badge that briefly stretches tall before settling to its final position — like a drop of liquid landing.

### CSS Implementation

**Button press (tactile click feedback):**
```css
.button {
  transition: transform 80ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.button:active {
  /* Squash on press: compress Y, expand X to preserve volume */
  transform: scaleX(1.04) scaleY(0.94);
}
```

**Number counter popping in (value reveal with impact):**
```css
@keyframes countReveal {
  0%   { transform: scaleX(0.85) scaleY(1.2); opacity: 0; }
  60%  { transform: scaleX(1.04) scaleY(0.96); opacity: 1; }
  80%  { transform: scaleX(0.98) scaleY(1.01); }
  100% { transform: scaleX(1) scaleY(1); }
}

.result-number {
  animation: countReveal 280ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
```

**Card interaction (press and release):**
```css
.card {
  transition: transform 120ms ease-out;
}
.card:active {
  transform: scaleX(1.02) scaleY(0.97) translateY(2px);
}
```

### Calibration Rules [ASSUMED based on principle]

- Subtle UI: 2-4% squash/stretch differential. Keeps it professional.
- Playful UI: 6-10% differential. Feels bouncy and responsive.
- Above 15%: Cartoonish. Only for celebration/success states.
- Duration: 60-120ms for press squash. 200-350ms for return/settle.
- Volume must be roughly preserved: if scaleY drops by 0.08, scaleX should rise by ~0.05-0.06.

---

## 2. Anticipation

### The Principle

Before a major action, there is a preparatory movement in the opposite direction. A baseball player winds up before throwing. A character crouches before jumping. This wind-up accomplishes two things: (1) it signals to the viewer that something is about to happen, (2) it builds kinetic energy that makes the subsequent action feel more powerful.

**Why it matters for UI:** Anticipation is the principle that makes transitions feel earned rather than jarring. Without it, state changes feel instantaneous and cheap — the UI teleports rather than moves. Anticipation also reduces cognitive surprise: the user's eye has already been primed for where the motion is going.

### What it looks like MISSING

A drawer that snaps open with no warning. A button that immediately navigates with no acknowledgment. A tooltip that appears from nowhere. The user's attention is always one step behind the interface.

### What it looks like PRESENT

A "Submit" button that pulls back very slightly (scale 0.97) on hover — as if gathering force — before the click action fires. A sidebar that shifts 2px inward before sweeping open. A loading skeleton that pulses once before data appears.

### CSS Implementation

**Button hover anticipation (pull-back before action):**
```css
.cta-button {
  transition: transform 150ms ease-in-out;
}

.cta-button:hover {
  /* Anticipation: slight pull-back creates tension */
  transform: scale(0.97);
}

.cta-button:active {
  /* Release: spring forward on click */
  transform: scale(1.04);
  transition-duration: 80ms;
}
```

**Drawer/panel anticipation before open:**
```css
.drawer {
  transform: translateX(-100%);
  transition: transform 350ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* JS adds .is-opening first, then .is-open after 50ms */
.drawer.is-opening {
  transform: translateX(-105%); /* over-retract = anticipation wind-up */
  transition-duration: 80ms;
  transition-timing-function: ease-in;
}

.drawer.is-open {
  transform: translateX(0);
}
```

**Reveal anticipation (content about to appear):**
```css
@keyframes anticipateReveal {
  0%   { transform: scale(0.94); opacity: 0; }
  30%  { transform: scale(0.92); opacity: 0.2; }  /* pull back further */
  100% { transform: scale(1); opacity: 1; }
}

.reveal-element {
  animation: anticipateReveal 400ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
```

### Calibration Rules [ASSUMED]

- Anticipation magnitude: 3-8% of main action magnitude. Too much feels theatrical.
- Anticipation duration: 15-30% of total animation duration.
- Hover anticipation: 100-200ms. Long enough to notice, short enough not to delay.
- Do NOT use on every interaction — reserve for high-stakes actions (submit, navigate, reveal).

---

## 3. Staging

### The Principle

Present an idea so it is completely clear to the audience. Only one thing should capture attention at a time. In film, this is camera composition, lighting, and framing. In animation, it is choosing which element moves, when, and against what background. The purpose is not decoration — it is clarity of communication.

**Why it matters for UI:** Staging is the hardest principle to apply in UI because designers tend to animate everything at once. Multiple elements animating simultaneously create visual noise that overwhelms the user. Staging means choosing a reading order and enforcing it through timing, contrast, and motion hierarchy.

### What it looks like MISSING

A dashboard that loads 12 cards all simultaneously, or a modal that fades in while the trigger button also animates. The user's eye doesn't know where to land. Cognitive load spikes.

### What it looks like PRESENT

A result page where: (1) background darkens first (150ms), then (2) the result number appears and pulses (300ms), then (3) supporting labels fade in staggered (50ms apart each), then (4) CTA button appears last. The user reads the result in the order the designer intended.

### CSS/JS Implementation

**Staggered staging — result reveal sequence:**
```css
.result-overlay   { transition: opacity 150ms ease-out; }
.result-number    { transition: opacity 300ms ease-out 150ms, transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1) 150ms; }
.result-label-1  { transition: opacity 200ms ease-out 400ms; }
.result-label-2  { transition: opacity 200ms ease-out 480ms; }
.result-label-3  { transition: opacity 200ms ease-out 560ms; }
.result-cta      { transition: opacity 200ms ease-out 700ms; }

/* All start hidden */
.result-overlay,
.result-number,
.result-label-1,
.result-label-2,
.result-label-3,
.result-cta {
  opacity: 0;
}

/* JS adds .staged class, CSS cascades the timing */
.staged .result-overlay  { opacity: 0.7; }
.staged .result-number   { opacity: 1; transform: none; }
.staged .result-label-1  { opacity: 1; }
.staged .result-label-2  { opacity: 1; }
.staged .result-label-3  { opacity: 1; }
.staged .result-cta      { opacity: 1; }
```

**Focus staging with blur (modal / result card):**
```css
.background-blur {
  transition: filter 200ms ease-out, opacity 200ms ease-out;
}

.background-blur.staged {
  filter: blur(4px);
  opacity: 0.6;
}

.foreground-element {
  /* No blur, sits above — contrast creates staging */
  position: relative;
  z-index: 10;
}
```

**JS stagger utility (dynamic element count):**
```js
function stageElements(elements, baseDelay = 0, staggerMs = 60) {
  elements.forEach((el, i) => {
    el.style.transitionDelay = `${baseDelay + i * staggerMs}ms`;
    el.classList.add('visible');
  });
}
```

### Staging Hierarchy [VERIFIED — NN/G, UX Collective]

1. Movement beats stillness — a moving element wins attention over static ones
2. Contrast beats sameness — bright on dark, large on small, fast on slow
3. Sequence beats simultaneous — enter elements in reading order
4. Primary action gets full motion; supporting elements get fade-only
5. Never animate more than 2-3 elements in the same 300ms window

---

## 4. Straight Ahead vs. Pose to Pose

### The Principle

Two opposing animation workflows. Straight Ahead: animate frame-by-frame from start to finish without planning ahead — good for fluid, organic, unpredictable motion (fire, water, cloth, smoke). Pose to Pose: define the key states first, then fill in the in-betweens — good for controlled, structured, emotionally precise motion.

**Why it matters for UI:** This principle maps directly to the choice between CSS animation (pose to pose — you define keyframes) and procedural/physics animation (straight ahead — a spring or physics engine determines intermediate states). Choosing the wrong approach produces either overcontrolled organic effects or undercontrolled UI transitions.

### When to Use Each in Web UI [VERIFIED — Adobe, Animation Mentor]

**Pose to Pose (CSS keyframes / defined transitions):**
- State transitions with known start/end (open/close, show/hide)
- Sequenced reveals with precise timing
- Brand motion with controlled rhythm
- Any animation that must land exactly on a specific value

**Straight Ahead (physics/spring/requestAnimationFrame):**
- Drag interactions
- Particle effects
- Fluid or cloth-like trailing elements
- Gesture-driven animations
- Any animation where the end state isn't known until runtime

### CSS Implementation (Pose to Pose)

```css
/* Classic pose-to-pose: you define every key state */
@keyframes resultReveal {
  0%   { opacity: 0; transform: translateY(20px) scale(0.95); }
  /* In-between: you define this explicitly */
  60%  { opacity: 1; transform: translateY(-4px) scale(1.02); }
  80%  { transform: translateY(2px) scale(0.99); }
  100% { transform: translateY(0) scale(1); }
}
```

### JS Implementation (Straight Ahead — Spring Physics)

```js
// Spring animation: state evolves frame-by-frame
// No CSS keyframes — physics determines each intermediate position
class SpringAnimation {
  constructor(stiffness = 200, damping = 20) {
    this.stiffness = stiffness;
    this.damping = damping;
    this.position = 0;
    this.velocity = 0;
    this.target = 0;
  }

  step(dt) {
    const force = -this.stiffness * (this.position - this.target);
    const dampingForce = -this.damping * this.velocity;
    const acceleration = (force + dampingForce) / 1; // mass = 1
    this.velocity += acceleration * dt;
    this.position += this.velocity * dt;
    return this.position;
  }
}

// Each frame is computed — classic straight-ahead approach
function animateSpring(element, targetValue) {
  const spring = new SpringAnimation(180, 22);
  spring.target = targetValue;

  let lastTime = null;
  function tick(timestamp) {
    if (!lastTime) lastTime = timestamp;
    const dt = (timestamp - lastTime) / 1000;
    lastTime = timestamp;

    const pos = spring.step(dt);
    element.style.transform = `translateX(${pos}px)`;

    if (Math.abs(spring.velocity) > 0.01 || Math.abs(pos - targetValue) > 0.01) {
      requestAnimationFrame(tick);
    } else {
      element.style.transform = `translateX(${targetValue}px)`;
    }
  }
  requestAnimationFrame(tick);
}
```

**Modern CSS alternative (spring-like with linear()):**
```css
/* CSS linear() can approximate spring behavior — no JS needed */
.spring-element {
  transition: transform 600ms linear(
    0, 0.009, 0.035, 0.078, 0.138 15.4%,
    0.373, 0.654, 0.854, 0.968, 1.029,
    1.051 45.4%, 1.053, 1.038, 1.012 63.1%,
    0.99, 0.977, 0.971 73.3%, 0.973, 0.992, 1.004, 1.008,
    1.007, 1.002, 0.999, 1
  );
}
```

### Hybrid Approach [VERIFIED — Animation Mentor, Adobe]

Most complex UI interactions use both: pose-to-pose for the overall structure (element enters from bottom, settles at target) and straight-ahead for secondary elements (trailing shadow, particle burst on arrival). Define the skeleton with keyframes, handle organic details with physics.

---

## 5. Follow-Through and Overlapping Action

### The Principle

Two related concepts. Follow-Through: when a main action stops, loose parts continue moving briefly past the stopping point before catching up. Overlapping Action: different parts of an object or system move at different rates — they don't all start and stop simultaneously.

**Why it matters for UI:** When every element in a UI update starts and stops at the exact same millisecond, the result looks mechanical and lifeless. Overlapping action — staggering start/stop times and having some elements overshoot — is what separates premium motion design from competent motion design. The difference between a notification system that feels alive and one that feels like a PowerPoint slideshow.

### What it looks like MISSING

Three list items appearing simultaneously with identical 300ms fade. No element moves after the primary transition ends. Everything locks into position at the same frame.

### What it looks like PRESENT

A card slides into position (main action). Its shadow arrives 40ms later and settles slightly further, then pulls back (follow-through). A list of results appears with each item staggered 60ms after the previous, and the last item overshoots slightly before settling (overlapping action + follow-through).

### CSS Implementation

**Staggered list with overlapping action:**
```css
.list-item {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 280ms ease-out, transform 350ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Each item has a different delay — overlapping action */
.list-item:nth-child(1) { transition-delay: 0ms; }
.list-item:nth-child(2) { transition-delay: 55ms; }
.list-item:nth-child(3) { transition-delay: 110ms; }
.list-item:nth-child(4) { transition-delay: 165ms; }
.list-item:nth-child(5) { transition-delay: 220ms; }

.list-item.visible {
  opacity: 1;
  transform: translateY(0);
}
```

**Follow-through on a sliding panel (overshoots, pulls back):**
```css
.panel {
  transform: translateX(100%);
  transition: transform 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
  /* cubic-bezier values > 1 = overshoot = follow-through effect */
}

.panel.open {
  transform: translateX(0);
}
```

**Shadow follow-through (arrives after element, settles later):**
```css
.card {
  transform: translateY(20px);
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
  transition:
    transform 300ms ease-out,
    filter 380ms ease-out 40ms; /* shadow arrives 40ms late = follow-through */
}

.card.visible {
  transform: translateY(0);
  filter: drop-shadow(0 8px 24px rgba(0,0,0,0.15));
}
```

**JS dynamic overlapping action (for dynamic lists):**
```js
function revealWithOverlap(elements, baseDelay = 0) {
  elements.forEach((el, i) => {
    // Stagger decreases as list grows — avoids waiting 3 seconds for 50 items
    const stagger = Math.min(60, 400 / elements.length);
    setTimeout(() => {
      el.classList.add('visible');
    }, baseDelay + i * stagger);
  });
}
```

### Calibration [ASSUMED from principle, VERIFIED for stagger values from NN/G]

- Stagger between elements: 40-80ms for lists. Below 40ms is imperceptible. Above 100ms feels like a pageload bug.
- Follow-through overshoot: 5-15% beyond target. Use overshoot cubic-bezier (y values > 1).
- Shadow delay: 30-60ms behind primary element.
- Number of simultaneous animations: maximum 3-4 in the same visual zone.

---

## 6. Slow In and Slow Out (Easing)

### The Principle

Natural objects accelerate and decelerate — they don't move at constant speed. A ball dropped from height starts slow, accelerates through the middle, and decelerates as a hand catches it. Constant-speed (linear) animation is the most unnatural motion possible in the physical world.

"Slow in" = ease-in = starts slow, ends fast (like something launching)
"Slow out" = ease-out = starts fast, ends slow (like something landing)
Combined = ease-in-out = the natural arc of most physical motion

**Why it matters for UI:** Linear animations feel robotic. The easing curve IS the emotional character of a motion. Two animations moving an element from the same point A to point B can feel completely different based on their easing alone — one feels light, one feels heavy, one feels confident, one feels nervous.

### Easing Emotional Map [VERIFIED — Josh Collinsworth, Motion.dev]

| Easing | Cubic Bezier | Emotional Character | UI Use Case |
|--------|-------------|---------------------|-------------|
| ease-out | `cubic-bezier(0, 0, 0.58, 1)` | Confident arrival, authoritative | Elements entering screen, reveals |
| ease-in | `cubic-bezier(0.42, 0, 1, 1)` | Committed exit, no hesitation | Elements leaving screen, dismissals |
| ease-in-out | `cubic-bezier(0.42, 0, 0.58, 1)` | Balanced, neutral, professional | Object moving across screen |
| Spring overshoot | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful, energetic, confident | Buttons, card reveals, badges |
| Sharp ease-out | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Instant, precise, responsive | Hover states, micro-interactions |
| Gentle ease-out | `cubic-bezier(0.0, 0.0, 0.6, 1)` | Soft, calm, medical | Healthcare, wellness contexts |

### Custom Easing for Specific Emotions [VERIFIED — Josh Collinsworth blog]

**Emotional easing by context:**

```css
:root {
  /* Responsive: feels immediate, user in control */
  --ease-snap:    cubic-bezier(0.0, 0.0, 0.15, 1.0);

  /* Confident: for result reveals — arrives fast, settles */
  --ease-land:    cubic-bezier(0.0, 0.0, 0.3, 1.0);

  /* Playful: for success states, celebrations */
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Medical/calm: for anxiety-reducing contexts */
  --ease-gentle:  cubic-bezier(0.25, 0.46, 0.45, 0.94);

  /* Urgent: for alerts, warnings */
  --ease-urgent:  cubic-bezier(0.55, 0, 1, 0.45);

  /* Dismissal: element leaving, no return */
  --ease-exit:    cubic-bezier(0.4, 0, 1, 1);
}
```

**The rule for entering vs exiting elements** [VERIFIED — Josh W. Comeau, NN/G]:
```css
/* Elements entering: ease-OUT (fast start, slow settle = confident arrival) */
.element-enter {
  animation: slideIn 280ms cubic-bezier(0, 0, 0.3, 1) forwards;
}

/* Elements exiting: ease-IN (slow start, fast end = committed departure) */
.element-exit {
  animation: slideOut 220ms cubic-bezier(0.4, 0, 1, 1) forwards;
}

/* Exit is always SHORTER than enter — psychologically correct */
/* Exit: 180-250ms. Enter: 250-400ms. */
```

**Constructing custom cubic-bezier for weight:**
```css
/* Heavy object — slow start, very slow end, takes time to decelerate */
--ease-heavy: cubic-bezier(0.14, 0.0, 0.0, 1.0);

/* Light object — accelerates quickly, barely decelerates */
--ease-light: cubic-bezier(0.0, 0.0, 0.55, 1.0);

/* Weightless/floating — continuous gentle curve */
--ease-float: cubic-bezier(0.37, 0, 0.63, 1);
```

### Duration Map by Interaction Type [VERIFIED — NN/G animation-duration article]

| Interaction | Duration Range | Reason |
|------------|---------------|--------|
| Hover state feedback | 100-200ms | Must feel instant |
| Button press response | 60-120ms | Tactile immediacy |
| Tooltip appear | 150-250ms | Quick, unobtrusive |
| Card/panel reveal | 250-400ms | Enough time to notice motion |
| Page transition | 300-500ms | User expects travel time |
| Modal/overlay | 200-350ms | Focus shift needs acknowledgment |
| Data load reveal | 350-600ms | Multiple elements, sequenced |
| Celebration/success | 400-800ms | Allowed to linger, earned |

---

## 7. Arcs

### The Principle

All natural motion follows curved paths — arcs — not straight lines. A hand doesn't move from A to B in a straight line; it follows a slight arc. Joints rotate around pivot points. Eyes track in curves. Straight-line motion reads as mechanical because nothing in biology or physics produces perfectly straight trajectories.

**Why it matters for UI:** Most UI animations move in straight lines because `translate` is linear by default. This is why even technically well-done animations can feel robotic. Adding arc to motion — particularly for elements moving significant distances — immediately upgrades the perceived quality from "competent" to "refined."

### What it looks like MISSING

A tooltip that slides directly left-to-right from the cursor position. A card that translates straight down to its target. A number that counts up in a linear trajectory with no arc at all.

### What it looks like PRESENT

A notification that enters from the top-right in a slight arc (starts moving down and left, curves to settle). A modal that rises from below with a subtle curve (slight X drift as it rises). A drag-and-drop item that traces a natural arc as it returns to position.

### CSS Implementation

**Layered animation technique (arc without motion-path)** [VERIFIED — Tobias Ahlin]:
```css
/* Technique: separate X and Y transitions with different easings
   The different easing on each axis creates a curved path */

.arc-element {
  /* X: ease-out (fast start, slow end) */
  /* Y: ease-in (slow start, fast end) */
  /* Combined: creates a natural parabolic arc */
}

@keyframes arcX {
  from { transform: translateX(0); }
  to   { transform: translateX(200px); }
}
@keyframes arcY {
  from { transform: translateY(0); }
  to   { transform: translateY(-100px); }
}

.arc-element {
  animation:
    arcX 500ms cubic-bezier(0.4, 0, 0.6, 1) forwards,
    arcY 500ms cubic-bezier(0, 0, 0.4, 1) forwards;
}
/* Result: element follows a natural arc, not a straight diagonal */
```

**Modern CSS motion-path (true curve)** [VERIFIED — MDN CSS motion path]:
```css
.notification-enter {
  offset-path: path('M 20 -60 Q 40 20 0 0');
  /* Q = quadratic bezier curve — defines the arc */
  offset-distance: 0%;
  animation: followArc 400ms cubic-bezier(0, 0, 0.3, 1) forwards;
}

@keyframes followArc {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}
```

**Rotational arc (elements orbiting or swinging):**
```css
.pendulum {
  transform-origin: top center; /* pivot point = arc center */
  animation: swing 2s ease-in-out infinite alternate;
}

@keyframes swing {
  from { transform: rotate(-15deg); }
  to   { transform: rotate(15deg); }
}
/* Result: pure arc motion, mathematically correct */
```

**Tooltip arc entry:**
```css
.tooltip {
  transform-origin: bottom center;
  animation: tooltipEnter 200ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes tooltipEnter {
  from {
    opacity: 0;
    transform: translateY(6px) scale(0.92) rotate(-2deg); /* slight rotation = arc suggestion */
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1) rotate(0deg);
  }
}
```

### When Arc Matters Most [ASSUMED]

- Large-distance movements (>100px): arc is strongly needed
- Small micro-interactions (<20px): arc is optional, slight rotation achieves similar feel
- Pendulum/orbital motion: arc is the motion, not an enhancement
- Number counting: arc doesn't apply (numerical progression, not spatial movement)

---

## 8. Secondary Action

### The Principle

A secondary action is a supporting motion that reinforces or enriches the main action without competing with it. In character animation: while a character walks (primary action), their arms swing and their hair moves (secondary actions). The secondary actions must never distract from — or be mistaken for — the primary action.

**Why it matters for UI:** Secondary actions are the difference between an animation that communicates and an animation that delights. The primary action carries information. The secondary action carries personality. A result number appearing (primary) with a subtle glow pulse (secondary) communicates the same information but feels like the tool is alive and responding.

**The risk:** Secondary actions that become primary actions — ripples too large, particles too bright, shadow too obvious. When secondary actions grab attention, the user misses the primary action.

### What it looks like MISSING

A submit button that changes to "Loading..." with a spinner. Functional, communicates state. But sterile — no sense the system received the input and is working hard.

### What it looks like PRESENT

Submit button changes to "Loading..." (primary) and its background subtly pulses (secondary) and there is a very faint progress bar growing behind the text (secondary). The user feels the system is active.

### CSS Implementation

**Button submit: primary = label change, secondary = pulse:**
```css
.submit-button {
  position: relative;
  overflow: hidden;
}

/* Secondary: background sweep (progress cue) */
.submit-button.loading::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  transform: translateX(-100%);
  animation: shimmer 1.4s ease-in-out infinite;
}

@keyframes shimmer {
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}

/* Secondary: subtle scale pulse (system is alive) */
.submit-button.loading {
  animation: alivePulse 1.8s ease-in-out infinite;
}

@keyframes alivePulse {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.005); } /* barely perceptible — secondary */
}
```

**Result reveal: primary = number appears, secondary = background glow:**
```css
.result-card {
  position: relative;
}

/* Primary: number animation — handled elsewhere */

/* Secondary: soft glow behind the result (card "activates") */
.result-card::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, var(--accent-color, #00d4aa) 0%, transparent 70%);
  opacity: 0;
  border-radius: inherit;
  transition: opacity 400ms ease-out 200ms; /* arrives AFTER the number = secondary */
  pointer-events: none;
}

.result-card.revealed::before {
  opacity: 0.08; /* very subtle — secondary must not compete */
}
```

**Check/success: primary = checkmark draws, secondary = ripple:**
```css
.success-icon {
  position: relative;
}

.success-icon::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid var(--success-color);
  opacity: 0;
  transform: scale(0.8);
  animation: rippleOut 600ms ease-out 300ms forwards; /* 300ms delay = after checkmark */
}

@keyframes rippleOut {
  from { opacity: 0.8; transform: scale(0.8); }
  to   { opacity: 0; transform: scale(1.8); }
}
```

### Calibration Rules [VERIFIED — IxDF, Ripplix]

- Secondary action opacity: maximum 15% of primary action's visual weight
- Secondary timing: starts 100-300ms AFTER primary (never simultaneously)
- Secondary duration: can be longer than primary — it fades while user reads the result
- If secondary animation catches your eye in user testing, it's too strong
- One secondary action per primary action. Never two simultaneous secondaries.

---

## 9. Timing

### The Principle

The number of frames (and in web, the milliseconds) an action takes determines its weight, urgency, and emotional character. More time = heavier, slower, more weight. Less time = lighter, faster, more energy. Spacing of keyframes within a fixed duration determines whether motion is mechanical or natural.

**Why it matters for UI:** Timing is the most precise tool in the animation craft because it communicates invisible properties — mass, urgency, confidence, caution — that cannot be shown directly. A result appearing in 200ms feels instant and confident. The same result appearing in 800ms with no other change feels slow and uncertain. Users interpret timing as a signal about system quality.

### Timing as Emotional Communication [VERIFIED — Pluralsight, Whizzy Studios]

| Characteristic | Fast Timing (<200ms) | Medium Timing (250-400ms) | Slow Timing (>500ms) |
|---------------|---------------------|---------------------------|----------------------|
| Perceived weight | Light, weightless | Normal, physical | Heavy, substantial |
| Perceived confidence | Instant, snappy | Deliberate, considered | Sluggish, uncertain |
| Emotional register | Playful, responsive | Professional, balanced | Meditative, heavy |
| Risk | Feels glitchy if too fast | Safe zone | Feels broken if not justified |

### Keyframe Spacing for Weight

Keyframe spacing within a fixed duration is as important as the duration itself:

```css
/* LIGHT object: most movement happens early (eases out quickly) */
@keyframes lightFall {
  0%   { transform: translateY(0); }
  20%  { transform: translateY(60%); }  /* covers most distance early */
  60%  { transform: translateY(92%); }
  100% { transform: translateY(100%); }
}

/* HEAVY object: slow start, weight builds momentum */
@keyframes heavyFall {
  0%   { transform: translateY(0); }
  40%  { transform: translateY(15%); }  /* slow start = building momentum */
  70%  { transform: translateY(60%); }
  100% { transform: translateY(100%); }
}

/* SNAPPY interaction: instant response, controlled settle */
@keyframes snapResponse {
  0%   { transform: scale(1); }
  15%  { transform: scale(0.93); }  /* most change happens in first 15% of time */
  100% { transform: scale(1); }
}
```

**Result counter: timing as weight signal:**
```js
// Fast count (light, energetic) — good for low-stakes numbers
function countUpFast(el, from, to) {
  const duration = 600; // ms
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    // ease-out: t starts fast, slows at end
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(from + (to - from) * eased);
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// Slow deliberate count (heavy, precise) — for medical results, significant numbers
function countUpDeliberate(el, from, to) {
  const duration = 1800; // ms — slow = weighty
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    // ease-in-out: slow start AND slow end = deliberate, considered
    const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    el.textContent = Math.round(from + (to - from) * eased);
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

### The Pause [ASSUMED based on principle — not explicitly documented in web UI literature]

In traditional animation, a held pose (pause between actions) is as expressive as the motion itself. The pause says: "look at this." In UI, pauses are underused.

```css
/* Pause built into keyframe: holds at key moment */
@keyframes revealWithPause {
  0%   { opacity: 0; transform: translateY(20px); }
  40%  { opacity: 1; transform: translateY(0); }
  /* 40% to 65%: HOLD — user reads the result */
  65%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
/* The pause from 40%-65% is doing work: it's saying "this is important, read it" */
```

---

## 10. Exaggeration

### The Principle

Exaggeration is not distortion — it is amplifying the essence of an action to make it read clearly. A character who is extremely happy doesn't just smile; their cheeks inflate, their eyes squeeze shut, their arms fly up. The exaggerated version communicates the emotion faster and more clearly than the realistic version. Exaggeration serves clarity, not spectacle.

**Why it matters for UI:** In UI animation, exaggeration is most important for success/error states. A form submission success needs to communicate "it worked, you did it" with enough force that the user feels it. A subtle checkmark that fades in communicates the same information as a burst of confetti, but only the latter produces dopamine. Exaggeration is the mechanism of delight.

**The calibration problem:** Too little exaggeration = soulless. Too much = cartoonish and untrustworthy. The correct amount depends on context (medical vs. fitness vs. celebration).

### Context-Appropriate Exaggeration Scale [ASSUMED]

| Context | Max scale overshoot | Animation character | Example |
|---------|--------------------|--------------------|---------|
| Medical/clinical | 2-3% | Barely perceptible | Lipid panel result appears |
| Wellness/health | 4-8% | Subtle spring | TDEE result bounces in |
| Fitness/performance | 8-14% | Confident spring | PR weight calculation pops |
| Celebration/milestone | 15-30% | Playful bounce | First goal achieved |

### CSS Implementation

**Subtle overshoot (wellness context):**
```css
.result-value {
  animation: subtleReveal 350ms cubic-bezier(0.34, 1.3, 0.64, 1) forwards;
  /* 1.3 = small overshoot = subtle spring */
}

@keyframes subtleReveal {
  from { opacity: 0; transform: scale(0.9); }
  to   { opacity: 1; transform: scale(1); }
}
```

**Strong overshoot (fitness/celebration context):**
```css
.milestone-number {
  animation: strongReveal 500ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  /* 1.56 = strong overshoot = bouncy spring */
}

@keyframes strongReveal {
  0%   { opacity: 0; transform: scale(0.7); }
  70%  { transform: scale(1.12); } /* explicit overshoot keyframe */
  85%  { transform: scale(0.97); } /* pull-back */
  100% { opacity: 1; transform: scale(1); }
}
```

**Exaggerated error state (shake = exaggerated "no"):**
```css
@keyframes errorShake {
  0%        { transform: translateX(0); }
  10%, 90%  { transform: translateX(-8px); }
  20%, 80%  { transform: translateX(8px); }
  30%, 50%, 70% { transform: translateX(-6px); }
  40%, 60%  { transform: translateX(6px); }
  100%      { transform: translateX(0); }
}

.input.error {
  animation: errorShake 600ms cubic-bezier(0.36, 0.07, 0.19, 0.97) forwards;
}
/* Shake = exaggerated physical "no" — universally understood without language */
```

**CSS spring via linear() for exaggeration** [VERIFIED — Josh W. Comeau]:
```css
/* Overshoot and bounce — the linear() function allows values > 1 */
.bounce-element {
  transition: transform 500ms linear(
    0, 0.6 10%, 1.1 40%, 0.95 60%, 1.02 75%, 1
  );
}
/* Values > 1 (like 1.1) overshoot the target, then settle back */
```

---

## 11. Solid Drawing

### The Principle

In 2D animation, solid drawing means understanding the character as a 3D form existing in 3D space — even though it is drawn on paper. A character's proportions, weight, and volume must remain consistent as it moves through 3D space. The drawing must obey perspective, gravity, and volume conservation.

**Web translation:** The principle becomes "visual consistency and dimensional integrity during animation." UI elements must not lose their visual weight, proportion, or apparent depth as they animate. An element that feels like a card with physical presence should animate in ways that reinforce that 3D-ness — not flatten it or contradict it.

### What it looks like MISSING

A card component that scales uniformly during reveal — it flattens and looks 2D. A modal that fades in without any sense of depth — it materializes rather than arriving. An element whose shadow doesn't change as it moves — the light source is inconsistent, breaking the illusion of 3D space.

### What it looks like PRESENT

A card that appears to lift from the surface (shadow grows, element scales up slightly = perspective-correct arrival from below). A modal that descends from above (slight scale decrease as it approaches, shadow grows). Elements that maintain consistent visual weight whether static or in motion.

### CSS Implementation

**Depth-consistent card lift:**
```css
.card {
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  transform: translateY(0) scale(1);
  transition:
    transform 250ms cubic-bezier(0.34, 1.56, 0.64, 1),
    /* Use filter:drop-shadow for animated shadows — more performant */
    filter 250ms ease-out;
}

.card:hover {
  /* Lifting UP = element moves away from surface in Z-space */
  /* Shadow grows (light source consistent), scale grows (closer to viewer) */
  transform: translateY(-6px) scale(1.01);
  filter: drop-shadow(0 12px 28px rgba(0,0,0,0.18));
  /* Volume preserved: slight scale increase compensates for Z-axis rise */
}
```

**Modal arriving with depth (descends from above):**
```css
@keyframes modalArrive {
  0%   {
    opacity: 0;
    transform: scale(0.96) translateY(-16px);
    /* Smaller scale = perspective of distant object */
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
    /* Full scale = arrived at viewer's depth */
    filter: drop-shadow(0 24px 48px rgba(0,0,0,0.25));
  }
}

.modal {
  animation: modalArrive 350ms cubic-bezier(0, 0, 0.3, 1) forwards;
}
```

**Perspective on interactive cards (3D tilt):**
```js
// 3D tilt that responds to cursor — reinforces card as 3D object
function add3DTilt(card) {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) / (rect.width / 2);
    const dy = (e.clientY - cy) / (rect.height / 2);

    // Max tilt: 8 degrees — subtle enough to feel dimensional, not dramatic
    card.style.transform = `perspective(800px) rotateX(${-dy * 8}deg) rotateY(${dx * 8}deg)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(800px) rotateX(0) rotateY(0)';
    card.style.transition = 'transform 400ms cubic-bezier(0.34, 1.56, 0.64, 1)';
  });
}
```

### Visual Consistency Checklist During Animation [ASSUMED]

1. Shadow must change when Z-position changes (lift up = shadow grows and blurs)
2. Scale must change predictably with Z-movement (closer = larger)
3. Saturation can decrease very slightly for receding elements (atmospheric perspective)
4. Proportions must not deform unless Squash & Stretch is the intentional technique
5. Light source must remain consistent across all element states

---

## 12. Appeal

### The Principle

The least technical of the 12. An animated character or scene should be appealing — not necessarily likeable, but watchable. Even a villain must have appeal. Appeal comes from clarity of design, readable silhouette, charisma, and the feeling that the animation has been crafted with intention.

**Appeal breaks into two forces** [VERIFIED — Animation Mentor, drawntoanimation.com]:
1. **Order:** The pattern or logic applied to motion — the rule
2. **Interest:** The variation, surprise, and personality within that rule

An animation with only Order is mechanical. An animation with only Interest is chaos. Appeal is the tension between them.

**Why it matters for UI:** A UI that animates technically correctly but has no appeal feels like documentation. Appeal is what makes a user show someone else the tool. It is the accumulated effect of every other principle applied with craft — but it also requires something additional: personality. The tool must feel like it has a point of view.

### What it looks like MISSING

Every transition is a 300ms ease-out fade. Technically correct. No identity. No personality. The animation serves as state communication but never as brand communication. The user gets information but no delight.

### What it looks like PRESENT

The same state transition, but the primary color element arrives with a spring (personality), the number counts up with a custom easing that feels precise and deliberate (point of view), and a very faint secondary glow pulses briefly (the tool is alive). The functional output is identical. The experience is different.

### The Appeal Framework for UI [ASSUMED — derived from animation principles]

**Clarity (Order dimension):**
```css
/* Every animation has ONE point of emphasis per scene */
/* Readable at a glance — the hierarchy is obvious */
/* No animation fights another animation for attention */

/* Silhouette test: if you made every element a solid color,
   would the animation still communicate its intent?
   If yes: good clarity. If no: visual noise. */
```

**Personality (Interest dimension):**
```css
/* The spring overshoot: "I arrive with confidence" */
.result-reveal {
  animation: confident 400ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

/* The pause before reveal: "This matters, wait for it" */
@keyframes withPause {
  0%   { opacity: 0; transform: scale(0.9); }
  30%  { opacity: 0; transform: scale(0.92); } /* wait */
  60%  { opacity: 1; transform: scale(1.04); } /* arrive */
  80%  { transform: scale(0.99); }
  100% { transform: scale(1); }
}

/* The breathing idle: "The system is alive" */
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.003); } /* barely visible — personality, not distraction */
}

.pulse-dot {
  animation: breathe 3s ease-in-out infinite;
}
```

**Watchability — the test:**
Does the animation make a user want to trigger it again just to see it?
- If yes: appeal is working
- If no: technically functional, no appeal

**Appeal by context:**
```css
/* Clinical context: appeal = precision and restraint */
/* The appeal IS the accuracy, the deliberate timing */
.medical-result {
  animation: preciseReveal 400ms cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}

/* Fitness context: appeal = energy and snap */
.fitness-result {
  animation: snapReveal 300ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

/* Celebration: appeal = joy and permission to be exaggerated */
.milestone-reveal {
  animation: joyReveal 600ms cubic-bezier(0.34, 1.8, 0.64, 1) forwards;
}
```

**The coherence requirement:**
Appeal requires that all 12 principles cohere around a single emotional register. A calculator that uses gentle ease-outs everywhere except a cartoonish 2x scale celebration breaks appeal — the tone is inconsistent. Every animation decision must ask: "does this match the emotional register of the other animations on this page?"

---

## Cross-Principle Reference: Which Principles Apply Where

| UI Pattern | Key Principles | Notes |
|------------|---------------|-------|
| Button press | Squash & Stretch, Anticipation, Timing | Most compressed application of principles |
| Result reveal | Staging, Follow-Through, Timing, Secondary Action | Sequence is everything |
| List/card load | Overlapping Action, Follow-Through, Staging | Stagger = the whole game |
| Modal open/close | Staging, Arcs, Solid Drawing, Timing | Enter: ease-out. Exit: ease-in. |
| Error state | Exaggeration, Timing, Appeal | Shake = exaggerated "no" |
| Success/celebration | Exaggeration, Secondary Action, Appeal | Permission to exceed normal calibration |
| Hover state | Anticipation, Slow In/Out, Timing | 100-200ms max |
| Number counter | Timing, Exaggeration (subtle), Appeal | Easing = emotional weight of number |
| Loading state | Secondary Action, Timing, Solid Drawing | System feels alive, not frozen |
| Page transition | Staging, Arcs, Overlapping Action | Route the user's eye, don't teleport them |

---

## Falsifiability

1. **Timing ranges** — NN/G reports 200-500ms as optimal. If user testing shows completion of longer animations is preferred, the duration map needs revision.
2. **Easing emotional map** — "ease-out = confident arrival" is inferred from animation principles, not measured in UI testing. Could be cultural. [ASSUMED tag on emotional associations]
3. **Squash and stretch calibration** — the 2-4% subtle / 6-10% playful split is derived from visual review of examples, not quantified user studies. Actual threshold for "cartoonish" is user-dependent.
4. **Secondary action timing** — "arrives 100-300ms after primary" is derived from principle, not benchmarked. Could be tighter or looser depending on element complexity.
5. **Appeal is the hardest to falsify** — it is inherently subjective. The order/interest framework gives structure, but "watchable" remains a human judgment.

## What We Are Not Sure About

1. Whether these calibrations hold across cultures — some research suggests different cultures have different speed preferences for UI animation.
2. Whether the easing emotional map generalizes — "gentle ease-out = calm/medical" is inferred, not empirically tested.
3. Whether reduced-motion users lose meaningful communication when all animations are removed — some state changes rely entirely on animation as the communicator.
4. The exact threshold between "appropriate exaggeration" and "cartoonish" in medical contexts — this likely requires user testing specific to the audience.

---

## Sources

- [Animation Principles for the Web — CSS Animation](https://cssanimation.rocks/principles/)
- [Disney's 12 Principles Exemplified in UX — UX Collective](https://uxdesign.cc/disneys-12-principles-of-animation-exemplified-in-ux-design-5cc7e3dc3f75)
- [Applying Disney's Principles to UI Design — Dribbble](https://dribbble.com/stories/2020/07/27/disney-principles-of-animation-ui-interactions)
- [Disney's 12 Principles in Everyday UI — Medium/Bootcamp](https://medium.com/design-bootcamp/disneys-12-principles-of-animation-in-everyday-ui-design-71c6592064fe)
- [UI Animation — How to Apply Disney's 12 Principles — IxDF](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)
- [Understanding Easing and Cubic-Bezier Curves — Josh Collinsworth](https://joshcollinsworth.com/blog/easing-curves)
- [Springs and Bounces in Native CSS — Josh W. Comeau](https://www.joshwcomeau.com/animation/linear-timing-function/)
- [Moving Along a Curved Path in CSS — Tobias Ahlin](https://tobiasahlin.com/blog/curved-path-animations-in-css/)
- [CSS Motion Path — MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_motion_path)
- [Executing UX Animations: Duration and Motion — NN/G](https://www.nngroup.com/articles/animation-duration/)
- [The Role of Animation and Motion in UX — NN/G](https://www.nngroup.com/articles/animation-purpose-ux/)
- [Follow Through and Overlapping Action — garagefarm.net](https://garagefarm.net/blog/follow-through-and-overlapping-action-in-animation)
- [Easing Functions Cheat Sheet — easings.net](https://easings.net/)
- [Repeatable Staggered Animation — CSS-Tricks](https://css-tricks.com/repeatable-staggered-animation-three-ways-sass-gsap-web-animations-api/)
- [Animate Along a Path in CSS — Smashing Magazine](https://www.smashingmagazine.com/2023/10/animate-along-path-css/)
- [Appeal: The 12 Basic Principles — Animation Mentor](https://www.animationmentor.com/blog/appeal-the-12-basic-principles-of-animation/)
- [Staging in Animation — BuzzFlick](https://buzzflick.com/staging-in-animation/)
- [Solid Drawing Animation — Pixune](https://pixune.com/blog/solid-drawing/)
- [Getting Deep Into Shadows — CSS-Tricks](https://css-tricks.com/getting-deep-into-shadows/)
- [Smashing Guide to CSS Animation](https://www.smashingmagazine.com/2011/09/the-guide-to-css-animation-principles-and-examples/)
- [Dynamic CSS Animations with Linear Easing — LogRocket](https://blog.logrocket.com/dynamic-css-animations-linear-easing-function/)
- [Overlapping Action with CSS Animation — thenewcode.com](https://thenewcode.com/1058/Overlapping-Action-with-CSS-Animation)
