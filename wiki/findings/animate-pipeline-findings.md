# /animate Pipeline Findings

> The /animate pipeline adds value through RESTRAINT -- what it helps leave out -- not through elaboration. But restraint must be matched to content register: subtle content benefits from restraint, energetic content needs richer specification.

**Confidence:** MEDIUM
**Last compiled:** 2026-04-06
**Sources:** 0 raw files, 2 memory files

---

## Core Findings

### The /animate Pipeline

The /animate pipeline is a structured creative framework (FEEL/CONVERGENCE/VISUAL + cross-domain principles) used to craft prompts. It differs from direct research-informed prompting by imposing a process that evaluates emotional register, convergence points, and visual translation before writing the prompt. [VERIFIED -- pipeline description from memory files]

### v19: Restraint Won on Subtle Content

**Test setup:** Coffee shop woman, photoreal human, Kling AI. BOTH prompts were research-crafted (not terse vs crafted). The /animate-designed prompt was compared against a directly research-crafted prompt. [TESTED]

**Result:** /animate prompt won on re-evaluation.

**Why it won -- through what it left OUT:**
- More physically plausible: no impossible steam, no over-described environmental details
- More natural emotional sequence: loading, hold, release = involuntary, genuine reaction (vs directly specified emotional beats)
- Better framing from NOT specifying camera: profile framing = candid, observed quality; front-facing framing = posed quality

The /animate framework's FEEL step identified the emotional register as subtle/internal, and the process naturally produced a restrained prompt. The value was in the discipline of the framework preventing over-specification, not in adding more detail. [TESTED]

### v20: Restraint Lost on Energetic Content

**Test setup:** Pixar x Pokemon creature, stylized, Kling AI. /animate-designed prompt vs directly crafted prompt. [TESTED]

**Result:** Crafted-without-animate won.

**Why it lost -- restraint mismatched to content:**
- The restrained loading approach produced static output for content that required energy
- The direct crafted approach had more fluidity and motion
- Operator: "I would want to see what happens with B" (the non-/animate output)

**Root cause:** The /animate prompt chose restraint because v19 won with restraint. This was recency bias in application, not a framework flaw. The v20 content (energetic creature sparking with electricity) called for rich motion description, not subtle loading. The FEEL step of /animate should have identified the emotional register as energetic and produced accordingly. The agent applied the framework with a bias toward the previous session's winning approach. [TESTED]

### The Synthesis: Match Restraint to Register

/animate pipeline score: 1-1. [TESTED -- N=2, directional only]

| Content Register | /animate Approach | Outcome |
|-----------------|-------------------|---------|
| Subtle emotional (v19) | Restrained loading, minimal camera, natural emotional sequence | WIN |
| Energetic spectacle (v20) | Restrained loading (misapplied) | LOSS |

The finding is not "/animate = restraint." The finding is "/animate should produce the level of specification that matches the content's emotional register." Subtle content benefits from what the framework helps leave out. Energetic content needs what the framework should help include. [TESTED -- but N=2, so directional]

### Progressive Disclosure and Pacing

The /animate pipeline's approach to animation aligns with confirmed pacing principles. [VERIFIED -- from animation pacing feedback]

Validated animation patterns:
- Progressive disclosure with dimming: prior content fades when contrasting content appears
- Deliberate pauses before reveals ("beat drops")
- Staggered element reveals
- Pacing as material, not just motion

These patterns work because they match how the /animate FEEL step processes timing -- identifying where pauses carry weight, where motion should accelerate, where stillness IS the content. The 1-2 second pause in 8 seconds carries enormous weight (Miyazaki's "Ma" principle). [VERIFIED]

### Relationship to Acting Chains

/animate's value for character work is complementary to the acting-chain finding. Acting chains provide the WHAT (stimulus, processing, response). /animate provides the HOW MUCH (how specified, how restrained, how much camera direction). The v19 win combined both: acting-chain structure with /animate-derived restraint in camera and environmental specification. [TESTED -- v19]

---

## Operational Rules

1. **When using /animate for subtle/emotional content:** Let the framework's restraint work. Do not specify camera. Do not over-describe environmental details. Trust the loading, hold, release emotional sequence. The value is what gets left out.

2. **When using /animate for energetic/spectacle content:** Override the restraint default. The FEEL step should identify the register as energetic and produce correspondingly rich motion description, dynamic transitions, and active visual elements. Do not default to the previous session's approach.

3. **When comparing /animate vs direct craft:** Both prompts should be research-informed. The test is whether the /animate PROCESS adds value over direct application of the same research, not whether research craft beats terse.

4. **When the /animate prompt produces unexpectedly static output:** Check whether the content register was energetic and the prompt was restrained. The mismatch is the most likely cause.

5. **When applying pacing principles:** Use progressive disclosure, beat drops, and staggered reveals. These are confirmed patterns that the /animate framework naturally produces when the FEEL step correctly identifies pacing.

6. **When evaluating /animate results:** N=2 is insufficient for firm conclusions. Continue testing across registers before treating the restraint-matching pattern as established.

---

## Source Files

| File | Contribution |
|------|-------------|
| `memory/project-curriculum-elements.md` | v19 and v20 test records, /animate pipeline score, cross-model finding (Kling for humans) |
| `memory/feedback-character-prompt-specificity.md` | v19 detailed analysis (restraint value), v20 recency bias diagnosis, framework-vs-application distinction |
| `memory/feedback-animation-pacing.md` | Progressive disclosure, beat drops, staggered reveals as confirmed pacing patterns |

---

## Related Concepts

- [[acting-chains-beat-camera]] -- Acting chains provide the content; /animate provides the calibration of how much to specify
- [[prompting-craft-depth]] — EXTENDS: /animate is a structured approach to craft depth; the question is whether the structure adds value over direct craft
- [[ab-test-results]] — DEPENDS_ON: v19 and v20 are the specific tests; see full record
- [[character-design-prompting]] -- The character design research that /animate draws from
- [[narrative-coherence]] — INFORMS: /animate's restraint helps maintain narrative coherence by preventing over-specification that introduces contradictions

---

## Deep Reference

- **When** applying /animate and need to calibrate restraint level for the content register → **read** `memory/feedback-character-prompt-specificity.md` §(v19 finding + v20 nuance) **for** the evidence that v19's value was in what /animate helped leave out (no impossible steam, better framing from NOT specifying camera), while v20's failure was applying v19's restraint to energetic content where it didn't fit — the FEEL step must match content's emotional register, not default to previous session's winning approach
- **When** deciding whether the /animate pipeline or direct craft is better for a specific subject → **read** `memory/project-curriculum-elements.md` §(v19-v20 results) **for** the 1-1 score showing /animate won on subtle emotional content (v19 photoreal human), lost on energetic spectacle (v20 stylized creature), and the operator diagnosis that the framework works but the agent applied it with recency bias
- **When** progressive disclosure pacing is part of the /animate design and need confirmed timing patterns → **read** `memory/feedback-animation-pacing.md` (full file) **for** the operator-validated patterns: dimming prior content when introducing contrasts, 1.8s beat drop pause before reveals, staggered bar reveals, and "pacing as material, not just motion"

---

## Open Questions

- N=2 is not enough to establish the restraint-matching pattern. What is the minimum N needed per content register?
- Does /animate add value for photoreal non-human subjects (environments, objects) or only for character/human work?
- Can the FEEL step be formalized to automatically identify the correct restraint level for a given content register, or does it require operator judgment?
- The v20 "fix the application, not the framework" diagnosis is untested -- would /animate with an energetic-calibrated FEEL step have beaten direct craft on v20?
- Does the /animate framework's value scale with prompt complexity? (i.e., is it more valuable for complex multi-beat scenes than simple single-beat ones?)
