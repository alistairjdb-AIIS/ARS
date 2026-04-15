# Prompting Craft Depth

> The methodology for testing whether deeper prompt craft improves AI video output: controlled-brief A/B testing with declared intent, isolating craft depth as the single variable, and measuring against floor/bar quality axes.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 0 raw files, 4 memory files

---

## Core Findings

### The Controlled-Brief Protocol

When A/B testing craft approaches, BOTH outputs must target the IDENTICAL brief. The variable is HOW the brief is expressed (terse vs crafted), not WHAT is being requested. [TESTED -- protocol established after operator correction on v1, refined through v1-v20]

If prompt A says "ceramic bowl with morning light" and prompt B says "ceramic bowl with morning light AND steam AND dolly push-in AND 85mm lens," that is not a craft-depth test -- it is a different-brief test. The outputs are not comparable on craft quality because they were aimed at different targets. [TESTED -- v1 was uncontrolled, operator corrected]

**The three-step brief construction:**
1. Write the BRIEF (target output description). This is the shared north star both variants aim at.
2. First-instinct prompt = terse paste of the brief, minimal framing. Same asks, stripped of craft scaffolding.
3. Internal-dialogue prompt = the brief expanded into craft-appropriate language (shot-list, cinematography terms, lighting direction, style descriptors). NO NEW SUBJECT ELEMENTS added beyond the brief.

Both prompts request identical outputs. The only variable is prompt-craft depth. [TESTED]

### Declare Intent Before Viewing

Before presenting any A/B test outputs to the operator, state three things up front. [TESTED -- protocol established by operator directive 2026-04-05]

1. **Test hypothesis** -- what single variable is being isolated (e.g., "does prompt-craft-depth produce better execution of the same brief?")
2. **Target specification** -- what the output is supposed to reflect: subject, mood, constraints, expected qualities
3. **Success criteria** -- what the operator should evaluate against

Without declared intent, the operator reacts to surface aesthetics. With intent declared, they can judge craft execution against the goal and spot mismatches between aim and output. This is the fabrication guard applied to A/B presentation -- state what is being tested, do not leave it implicit. [TESTED]

### The Prompt-Depth Finding (N=20)

After 20 controlled A/B tests across three registers, prompt-depth as a variable was RETIRED as a test axis. It was established as a proxy, not the cause. [TESTED -- reframe after N=8 photoreal, confirmed through N=20]

**Photoreal subjects (v1-v10):** Terse decisive 4x (v3, v4, v5, v8), Crafted decisive 2x (v2, v6), TIE 2x (v9, v10). No clear winner -- prompt depth is not the causal axis. [TESTED]

**Stylized characters (v11-v17):** Research-crafted 5, Terse 1, Inconclusive 1. Research-informed craft consistently wins for character work. [TESTED]

**Photoreal humans (v18-v20):** Research-crafted 1 (v18), /animate-crafted 1 (v19), Terse 0. Craft wins, but the TYPE of craft matters. [TESTED]

### What Prompt-Depth Is a Proxy For

Prompt-depth correlates with two deeper causes:

1. **Narrative coherence** -- Crafted prompts sometimes force condition coexistence (if rain then no direct sun). Terse prompts sometimes produce coherent atmosphere by luck. The variable is whether elements tell one physical story, not how many words were used. [TESTED -- see [[narrative-coherence]]]

2. **Acting-chain specificity** -- For character work, crafted prompts that spend tokens on acting chains (stimulus, processing beat, response) reliably outperform terse. But crafted prompts that spend tokens on camera choreography HURT. The type of specificity matters more than the amount. [TESTED -- see [[acting-chains-beat-camera]]]

### Sub-Register Patterns

Not all content benefits equally from craft depth. [TESTED -- directional, N varies per sub-register]

- Scene-population scenes (architecture v6, still-life v2) favor crafted
- Controlled close-ups, motion-primary, interior scenes (v3, v4, v5, v8, v9) favor terse
- All anime sub-register tests favor crafted (v11, v12, v16)
- Pixar split 1-1 (v13 terse, v14 research-crafted)
- Cartoon favors crafted (v17)
- Photoreal humans favor research-crafted (v18, v19)

### The Curriculum Approach

Each "element" (photoreal subjects, camera craft, stylized characters, photoreal humans, combinations) gets independent bar and floor references established via blind A/B plus operator judgment. Lock the current element before advancing to the next. Combine at the end. [VERIFIED -- operator-confirmed curriculum structure]

Element progression order:
1. Photoreal subjects -- ADVANCED PAST (operator priority shift 2026-04-05)
2. Photoreal motion/camera craft -- cross-cutting sub-skill
3. Stylized characters -- ACTIVE as of 2026-04-06
4. Photoreal humans -- ACTIVE as of 2026-04-06
5. Combinations -- advanced phase, after individuals locked

### Cross-Tool Prompt Dialect (2026-04-07)

**Each model speaks a different prompt language.** Prompt craft is not portable between tools. [VERIFIED-research — Prompt-A-Video, NeurIPS]

| Tool | Dialect | Effective Structure |
|---|---|---|
| **Kling** | Action/timeline | Beat-marked sequences, concrete physical actions |
| **Veo** | Structured/data-like | Shot-list format, sensory detail, 5-part formula |
| **Runway** | Force/physics prose | Short sentences, momentum/resistance/impact language |

**Implications for craft-depth testing:**
- A/B tests WITHIN a tool should use that tool's native dialect for both variants
- A/B tests ACROSS tools should use tool-optimized prompts (same intent, different syntax) — never identical prompts
- The acting-chain approach transfers conceptually across tools, but the FORMAT differs: beat-marked timelines for Kling, structured shot-list for Veo, prose narrative for Runway

**This answers the open question** "How should craft depth be calibrated for Kling AI vs Veo 3.1?" — it should be calibrated per tool, using each model's native prompt language.

### Quality Modifiers Suppress Motion

Image-derived quality descriptors ("cinematic," "photorealistic," "8K detailed") actively reduce motion magnitude in video generation. [VERIFIED-research — Prompt-A-Video, NeurIPS]

- Quality modifiers compete with motion descriptors for model attention capacity
- Adding aesthetic descriptors that work for images suppresses dynamic degree scores in video
- The model may interpret "cinematic" as "slow/stable" rather than "high quality"

**Operational implication:** Craft depth for video should allocate tokens to acting chains and motion, NOT to aesthetic quality modifiers. This refines the finding that "acting-chain specificity helps, camera over-specification hurts" — now extended to: **quality modifier over-specification also hurts**.

**Structure > Length (meta-analysis of 1,500 papers):** [VERIFIED-research]
- Structured short prompts outperform verbose alternatives while cutting costs by 76%
- XML/structured formatting delivers 15% performance boost regardless of word choice
- For video: 2-4 sentences covering scene, camera, motion, pacing is optimal
- The acting-chain approach works not because it adds length but because it adds STRUCTURE

---

## Operational Rules

1. **When designing an A/B test:** Write the brief FIRST. Both prompts target the same brief. The terse version strips craft scaffolding. The crafted version adds craft language. NO new subject elements in the crafted version.

2. **When presenting results:** Declare test hypothesis, target specification, and success criteria BEFORE the operator views any output. State whether the test was controlled (held brief constant) or uncontrolled.

3. **When interpreting results:** Do not conclude "terse wins" or "crafted wins" from a single test. Ask: did the winner have better narrative coherence? Was acting-chain specificity or camera over-specification present? Prompt-depth is the proxy; coherence and specificity type are the causes.

4. **When choosing craft depth for production (not testing):** Match craft approach to register. Scene-population and character work benefit from craft. Close-ups and motion-primary photoreal may do as well or better with terse. Subtle emotional content benefits from /animate-style restraint.

5. **When building competency on a new element:** Start with controlled A/B tests, accumulate N greater than or equal to 5, identify the causal axes for that element, then lock floor and bar references before advancing.

6. **When the same finding appears 3+ times:** Stop testing that variable and declare it established. Redirect testing effort to the next unknown.

---

## Deep Reference

- **When** translating a prompt from one tool to another → **read** [[runway-gen4]] §Prompt Dialect **for** Runway-native force/physics patterns, and [[veo-3-1]] §Prompt Patterns **for** Veo's 5-part formula and vocabulary reference
- **When** deciding optimal prompt length → **read** Prompt-A-Video (arXiv 2412.15156) **for** evidence that structured short prompts (2-4 sentences) outperform verbose, and that image-quality descriptors actively suppress video motion magnitude
- **When** writing acting chains for a specific tool → **read** [[acting-chains-beat-camera]] §The Acting Chain Template **for** the stimulus/processing/response structure, then adapt FORMAT to tool dialect (beat-marked for Kling, shot-list for Veo, prose for Runway)
- **When** choosing between craft depth levels for a sub-register → **read** `memory/project-curriculum-elements.md` **for** full v1-v20 score tallies broken down by register, showing which sub-registers favor terse vs crafted
- **When** assessing whether a quality modifier is helping or hurting → **read** [[photoreal]] §Quality Modifiers Suppress Motion **for** the research-backed finding and the replacement pattern (motion-specific language instead of aesthetic descriptors)

---

## Source Files

| File | Contribution |
|------|-------------|
| `memory/feedback-ab-test-controlled-brief.md` | Controlled-brief protocol: hold brief constant, vary only craft depth |
| `memory/feedback-ab-declare-intent-first.md` | Three-element declaration protocol before operator viewing |
| `memory/feedback-character-prompt-specificity.md` | Type of craft matters: acting chains help, camera choreography hurts |
| `memory/project-curriculum-elements.md` | Full A/B test record, element curriculum, sub-register patterns, prompt-depth retirement as test variable |

---

## Related Concepts

- [[narrative-coherence]] -- The true causal axis that prompt-depth proxied for
- [[too-perfect-veto]] -- Crafted prompts carry higher too-perfect risk from over-specification
- [[acting-chains-beat-camera]] -- The specific finding about WHICH type of craft depth helps
- [[ab-test-results]] -- Complete record of all v1-v20 test results
- [[floor-bar-quality-references]] -- The quality framework that A/B tests calibrate against
- [[animate-pipeline-findings]] — EXTENDS: /animate pipeline as a craft-depth tool
- [[character-design-prompting]] — EXTENDS: character-specific prompting (shape language, acting chains, color rules) is the register-specific application of craft depth for stylized and human character work

---

## Open Questions

- Is there a prompt length sweet spot (Veo documentation suggests 150-300 characters) that interacts with craft depth?
- Does the sub-register pattern (scene-population favors crafted, close-ups favor terse) hold with more N?
- Would a structured brief template (vs free-form) systematically improve craft-depth testing?
- ~~How should craft depth be calibrated for Kling AI vs Veo 3.1?~~ **ANSWERED (2026-04-07):** Each model has a distinct prompt dialect. Calibrate per tool using native syntax. See §Cross-Tool Prompt Dialect above.
