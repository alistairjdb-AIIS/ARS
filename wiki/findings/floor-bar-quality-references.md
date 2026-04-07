# Floor-Bar Quality References

> Two independent quality axes: Floor (minimum acceptable = ReviewGold V3, aesthetic cleanliness) and Bar (target quality = ReviewBoardingPass, creativity multiplied by execution). A clean but derivative output passes floor but misses bar. A creative but sloppy output reaches for bar but falls below floor.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 0 raw files, 2 memory files

---

## Core Findings

### The Two-Axis Principle

Creative ceiling and aesthetic floor are DISTINCT axes, not a single ranking. This distinction had been implicit across sessions but was captured explicitly when the operator was asked "what are the top reels by your judgment?" and clarified the two independent dimensions. [TESTED -- operator calibration 2026-04-05]

- **Floor** (aesthetic cleanliness) = non-negotiable baseline. Output below this = reject.
- **Bar** (creativity x execution) = target to reach for. Output reaching this = success.

A clean reel can be derivative: passes floor, misses bar. A creative reel can be sloppy: reaches for bar, falls below floor. Both dimensions matter independently. [VERIFIED -- operator explicitly separated the two axes]

### The Floor Reference: ReviewGold V3

**Source session:** April 4, 2026. Gemini scoring feedback loop. [TESTED]

Iteration history:
- V1: 5/10 (Gemini score)
- V2: 7/10 (Gemini score)
- V3: 6.5/10 (Gemini score) -- but operator called it "stunning" and preferred it over V2
- V4: Research-informed fix (post-V3)

Operator quote: "from a personal judgment of cleanliness, V3 is sort of the bar and the floor." V3's aesthetic cleanliness IS the floor. Future outputs must match or exceed this baseline. [TESTED]

The divergence between Gemini scoring (6.5 < 7.0) and operator judgment ("stunning," preferred over V2) demonstrates that automated scoring does not capture the floor dimension reliably. The floor is an operator-calibrated human judgment, not a computed metric. [VERIFIED]

**Deployed reference:** `/review-gold-compare` (all 4 versions side by side for calibration).

### The Bar Reference: ReviewBoardingPass

**Source session:** Prior session, Harmonia Dental review reels (A/B/C comparison). [TESTED]

Operator called it "new bar" at time of shipping.

Operator quote: "probably that one has the highest bar. The boarding pass one. Mix of creativity as in not rigid but discovery and trying something new. Plus execution."

Why it is the bar: BOTH axes hit simultaneously. Creative discovery (ticket/boarding pass metaphor applied to dental reviews, not a rigid template) AND strong execution (aesthetic cleanliness at or above floor level). The metaphor import from an adjacent industry (travel boarding pass applied to dental review) exemplifies the [[whitespace-opportunity-framework]]. [TESTED]

**Deployed reference:** `/review-reels` (option B).

### Secondary Floor References

Additional outputs that meet the V3 aesthetic floor, named by operator in prior sessions. [VERIFIED -- operator-named]

- **LayerPeel** -- meets V3 floor
- **DataPulse** -- meets V3 floor
- **Scale** -- meets V3 floor

These were collectively described as "V3 aesthetic floor reels -- much better" compared to Skinvive Redact, which "lacks fluidity/motion." The fluidity/motion dimension is part of the floor, not a separate axis. [VERIFIED]

### The Design Floor Achievement

The operator confirmed the design system's output meets the quality floor as of March 22, 2026: "Honestly beautiful. At this point my floor is your floor and now is only judgment driven." [VERIFIED -- operator quote]

This means:
- Technical quality of design output no longer needs correction
- The remaining delta is taste/vision decisions requiring operator judgment
- The floor is met autonomously; the bar requires collaboration

### The Decision Hierarchy

When evaluating any creative output for shipping. [VERIFIED -- derived from operator feedback across multiple sessions]

| Evaluation | Action |
|-----------|--------|
| Floor failure | Reject unconditionally. Iterate until floor is met. |
| Floor pass, bar miss | Ship if needed, but flag that the target was not reached. Acceptable for production, not for portfolio. |
| Floor pass, bar hit | Celebrate. Study the path that produced it. Document for future reference. |

### Floor and Bar in A/B Testing Context

The floor/bar framework applies to A/B test evaluation as well. [VERIFIED -- integrated into test methodology]

- **Narrative coherence failure** = below floor, regardless of other qualities (see [[narrative-coherence]])
- **Too-perfect veto** = below floor, regardless of other qualities (see [[too-perfect-veto]])
- **Both A and B pass floor** = evaluate on bar dimensions (creativity, engagement, coherence quality)
- **Neither passes floor** = reject both, iterate

### Anti-Rigidity Mechanisms

The operator flagged a concern that saved references could make the quality system rigid. Four mechanisms prevent this. [VERIFIED -- operator-directed safeguards]

1. **Context-scoped references:** Each bar/floor tagged with its domain (e.g., "photoreal still-life, steam physics dimension"). Non-transferable across domains.
2. **Dissent-on-apply:** Before invoking a saved reference to reject new work, state the reference and ask operator if it still applies. No silent gatekeeping.
3. **Sunset cadence:** References unused or unchallenged for 3 sessions get surfaced for re-evaluation.
4. **Multiple anchors per element:** Collect more than one bar, more than one floor. Range, not single correct answer.

Memory-as-reference, not memory-as-law. [VERIFIED -- operator directive]

---

## Operational Rules

1. **Before shipping any creative output:** Evaluate on BOTH axes independently. Floor check first (does cleanliness match or exceed ReviewGold V3?), then bar check (does it show creative discovery AND execution quality?).

2. **When floor is not met:** Reject and iterate. Do not ship below-floor work regardless of creative ambition, deadline pressure, or aggregate quality on other dimensions.

3. **When floor is met but bar is missed:** Ship if needed for production. Flag it as acceptable but not target quality. Do not add to portfolio references.

4. **When invoking a reference to reject work:** State which reference is being applied and verify with the operator that it still applies to the current context and domain. Do not silently gatekeep.

5. **When 3 sessions pass without a reference being challenged or used:** Surface it for re-evaluation. It may be stale or the domain may have evolved.

6. **When automated scoring (Gemini, etc.) diverges from operator judgment:** Operator judgment is authoritative for floor/bar calibration. Automated scoring is a diagnostic, not a decision.

7. **When working in a new domain:** Do not assume existing floor/bar references transfer. Establish domain-specific references through calibration in the new domain.

---

## Source Files

| File | Contribution |
|------|-------------|
| `memory/project-design-top-reels.md` | Floor (ReviewGold V3) and Bar (ReviewBoardingPass) references, decision hierarchy, secondary references, anti-rigidity mechanisms |
| `memory/feedback-design-floor.md` | Design system floor achievement confirmation, operator quote, transition from execution quality to taste/judgment |

---

## Related Concepts

- [[narrative-coherence]] -- Narrative coherence failure = below floor
- [[too-perfect-veto]] -- Too-perfect element = below floor
- [[whitespace-opportunity-framework]] -- ReviewBoardingPass IS the bar because it exemplifies whitespace format import
- [[range-building-philosophy]] -- Range-building happens above the floor; floor is the non-negotiable baseline
- [[ab-test-results]] -- A/B tests calibrate floor and bar references per element
- [[prompting-craft-depth]] -- The curriculum approach establishes floor and bar per element before advancing

---

## Open Questions

- Should there be a formal "bar hit" count? (i.e., how many outputs have reached ReviewBoardingPass level since it was established as the reference?)
- The floor is human-judged. Can any dimensions of floor quality be automated (e.g., fluidity/motion detection, color consistency checking)?
- ReviewGold V3 was established in a Gemini scoring context. Does the floor transfer to non-reel formats (static design, interactive pages)?
- The anti-rigidity mechanisms depend on operator engagement. What happens if references go unchallenged because the operator is not reviewing output for multiple sessions?
- Is there a "super-bar" -- outputs that exceed ReviewBoardingPass -- and should those be tracked separately?
