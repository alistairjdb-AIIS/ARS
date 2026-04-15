# Choreography and Stagger

> Orchestrating multiple animated elements into a single cohesive sequence: stagger origin patterns, the conductor model, grouped bursts, overlap timing, and the planning process that separates premium motion from noise.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### The Core Distinction

The difference between a screen that feels alive and a screen that feels noisy is almost always choreography, not individual animation quality. Choreography is the coordination of MULTIPLE animated elements into a single sequence -- not how one element moves, but how a group moves together. [VERIFIED -- animation_choreography.md, IBM Carbon, Material Design, Disney's 12 Principles]

### Five Stagger Origin Patterns

Beyond uniform delay, GSAP and Motion.dev document five named stagger origins. [VERIFIED -- GSAP documentation, Motion.dev stagger API]

| Pattern | `from` Value | Behavior | Use Case |
|---------|-------------|----------|----------|
| Left-to-right | `"start"` | First element first, last element last | Reading order reveals (text, lists) |
| Right-to-left | `"end"` | Last element first, works backward | Exits, undo feedback |
| Ripple from center | `"center"` | Middle element first, radiates outward | Drawing attention to focal point (result, key stat) |
| Ripple from edges | `"edges"` | Outer elements first, collapses inward | Closing/focusing, gathering effect |
| Random-within-range | `"random"` | Unpredictable order within timing constraints | Organic/alive feeling, particle-like reveals |

### Grid-Based Radial Stagger

When elements are in a 2D grid, stagger distance can be calculated from a center point across both axes simultaneously, creating a ripple that radiates from a specified origin cell. GSAP uses `getBoundingClientRect()` to auto-calculate with `grid: "auto"`. Set `axis: null` for true radial ripple across both X and Y. [VERIFIED -- GSAP grid stagger documentation]

### Grouped Burst Pattern

Instead of staggering individual elements, stagger GROUPS. [VERIFIED -- IBM Carbon Design System, UX Collective]

Structure:
- Group A (structural/background) -- animates first, all elements inside A are simultaneous
- Group B (content layer) -- starts 80-120ms after A completes
- Group C (actions/CTAs) -- starts after B

This avoids the "slideshow" problem where long individual staggers make the last card feel forgotten. Groups feel intentional; long individual staggers feel like slow loading. [VERIFIED]

**Rule: keep stagger groups to 3-7 items.** More than 7, the last item waits too long and the sequence loses coherence. [VERIFIED -- animation_choreography.md]

### The Conductor Model

Comes from Disney's Principle 6 (Follow Through and Overlapping Action): primary action leads, everything else follows at defined offsets. [VERIFIED -- Disney's 12 Principles, IBM Design Language]

In a UI element group:
- **Lead** (most important element): animates first, sets the rhythm
- **Body** (supporting elements): follows at 40-80ms offset
- **Tail** (decorative/contextual): follows at 80-150ms offset from body

Assign the conductor role to the element that answers: "What does the user need to orient to first?" This mirrors task hierarchy, not visual hierarchy. [THEORETICAL -- inferred from principles]

**Calculator result example:**
- Lead: the number/result (anchors everything)
- Body: interpretation text (what the number means)
- Tail: actions/CTAs (what to do next)
- Decorative: background elements, accent lines

### Overlapping vs Sequential Offsets

Each follower should start BEFORE the leader finishes. Not sequential (robotic) but overlapping (organic). [VERIFIED -- Disney Overlapping Action, UX Collective]

If element duration is 300ms and stagger is 80ms, elements are running simultaneously for 220ms -- that overlap creates fluid, connected motion. Without overlap, the sequence feels like a PowerPoint slideshow. [VERIFIED]

### Timing Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| Stagger delay between items | 30-80ms | Cohesive, connected -- one system breathing |
| Stagger delay between items | 80-200ms | Deliberate, counted reveals |
| Stagger delay between items | 200ms+ | Reads as loading, not animation |
| Stagger delay as % of duration | 30-70% of duration | Sweet spot for overlap feel |
| Element duration (entrances) | 200-400ms | Standard UI |
| Element duration (exits) | 150-250ms | Exit always faster than entrance |

[VERIFIED -- GSAP docs, Frontend Masters, Aninix, NNGroup, animation_choreography.md]

### Entrance Choreography: 10+ Elements

Never animate 10 elements as 10 individual staggers. Group them by function (structural, content, action, decoration), animate groups as units, stagger groups from each other. [VERIFIED -- IBM Carbon, Material Design, NNGroup]

**The "Backdrop First" Rule:** backdrop --> container --> content --> actions. Background sets the stage, container shapes appear, content populates, action elements arrive last (they require context before they are meaningful). Breaking this order feels disorienting. [VERIFIED -- Aninix, IBM Carbon]

**Direction Consistency:** Elements entering from the same direction create implied origin. Different directions simultaneously create visual noise. Content reveals enter from below. Contextual "behind" content enters from left/right (shared axis). Travel distances should be short: 10-30px max for UI elements. [VERIFIED -- Material Design Shared Axis pattern]

### Exit Choreography

Three strategies: reverse order (last in, first out -- for going backward), simultaneous fade (fast transitions), cascade outward (for replacement). [VERIFIED -- Aninix, UX Collective]

**Key rule:** exits should be faster than entrances. Standard ratio: entrance 300ms, exit 200ms. For groups: entrance stagger 50ms, exit stagger 25ms or eliminate entirely. [VERIFIED]

Staggering exits in the same direction as entrances feels like the screen is slowly draining -- creates incomplete feeling. Reverse the order or use simultaneous. [THEORETICAL]

### The FLIP Technique

FLIP = First, Last, Invert, Play. The canonical technique for animating elements that change position or size during state changes (grid to list, sort, filter, expand/collapse). Records current position, applies end-state DOM change, applies inverse transform, then removes it with transition. Only animates transform and opacity -- compositor thread at 60fps. [VERIFIED -- Paul Lewis/Aerotwist, CSS-Tricks, GSAP Flip plugin]

### The Planning Process

**Phase 1 -- Storyboard:** Identify keyframes (start state, trigger, end state).
**Phase 2 -- Timing Sheet:** Map each element group to a time axis with duration and easing.
**Phase 3 -- Implementation:** Build using timing sheet as source of truth.

A timing sheet catches what code doesn't: the 23rd element starting at 1,150ms, two unrelated elements accidentally conflicting, sequences with no clear conductor. [VERIFIED -- Milanote, Toon Boom, story-boards.ai]

### Cross-Domain Convergence

Five choreography principles appear independently in IBM Carbon, Material Design, Disney, GSAP, and UX research. This convergence makes them the closest to ground truth. [VERIFIED -- animation_choreography.md]

1. **Lead and follow** -- one element leads, others follow at offsets
2. **Entrance slower than exit** -- enter at full duration, exit at 60-70%
3. **Group before stagger** -- stagger groups above 4+ items, not individuals
4. **Direction encodes meaning** -- up=reveal, right=forward, left=back, down=dismiss
5. **Overlap creates connection** -- each element starts before previous finishes

---

## Operational Rules

1. **When animating 4+ elements simultaneously, group them by function before staggering** -- because individual staggers for many elements produce a "slideshow" or "loading" feeling instead of choreographed motion.

2. **When building any multi-element sequence, identify the conductor element first** -- because without a clear lead, all elements start at the same delay and there is no reading hierarchy.

3. **When setting stagger timing, use 30-80ms between items for cohesion, never exceed 200ms** -- because above 200ms the delay reads as page load, not animation, and the sequence loses coherence.

4. **When elements enter a screen, always use the backdrop-first rule (structure --> content --> actions)** -- because actions shown before content are meaningless, and the user reaches for CTAs before understanding what they do.

5. **When elements exit, use reverse order at 60-70% of entrance duration** -- because exits should be fast (user has already processed the content) and same-direction exit feels like draining.

6. **When planning complex sequences, write a timing sheet before code** -- because a timing sheet exposes conflicts (simultaneous elements, missing conductor, excessive total duration) that are invisible in implementation.

7. **When overlapping element animations, ensure each follower starts while the leader is still 40-60% through** -- because fully sequential motion feels robotic, and the overlap is what creates the illusion of connected, organic motion.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/animation_choreography.md` | Stagger patterns, conductor model, entrance/exit strategy, FLIP technique, GSAP timeline structure, planning process |
| `research-data/animation_12_principles.md` | Follow-through, overlapping action, staging hierarchy, secondary action timing |

---

## Related Concepts

- [[squash-stretch-weight]] — DEPENDS_ON: weight classes determine how individual elements within a choreographed sequence behave
- [[motion-curves-easing]] — DEPENDS_ON: the curves used for each element in the sequence
- [[transitions-state-change]] — INFORMS: transitions between screens use choreography principles for multi-element coordination
- [[progressive-disclosure-pacing]] — INFORMS: pacing builds on choreography's stagger and staging principles
- [[continuity-editing-scene-flow]] — INFORMS: continuity editing's match-on-action and overlap techniques provide the cross-cut coordination principles that choreographed stagger sequences implement within a single scene
- [[editorial-pacing-rhythm]] — DEPENDS_ON: Murch's Rule of Six and Eisenstein's montage methods provide the film-editing theory that choreography's timing, overlap, and grouped-burst patterns operationalize at the element level
- [[cross-domain-motion-graphics]] — EXTENDS: metachronal wave (zoology) and stagger orchestra are cross-domain refinements of choreography stagger applied to motion graphics overlays

---

## Deep Reference

- **When** a card grid reveal needs to radiate from a focal point and you need GSAP stagger syntax → **read** `research-data/animation_choreography.md` §1d (Grid-Based Radial Stagger) **for** the `grid: "auto"` option that uses `getBoundingClientRect()` to auto-detect layout, `axis: null` for true radial ripple, and the complete GSAP `stagger` object with `amount`, `from`, `grid`, `axis` parameters
- **When** deciding which element should animate first in a multi-element group → **read** `research-data/animation_choreography.md` §2 (The Conductor Model) **for** the rule that conductor assignment follows TASK hierarchy not visual hierarchy, lead/body/tail offset values (40-80ms body, 80-150ms tail), and the "breath" pattern where inhale = elements gather inward, exhale = expand to final positions
- **When** a sequence of 10+ staggered elements feels like slow loading rather than animation → **read** `research-data/animation_choreography.md` §1b (Grouped Burst Pattern) **for** how grouping elements by function (structural → content → actions) with 80-120ms inter-group delay eliminates the slideshow problem, and the 3-7 items per group ceiling
- **When** elements exit in the same direction they entered and it feels like the screen is draining → **read** `research-data/animation_choreography.md` §4 (Exit Choreography) **for** the three exit strategies (reverse order, simultaneous fade, cascade outward), the exit stagger halving rule (entrance 50ms → exit 25ms), and when to eliminate exit stagger entirely

---

## Open Questions

- "Lead and follow" improving perceived quality has not been directly A/B tested (only NNGroup on duration indirectly touches this)
- "Group before stagger" could be wrong if users perceive individual-element staggers for 8+ items as more dynamic -- no direct user test cited
- "Direction encodes meaning" is a Material Design convention that reverses in right-to-left locales
- The breath pattern applied to UI elements is THEORETICAL, derived from character animation principles without direct UI testing
