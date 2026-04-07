# Pixar/3D Animation Register (R02)

> The Pixar/3D register covers CG-animated character and environment generation — characterized by controlled exaggeration within physics-plausible bounds, strong shape language, emotional storytelling through acting chains, and the most consistent model priors of any stylized register in current AI video tools.

**Confidence:** MEDIUM (split 1-1 in A/B; crafted prompting helps for acting depth but camera over-specification hurts)
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 2 memory files

---

## Core Findings

### Sub-Registers / Taxonomy

The Pixar/3D register is less internally differentiated than anime or Western cartoon. The primary axis is **exaggeration level**, not named sub-styles:

| Sub-Register | Proportions | Motion Quality | Prompt Anchors |
|---|---|---|---|
| **Feature-film Pixar** | 5-7 heads tall, exaggerated features within anatomy | Smooth ease-in/ease-out, physics-plausible squash-stretch | `"Pixar-style 3D animation, smooth rendering, expressive character"` |
| **Chibi/Cute 3D** | 2-3 heads tall, oversized head | Bouncy, lightweight | `"chibi 3D character, oversized round head, stubby body, cute"` |
| **Heroic 3D** | 8+ heads tall, idealized | Powerful, deliberate | `"tall heroic proportions, elongated legs, dramatic 3D animation"` |
| **Stylized 3D (Arcane-adjacent)** | Realistic proportions, painterly textures | Hybrid 2D/3D feel | `"stylized 3D animation, hand-painted textures, Art Nouveau influences"` |

**Note:** `"Pixar-like 3D animation"` is a strong, high-reliability trigger keyword in AI video models. [VERIFIED — cartoon_animation_styles_research confirms it as a recognized keyword]

### Character Design Principles

**Shape language** drives personality at the design level: [VERIFIED — character_design_acting_research]

| Shape | Communicates | Prompt Language |
|---|---|---|
| Circles/Rounds | Friendly, warm, innocent | `"round face, soft rounded features, plump build, circular head shape"` |
| Squares/Rectangles | Stable, strong, dependable | `"broad-shouldered, blocky build, square jaw, stocky frame"` |
| Triangles/Angles | Threatening, cunning, dynamic | `"sharp angular features, pointed chin, narrow eyes, lean angular build"` |

Most characters combine: dominant shape (first read) + secondary shape (nuance). Hero = square + round (strong + likable). Villain = triangle + square (threatening + formidable). [VERIFIED]

**Don't write shape-theory language.** Write the physical traits: `"round cheeks, wide eyes, soft body"` not `"circle-based character."` The model translates physical description into shape language automatically. [VERIFIED]

**60-30-10 color rule for characters:** [VERIFIED]

| Role | Percentage | Purpose | Example |
|---|---|---|---|
| Dominant | 60% | Main personality read | Blue hooded cloak (trustworthy) |
| Secondary | 30% | Depth, contrast | White accents (pure) |
| Accent | 10% | Eye-catching signature | Gold trim (noble) |

Name specific colors: `"cobalt blue hooded cloak"` not `"blue character."` [VERIFIED]

**Proportion system (head count):** [VERIFIED]

| Heads Tall | Read | Prompt |
|---|---|---|
| 2-3 | Maximum cuteness, chibi | `"tiny chibi character, oversized head, stubby body"` |
| 3-4 | Child-like, innocent | `"childlike proportions, large head relative to body"` |
| 5-6 | Teenager, youthful | `"teenage proportions, youthful build"` |
| 6-7 | Standard adult (default) | `"adult proportions"` |
| 8+ | Heroic, idealized | `"tall heroic proportions, elongated legs"` |

### Prompting Patterns

**The optimal character prompt architecture** (from character_design_acting_research): [VERIFIED]

```
[STYLE + register] + [CAMERA (minimal)] + [CHARACTER: build + silhouette features + face + color palette] + [MOVEMENT QUALITY + ACTION: stimulus → processing → response] + [ENVIRONMENT: 3-5 elements max] + [LIGHTING/MOOD]
```

**Acting chain is the high-leverage investment.** The single-transition arc (State A → Trigger → State B) is the minimum viable emotional arc for 8 seconds: [VERIFIED]

- `"Calm → sees something → alarmed"`
- `"Excited → realizes mistake → deflated"`
- `"Bored → gets idea → energized"`

**The processing beat is critical.** Between stimulus and response, include visible thinking — a pause, a blink, a held breath. Without it, emotional transitions read as mechanical. [VERIFIED]

**Physical descriptors over abstract labels:** [VERIFIED]

| Level | Example | Quality |
|---|---|---|
| Abstract label | "sad" | Model's generic default |
| Body-level | "shoulders slumped, eyes downcast" | Physical targets |
| Micro-action sequence | "hand trembles as she reaches out, then pulls back" | Temporal arc |
| Full cluster | "sitting alone, shoulders curved inward, one hand loosely holding an empty cup, staring at nothing" | Complete scene |

Sweet spot for Veo 3.1: micro-action sequence and full cluster levels. [VERIFIED]

**Object interaction reveals personality:** The HOW of handling objects matters more than what is handled. [VERIFIED]

| Emotion | Coffee Cup | Phone |
|---|---|---|
| Gentle | Cradles in both hands, sips slowly | Holds delicately, scrolls carefully |
| Aggressive | Grabs it, slams it down | Jabs the screen, grips tight |
| Anxious | Turns it in circles, never drinks | Checks repeatedly, flips over |

**Movement quality as personality** (Laban-derived, don't name the theory): [VERIFIED]

| Quality | Character Read | Prompt Language |
|---|---|---|
| Fast + Light + Indirect | Playful, distracted | `"She flits around the room, fingers trailing along surfaces, never settling"` |
| Strong + Sudden + Direct | Decisive, dangerous | `"He crosses the room in three decisive strides, plants his hands on the desk"` |
| Light + Sustained + Indirect | Dreamy, ethereal | `"She drifts through the space, gaze wandering"` |
| Strong + Sustained + Direct | Immovable, resolute | `"He stands planted, hands flat on the table, leaning forward, not blinking"` |

### A/B Test Results

**Pixar sub-register: Split 1-1 (inconclusive at current N).** [TESTED]

| Test | Subject | Result | Key Finding |
|---|---|---|---|
| v13 | Pixar robot | Terse won (pre-research) | Heavy camera choreography in crafted prompt hurt output |
| v14 | Pixar fox | Research-crafted won (post-research) | Acting-chain specificity + physical descriptors + color control succeeded |

**The critical difference between v13 (loss) and v14 (win):** v13's crafted prompt spent tokens on camera specification (`"slow dolly-in from medium-wide to medium close-up, slightly low angle"`). v14 spent tokens on acting-chain behavior (`"ears perk up → freezes → slowly crosses eyes → whiskers twitch → smile spreads"`). The v14 operator feedback: "you can see that one is a craft, the other is more generic." [TESTED]

**Cross-register context:** Across all stylized characters (v11-v17), research-crafted wins 5-1. Pixar's 1-1 split is the weakest signal, suggesting crafted prompting helps LESS in this register than anime (3-0) or cartoon (1-0). [TESTED]

**Hypothesis:** Pixar/3D has the strongest model priors of any stylized register — the model already "knows" 3D character geometry well. Crafted prompting adds value through acting depth, but the baseline is already higher so the delta is smaller. [THEORETICAL — consistent with character_design_acting_research noting "Pixar/3D: Most consistent — strong model priors for 3D character geometry"]

### Known Failure Modes

**Hand morphing (severe):** Describe `"anatomically correct hands with five distinct fingers"` or hide hands in framing. [VERIFIED]

**Face drift over time (moderate-severe):** Use reference images; lock character description verbatim across shots. [VERIFIED]

**Proportion shift mid-clip (moderate):** Shorter clips (3-4s) chain better than 8s for complex motion. [VERIFIED]

**Temporal coherence collapse (moderate):** Error accumulation follows power law; quality drops 3-7s then plateaus. [VERIFIED]

**Camera over-specification hurts:** Detailed camera moves (`"slow dolly-in from medium-wide to medium close-up, slightly low angle"`) leave Veo no room to make its own — often better — composition choices. [TESTED — v13]

**Pixar/3D register exaggeration bounds:** Squash-stretch is present but subtle (within ~20% distortion range). Physics stays plausible. Unlike Western cartoon (extreme distortion) or anime (selective distortion for gags), Pixar maintains anatomy. Prompting for extreme cartoon exaggeration in a Pixar-style prompt will produce unpredictable results. [VERIFIED — cartoon_animation_styles_research exaggeration spectrum]

### Tool Selection

**Veo 3.1** is the primary tool for Pixar/3D. Has the strongest model priors for 3D character geometry of any stylized register. [VERIFIED]

**Kling AI** tested on hybrid Pixar x Pokemon content (v20) — produced usable results but the test was about /animate pipeline, not tool comparison. [TESTED — limited data]

---

## Operational Rules

1. **Spend tokens on acting chains, not camera choreography.** Stimulus → processing beat → response is the high-leverage pattern. Camera: 1-2 simple descriptors max. [TESTED — v13 vs v14 delta]
2. **Encode shape language through physical traits, not theory.** `"round cheeks, wide eyes"` not `"circle-based design."` [VERIFIED]
3. **Apply 60-30-10 color intentionally.** Name specific colors on specific elements. [VERIFIED]
4. **Include the processing beat.** Between stimulus and response, describe visible thinking — a pause, a head tilt, a blink. Without it, transitions read as jump-cuts. [VERIFIED]
5. **Front-load character description before environment.** Keep environment to 3-5 elements max when character is focus. [VERIFIED]
6. **Optimal prompt length: 150-300 characters.** [VERIFIED — Veo official guide]
7. **The model is the cinematographer. You are the acting director.** [TESTED — feedback-character-prompt-specificity]
8. **Limit to 2-3 acting beats per 8 seconds.** [TESTED — v15]

---

## Source Files

| File | Contribution |
|------|-------------|
| `character_design_acting_research.md` | Shape language, proportion systems, color personality, acting chains, movement quality, emotion-to-physical dictionary, Veo 3.1 patterns, style impact ranking |
| `cartoon_animation_styles_research.md` | Exaggeration spectrum comparison (Pixar vs cartoon vs anime), line/color conventions, style drift patterns |
| `project-curriculum-elements.md` | A/B results (v13-v14 split), cross-register scoring, camera-vs-acting finding |
| `feedback-character-prompt-specificity.md` | Acting-chain specificity helps, camera choreography hurts, "be the director not the DP" |

---

## Related Concepts

- [[anime]] — Adjacent register; anime has weaker model priors but stronger crafted-prompt advantage
- [[cartoon-western]] — Pixar shares shape language principles but operates at controlled exaggeration vs cartoon's extreme exaggeration
- [[photoreal]] — Pixar is the furthest from photoreal uncanny valley concerns; painterly quality forgives drift
- [[character-design-prompting]] — All acting chain and shape language principles originate here

---

## Deep Reference

- **When** building a Pixar-style character prompt and need shape language that produces specific personality reads → **read** `research-data/character_design_acting_research.md` [SOURCE FORMAT: conversation JSON — search for "shape language" and "proportion systems"] **for** the shape-to-personality mapping (circles = friendly, squares = stable, triangles = threatening), proportion systems (toushin head-count table), the 60-30-10 color rule, and how dominant + secondary shapes combine (hero = square + round)
- **When** Pixar prompts produce generic output and you suspect model priors are overriding → **read** `memory/project-curriculum-elements.md` §(Element 3 — Stylized characters) **for** the style impact ranking ("Pixar most consistent" = strongest model priors), the v13-v14 split (camera specification lost, acting specificity won), and why Pixar's painterly quality "forgives drift that photoreal cannot"
- **When** deciding whether to specify camera or leave it to the model for Pixar-style output → **read** `memory/feedback-character-prompt-specificity.md` (full file) **for** the v13 evidence (pre-research heavy camera specification lost to terse) vs v14 (post-research acting chain won), confirming that acting chains are the right place to spend prompt tokens for this register

---

## Open Questions

- Why does crafted prompting help less for Pixar than anime? Is it the stronger model priors, or is 1-1 simply insufficient N? [TESTED at N=2, needs more]
- Does the 60-30-10 color rule produce measurably different outputs than unstructured color description? [THEORETICAL — untested via A/B]
- Does Laban movement quality language produce different outputs than simpler speed/weight words? [THEORETICAL — untested]
- Does shape language in prompts (e.g., `"round-bodied"`) actually produce friendlier-reading characters than unspecified? [THEORETICAL — untested]
- Kling AI capability for Pixar/3D register is barely tested. [UNKNOWN at meaningful N]
