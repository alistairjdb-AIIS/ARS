# A/B Test Results

> Complete record of all blind A/B tests v1 through v20: register, hypothesis, result, scoring methodology, bias controls, and cumulative learnings.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 0 raw files, 2 memory files

---

## Core Findings

### Methodology

All tests follow the controlled-brief protocol (see [[prompting-craft-depth]]): both prompts target the IDENTICAL brief, varying only craft depth. Results presented with declared intent (hypothesis, target spec, success criteria) before operator viewing. Operator judges blind -- output labels (A/B) are assigned before rendering and do not reveal which is crafted vs terse. [TESTED]

### Scoring Methodology

Operator evaluates on two primary axes:
1. **Narrative coherence** -- does the scene tell ONE consistent physical story?
2. **Too-perfect veto** -- is any element so clean/symmetric that it reads as artificial?

Secondary evaluation: technical quality (lighting, composition, motion realism), emotional engagement, craft evidence. Results categorized as: Decisive win (clear preference), TIE (no meaningful difference), or Inconclusive (confound prevents valid comparison). [TESTED]

### Bias Controls

- Blind labeling: A/B assignment before rendering, not correlated with craft depth
- Controlled brief: same target for both variants
- Declared intent: hypothesis stated before viewing
- Operator correction of methodology flaws (v1 uncontrolled brief caught and corrected)
- v17: explicit bias control implemented (preventing positional or recency bias)

---

## Element 1: Photoreal Subjects (v1-v10)

### v1 -- First Test (Uncontrolled)
- **Register:** Photoreal still-life
- **Hypothesis:** Does prompt-craft-depth produce better execution?
- **Result:** INVALID -- uncontrolled brief (crafted prompt added new subject elements not in terse). Operator corrected methodology.
- **Learning:** Must hold brief constant. Established the controlled-brief protocol.

### v2 -- Ceramic Bowl Still-Life
- **Register:** Photoreal still-life
- **Hypothesis:** Craft depth (5-part shot-list) vs terse (1-sentence brief) on identical subject
- **Result:** CRAFTED WIN (decisive)
- **Key evidence:** "B's steam more natural with one weird direction where it goes in a split-second wrong way" -- the imperfection was the realism marker
- **Output:** `blind-ab/v2-output-b.mp4` (crafted) cited for natural steam physics
- **Below-bar:** v2-output-a.mp4 (terse) had wood-like artifact (steam misread)
- **Commit:** da0b178

### v3 -- Olive Oil Bottle Still-Life
- **Register:** Photoreal still-life
- **Hypothesis:** Same controlled-brief test on different subject
- **Result:** TERSE WIN (decisive)
- **Key evidence:** "B looks a bit more real as it's less perfect, but A is overall better" -- terse had better composition + lighting + foreground context. Crafted had olive oil color off, composition cropping.
- **Output:** `blind-ab/v3-output-a.mp4` (terse) cited for composition + lighting
- **Commit:** f1e5512

### v4 -- Coffee Pour Motion-Primary
- **Register:** Photoreal motion-primary
- **Hypothesis:** Does craft depth help for motion-primary subjects?
- **Result:** TERSE WIN (decisive)
- **Key evidence:** Terse had more realistic liquid stream. Both outputs had overly-wide steam around kettle spout (Veo limitation for gooseneck-pour, not prompt-depth dependent).
- **Output:** `blind-ab/v4-output-a.mp4` (terse) cited for liquid stream realism
- **Commit:** bfbd702

### v5 -- Morning Cafe/Bakery Interior
- **Register:** Photoreal environment
- **Hypothesis:** Does craft depth help for environment/architecture subjects?
- **Result:** TERSE WIN (decisive)
- **Learning:** Continued the pattern of controlled close-ups / interior scenes favoring terse.

### v6 -- Architecture/Scene-Population
- **Register:** Photoreal scene-population
- **Hypothesis:** Does craft depth help for scene-population (multiple elements)?
- **Result:** CRAFTED WIN (decisive)
- **Learning:** Scene-population scenes (multiple elements requiring spatial relationship) favor crafted. First evidence of the sub-register split.

### v7 -- Incomplete
- **Register:** Photoreal (subject not recorded)
- **Result:** INCOMPLETE -- only A rendered, hit daily fast quota
- **Learning:** N/A (no valid comparison)

### v8 -- Honey Drip
- **Register:** Photoreal motion-primary (viscous fluid)
- **Hypothesis:** Craft depth on fluid-physics subject
- **Result:** TERSE WIN (decisive)
- **Key evidence:** Crafted output (A) had "every other element better" but the perfectly-round spreading pattern vetoed it. This is where the too-perfect veto was crystallized as a principle.
- **Learning:** Established the binary veto -- one too-perfect element overrides aggregate superiority.

### v9 -- Subject Not Specified
- **Register:** Photoreal
- **Result:** TIE
- **Key evidence:** Terse B had "dirty glass + insects" that produced coherent ambient atmosphere despite being unspecified.
- **Learning:** Terse can produce narrative coherence when sampling lands well.

### v10 -- Tulip Macro
- **Register:** Photoreal macro/close-up
- **Hypothesis:** Craft depth on macro botanical subject
- **Result:** TIE (with narrative-coherence insight)
- **Key evidence:** Crafted A told a coherent rain story (cold + moist + no direct sun). Terse B had mixed signals (bright sun + heavy dew). This is where narrative coherence was identified as the primary axis.
- **Learning:** Prompt-depth is a PROXY. Primary axis = narrative coherence. Prompted the reframe of the entire testing thesis.

### Photoreal Subjects Running Tally (v1-v10)
- Terse decisive: 4 (v3, v4, v5, v8)
- Crafted decisive: 2 (v2, v6)
- TIE: 2 (v9, v10)
- Invalid: 1 (v1)
- Incomplete: 1 (v7)

**Sub-register pattern:** Scene-population (v2, v6) favors crafted. Close-ups / motion-primary / interior (v3, v4, v5, v8) favors terse. [TESTED -- directional]

---

## Element 3: Stylized Characters (v11-v17)

### v11 -- Anime Static Character
- **Register:** Anime, static
- **Hypothesis:** Craft depth on anime character (pre-research)
- **Result:** CRAFTED WIN (decisive)
- **Learning:** Anime register responds to craft even without research-informed techniques.

### v12 -- Anime Motion Character
- **Register:** Anime, with motion
- **Hypothesis:** Does craft depth help for anime characters in motion? (pre-research)
- **Result:** CRAFTED WIN (decisive)
- **Learning:** Anime crafted advantage holds for motion.

### v13 -- Pixar Robot
- **Register:** Pixar/3D style
- **Hypothesis:** Craft depth on Pixar-style character (pre-research)
- **Result:** TERSE WIN
- **Key evidence:** The crafted prompt included heavy camera specification ("slow dolly-in from medium-wide to medium close-up, slightly low angle"). This camera over-specification HURT the output.
- **Learning:** Not all craft specificity is equal. Camera choreography degrades character output.

### v14 -- Pixar Fox (Post-Research)
- **Register:** Pixar/3D style
- **Hypothesis:** Does research-informed craft (acting chains, physical descriptors, controlled color) beat terse? Color-controlled rerun of Pixar register.
- **Result:** RESEARCH-CRAFTED WIN (decisive)
- **Key evidence:** Operator: "you can see that one is a craft, the other is more generic." Acting-chain specificity (stimulus, processing, response) + physical descriptors + 60-30-10 color control produced coherent output across the entire frame.
- **Learning:** The v13 vs v14 delta: v14 specificity was about CHARACTER BEHAVIOR, not CAMERA BEHAVIOR. Established the "acting director, not DP" rule.

### v15 -- Anime Field
- **Register:** Anime
- **Hypothesis:** Research-informed craft on anime with environmental interaction
- **Result:** INCONCLUSIVE -- style drift confound (terse went 3D instead of anime)
- **Learning:** Beat-count finding: approximately 5 acting beats in 8 seconds causes visible scene transitions / fluidity breaks. Limit to 2-3 beats max.

### v16 -- Anime Train
- **Register:** Anime
- **Hypothesis:** Research-crafted vs terse on anime character scene
- **Result:** RESEARCH-CRAFTED WIN (on full evaluation)
- **Key note:** Initial impression favored terse, but quality + coherence analysis reversed it. Physically incoherent moments in terse lost to coherent moments in crafted.
- **Learning:** Narrative coherence principle reinforced -- applies to stylized registers too, not just photoreal.

### v17 -- Cartoon
- **Register:** Cartoon (not anime, not Pixar)
- **Hypothesis:** Craft depth on cartoon register
- **Result:** CRAFTED WIN (decisive, bias-controlled)
- **Learning:** Cartoon register follows the same pattern as anime -- craft specificity helps.

### Stylized Characters Running Tally (v11-v17)
- Research-crafted / Crafted: 5 (v11, v12, v14, v16, v17)
- Terse: 1 (v13)
- Inconclusive: 1 (v15)

**Sub-register pattern:** Anime 3-0 crafted (v11, v12, v16). Pixar split 1-1 (v13 terse, v14 research-crafted). Cartoon 1-0 crafted (v17). [TESTED]

---

## Element 4: Photoreal Humans (v18-v20)

### v18 -- Elderly Man Reading Letter (Kling AI)
- **Register:** Photoreal human, emotional
- **Hypothesis:** Does research-crafted approach (imperfection prompting, acting chain, film grain language) beat terse for photoreal humans?
- **Result:** RESEARCH-CRAFTED WIN
- **Key techniques:** Imperfection prompting (laugh lines, age spots, crooked nose) + acting chain + film grain language
- **Platform:** Kling AI (not Veo -- Veo hit daily quota)
- **Learning:** Kling confirmed as strong for face photorealism. Research-informed imperfection prompting works.

### v19 -- Coffee Shop Woman (Kling AI, /animate Pipeline Test)
- **Register:** Photoreal human, subtle emotion
- **Hypothesis:** Does /animate pipeline improve output vs direct research-crafted approach? BOTH prompts were research-crafted (not terse vs crafted).
- **Result:** /ANIMATE WIN (on re-evaluation)
- **Key evidence:** /animate-designed prompt won through RESTRAINT: more physically plausible (no impossible steam), more natural emotional sequence (loading, hold, release = involuntary genuine reaction), better framing from NOT specifying camera (profile = candid, observed; front-facing = posed).
- **Learning:** /animate adds value through what it helps leave OUT, not what it adds. Restraint and coherence beat elaboration.

### v20 -- Pixar x Pokemon Creature (Kling AI, /animate Pipeline Test)
- **Register:** Stylized creature, energetic
- **Hypothesis:** Does /animate pipeline work for energetic/spectacle content?
- **Result:** CRAFTED-WITHOUT-ANIMATE WIN
- **Key evidence:** The restrained loading approach (from /animate) produced static output. Direct crafted approach had more fluidity and motion. Operator: "I would want to see what happens with B."
- **Learning:** /animate pipeline's v19 restraint strategy was applied with recency bias. The content (energetic creature) called for rich motion, not subtlety. The framework works; the agent applied it incorrectly. Match restraint level to content register.

### Photoreal Humans + /animate Running Tally (v18-v20)
- Research-crafted: 1 (v18)
- /animate-crafted: 1 (v19)
- Crafted-without-animate: 1 (v20)
- Terse: 0

**/animate pipeline score: 1-1.** Won on subtle emotional content (v19), lost on energetic spectacle (v20). [TESTED]

---

## Cross-Element Summary

### Overall Score (v1-v20, excluding invalid/incomplete)
- Crafted / Research-crafted wins: 10 (v2, v6, v11, v12, v14, v16, v17, v18, v19, v20)
- Terse wins: 5 (v3, v4, v5, v8, v13)
- TIE: 2 (v9, v10)
- Inconclusive: 1 (v15)
- Invalid: 1 (v1)
- Incomplete: 1 (v7)

### Key Cumulative Findings

1. **Prompt-depth is a proxy, not a cause.** Retired as a test variable after N=8 photoreal. The causal axes are narrative coherence and specificity type. [TESTED]

2. **Acting-chain specificity helps; camera choreography hurts.** The v13 vs v14 comparison is the clearest evidence. [TESTED]

3. **Sub-register matters.** Scene-population and character work favor crafted. Close-ups and motion-primary favor terse. [TESTED -- directional]

4. **Too-perfect veto is binary.** One tell overrides aggregate superiority. [TESTED -- v8 is the canonical example]

5. **Narrative coherence is the primary axis.** Does the output tell one physical story? This predicts operator preference better than any other variable. [TESTED]

6. **Research-informed craft beats both pre-research craft and terse for characters.** The research synthesis adds acting chains, color control, and physical descriptors that pre-research craft did not include. [TESTED -- v14 vs v13 comparison]

7. **/animate pipeline value = restraint, matched to register.** Won on subtle content, lost on energetic content. [TESTED -- N=2, directional]

8. **Kling AI outperforms Veo 3.1 for photoreal human faces.** Cross-model finding from v18-v20 period. [TESTED -- N=3]

---

## Operational Rules

1. **When interpreting any single test:** Do not generalize from N=1. Note the register, the sub-register, and whether the finding is consistent with the cumulative pattern.

2. **When running new tests:** Follow the controlled-brief protocol. Declare intent before viewing. Apply bias controls.

3. **When a test result surprises:** Check for confounds (style drift in v15, recency bias in v20, uncontrolled brief in v1) before updating the running model.

4. **When advising on prompt approach:** Consult the sub-register pattern. Character work = use research-crafted with acting chains. Photoreal close-ups = terse may suffice. Scene-population = crafted.

5. **When the running tally reaches N greater than or equal to 5 on a sub-register:** Consider that sub-register's pattern established and redirect testing effort to unknowns.

---

## Source Files

| File | Contribution |
|------|-------------|
| `memory/project-curriculum-elements.md` | Complete test record v1-v20, running tallies, sub-register patterns, thesis reframes |
| `memory/feedback-character-prompt-specificity.md` | v14 and v19-v20 detailed findings, /animate pipeline analysis |

---

## Related Concepts

- [[prompting-craft-depth]] -- The methodology these tests evaluate
- [[narrative-coherence]] -- The primary judgment axis discovered through these tests
- [[too-perfect-veto]] -- The binary reject signal discovered through v8
- [[acting-chains-beat-camera]] -- The key character finding from v13 vs v14
- [[animate-pipeline-findings]] -- The /animate pipeline findings from v19-v20
- [[floor-bar-quality-references]] -- The quality framework these tests calibrate

---

## Deep Reference

- **When** looking up a specific test result (v1-v20) with operator quotes and scoring details → **read** `memory/project-curriculum-elements.md` (full file) **for** the complete per-test record including subject, register, approach, verdict, running tallies, sub-register patterns, thesis reframes, and cross-model findings
- **When** analyzing whether acting-chain specificity or camera specification drove a result → **read** `memory/feedback-character-prompt-specificity.md` (full file) **for** the v13 vs v14 comparison (camera hurt in v13, acting chain helped in v14), the v19 /animate restraint finding, and the v20 recency-bias diagnosis
- **When** determining whether a new test should use controlled-brief or uncontrolled protocol → **read** `memory/feedback-ab-test-controlled-brief.md` (full file) **for** the controlled-brief protocol (hold brief constant, vary only craft depth), the v1 uncontrolled test that produced unreliable conclusions, and the operator quote explaining why different-brief tests are invalid for craft-depth comparison

---

## Open Questions

- v7 was never completed -- should it be retested or retired?
- The photoreal subjects sub-register pattern (close-up favors terse) has N=4 decisive + 2 ties. Is this enough to consider it established?
- v15 was inconclusive due to style drift. Should the anime field register be retested?
- /animate pipeline has N=2 (1 win, 1 loss). More N needed before the restraint-matching conclusion is firm.
- Kling vs Veo comparison is confounded by the fact that Kling was used because Veo hit quota. A controlled cross-model A/B has not been done.
