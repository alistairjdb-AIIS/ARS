# Narrative Coherence

> The primary judgment axis for photoreal AI video: does the scene tell ONE consistent physical story where all elements agree on conditions -- time, weather, temperature, season, cause and effect?

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 2 memory files

---

## Core Findings

### The Principle

Narrative coherence means every element in the scene could coexist in a single real moment. If it just rained, there is no direct sun. If it is cold, breath or frost should be visible. If it is summer, there is no frost. The model has no narrative enforcer -- the prompt writer must enforce condition coexistence. [TESTED -- surfaced by operator on v10, confirmed across v2-v18]

This supersedes prompt-depth (terse vs crafted) as the primary judgment axis. Prompt-depth correlates with coherence but does not cause it. Crafted prompts sometimes enforce coexistence (v10-A); terse prompts sometimes produce coherent ambient atmosphere (v9-B "dirty glass + insects"). The driving variable is whether the output's elements tell one physical story. [TESTED -- reframe established after N=8 controlled A/B tests]

### Origin Evidence

The operator surfaced this principle on v10 (tulip macro, 2026-04-05):

> "If it just rained, by the way, if it just rained in this context, then A is way better. Because usually if it just rained in the morning, there's no sun. That means the sun is covered. So from a pure realistic standpoint, A is way better, because if you really think into depth, that means it just rained or was raining, that means sun is sort of unlikely."

The crafted A told a coherent story: cold + moist + no direct sun = just rained. The terse B had technical polish but mixed narrative signals: bright sun + heavy dew + summer light + cold-morning droplets -- physically inconsistent. [TESTED]

### The Model Has No Narrative Enforcer

AI video models compose scenes by sampling from learned distributions. They do not check whether rain + bright sun + frost coexist physically. Each element is generated somewhat independently. The prompt writer is the only narrative enforcer in the pipeline. [VERIFIED -- consistent finding across all photoreal A/B tests; confirmed by photoreal humans research noting models lack "logic, realism, and anything you want to match frame to frame"]

### Condition Coexistence Rules

When crafting prompts, specify conditions that FORCE coexistence. [VERIFIED -- derived from operator feedback + physical principles]

| If this condition | Then these must follow | And these must NOT appear |
|-------------------|----------------------|--------------------------|
| Just rained | Wet surfaces, overcast sky, diffused light | Direct sun, dry ground, harsh shadows |
| Cold morning | Frost or condensation, cool light, breath vapor | Warm golden light, summer foliage, insects |
| Golden hour | Long shadows, warm directional light, low sun angle | Overhead sun, cool blue light, midday shadows |
| Heavy fog | Reduced visibility, diffused light, muted colors | Sharp shadows, clear distant detail, high contrast |
| Indoor window light | Directional light from window, interior shadows | Multiple light sources from opposite directions |
| Night | Artificial or moonlight sources, limited color | Bright ambient light, vivid colors without source |

### Reinforcement Across Registers

Narrative coherence applies beyond photoreal environments. In stylized character work (v16, anime train scene), physically incoherent moments lost to coherent outputs even when the incoherent version was flashier. The principle transfers across registers. [TESTED -- v16]

### Relationship to "Too Perfect"

Narrative coherence and the too-perfect veto are the two primary judgment axes identified from controlled testing. They are independent: a scene can be narratively coherent but too-perfect (every droplet identical), or narratively incoherent but imperfect-looking (mixed signals but with natural variance). Both must pass for output to succeed. [TESTED -- see operator judgments across v2-v18]

### Photoreal Humans Amplify the Problem

For human subjects, narrative incoherence compounds with uncanny valley effects. A human face rendered with warm golden light from the left and cool blue light from the right without a physical justification triggers discomfort beyond what the same inconsistency would produce in a landscape. Human perception detects facial violations within 40-60 milliseconds, and narrative inconsistency in the lighting/environment around a face amplifies the detection. [VERIFIED -- photoreal humans research on perceptual mismatch]

---

## Operational Rules

1. **When crafting prompts:** Specify conditions that FORCE coexistence. If you write "just rained," also write "overcast sky, wet surfaces, diffused light" and do NOT include "golden sun" or "harsh shadows." Make the physical story explicit.

2. **When judging outputs:** Ask "could this moment exist in one real world?" If elements contradict (bright sun + heavy dew, golden hour + full fog), the output is technically composed but narratively broken. This is the primary axis, evaluated before any other quality dimension.

3. **When analyzing A/B results:** Evaluate narrative coherence as the primary axis. Prompt-depth becomes evidence/context, not the conclusion. An output that tells a coherent physical story with lower technical polish beats a technically polished output with mixed signals.

4. **When building multi-element scenes:** Establish the physical story first (time of day, weather, season, recent events), then derive all visual elements from that story. Do not mix-and-match visual elements from different conditions for aesthetic appeal.

5. **When prompting human subjects:** Narrative coherence is even more critical. Lighting inconsistency around faces triggers uncanny valley at 40-60ms detection speed. Ensure a single, physically justified light source setup.

6. **When reviewing for shipping:** If narrative incoherence is present, reject. Do not average it against other strengths. Coherence is a baseline, not a dimension to trade off.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/photoreal_humans_research.md` | Uncanny valley timing (40-60ms), perceptual mismatch as strongest trigger, lighting consistency requirements |
| `memory/feedback-narrative-coherence.md` | Primary axis definition, v10 operator evidence, condition coexistence principle |
| `memory/project-curriculum-elements.md` | Narrative coherence confirmed as primary axis after N=8 controlled tests; reinforced in v16 stylized work |

---

## Related Concepts

- [[too-perfect-veto]] -- The second independent judgment axis (operates alongside narrative coherence)
- [[character-design-prompting]] -- Acting chains help enforce narrative coherence by grounding characters in physical cause-and-effect
- [[prompting-craft-depth]] -- Prompt-depth was the original test variable; narrative coherence emerged as the true causal axis
- [[floor-bar-quality-references]] -- Narrative coherence failure = below floor, regardless of other qualities
- [[continuity-editing-scene-flow]] — DEPENDS_ON: continuity editing enforces the spatial and temporal consistency (screen direction, eyeline match, match on action) that makes narrative coherence possible across multi-shot sequences
- [[anime]] — INFORMS: narrative coherence applies across registers including anime; v16 anime train confirmed physically incoherent moments lose even in stylized work
- [[photoreal]] — DEPENDS_ON: photoreal register depends on narrative coherence as its primary judgment axis; incoherence around human faces compounds with uncanny valley
- [[ab-test-results]] — INFORMS: N=8 controlled A/B tests surfaced narrative coherence as the true causal axis, replacing prompt-depth as the test variable
- [[acting-chains-beat-camera]] — INFORMS: acting chains enforce narrative coherence by grounding characters in physical cause-and-effect sequences
- [[animate-pipeline-findings]] — INFORMS: /animate's restraint helps maintain narrative coherence by preventing over-specification that introduces contradictions

---

## Deep Reference

- **When** crafting a photoreal prompt and need to enforce element coexistence (e.g., rain implies no direct sun) → **read** `memory/feedback-narrative-coherence.md` (full file) **for** the v10 tulip macro operator quote explaining why physical consistency matters ("if it just rained, sun is unlikely"), the coexistence enforcement rules (rain → no direct sun, cold → breath/frost visible, summer → no frost), and why prompt-depth correlates with but doesn't cause coherence
- **When** judging an AI output and need to apply the narrative coherence test → **read** `memory/project-curriculum-elements.md` §(Element 1 — Photoreal subjects) **for** the running tally of N=8 controlled tests showing when coherence correlated with prompt approach, the v10 thesis reframe (prompt-depth is proxy, coherence is causal), and the sub-register pattern (scene-population favors crafted, close-ups favor terse)
- **When** evaluating whether a photoreal human output passes the coherence threshold → **read** `research-data/photoreal_humans_research.md` §(Uncanny Valley) [SOURCE FORMAT: conversation JSON — search for "uncanny valley" and "perceptual mismatch"] **for** the 40-60ms perceptual mismatch detection timing, lighting consistency as the strongest trigger of incoherence, and skin texture failures that break the physical story

---

## Open Questions

- Can narrative coherence be automatically detected in generated outputs (e.g., by a scoring model), or does it require human judgment?
- At what threshold of subtlety does narrative incoherence stop mattering? (e.g., slightly wrong shadow angle vs completely wrong weather)
- Does the principle transfer fully to non-photoreal registers (abstract, geometric, surreal) where physical rules are intentionally broken?
- Is there a diminishing return on coherence enforcement -- does overly rigid physical consistency prevent happy accidents?
