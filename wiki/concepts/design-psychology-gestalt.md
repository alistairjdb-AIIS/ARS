# Design Psychology and Gestalt Principles

> Gestalt perceptual grouping, Von Restorff isolation effect, cognitive load theory, Disney animation principles, dopamine mechanics, visual rhythm, negative space, Don Norman's three-level emotional design framework, and the uncanny valley of web design — compiled for web animation and interactive content decisions.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### Gestalt Psychology: The 7 Principles

Gestalt psychology (1920s German school) established that humans perceive patterns as wholes, not collections of parts. The brain actively resolves ambiguity into the simplest stable interpretation. This is involuntary — users cannot avoid perceiving Gestalt patterns. [VERIFIED]

**1. Proximity:** Elements close together are grouped as related. Form labels must be closer to their input than to adjacent labels. Card internal padding must be smaller than external gap. Section headings must be closer to content below than content above. In animation: elements that should be perceived as a unit must move together. Stagger interval for grouped items: 40-60ms per item. [VERIFIED]

**2. Similarity:** Elements sharing visual properties (color, shape, size) are grouped as related. All interactive elements should share a visual property that non-interactive elements lack. Color-coding creates automatic grouping. In animation: elements with the same easing curve and duration are perceived as the same type. Animation signature functions as a similarity signal. [VERIFIED]

**3. Closure:** The brain completes incomplete shapes. Partially visible elements (cards cut off at scroll edge) signal "there is more." Progress indicators work because the brain is driven to complete the gap. In animation: a card that animates 80% into frame then finishes quickly creates sensation of arrival vs. full mechanical travel. [VERIFIED]

**4. Continuity:** The eye follows lines and curves through interruptions. Aligned grids create reading flow; broken alignment stops the eye. Scroll-triggered animations should follow the scroll axis — perpendicular animations feel jarring. Section transitions that continue a visual line maintain flow. [VERIFIED]

**5. Figure/Ground:** The brain separates scenes into primary subject (figure) and background (ground). Modal overlays exploit this by dimming background. Hero sections with high-contrast subject against blurred background. In animation: dimming background when a panel opens = instant figure/ground (200-300ms). [VERIFIED]

**6. Common Fate:** Elements that move together are perceived as belonging together. This is the most powerful Gestalt principle for web animation. Staggered entrance of related items: they share direction and easing, only offset in timing. They move together despite not starting simultaneously. [VERIFIED — MDPI 2024 perceptual hierarchy study]

**7. Symmetry:** Symmetrical compositions = stable, complete, ordered. Asymmetry = tension, energy. Deliberate asymmetry reads as "designed." Accidental asymmetry reads as "broken." In animation: symmetrical entrance/exit feels mechanical; asymmetrical (longer entrance, shorter exit) feels intentional. [VERIFIED]

### Color Psychology: What the Research Actually Says

Most "color psychology" content is generic and poorly supported. The actual peer-reviewed findings: [VERIFIED]

**Saturation is the strongest predictor of arousal.** A 2017 study (Soares et al., Psychological Research, Springer) found brightness and saturation significantly influence emotional ratings, with higher saturation linked to higher arousal and more positive valence. [VERIFIED]

**A 2025 systematic review (132 studies, 42,266 participants) confirmed:** Saturated colors = high arousal, power, positive emotions. Desaturated = low arousal, low power, neutral/negative. Warm hues increase arousal more than cool. Lightness and saturation are the dominant variables; hue has a secondary effect. [VERIFIED — PMC systematic review, Psychonomic Bulletin & Review]

**Cultural variation is real:** Monotype neuroscience research (2022) found different font/color combinations evoke different emotional responses depending on country. "Blue = trust" may not hold globally. [VERIFIED]

**Color temperature and reading:** Cool light/color environments produce higher calm and better sustained attention. Warm environments produce higher arousal and agitation. Implication: cool backgrounds reduce arousal and allow sustained reading; warm accents pull attention to key moments. [VERIFIED — MDPI 2025 classroom study, PMC 2021]

**The 90-second rule:** 62-90% of product perception is based on color within 90 seconds of first exposure. [THEORETICAL — widely cited, original study not independently verified]

### Animation Psychology: Attention Mechanism

Human peripheral vision evolved to detect motion as a survival signal. Any animation in peripheral vision hijacks attention involuntarily. This makes animation the most powerful and most dangerous tool in web design. [VERIFIED — Pratt et al. 2010, cited by NN/G]

**Animation helps when:** Confirming user actions, communicating state transitions, combating change blindness (state changes without animation may go unnoticed), teaching gesture directions. [VERIFIED — NN/G]

**Animation hurts when:** Not tied to user action (ambient, decorative, looping), multiple simultaneous animations (competing for the same involuntary attention), over 500ms on small UI elements (feels sluggish), in peripheral vision while user is reading. [VERIFIED — NN/G]

### Disney's 12 Principles (5 Most Applicable to Web)

**Squash and Stretch:** Button compresses 2-3% on click, springs back. `transform: scale(0.97)` on mousedown, `scale(1)` on release. Duration: 80-100ms compress, 150ms release. [VERIFIED]

**Anticipation:** Small motion in opposite direction before main motion. Dropdown shifts 2px up before expanding down. Most web anticipation is via easing curves (ease-in before ease-out). Duration: 50-100ms. [VERIFIED]

**Timing and Spacing:** Maps directly to animation duration and easing. Fast + ease-out = decisive arrival. Slow + ease-in-out = deliberate, considered. [VERIFIED]

**Staging:** Most important element has most visual focus. When a result appears, animate it first (or exclusively). The rest holds still. The most important element enters last (the reveal). [VERIFIED]

**Follow-Through and Overlapping Action:** Elements don't stop simultaneously. Card arrives, then text inside fades in 80ms later. Stagger: 60-100ms between primary and secondary. [VERIFIED]

### Animation Timing Reference

| Interaction | Duration | Basis |
|------------|---------|-------|
| Toggle / checkbox | 100ms | NN/G |
| Button press feedback | 80-120ms | NN/G + industry |
| Modal / panel enter | 200-300ms | NN/G |
| Modal / panel exit | 150-250ms | NN/G: exits 20-30% faster than entrances |
| Page-level transition | 300-400ms | NN/G |
| Loader / ambient | 400-500ms per cycle | NN/G: 500ms sluggishness threshold |
| DO NOT EXCEED | 500ms for UI elements | NN/G |

[VERIFIED — NN/G "Executing UX Animations: Duration and Motion Characteristics"]

**Device scaling:** Mobile: baseline (250ms modal). Tablet: +30% (325ms). Smartwatch: -30-50% (125-175ms). [VERIFIED — Material Design]

### The Easing Curve as Emotional Signal

The easing curve communicates physics and therefore meaning. [VERIFIED — Josh Collinsworth]

| Curve | CSS | Signal |
|-------|-----|--------|
| Linear | `linear` | Mechanical, robotic. Avoid for UI. |
| Ease-out | `cubic-bezier(0,0,0.2,1)` | Decisive arrival. Confident. |
| Ease-in | `cubic-bezier(0.4,0,1,1)` | Gathering momentum. Used for exits. |
| Ease-in-out | `cubic-bezier(0.4,0,0.2,1)` | Measured, thoughtful. Screen transitions. |
| Spring/bounce | `cubic-bezier(0,1.2,1,0.2)` | Tactile, alive, playful. Use sparingly. |

**The rule:** UI elements arriving = ease-out (decelerate to rest, feel mass). UI elements leaving = ease-in (accelerate away, dismissed). [VERIFIED]

**The adverb principle:** "The transition is the verb; the easing curve is the adverb." A modal with ease-in-out says "carefully." With ease-out, "decisively." [VERIFIED — Collinsworth]

### Negative Space and Cognitive Load

Negative space reduces cognitive load, allowing the brain to process content more efficiently. This is measurable in processing speed and comprehension, not just aesthetic preference. [VERIFIED]

**Whitespace correlates with perceived premium quality and trust.** Generous white space correlates with sophistication, trust, and premium quality in consumer perception. [VERIFIED]

**The visual resting point:** High-density sections increase arousal. Following with a high-whitespace section lowers arousal, resets attention, makes the next dense section feel fresh. [THEORETICAL]

**Premium signal:** For content needing authority or trust (medical results, health data), increase whitespace by 30-50% beyond comfortable reading minimum. The extra space signals "this is not rushed." [THEORETICAL]

**Apple's use:** Consistent 80-100px vertical whitespace between sections. Scarcity of visual elements = perceived value of each element. [VERIFIED]

### Dopamine and Interface Design

Dopamine is released in response to reward prediction, not reward receipt. Variable reward schedules produce stronger dopamine responses than fixed schedules. [VERIFIED — behavioral neuroscience, Skinner]

**Key triggers for calculators:**
- **Progress bar filling:** Closure + reward anticipation. As bar approaches 100%, dopamine rises. [VERIFIED]
- **Confirmation checkmark:** Must appear within 100ms to feel like direct feedback. At 200ms it disconnects. [VERIFIED — NN/G]
- **Result reveal animation:** The moment between submit and result is pure anticipation. 400-600ms apparent calculation time, even if instant, creates anticipation. Ethical when delay is fixed/consistent; manipulative if variable. [VERIFIED]
- **Micro-interaction feedback:** Button scales to 0.95 on press (100ms), releases to 1.0 (150ms). Physical "press" and "release" sensation. [VERIFIED]

Completion indicators (progress bars, percentages, checkmarks) can increase conversions by 20-40%. [THEORETICAL — widely cited, original studies not independently verified]

### Don Norman's Three Levels of Emotional Design

**Visceral (instinctive, before interaction):** Immediate unconscious reaction to appearance. Happens in milliseconds. Cannot be overridden by reasoning. The above-the-fold experience is entirely visceral. The first animation sets the tone for the entire experience — if laggy or mechanical, the site feels cheap permanently. [VERIFIED — Norman 2004, IxDF]

**Behavioral (usability, during interaction):** Experience of using the product. Task completion, response time, clarity of feedback. Calculator inputs must be effortless. Results must appear without scrolling. Error states must tell user what to do, not just what went wrong. [VERIFIED — Norman, IxDF]

**Reflective (self-image, after interaction):** User's conscious evaluation of what using the product says about them. Share card design, product framing, credibility signals. Must make user feel good about sharing. [VERIFIED — Norman, IxDF]

**The hierarchy:** Behavioral is the floor. A beautiful calculator with wrong answers will fail. Visceral and reflective determine the ceiling. Behavioral excellence alone is insufficient. [VERIFIED]

### The Uncanny Valley of Web Design

When a site is close enough to premium to trigger premium expectations but has micro-violations, users feel distrust they cannot articulate. [VERIFIED]

**Triggers:** Spacing inconsistency (12px and 16px where they should match), easing mismatch (some ease-out, some linear), color near-miss (#2B7FFF and #3080FF — worse than one color or two distinct colors), typography hierarchy gaps (sizes that don't follow a clear scale), content/quality mismatch (excellent visuals with mediocre copy). [VERIFIED]

**Premium signals:** Generous consistent whitespace, one serif + one sans-serif max, animations under 300ms with ease-out, 1 dominant + 1 accent + 1 neutral color, text that breathes (line-height 1.5+, line-length <75 chars), directionally consistent shadows. [VERIFIED]

**The intentionality test:** The most reliable signal of premium vs. cheap is whether every visual decision feels intentional. Intentional asymmetry = designed. Accidental asymmetry = broken. [VERIFIED]

### Visual Rhythm: Music Theory Applied to Design

**Tension and release pattern:** Build (increasing complexity, density, motion) to Peak (maximum visual energy) to Release (space, calm, resolution). Maps to: scroll acceleration, dense information moment, whitespace breathing section. [VERIFIED]

**The "pause creates power" principle:** A scroll-triggered animation that delays 200ms before starting creates more anticipation than one that starts immediately. The empty moment is a rest beat. [VERIFIED — KOTA design research]

**Stagger as beat:** List items at 60ms intervals create visual rhythm. Too fast (<40ms) = all at once. Too slow (>100ms) = tedious. [VERIFIED]

**Pacing and authority:** Snappy micro-interactions signal energy. Lingering transitions communicate composure. Fast pace = accessible, energetic. Slow pace = premium, authoritative. [VERIFIED — KOTA]

### Dark Mode Design Psychology

**Premium dark mode signals (cross-app convergence from WHOOP, Oura, Apple, Strava):** [VERIFIED]

1. Near-black, not gray. `#000000` or `#0B0B0B` reads as "designed this way." `#3A3A3A` reads as "dark mode added."
2. One or two accent colors maximum per screen.
3. Color encodes category or state, not binary good/bad judgment.
4. Typography carries hierarchy (size/weight), not color.
5. Generous spacing — dark amplifies density.
6. Glow on the one thing that matters per screen. Everything else dimmer.
7. Dark as identity, not option. When dark is a toggle, it is a feature. When dark is the product, it is a brand.

---

## Operational Rules

1. **When grouping related elements, apply Proximity + Common Fate together.** Elements must be spatially close AND move with the same timing/direction. If they animate independently, they break the perceptual group regardless of proximity. [VERIFIED]

2. **When any UI element animates, never exceed 500ms duration.** At 500ms, NN/G research shows elements "start to feel like a real drag." Modal enter: 200-300ms. Modal exit: 150-250ms (20-30% faster). Button feedback: 80-120ms. [VERIFIED]

3. **When choosing easing curves, match to meaning: ease-out for arrivals, ease-in for exits, never linear for UI.** Linear reads as mechanical and cheap. The easing curve IS the emotional signal. [VERIFIED]

4. **When a result reveal needs anticipation, use 400-600ms apparent calculation time even if computation is instant.** This exploits dopamine reward prediction. Must be fixed and consistent — variable delays are manipulative. [VERIFIED]

5. **When designing for premium perception, apply the uncanny valley check: verify spacing consistency, easing consistency, color precision, and typography scale.** Near-misses are worse than clearly different values. [VERIFIED]

6. **When creating dark UI, never encode health signal valence (good/bad) in color.** Use copy and typography. Binary green/red is clinical pattern. Premium apps use color for identity or biometric state, not judgment. [VERIFIED]

7. **When building page rhythm, alternate dense content sections with whitespace sections.** Dense = information. Sparse = meaning. Add 80-100px of whitespace after result panels to let information "land." [THEORETICAL]

8. **When designing any element, run Norman's three-level check.** Visceral: does it look correct in 200ms? Behavioral: can the user accomplish their goal? Reflective: would they share it? Behavioral is the floor; do not sacrifice it for visceral appeal. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/design_psychology_research.md` | Gestalt principles (7), color psychology (systematic review), animation psychology (NN/G), Disney principles, animation timing, easing curves, negative space, dopamine mechanics, Norman's emotional design, uncanny valley, visual rhythm, typography psychology, composition |
| `research-data/dark_mode_health_ui_research.md` | Premium dark mode patterns (WHOOP, Oura, Apple, Strava), accent color strategies, positive/negative signal handling, typography on dark, glow/shadow/depth, breathing room, accessibility requirements |

---

## Related Concepts

- [[camera-language]] — Common Fate maps directly to tracking shots; elements that move together are perceived as belonging together
- [[lighting-design]] — Figure/ground separation depends on lighting; low-key UI is a figure/ground strategy
- [[color-narrative]] — Saturation as arousal links directly to the color psychology systematic review findings here
- [[typography-comprehension]] — Typography hierarchy creates the progressive disclosure architecture; Norman's behavioral level requires readable type
- [[visual-storytelling-mise-en-scene]] — Staging (Disney) and composition (art) are mise-en-scene elements; the five-layer check maps to directing principles

---

## Open Questions

- Most UX animation research is on consumer apps and e-commerce, not health calculators. Task-focused users may respond differently to dopamine patterns and pacing than browsing/leisure users.
- High arousal (from warm colors, fast pacing, dense animations) may conflict with the calm, focused state needed for health decision-making. The tension between arousal and readability is unresolved.
- The 40% trustworthiness increase for serif fonts is widely cited but the original study is difficult to trace. If a controlled test shows <10% difference, the effect is overstated.
- The 20-40% conversion lift for progress bars and completion indicators is directionally supported but lacks precise effect-size data from independent verification.
- Whether the uncanny valley analogy from robotics actually applies to web design with measurable user impact, or is a useful metaphor without empirical backing.
