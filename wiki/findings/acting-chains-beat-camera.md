# Acting Chains Beat Camera

> The finding that acting-chain specificity (stimulus, processing beat, response + physical descriptors + movement quality) improves AI video character output, while camera choreography over-specification degrades it. "Be the acting director, not the DP."

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 2 memory files

---

## Core Findings

### The Core Insight

Not all prompt specificity is equal for character work. Two types exist with opposite effects on output quality. [TESTED -- confirmed v13 vs v14 comparison, reinforced across v11-v17]

**Helps (acting-chain specificity):**
- Stimulus, processing beat, response sequence: "ears perk up, freezes, slowly crosses eyes, whiskers twitch, smile spreads"
- Physical descriptors over emotion labels: "whiskers twitch" not "looks curious"
- Movement quality as personality: "slowly crosses" = gentle character
- Object interaction with manner: "one paw dabbling in water" = playful personality
- Color temperature coherence: "soft dappled light" not just "warm sunlight"

**Hurts (camera choreography over-specification):**
- Detailed camera moves: "slow dolly-in from medium-wide to medium close-up, slightly low angle"
- Over-constraining framing leaves the model no room to make its own (often better) character composition choices

### The v13 vs v14 Evidence

This is the clearest controlled comparison. [TESTED]

**v13 (pre-research, crafted, LOST):** The crafted prompt included heavy camera specification: "slow dolly-in from medium-wide to medium close-up, slightly low angle looking up at bench, shallow depth of field with autumn trees softly blurred behind." No acting chain. Robot is just sitting. Object interaction lacks manner specification. Movement quality unspecified. The camera ate the prompt budget.

**v14 (post-research, research-crafted, WON):** Acting chain present -- character notices pigeon approaching, tilts head with mechanical whir, carefully reaches into bag, extends hand with slow gentle precision. 60-30-10 color encoded. Movement quality specified ("slow gentle precision" = personality). Camera reduced to "slow dolly-in, slightly low angle, shallow depth of field."

Operator feedback on v14: "you can see that one is a craft, the other is more generic." Coherence across the whole frame -- water, butterfly effects, color temperature, motion pacing -- all pulling in the same direction. The acting chain created a "lived-in starting state" before the main beat. [TESTED]

The delta: v14's specificity was about CHARACTER BEHAVIOR, not CAMERA BEHAVIOR. [TESTED]

### The Acting Chain Template

The minimum viable emotional arc for 8-second clips: State A, Trigger, State B. [VERIFIED -- animation industry principle confirmed in AI testing]

Structure: "[Character in initial state]. [Trigger event occurs]. [Processing beat -- visible thinking]. [New emotional state with specific physical indicators]."

Examples of effective chains:
- "Calm, sees something, alarmed"
- "Excited, realizes mistake, deflated"
- "Bored, gets idea, energized"

The processing beat is critical. Between stimulus and response, include visible thinking -- a pause, a blink, a held breath. Without it, emotional transitions read as mechanical jump-cuts. [VERIFIED -- animation research; TESTED in v14, v16]

### The Five-Layer Completeness Test

Before finalizing a character emotion prompt, verify five layers are present. [VERIFIED -- from character design research, applied successfully in v14+]

1. Body state? (posture, weight, tension)
2. Movement quality? (speed, weight, directness)
3. Hands/gesture? (what they are doing and how)
4. Face? (specific physical indicators, not labels)
5. Change/arc? (something happens, something shifts)

### Cross-Register Confirmation

The acting-chain advantage holds across registers. [TESTED -- directional]

- **Anime:** Crafted 3-0 (v11, v12, v16). Acting-chain and physical-descriptor specificity consistently win.
- **Pixar:** v13 (camera-heavy crafted) lost; v14 (acting-chain crafted) won. The variable was specificity TYPE, not amount.
- **Cartoon:** v17 crafted win (bias-controlled).
- **Photoreal humans:** v18 research-crafted win. Acting chain + imperfection prompting confirmed for human characters on Kling AI.

### Micro-Expression Transfer to Photoreal

The physical-descriptor approach transfers from stylized to photoreal humans and becomes MORE important. [VERIFIED -- photoreal humans research + v18 test]

Instead of: "He looks scared"
Use: "He bursts into wild laughter, head thrown back. Mid-laugh, he stops, eyes widening in terror, then whispers softly: 'Did you hear that?'"

Effective micro-expression prompts: "A blink of hesitation," "a micro-expression of doubt," "an almost invisible quiver of a lip," "eyes narrowing slightly." Micro-expressions last under 0.5 seconds with very small amplitudes -- prompting must be precise about the physical movement, not the emotional label. [VERIFIED]

### Why Camera Over-Specification Hurts

The model allocates attention across all prompt elements. Camera specification competes with character specification for that attention budget. When camera moves are over-specified, the model prioritizes satisfying the camera constraint over producing coherent character behavior. Additionally, the model's own composition choices are often superior to prompted framing -- particularly for character subjects where it has strong priors from training data. [THEORETICAL -- inferred from v13 vs v14 and Veo documentation on 150-300 character sweet spot]

### The Rule

The model is the cinematographer. You are the acting director. Spend prompt tokens on what the character DOES, FEELS (physically), and HOW they move. Keep camera to 1-2 simple descriptors. [TESTED]

---

## Operational Rules

1. **When writing character prompts:** Allocate the majority of prompt tokens to acting chains (stimulus, processing beat, response), physical-descriptor emotions, and movement quality. Maximum 1-2 camera descriptors.

2. **When specifying camera:** Use at most "medium close-up, shallow depth of field" or equivalent. Never specify dolly speeds, angle transitions, or multi-phase camera movements.

3. **When describing character emotion:** Use the five-layer test: body state, movement quality, hands/gesture, face (physical not abstract), change/arc. If any layer is missing, add it before adding camera detail.

4. **When transitioning from pre-research to post-research craft:** The shift is from camera-budget prompts to acting-budget prompts. Same total specificity, redirected target.

5. **When evaluating whether a prompt is "crafted":** Count how many tokens describe character behavior vs camera behavior. If camera tokens exceed character tokens, the prompt is mis-allocated.

6. **When the model produces unexpectedly poor character output from a detailed prompt:** Check for camera over-specification first. It is the most common cause of "detailed but generic" character output.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/character_design_acting_research.md` | Acting chain template, five-layer completeness test, movement quality framework, object interaction patterns, Veo character-specific patterns |
| `memory/feedback-character-prompt-specificity.md` | v13 vs v14 evidence, acting-chain helps / camera hurts finding, the acting-director rule, /animate restraint finding |
| `memory/project-curriculum-elements.md` | v11-v17 test record showing cross-register confirmation, beat-count limit, score tallies |

---

## Related Concepts

- [[character-design-prompting]] -- The full character design framework (shape language, color, silhouette) that acting chains sit within
- [[prompting-craft-depth]] -- Acting chains are what "craft depth" means for character prompts; camera over-specification is craft depth misdirected
- [[ab-test-results]] -- v13 vs v14 is the canonical evidence; see full test record
- [[narrative-coherence]] -- Acting chains enforce narrative coherence by grounding characters in cause-and-effect
- [[animate-pipeline-findings]] -- /animate adds value through restraint, which includes camera restraint

---

## Deep Reference

- **When** writing an acting chain and need the five-layer template → **read** `research-data/character_design_acting_research.md` [SOURCE FORMAT: conversation JSON — search for "acting chain" and "five-layer"] **for** the stimulus-processing-response sequence structure, the micro-expression dictionary (physical descriptors mapped to emotions: "whiskers twitch" not "looks curious"), movement quality framework, and object interaction patterns that reveal personality
- **When** deciding how many camera descriptors to include in a character prompt → **read** `memory/feedback-character-prompt-specificity.md` (full file) **for** the maximum-two rule ("medium close-up, shallow depth of field" = enough), the v14 operator quote ("you can see that one is a craft, the other is more generic"), and the finding that model composition choices are often better than specified ones
- **When** evaluating whether the acting-chain finding holds across registers → **read** `memory/project-curriculum-elements.md` §(Element 3 — Stylized characters) **for** cross-register confirmation (anime 3-0, Pixar 1-1, cartoon 1-0), the v16 narrative-coherence reinforcement in stylized work, and the 150-300 character Veo prompt sweet spot that creates the budget constraint forcing camera vs acting allocation

---

## Open Questions

- At what level of camera simplicity does output start to degrade? Is "medium close-up" the sweet spot, or would even less (no camera descriptor at all) be better?
- Does this finding hold for non-character subjects? (e.g., would camera over-specification also hurt photoreal environment prompts?)
- The 150-300 character Veo sweet spot may explain WHY camera and acting compete -- in a constrained token budget, allocation matters more. Does this change for models with larger effective prompt windows?
- Physical-descriptor micro-expressions at under 0.5 seconds -- does the model actually render these in 8-second clips, or does it interpret them as general mood?
