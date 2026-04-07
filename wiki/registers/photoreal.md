# Photoreal Human Video Register (R04)

> The photoreal register covers photorealistic human generation in AI video — the highest-ceiling, hardest-to-maintain register, where narrative coherence is the primary judgment axis, a single "too perfect" element can veto an otherwise superior output, and imperfection prompting is the core technique for breaking the AI face.

**Confidence:** HIGH (principles confirmed across multiple A/B tests; tool selection confirmed; failure taxonomy is comprehensive)
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 4 memory files

---

## Core Findings

### Primary Judgment Axis: Narrative Coherence

The primary axis for judging photoreal output is: **does the scene tell ONE consistent physical story where all elements agree on conditions?** [TESTED — operator-surfaced on v10, reinforced on v16]

**The principle:** If it just rained, then no direct sun. If it's cold, then breath/frost visible. If summer, then no frost. Every element in the frame must participate in the same physical story. [TESTED]

**How this emerged:** On v10 (tulip macro), crafted-A told a coherent story (cold + moist + no direct sun = just rained). Terse-B had technical polish but mixed narrative signals (bright sun + heavy dew + summer light + cold-morning droplets — physically inconsistent). The operator identified narrative coherence as the deciding factor, not prompt depth. [TESTED]

**Application:**
- When crafting prompts: specify conditions that FORCE coexistence (if rain → no direct sun; if cold → breath/frost visible) [TESTED]
- When judging outputs: ask "could this moment exist in one real world?" Elements contradicting (bright sun + heavy dew, golden hour + full fog) = technically composed but narratively broken [TESTED]
- The model has no narrative enforcer — the prompt writer is the narrative enforcer [TESTED]

**Prompt-depth is a proxy, not the cause.** After N=8 A/B tests, prompt depth was retired as the primary test variable. Crafted prompts sometimes enforce element coexistence; terse prompts sometimes produce coherent atmosphere. The driving variable is whether the output's elements tell one physical story. [TESTED]

### The Too-Perfect Veto (Binary)

One too-symmetric / too-clean element can veto an otherwise superior output. The veto is an output property, not a prompt-depth property. [TESTED — confirmed across v2, v3, v8, v10]

**Evidence chain:** [TESTED]
- **v8-A (crafted, honey):** "every other element on A is better... I would have bought that honey" but perfectly-round spreading pattern vetoed it. ONE tell, ONE veto.
- **v10-B (terse, tulip):** "B looks sort of too good... too perfect and when it's too perfect, it's not realistic."
- **v3 (terse won):** "B looks a bit more real as it's less perfect"
- **v2 (crafted won):** "B's steam more natural with one weird direction where it goes in a split-second wrong way" — the imperfection was the deciding evidence of realism.

**Prompt-writing implications — avoid perfectionist language:** [TESTED]
- Do NOT use: "flawlessly," "perfectly uniform," "evenly spaced," "smoothly symmetric"
- Do NOT use deterministic fluid specs: "smooth viscous stream," "slowly spreading," "steady pour" (invites too-clean execution)
- Do NOT lock motion/physics to a specific geometric outcome
- DO use variance language: "irregular," "natural imperfection," "slight deviations," "one-off variations"
- DO use loose motion specs: "slow drip" instead of "viscous stream"; "breeze" instead of "laminar air current"

**Judgment application:** Don't average a too-perfect tell against strengths. The tell is binary — one too-symmetric element vetoes regardless of aggregate quality. Crafted prompts are at higher tell-risk because they over-specify. [TESTED]

### Sub-Registers / Taxonomy

The photoreal register doesn't have named sub-styles like anime. Instead, it varies along these axes:

**By subject complexity:** [VERIFIED — photoreal_humans_research]
| Subject | Difficulty | Why |
|---|---|---|
| Objects/environments | Moderate | No uncanny valley; physics is the main challenge |
| Distant human figures | Moderate | Small-scale forgives face/hand artifacts |
| Human medium shots | Hard | Face visible but hands manageable |
| Human close-ups | Very Hard | Uncanny valley maximally triggered |
| Speaking close-ups | Hardest | Lip sync + face consistency + temporal coherence |

**By scene type (from A/B test results):** [TESTED — directional]
- Scene-population scenes (architecture, still-life) favor crafted prompts
- Controlled close-ups / motion-primary / interior favor terse prompts
- This pattern is directional, not confirmed at high N

### Uncanny Valley Taxonomy

Human perception detects facial violations within 40-60 milliseconds. The triggers: [VERIFIED — peer-reviewed research + community convergence]

**Perceptual mismatch:** Different parts of the face at different levels of realism (realistic eyes + synthetic skin, natural skin + lifeless eyes). The brain doesn't process "almost human" as "close to human" — it processes it as "something wrong with this human." [VERIFIED — PMC research]

**Emotion depth deficit:** Missing the coordinated movement of 43 facial muscles. AI faces lack micro-expression depth, appearing "cold or soulless." [VERIFIED — community + theoretical]

**The familiarity penalty:** Uncanny valley deepens for FAMILIAR activities (eating, speaking, laughing). Activities we've observed millions of times expose limitations more than novel movements. Close-up dialogue fails where distant landscape figures pass. [VERIFIED — community]

**Evolutionary basis:** Discomfort may be an evolved pathogen-avoidance mechanism — facial anomalies historically signaled disease. [VERIFIED — peer-reviewed research]

### Prompting Patterns

#### Imperfection Prompting (Core Technique)

"Perfection triggers the uncanny valley while imperfection creates realism." [VERIFIED — strongly convergent across sources]

**Specific imperfection descriptors that work:** [VERIFIED — community + tested in v18]
- "Light freckles across the nose bridge"
- "Faint laugh lines" / "Deep wrinkles around eyes and mouth" (age-appropriate)
- "A small scar on the left cheek"
- "Slightly messy eyebrows"
- "Natural redness around the nose"
- "Fine facial hair (peach fuzz)"
- "Asymmetric smile"
- "Slightly crooked teeth"
- "Visible pores on forehead and cheeks"
- "Subtle under-eye circles"
- "Age spots on hands and temples" (elderly)
- "Weathered hands with visible veins" (elderly)

**v18 confirmation:** Research-crafted prompt with imperfection prompting (laugh lines, age spots, crooked nose) + acting chain + film grain beat terse for elderly man reading letter. [TESTED]

#### The Film Look

Latent diffusion models denoise — their job is to produce clean output. Film grain is literally noise, so models actively remove it, creating the hyper-clean "AI look." [VERIFIED — Metaphysic.ai technical analysis]

**Effective prompt patterns:** [VERIFIED — community-tested]
- `"Shot on 35mm film camera"`
- `"ISO 400"` or `"ISO 800"` (higher = more grain)
- Film stock names: `"Kodak Portra 400"`, `"Fuji Pro 400H"` (different grain signatures)
- `"Organic grain pattern"`, `"natural film texture"`
- `"Subtle grain, no flicker"` (prevents strobing)
- `"Phone-camera sharpness and compression"` (for UGC-style realism)
- `"Realistic motion blur"`, `"rolling-shutter realism"` (handheld authenticity)

**Critical caveat:** Diffusion models may not render grain authentically — model resolution may be finer than authentic halide grain. Post-production grain overlays may be more reliable. [VERIFIED — Metaphysic.ai]

**Warning from A/B tests:** "35mm film grain" language can produce literal filmstrip artifacts in some models. [TESTED — noted in project-curriculum-elements]

#### Lens and Camera for Portraits

Focal length matters enormously for face rendering: [VERIFIED — photography principles + community AI-tested]

| Focal Length | Effect | Use |
|---|---|---|
| **85mm** | Slight compression, flattering, strong background separation. Portrait standard. | Close-ups. Best for minimizing facial distortion. |
| **50mm** | Human-eye FOV. Natural perspective. | Medium shots, conversational scenes. Versatile default. |
| **135mm** | Maximum compression, extremely flattering, heavy bokeh. | Tight headshots. Risk: too "perfect"/editorial → [[too-perfect-veto]]. |
| **35mm** | Wider FOV, includes environment. Distorts if subject fills frame. | Environmental portraits only. Never for face close-ups. |

**Specific pattern:** `"Shot on 85mm lens, f/1.8, shallow depth of field, soft bokeh background"` outperforms generic `"portrait photo"` descriptors. [VERIFIED — community]

#### Lighting for Human Faces

Soft, diffused lighting minimizes uncanny valley. Harsh directional light exacerbates skin texture problems. [VERIFIED — community + theoretical]

| Lighting Setup | Best For | Prompt Language |
|---|---|---|
| **Soft window light** | Dialogue, naturalistic | `"Soft window light from camera-left, gentle shadow falloff"` |
| **Rembrandt** | Dramatic, emotional | `"Rembrandt lighting, triangular cheek highlight on shadow side"` |
| **Butterfly** | Beauty, aspirational | `"Butterfly lighting, light directly above, shadow under nose"` |
| **Rim/back** | Silhouette, hierarchy | `"Rim lighting, edge definition, separates from background"` |

#### Physical Description Specificity

Google's own Veo guidance: "Descriptions of the subject must be extremely specific, covering age, ethnicity, clothing materials, facial features, and even skin texture." [VERIFIED — Google Vertex AI docs]

**Character bible approach:** Write a complete text document with every visual detail. Reuse verbatim across every prompt for the same character. Most reliable method for multi-shot consistency. [VERIFIED — strongly recommended across multiple guides]

**Must include:**
- Age (specific: "35-year-old" not "middle-aged")
- Ethnicity and skin tone
- Hair: color, length, style, texture
- Eye color and shape
- Distinctive features (freckles, scars, asymmetries)
- Clothing materials and colors (also serves as identity anchor)
- Build and posture
- Emotional state via physical description, not abstract labels

#### Micro-Expression Prompting

Physical-descriptor approach transfers from stylized to photoreal and becomes MORE important: [VERIFIED — character_design_acting_research + photoreal_humans_research converge]

**Instead of:** "He looks scared"
**Use:** "He bursts into wild laughter, head thrown back. Mid-laugh, he stops, eyes widening in terror, then whispers softly: 'Did you hear that?'"

**Effective micro-expression language:** [VERIFIED — community]
- "A blink of hesitation"
- "A micro-expression of doubt"
- "An almost invisible quiver of a lip"
- "Eyes narrowing slightly"
- "Subtle furrow between brows"
- "Catching their breath"

#### Dialogue Syntax (Veo-Specific)

**Critical syntax rule:** Use a colon before quoted dialogue: [VERIFIED — GitHub Veo 3 Prompting Guide]
- CORRECT: `Character says: 'dialogue text'`
- INCORRECT: `Character says 'dialogue text'` (triggers unwanted subtitle generation)

**Best practices:** [VERIFIED]
- Keep dialogue under 8 seconds of natural speech per clip
- Medium shot or close-up showing mouth clearly for best lip-sync
- One speaker per clip stitched in post = highest reliability
- Combine emotion + action + speech for realistic transitions

### A/B Test Results

**Photoreal subjects (v1-v10, N=8):** Terse decisive 4x, Crafted decisive 2x, TIE 2x. [TESTED]

**Photoreal humans (v18-v19, N=2):** Research-crafted 1, /animate-crafted 1, Terse 0. [TESTED]

**Key findings from test history:** [TESTED]
- Prompt-depth (terse vs crafted) is a proxy — narrative coherence is the actual axis (surfaced v10)
- Too-perfect veto fires on BOTH crafted and terse outputs — it's an output property (v2, v3, v8, v10)
- Scene-population scenes favor crafted; controlled close-ups favor terse (directional)
- Imperfection prompting + acting chains + film grain language confirmed for human faces (v18)
- /animate pipeline won on subtle emotional content via restraint (v19)

### Known Failure Modes

**Ranked by severity:** [VERIFIED — photoreal_humans_research comprehensive taxonomy]

| Failure | Severity | Mitigation |
|---|---|---|
| **Uncanny valley (face)** | Critical | Imperfection prompting, medium shots, soft lighting, specific physical descriptors |
| **Hand morphing** | Severe | `"anatomically correct hands with five distinct fingers"` or limit hand visibility via shot framing |
| **Face drift (temporal)** | Moderate-severe | Reference images (2-3 angles), verbatim character description, shorter clips |
| **Dead eyes** | Moderate-severe | Specify gaze direction + catchlights: `"looking directly at camera, soft catchlights in both eyes"` |
| **Skin texture (waxy)** | Moderate | `"natural skin texture, visible pores, natural imperfections"`, soft diffused lighting |
| **Hair physics** | Moderate | Specify hair state explicitly, simpler hairstyles produce fewer artifacts |
| **Teeth/mouth artifacts** | Moderate | Medium shots, keep dialogue short, avoid wide smiles |
| **Body proportion shift** | Moderate | Simple movements, medium/wide shots, shorter clips |
| **Too-perfect veto** | Variable | Strip perfectionist language, allow variance, loose motion specs |
| **Lip sync failure** | Variable | Under 8s dialogue, medium shot showing mouth, one speaker per clip |

**The "AI face" problem:** Models default to conventionally attractive, symmetrical, smooth-skinned faces — a training data artifact where datasets over-represent beauty standards and denoising smooths toward averages. Imperfection prompting is the primary counter. [VERIFIED]

**Age-specific pitfalls:** [VERIFIED]
- Elderly: Models smooth away age markers — must explicitly prompt wrinkles, age spots, skin translucency
- Children: Different face proportions (larger eyes, rounder features), less training data
- Young adults: Easiest category (most training data) but most susceptible to "AI face"

### Tool Selection

**Kling AI > Veo 3.1 for photoreal human faces.** [TESTED — v18 + community convergence]

| Capability | Veo 3.1 | Kling 3.0 | Runway Gen-4.5 |
|---|---|---|---|
| Face photorealism | Strong | **Best-in-class** | Weak (4.3/10 — Curious Refuge) |
| Face consistency (temporal) | Good | **Best** | Good with reference image |
| Character consistency (multi-shot) | Weak | Weak (per-clip independent) | **Best (reference conditioning)** |
| Lip sync | **Best-in-class** | Strong | Untested |
| Native audio | **Yes (joint diffusion)** | No | No |
| Body motion realism | Strong | **Best for dynamic** | Moderate |
| Hand rendering | Moderate | Better than average | Weak ("blobs") |
| Max resolution | **4K** | 1080p | 1080p |
| Clip length | 8s | 10s | 10s |

**Recommendation:** Use Kling for human face work. Use Veo when dialogue/lip-sync or native audio is needed. Use Runway when multi-shot character consistency matters more than per-frame face quality. [TESTED — v18 confirmed Kling for faces; community convergence from Curious Refuge, Magic Hour, LumiChats, AI Journal]

**Architecture explains the ranking:** [VERIFIED-community + research]
- **Kling's 3D VAE** encodes video as spatiotemporal volume — face identity is a continuous trajectory, not per-frame reconstruction. This is WHY faces are stable.
- **Veo's joint audio-visual diffusion** constrains face geometry via lip-sync — you can't drift face proportions without breaking audio alignment. Underappreciated face advantage for talking heads.
- **Runway's A2D hybrid** relies on reference image conditioning for face identity — without a reference, face quality drops significantly. The autoregressive component excels at scene composition and narrative logic, not face fidelity.

**Other tools (lower confidence):** [VERIFIED — community reports]
- Runway Gen-4/4.5: Best character consistency across shots via reference images. See [[runway-gen4]] for full operational guide.
- Hailuo AI: Strong for skin texture detail and facial identity across camera angles
- Seedance 2.0: Best multi-scene narrative capabilities, but global launch paused

**Alternative interpretation:** The consensus that Kling leads for faces may reflect testing methodology bias — most comparisons use single-clip evaluation AND identical prompts across tools. Each model has a different prompt dialect (see §Prompt Dialect Translation below); tool-optimized prompts may shift the ranking. No systematic production-workflow comparison with tool-optimized prompts exists publicly. [THEORETICAL]

### Prompt Dialect Translation

**Critical finding: prompts do NOT transfer between tools.** Each model responds to a different vocabulary and structure. Using identical prompts across tools systematically disadvantages whichever model's dialect is most different. [VERIFIED-research — Prompt-A-Video, NeurIPS]

| Tool | Dialect | Structure | Example |
|---|---|---|---|
| **Kling** | Action/timeline | Beat-marked sequences, concrete physical actions | `"0-4s: she turns, eyes widening. 4-8s: steps back, hand to mouth"` |
| **Veo** | Structured/data-like | Shot-list format, technical specs, sensory detail | Camera + Subject + Action + Context + Style (5-part formula) |
| **Runway** | Force/physics prose | Short sentences, force-reaction language | `"She stumbles back, catching herself on the doorframe"` |

**For A/B testing across tools:** Write the brief once, then translate to each tool's native syntax. Compare outputs on the same INTENT, not the same text. [VERIFIED-research]

**Quality modifiers suppress motion (all tools):** [VERIFIED-research — Prompt-A-Video]
- Image-derived descriptors ("cinematic," "photorealistic," "8K detailed") reduce dynamic degree
- Quality modifiers compete with motion descriptors for model attention
- Strip them from video prompts. Use motion-specific language instead.
- "Steady tracking shot" achieves cinematic feel while preserving motion

### Cross-Cutting Findings (2026-04-07 Research)

#### AI Video Temporal Signature

AI video is NOT "too smooth" — it is **uniformly noisy**. [VERIFIED-research — ReStraV, NeurIPS 2025, Google DeepMind]

- **Real video:** Low average curvature but HIGH variance (long stability stretches with occasional sharp natural changes like scene cuts)
- **AI video:** Higher average curvature but LOW variance (consistently erratic, uniformly jittery)

This means "hold" moments in acting chains mask temporal artifacts rather than eliminating them. Static regions in AI video exhibit subtle frame-to-frame variation from the model regenerating each area independently. Post-production temporal smoothing applied uniformly would make AI video MORE detectable (low variance = more detectable).

#### Character Consistency Costs Motion

Enforcing identity consistency across shots degrades motion naturalness by ~32%. [VERIFIED-research — NVIDIA Video Storyboarding]

- Self-attention Q features encode BOTH motion patterns AND subject identity simultaneously
- Tight consistency without careful management paradoxically increases artifacts (frozen bodies with displaced limbs)
- Framewise attention outperforms cross-frame attention for motion quality

This is architectural, not prompt-fixable. The tradeoff is real: consistency OR motion naturalness, not both at full strength.

#### Concept Bleeding Has a Hard Ceiling

Multi-subject scenes fail at the text encoder compression stage — BEFORE the diffusion model processes them. [VERIFIED-research — Isolated Diffusion Guidance]

- Pre-trained text encoders compress all information into fixed-length representations
- Color specifications and fine-grained attributes bleed most frequently
- SDXL multi-subject: **86-95% failure rate** for complex attribute assignments
- Cannot be fixed by better prompting — it's a text encoder limitation

**Operational takeaway:** For scenes with multiple distinct characters, generate subjects separately and composite, or accept systematic attribute leakage.

#### Skin Tone Bias Mechanism

AI generators don't just "default to lighter skin" — they actively relight darker skin incorrectly. [VERIFIED-research — NeRFFaceLighting]

- Models produce albedo maps biased toward lighter tones and compensate with dimmer lighting for darker-skinned faces
- This is a mathematical ambiguity in the rendering equation, not only a training data problem
- Temporal artifacts will be WORSE for darker skin tones under changing lighting conditions
- Minimum consistency score: 0.4404 (severe worst-case)

**Operational takeaway:** When prompting diverse subjects, expect lighting inconsistency as an additional failure mode. Explicit lighting specification becomes MORE important for darker skin tones.

#### Post-Production vs Prompt Boundary

Professional consensus establishes a clear line: [VERIFIED-community]

**Fix in post-production:**
- Film grain overlays (more controllable than prompt)
- Color grading and correction
- Stabilization and motion smoothing
- Corner artifacts, minor flickering
- Audio design (even audio-generating models rarely produce usable audio)
- Text overlays and graphics, upscaling

**Fix in prompt:**
- Lighting direction and quality
- Camera angle and movement type
- Subject action and emotion
- Narrative coherence (cannot be added in post)
- Physical plausibility of interactions

**Fix in pre-production (neither prompt nor post):**
- Character reference sheets
- Lighting-consistent key frames
- Depth maps and compositional guides
- Style locking via reference images

The shift: treat AI output as **raw footage**, not finished product.

#### Physics Understanding Is Decoupled from Visual Quality

Models use "case-based imitation" for physics — matching the closest training example rather than applying learned physical rules. [VERIFIED-research — Physics-IQ, PhyWorld]

- Out-of-distribution physics errors are **35x higher** than in-distribution
- Scaling up data and model size has "little or negative impact" on reducing physics errors
- Attribute priority: color > size > velocity > shape (models preserve color, distort shapes)
- Specifying physical properties in prompts may be ignored in favor of visual similarity

**Falsifiability:** These findings are from research-era models. Kling 3.0, Veo 3.1, and Runway Gen-4.5 may have improved — but the architectural limitation (case-matching vs. rule-learning) is fundamental.

---

## Operational Rules

1. **Narrative coherence is the primary judgment axis.** Every element must participate in one physical story. The prompt writer is the narrative enforcer. [TESTED]
2. **Apply the too-perfect veto.** Scan for ONE too-symmetric/too-clean element. Don't average it against strengths — the tell is binary. [TESTED]
3. **Strip perfectionist language from prompts.** No "flawlessly," "perfectly uniform," "evenly spaced." Use variance language. [TESTED]
4. **Prompt imperfections, not perfection.** Freckles, asymmetries, pores, natural redness, fine facial hair. [TESTED — v18]
5. **Use physical descriptors, not abstract emotion labels.** "Shoulders slumped, eyes downcast" not "sad." [VERIFIED]
6. **Use Kling AI for human faces, Veo for dialogue/audio, Runway for multi-shot consistency.** [TESTED + VERIFIED]
6b. **Strip quality modifiers from video prompts.** "Cinematic," "photorealistic," "8K" suppress motion. Use motion-specific language. [VERIFIED-research]
6c. **Translate prompts to each tool's native dialect.** Kling = action/timeline, Veo = structured/data-like, Runway = force/physics prose. Same intent, different syntax. [VERIFIED-research]
7. **Prefer medium shots for faces.** Close-ups maximize uncanny valley; medium shots balance expressiveness with artifact avoidance. [VERIFIED]
8. **Use soft, diffused lighting.** Harsh directional light exacerbates skin texture problems. [VERIFIED]
9. **Reuse character description verbatim across shots.** Even small wording changes cause face drift. [VERIFIED]
10. **Keep dialogue under 8 seconds per clip, one speaker per clip.** [VERIFIED]
11. **The model is the cinematographer, you are the acting director.** Camera over-specification hurts; acting-chain specificity helps. [TESTED]
12. **Colon before dialogue in Veo:** `says: 'text'` not `says 'text'`. [VERIFIED]

---

## Deep Reference

- **When** writing Veo prompts specifically → **read** `photoreal_humans_research.md` **for** optimal prompt length (150-300 characters), front-load character description before environment, positive-direction-only prompting (no negative phrasing)
- **When** deciding clip length for complex motion → **read** `photoreal_humans_research.md` §Temporal Coherence **for** coherence collapse at 3-7s + temporal attention cap at ~5s. Keep complex motion clips to 3-4s.
- **When** writing acting chains for character prompts → **read** `character_design_acting_research.md` §Emotion-to-Physical Dictionary **for** full 9-emotion body/posture/gesture lookup table + Laban-derived movement quality taxonomy (fast+light, strong+sudden, etc.)
- **When** pre-checking character prompt completeness → **read** `character_design_acting_research.md` §Five-Layer Completeness Test **for** the 5-layer checklist (body state, movement quality, hands/gesture, face, change/arc)
- **When** matching restraint level to content → **read** `feedback-character-prompt-specificity.md` **for** v20 finding: restraint is NOT default — match to register (subtle→restrained, energetic→rich). /animate pipeline score context.
- **When** prompting dialogue scenes → **read** `photoreal_humans_research.md` §Dialogue **for** emotional monotone warning (flat delivery unless explicitly prompted with physical emotional descriptors) + multi-person handling (speaker order, positioning, visual identifiers)
- **When** packing acting beats → **read** `project-curriculum-elements.md` §Beat Count **for** 2-3 beats max per 8s clip (v15's 5 beats caused fluidity breaks)
- **When** using object interaction for character personality → **read** `character_design_acting_research.md` §Object Interaction **for** how someone handles objects reveals emotion (coffee cup, phone, letter examples)

---

## Practical Prompt Template

Synthesized from all research: [VERIFIED — photoreal_humans_research]

```
[CAMERA] Shot on 85mm lens, f/2.0, shallow depth of field, soft bokeh.
Medium close-up, slight handheld micro-shake.

[CHARACTER] A [specific age]-year-old [ethnicity] [gender] with [hair],
[eye color], [skin detail including imperfections],
wearing [clothing with materials]. [Build/posture].

[FACE] [Physical micro-expression description, not abstract emotion].
[Gaze direction]. [Eye behavior].

[ACTION] [Stimulus → processing beat → response].

[DIALOGUE] [Character] says in [vocal quality]: "[under 8 seconds]"

[LIGHTING] Soft window light from camera-left, gentle shadow falloff,
warm but restrained color grading.

[FILM LOOK] Shot on 35mm film, Kodak Portra 400, subtle grain, no flicker.
Natural skin texture, visible pores. No oversaturation, no artificial glow.

[AUDIO] [Environmental sounds matching the scene].
```

---

## Source Files

| File | Contribution |
|------|-------------|
| `photoreal_humans_research.md` | Uncanny valley taxonomy, failure mode catalog, imperfection prompting, film look, lighting, lens selection, dialogue syntax, competitive model comparison, prompt template |
| `character_design_acting_research.md` | Acting chains, micro-expression dictionary, movement quality, physical-descriptor prompting, Veo character patterns, "model face" breaking techniques |
| `feedback-narrative-coherence.md` | Narrative coherence as primary judgment axis (operator-surfaced v10), element coexistence rule |
| `feedback-too-perfect-veto.md` | Binary veto principle, perfectionist language avoidance, evidence chain (v2, v3, v8, v10) |
| `feedback-character-prompt-specificity.md` | Acting-chain vs camera-choreography finding, restraint principle, /animate pipeline value |
| `project-curriculum-elements.md` | Full A/B test history, score tallies, tool selection evidence, curriculum progression |

---

## Related Concepts

- [[anime]] — Opposite end of difficulty spectrum; anime's strong face priors and simplified features sidestep uncanny valley
- [[pixar-3d]] — Pixar's painterly quality forgives drift that photoreal cannot; "most consistent" register
- [[cartoon-western]] — No overlap in prompting approach; useful as contrast for understanding what photoreal demands
- [[runway-gen4]] — Multi-shot consistency specialist. Weak per-frame face quality but best reference-image workflow.
- [[narrative-coherence]] — The primary judgment axis for this register
- [[too-perfect-veto]] — The binary quality gate for this register
- [[character-design-prompting]] — Acting chains and physical descriptors originate here and are most critical in photoreal
- [[prompting-craft-depth]] — INFORMS: craft-depth A/B tests used photoreal as the primary test register; sub-register patterns (scene-population vs close-up) discovered here

---

## Open Questions

- Does Veo 3.1's claimed <120ms lip sync accuracy hold across diverse prompts and character types? No independent benchmark exists. [VERIFIED claim, UNKNOWN actual performance]
- Does Kling 3.0's face advantage persist in multi-shot production workflows vs. single-clip evaluation? [UNKNOWN]
- Does film grain prompting produce authentic film grain or digital noise at model level? Technical analysis suggests the latter — post-production overlays may be more reliable. [VERIFIED — needs testing]
- What is the actual success rate of micro-expression prompting in video vs. stills? Better studied in stills. [UNKNOWN]
- Does the "character bible" text approach outperform reference-image-based approaches for multi-shot consistency? No controlled comparison exists. [UNKNOWN]
- How does Hailuo AI compare to Kling for face photorealism at scale? Limited testing data. [UNKNOWN]
- Does Runway Gen-4.5 text-to-video match Kling for photoreal human faces? No internal A/B test yet. [UNKNOWN — planned test]
- Does Runway Gen-4 Turbo's reference-image workflow produce better face consistency than Kling 3.0 Elements? [UNKNOWN — planned test]
- Does tool-optimized prompting (translating to each model's dialect) shift the Kling > Veo > Runway ranking? [UNKNOWN — no systematic comparison exists]
- The durable prompting principles (imperfection, physical specificity, lighting, shot framing) are grounded in human perception and should survive model architecture changes. The model rankings will likely shift within 3-6 months. [THEORETICAL — meta-observation from research]
