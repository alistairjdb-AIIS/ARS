# Too-Perfect Veto

> "Too perfect = artificial." Perfectionist language in prompts invites synthetic tells. One too-perfect element in the output vetoes many strengths. This operates as a binary reject signal, not a weighted dimension.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Layer 1 -- Output Judgment (Binary Veto)

One too-symmetric or too-clean element can veto an otherwise superior output, regardless of how it was prompted. The veto is an output property, not a prompt-depth property. Both over-specified physics (crafted prompts) and sampling randomness (terse prompts) can produce "too perfect." The judge reacts to the artifact, not its origin. [TESTED -- confirmed across v2, v3, v8, v10]

**Evidence from A/B tests:**

- **v8-A (crafted, honey drip):** Operator said "every other element on A is better... I would have bought that honey" but the perfectly-round spreading pattern vetoed the output. ONE tell, ONE veto. [TESTED]
- **v10-B (terse, tulip macro):** "B looks sort of too good... too perfect and when it's too perfect, it's not realistic." Same veto pattern from a terse prompt. [TESTED]
- **v3 (terse won):** "B looks a bit more real as it's less perfect, but A is overall better." Variance decided the outcome despite aggregate quality favoring the other. [TESTED]
- **v2 (crafted won):** "B's steam more natural with one weird direction where it goes in a split-second wrong way." The imperfection was the deciding evidence of realism. [TESTED]

### Layer 2 -- Prompt Writing (Avoid Perfectionist Language)

Do not prompt for perfection, uniformity, or symmetric idealized motion. Allow variance to emerge. [TESTED -- derived from pattern across v2-v10]

**Words and phrases to strip from photoreal prompts:**
- "flawlessly," "perfectly uniform," "evenly spaced," "smoothly symmetric"
- Deterministic fluid specs: "smooth viscous stream," "slowly spreading," "steady pour" (invites too-clean execution)
- Any language that locks motion/physics to a specific geometric outcome
- "flawless skin," "perfect complexion," "smooth skin" (pushes toward synthetic aesthetic)

**Words and phrases to prefer:**
- Variance language: "irregular," "natural imperfection," "slight deviations," "one-off variations"
- Loose motion specs: "slow drip" instead of "viscous stream"; "breeze" instead of "laminar air current"
- Imperfection markers: "visible pores," "subtle freckles," "natural redness," "slight asymmetry"

### Imperfection Prompting for Humans

The too-perfect veto is especially potent for photoreal human faces. AI models are biased toward generating conventionally attractive, symmetrical, smooth-skinned faces -- a training data artifact where denoising smooths toward averages. [VERIFIED -- multiple independent sources in photoreal humans research]

Effective imperfection prompts for breaking the "AI face":
- "Light freckles across the nose bridge"
- "Faint laugh lines"
- "A small scar on the left cheek"
- "Slightly messy eyebrows"
- "Natural redness around the nose"
- "Fine facial hair" (peach fuzz)
- "Asymmetric smile"
- "Visible pores on forehead and cheeks"
- "Subtle under-eye circles"

The principle: "Perfection triggers the uncanny valley while imperfection creates realism." [VERIFIED -- strongly convergent community finding]

### The Uncanny Valley Connection

Human perception detects facial violations within 40-60 milliseconds. The most potent uncanny valley trigger is when different parts of the face sit at different levels of realism -- realistic eyes but synthetic skin, or natural skin but lifeless eyes. The "too perfect" signal is a specific instance of this: when ALL elements are too clean, the entire face reads as a single synthetic surface. [VERIFIED -- PMC research cited in photoreal humans research]

### Skin Texture Specifically

Real skin is not a single reflective surface -- it is translucent, layered, with variable reflectance. AI models commonly produce:
- Over-smoothing of pores (the "airbrushed" look)
- Erased capillary blush and subsurface scattering
- Uniform specular highlights instead of variable reflectance
- Skin rendered as a single material rather than layered

Prompt mitigations: "Natural skin texture, visible pores, natural imperfections," "soft skin texture, natural pores, minimal makeup" (from Google's Veo prompt guide). [VERIFIED]

### Soft Lighting Helps

Soft, diffused lighting minimizes both the too-perfect appearance and uncanny valley triggers. Harsh directional light exacerbates skin texture problems and casts shadows the model may render inconsistently. [VERIFIED -- convergent finding across photography principles and AI community testing]

### Domain Scope

This veto is confirmed for photoreal renders. Transfer to stylized characters or non-physical scenes is untested. Stylized registers (Pixar, anime) may have different tolerance because the aesthetic contract already accepts non-realism. [THEORETICAL]

---

## Operational Rules

1. **When writing photoreal prompts:** Strip perfectionist language. Do not specify fluid dynamics, spreading patterns, or geometric motion outcomes. Let the model sample naturally. Prefer "irregular," "natural," "slight variations."

2. **When judging outputs:** Look for ONE too-symmetric or too-clean element as a veto signal. Do not average it against strengths. The tell is binary -- one too-perfect element vetoes many good ones.

3. **When presenting A/B pairs:** Expect the operator to veto on single tells even when aggregate quality favors the vetoed output. Crafted prompts carry higher tell-risk because they over-specify physics.

4. **When prompting human faces:** Always include 2-3 imperfection markers (freckles, laugh lines, pores, asymmetry). Never use "flawless," "perfect complexion," or "smooth skin."

5. **When choosing lighting:** Default to soft, diffused light for photoreal human subjects. Harsh directional light amplifies the synthetic texture problem.

6. **When in doubt, strip rather than add:** If a prompt descriptor could produce too-clean output ("steady pour," "uniform spread," "symmetric flow"), remove it. The model's natural sampling variance is an asset, not a defect.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/photoreal_humans_research.md` | Imperfection prompting techniques, skin texture failures, uncanny valley timing, AI face problem, lighting recommendations |
| `memory/feedback-too-perfect-veto.md` | Binary veto principle, v2/v3/v8/v10 evidence, prompt-side and output-side framing, perfectionist language to avoid |

---

## Related Concepts

- [[narrative-coherence]] -- The other primary judgment axis (independent of too-perfect)
- [[prompting-craft-depth]] -- Crafted prompts carry higher too-perfect risk from over-specification
- [[floor-bar-quality-references]] -- Too-perfect veto = floor failure regardless of creativity
- [[character-design-prompting]] -- For character work, over-smooth movement quality triggers the same veto principle
- [[photoreal]] — DEPENDS_ON: photoreal register depends on the too-perfect veto as a binary quality gate; AI face smoothing and skin texture failures are the most potent triggers
- [[ab-test-results]] — INFORMS: the too-perfect veto was crystallized as a principle through v8 (honey drip) and confirmed across v2, v3, v10

---

## Deep Reference

- **When** writing a photoreal prompt and need to check whether any language invites too-clean execution → **read** `memory/feedback-too-perfect-veto.md` §(Layer 2 — Prompt writing) **for** the avoid list ("flawlessly," "perfectly uniform," "evenly spaced," "smoothly symmetric," deterministic fluid specs), the prefer list ("irregular," "natural imperfection," "slight deviations"), and why loose motion specs ("slow drip") beat precise ones ("viscous stream")
- **When** judging an A/B pair and one output looks technically superior but "off" → **read** `memory/feedback-too-perfect-veto.md` §(Layer 1 — Output judgment) **for** the evidence chain from v2/v3/v8/v10 showing ONE tell vetoes regardless of aggregate quality, and why the operator said "B looks sort of too good... too perfect and when it's too perfect, it's not realistic"
- **When** prompting for imperfection in photoreal human faces and skin → **read** `research-data/photoreal_humans_research.md` [SOURCE FORMAT: conversation JSON — search for "imperfection prompting" and "skin texture"] **for** specific imperfection descriptors that break the too-clean aesthetic (laugh lines, age spots, crooked nose, pores), and the film grain / film look technique for introducing organic variance

---

## Open Questions

- Does the too-perfect veto apply to stylized registers (Pixar, anime) or only photoreal?
- Is there a threshold of imperfection that goes too far and reads as "broken" rather than "real"?
- Can a scoring model detect too-perfect tells, or does this require human judgment (the 40-60ms perceptual detection suggests it may be hard to formalize)?
- Film grain prompting may produce digital noise rather than authentic film grain (Metaphysic.ai analysis) -- does this still help avoid the too-clean aesthetic?
