# Character Design Prompting

> Shape language, silhouette design, acting chains, and color rules that make AI video character prompts produce coherent, personality-rich output instead of generic defaults.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Shape Language -- The First Read

Characters communicate personality through geometric primitives before any detail is read. [VERIFIED -- animation industry standard (Thomas & Johnston, Ed Hooks), confirmed in research synthesis]

| Shape | Communicates | Prompt Language |
|-------|-------------|-----------------|
| Circles/Rounds | Friendly, warm, innocent | "round face, soft rounded features, plump build, circular head shape" |
| Squares/Rectangles | Stable, strong, dependable | "broad-shouldered, blocky build, square jaw, stocky frame" |
| Triangles/Angles | Threatening, cunning, dynamic | "sharp angular features, pointed chin, narrow eyes, lean angular build" |

Most characters combine a dominant shape (first read) with a secondary shape (nuance). A hero = square + round (strong + likable). A villain = triangle + square (threatening + formidable). [VERIFIED]

Do not write "circle-based character." Write the physical traits that produce the shape read: "round cheeks, wide eyes, soft body." The model translates physical description into shape language from its training data. [THEORETICAL]

### Silhouette -- Small-Screen Readability

Instagram Reels characters are viewed at approximately 2-3 inches tall on phone screens. Silhouette-defining features matter more than texture detail. [VERIFIED]

What survives small screens:
- Distinctive hair/headwear (the primary silhouette differentiator)
- Exaggerated body proportions (chibi or heroic)
- High-contrast character vs background
- Simplified shapes (90% of successful mobile game characters use round, simple shapes)
- Strong pose/gesture
- Asymmetric design elements

Silhouette test: Would the character be recognizable as a solid black shape? If not, the design is too dependent on internal detail. [THEORETICAL]

### The 60-30-10 Color Rule

Color encodes personality when applied with intentional ratios. [VERIFIED -- design industry standard]

| Role | Percentage | Purpose |
|------|-----------|---------|
| Dominant | 60% | Main personality read, what audiences remember |
| Secondary | 30% | Depth, contrast, complexity |
| Accent | 10% | Eye-catching detail, signature element |

Name specific colors in prompts ("cobalt blue hooded cloak" not "blue character"). Describe what the color is on. Use character-to-background temperature contrast intentionally: warm character on cool background = character stands out, feels present. [VERIFIED]

Saturation encodes maturity: High = bold/youthful. Medium = balanced/mature. Low/muted = tired/complex/morally grey. [THEORETICAL]

### Acting Chains -- Stimulus, Processing, Response

The single most impactful prompting technique for character work. Structure prompts as cognitive sequences, not static descriptions. [TESTED -- confirmed v14 blind A/B, operator-verified]

**Instead of:** "a woman picks up a letter"
**Write:** "a woman notices a letter on the table, her expression shifts from curiosity to dread as she reaches for it"

The chain has three parts:
1. **Stimulus** -- something happens in the environment
2. **Processing beat** -- visible thinking (a pause, a blink, a held breath, a head tilt). Without this, transitions read as mechanical jump-cuts.
3. **Response** -- physical action with manner that reveals personality

Example from the v14 winning prompt: "ears perk up, freezes, slowly crosses eyes, whiskers twitch, smile spreads." Each beat is a physical descriptor, not an emotion label. [TESTED]

### Physical Descriptors Over Emotion Labels

Always go physical, never abstract. [TESTED -- confirmed across v14, v16, v18]

| Level | Example | Quality |
|-------|---------|---------|
| Abstract label | "sad" | Model's generic default |
| Body-level | "shoulders slumped, eyes downcast" | Physical targets to render |
| Micro-action sequence | "her hand trembles as she reaches out, then pulls back" | Temporal arc with weight |
| Full cluster | "sitting alone, shoulders curved inward, one hand loosely holding an empty cup, staring at nothing" | Complete scene the model can reconstruct |

Sweet spot for Veo 3.1: micro-action sequence and full cluster levels. [VERIFIED -- Google's own Veo 3.1 guide confirms micro-action > labels]

### Movement Quality as Personality

How a character moves IS their personality. Derived from Laban Movement Analysis but never name the theory -- describe the physical result. [THEORETICAL -- Laban framework; TESTED via v14]

| Movement Quality | Character Read | Prompt Language |
|-----------------|----------------|-----------------|
| Fast + Light + Indirect | Playful, distracted | "flits around the room, fingers trailing along surfaces, never settling" |
| Strong + Sudden + Direct | Decisive, dangerous | "crosses the room in three decisive strides, plants hands on the desk" |
| Light + Sustained + Indirect | Dreamy, ethereal | "drifts through the space, gaze wandering, fingers trailing along the bookshelf" |
| Strong + Sustained + Direct | Immovable, resolute | "stands planted, hands flat on the table, leaning forward, not blinking" |

### Camera Choreography HURTS

Detailed camera specification degrades character output. The model makes better composition choices than over-specified camera prompts allow. [TESTED -- v13 crafted lost partly because of camera over-specification; v14 won with acting-chain specificity and minimal camera]

v13 crafted prompt included: "slow dolly-in from medium-wide to medium close-up, slightly low angle." This lost to the terse version.
v14 research-crafted prompt kept camera to minimal descriptors and spent tokens on acting chain instead. This won decisively.

The model is the cinematographer. You are the acting director. [TESTED]

### Object Interaction as Personality Revealer

HOW a character handles objects reveals more than any description. [VERIFIED -- animation principles]

| Emotion | Coffee Cup | Phone | Letter |
|---------|-----------|-------|--------|
| Gentle/Careful | Cradles in both hands, sips slowly | Holds delicately, scrolls carefully | Opens carefully along the seam |
| Aggressive | Grabs it, slams it down | Jabs the screen, grips tight | Tears it open |
| Anxious | Turns it in circles, never drinks | Checks repeatedly, flips over | Holds without opening, turns it |

Prompt pattern: "[Character] [holds/grips/cradles/fidgets with] [object], [specific manner that reveals emotion]" [VERIFIED]

### Beat Count Limit

Approximately 5 acting beats in 8 seconds causes visible scene transitions and fluidity breaks. Limit to 2-3 beats maximum per 8-second clip. [TESTED -- v15 finding]

---

## Operational Rules

1. **When writing character prompts:** Spend prompt tokens on acting chains (stimulus, processing beat, response), physical-descriptor emotions, and movement quality. Keep camera specification to 1-2 simple descriptors maximum ("medium close-up, shallow depth of field"). Let the model choose exact framing.

2. **When specifying color:** Apply the 60-30-10 rule with named colors on named surfaces. Match character color temperature to background for intentional contrast.

3. **When describing emotion:** Never use abstract labels ("sad," "happy," "curious"). Always use physical clusters: posture, hand behavior, facial micro-actions, gaze direction.

4. **When prompting movement:** Specify manner, not just action. "Carefully reaches" and "snatches" produce different characters doing the same physical task.

5. **When targeting mobile screens:** Test the silhouette. Fewer than 5 major visual elements. Head-to-body ratio intentional. Color palette separates from background.

6. **When specifying acting arcs:** Limit to 2-3 beats per 8-second clip. Always include a processing beat between stimulus and response. The pause IS the acting.

7. **When tempted to specify camera moves:** Stop. Reduce camera to at most "medium close-up, shallow depth of field." Redirect those tokens to character behavior specificity.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/character_design_acting_research.md` | Shape language, silhouette, color rule, acting chains, movement quality, object interaction, anime visual language, Veo patterns |
| `memory/feedback-character-prompt-specificity.md` | Acting-chain specificity helps, camera choreography hurts -- confirmed v14 A/B |

---

## Related Concepts

- [[narrative-coherence]] -- Acting chains enforce narrative coherence by making characters react to a consistent physical world
- [[too-perfect-veto]] -- Character outputs can also trigger the too-perfect veto if movement is too smooth/symmetric
- [[prompting-craft-depth]] -- Acting chains are part of what "craft depth" means for character prompts
- [[ab-test-results]] -- v11-v17 test character prompt approaches
- [[acting-chains-beat-camera]] -- The specific finding from this research applied to A/B testing
- [[anime]] — EXTENDS: anime register applies acting chains, color-as-mood, and physical-descriptor prompting from this framework within Japanese animation visual language
- [[cartoon-western]] — EXTENDS: Western cartoon register applies shape language, acting chains, and silhouette principles from this framework to flat-color 2D animation
- [[photoreal]] — EXTENDS: photoreal register applies acting chains, micro-expression prompting, and physical descriptors from this framework where they are most critical due to uncanny valley sensitivity
- [[pixar-3d]] — EXTENDS: Pixar/3D register applies shape language, 60-30-10 color, and acting chains from this framework with the strongest model priors of any stylized register
- [[animate-pipeline-findings]] — INFORMS: /animate pipeline calibrates how much acting-chain specificity to include, balancing restraint vs richness based on content register

---

## Deep Reference

- **When** writing an acting chain for a character prompt and need the stimulus-processing-response template → **read** `research-data/character_design_acting_research.md` §(Acting Chains) **for** the five-layer completeness test, the micro-expression dictionary (physical descriptors mapped to emotions), movement quality framework (Laban-derived speed/weight/flow descriptors), and object interaction patterns that reveal personality
- **When** choosing character proportions and the model output doesn't match intended age/personality → **read** `research-data/character_design_acting_research.md` §(Proportion Systems) **for** the toushin head-count table (2-3 heads = chibi, 6-7 = standard adult, 8+ = heroic), the baby schema cuteness mechanism, and prompt language that triggers specific proportion systems ("chibi style" vs "heroic proportions")
- **When** deciding how much camera direction to include in a character prompt → **read** `memory/feedback-character-prompt-specificity.md` (full file) **for** the v14 A/B evidence that acting-chain specificity helps but camera choreography over-specification hurts, the "be the acting director, not the DP" rule, and the v19 finding that /animate adds value through what it helps leave out
- **When** the model output drifts to the wrong style register (anime when you wanted Pixar, or 3D when you wanted 2D) → **read** `memory/project-curriculum-elements.md` §(Element 3 — Stylized characters) **for** sub-register win patterns (anime 3-0 crafted, Pixar split 1-1, cartoon 1-0 crafted), the beat-count limit (~5 beats in 8s causes scene breaks), and style drift confounds from v15

---

## Open Questions

- Does shape language in prompts ("round-bodied") actually produce friendlier-reading characters vs unspecified? Untested in A/B.
- Do Laban movement quality descriptors produce measurably different outputs than simpler speed/weight words?
- Does the processing beat survive in 8-second clips or does the model compress it out?
- Shape language associations (circles = friendly) are Western-culture-weighted. Transfer to other cultural contexts unknown.
- Proportion control through text prompts is approximate -- how reliable is head-count specification?
