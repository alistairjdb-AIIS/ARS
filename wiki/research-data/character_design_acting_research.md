# Character Design & Acting for AI Video Prompting

**Synthesized from 4 parallel research tracks, April 2026.**
**Consumer:** Agent crafting character prompts for Veo 3.1 (and similar text-to-video models).

---

## Part 1: Character Design Fundamentals

### Shape Language — The First Read

| Shape | Communicates | Prompt Language |
|-------|-------------|-----------------|
| **Circles/Rounds** | Friendly, warm, innocent | "round face, soft rounded features, plump build, circular head shape" |
| **Squares/Rectangles** | Stable, strong, dependable | "broad-shouldered, blocky build, square jaw, stocky frame" |
| **Triangles/Angles** | Threatening, cunning, dynamic | "sharp angular features, pointed chin, narrow eyes, lean angular build" |

Most characters combine: dominant shape (first read) + secondary shape (nuance). A hero = square + round (strong + likable). A villain = triangle + square (threatening + formidable).

**Prompt application:** Don't write "circle-based character." Write the physical traits that produce circular reads: "round cheeks, wide eyes, soft body." The model translates physical description into shape language automatically.

### Silhouette — Readability at Small Scale

Instagram Reels: characters viewed at ~2-3 inches tall on phone. Silhouette-defining features matter more than texture details.

**What survives small screens:**
- Distinctive hair/headwear (the #1 silhouette differentiator)
- Exaggerated body proportions (chibi or heroic)
- High-contrast character vs background
- Simplified shapes (90% of successful mobile game characters use round, simple shapes)
- Strong pose/gesture
- Asymmetric design elements

**Checklist before finalizing a character prompt:**
1. Would this character be recognizable as a solid black shape?
2. Does the color palette separate from the background?
3. Fewer than 5 major visual elements?
4. Is head-to-body ratio intentional?
5. Does dominant shape match personality?

### Proportion Systems (Head Count / Toushin)

| Heads Tall | Perceived As | Prompt Language |
|------------|-------------|-----------------|
| 2-3 | Maximum cuteness, chibi | "tiny chibi character, oversized head, stubby body" |
| 3-4 | Child-like, innocent | "childlike proportions, large head relative to body" |
| 5-6 | Teenager, youthful | "teenage proportions, youthful build" |
| 6-7 | Standard adult (most anime) | "adult proportions" (default) |
| 8+ | Heroic, idealized | "tall heroic proportions, elongated legs" |

**Cuteness mechanism:** Larger head relative to body = younger/cuter (biological baby schema). Works across species.

**Prompt tip:** Name the style directly ("chibi style") or describe the ratio ("oversized round head on a tiny body"). Specifying age as proxy: "a 5-year-old child" automatically triggers child proportions.

### Color as Personality — The 60-30-10 Rule

| Role | Purpose | Example |
|------|---------|---------|
| 60% Dominant | Main personality read, what audiences remember | Blue hooded cloak (trustworthy) |
| 30% Secondary | Depth, contrast, complexity | White accents (pure) |
| 10% Accent | Eye-catching detail, signature element | Gold trim (noble) |

**Color personality mappings:**
- Red = passion/anger/power
- Blue = calm/trustworthy/sad
- Yellow = joy/optimism/energy
- Green = nature/envy/renewal
- Purple = royalty/mystery/magic
- Orange = enthusiasm/adventure

**Temperature:** Warm character on cool background = character stands out, feels present. Cool character on warm background = isolated, different.

**Saturation:** High = bold/youthful. Medium = balanced/mature. Low/muted = tired/complex/morally grey.

**Prompt tip:** Name specific colors ("cobalt blue hooded cloak" not "blue character"). Describe what the color is on. Use character-to-background contrast intentionally.

---

## Part 2: Character Acting & Expression

### The Core Chain: Thinking → Emotion → Action

All physical action results from thinking. Structure prompts as cognitive sequences, not static descriptions.

**Instead of:** "a woman picks up a letter"
**Write:** "a woman notices a letter on the table, her expression shifts from curiosity to dread as she reaches for it"

### The Single-Transition Arc (Optimal for 8 Seconds)

**State A → Trigger → State B**

This is the minimum viable emotional arc for short-form:
- "Calm → sees something → alarmed"
- "Excited → realizes mistake → deflated"
- "Bored → gets idea → energized"

**The processing beat is critical:** Between stimulus and response, include visible thinking — a pause, a blink, a held breath. Without it, emotional transitions read as mechanical jump-cuts.

**Template:** "[Character in initial state]. [Trigger event occurs]. [Processing beat — visible thinking]. [New emotional state with specific physical indicators]."

### Granularity Spectrum — Always Go Physical, Not Abstract

| Level | Example | Quality |
|-------|---------|---------|
| Abstract label | "sad" | Model's generic default |
| Body-level | "shoulders slumped, eyes downcast" | Physical targets to render |
| Micro-action sequence | "her hand trembles as she reaches out, then pulls back" | Temporal arc with weight |
| Full cluster | "sitting alone, shoulders curved inward, one hand loosely holding an empty cup, staring at nothing" | Complete scene the model can reconstruct |

**Sweet spot for Veo 3.1:** Micro-action sequence and full cluster levels.

### Emotion-to-Physical Dictionary (Prompt-Ready)

**Joy:** Open posture, chest lifted, wide genuine smile reaching eyes, bouncy movement, arms spreading wide, increased energy.

**Sadness:** Slumped shoulders, curved spine, eyes downcast or distant, slow heavy movements, hands limp or clutching self, shallow breathing.

**Anger:** Clenched fists, stiff posture, shoulders raised, jaw tight, nostrils flared, narrowed eyes fixed on target, sharp aggressive gestures.

**Fear:** Wide eyes, pulled-back posture, rigid body, hands raised defensively, shallow breathing, frozen stillness or backing away.

**Confidence:** Chin raised, shoulders back and down, chest forward, smooth deliberate movements, taking up space, steady gaze.

**Anxiety:** Fidgeting (ring-turning, hair-touching, pen-tapping), avoiding eye contact, hunched shoulders, shallow rapid breathing, self-touching gestures.

**Relief:** Full exhale, shoulders dropping, eyes closing momentarily, body loosening, head tilting back, hand to chest.

**Determination:** Forward lean, set jaw, narrowed focused eyes, hands balling into fists then releasing, one step forward.

**Longing/Nostalgia:** Distant gaze, hand reaching out then pulling back, gentle smile with sad eyes, fingers touching a meaningful object.

### Movement Quality as Personality (Laban-Derived)

Don't name the theory. Describe the physical result:

| Movement Quality | Character Read | Prompt Language |
|-----------------|----------------|-----------------|
| Fast + Light + Indirect | Playful, distracted | "She flits around the room, fingers trailing along surfaces, never settling" |
| Strong + Sudden + Direct | Decisive, dangerous | "He crosses the room in three decisive strides, plants his hands on the desk" |
| Light + Sustained + Indirect | Dreamy, ethereal | "She drifts through the space, gaze wandering, fingers trailing along the bookshelf" |
| Strong + Sustained + Direct | Immovable, resolute | "He stands planted, hands flat on the table, leaning forward, not blinking" |

### Object Interaction — The Personality Revealer

The HOW of handling objects reveals character more than dialogue:

| Emotion | Coffee Cup | Phone | Letter |
|---------|-----------|-------|--------|
| Gentle/Careful | Cradles in both hands, sips slowly | Holds delicately, scrolls carefully | Opens carefully along the seam |
| Aggressive | Grabs it, slams it down | Jabs the screen, grips tight | Tears it open |
| Anxious | Turns it in circles, never drinks | Checks repeatedly, flips over | Holds without opening, turns it |
| Distracted | Holds forgotten, tilted | Leaves face-down on table | Sets aside unopened |

**Prompt pattern:** "[Character] [holds/grips/cradles/fidgets with] [object], [specific manner that reveals emotion]"

### Miyazaki's "Ma" — The Power of Pause

In 8 seconds, a 1-2 second pause carries enormous weight. "She stares out the rain-streaked window, fingers resting on the glass, breathing slowly" is a complete scene. The absence of action IS the acting.

### The Five-Layer Completeness Test

Before finalizing a character emotion prompt:

1. **Body state?** (posture, weight, tension)
2. **Movement quality?** (speed, weight, directness)
3. **Hands/gesture?** (what they're doing and how)
4. **Face?** (specific indicators, not labels)
5. **Change/arc?** (something happens, something shifts)

---

## Part 3: Anime Visual Language

### Color as Emotional Grammar

Anime uses color shifts to encode mood, not just represent physical light. The same room can be warm orange (happy) or desaturated blue-grey (sad).

| Mood | Prompt Language |
|------|----------------|
| Melancholic | "desaturated blue-violet palette, cool color grading, muted highlights" |
| Energetic | "warm orange-gold color grading, high saturation, vibrant warm tones" |
| Serene | "soft pastel green palette, gentle white highlights, low contrast" |
| Nostalgic | "warm amber color grading, slightly faded tones, nostalgic golden light" |
| Magical | "mystical purple palette with cyan accents, glowing highlights" |

**Critical:** "Anime style" alone produces generic results. Specify the register:
- `retro anime screencap, cel-shaded, VHS color palette` = 90s
- `Makoto Shinkai style, dramatic sky, volumetric lighting` = modern photorealistic-background
- `Studio Ghibli style, soft watercolor warmth, hand-painted backgrounds` = painterly

### Anime Sub-Register Triggers

| Register | Key Visual Markers | Prompt Triggers |
|----------|-------------------|-----------------|
| **Shonen** | Sharp angular eyes, bold lines, high saturation | "shonen anime, bold sharp lines, dynamic pose, intense eyes" |
| **Seinen** | Smaller realistic eyes, detailed lines, muted palette | "seinen anime, realistic proportions, muted palette, fine detail" |
| **Shojo** | Very large sparkling eyes, thin lines, pastels | "shojo anime, large sparkling eyes, delicate lines, soft pastels" |
| **Slice-of-Life** | Natural eyes, clean medium lines, muted naturalistic | "slice-of-life anime, natural proportions, muted warm palette" |
| **Moe** | Oversized round eyes, soft rounded lines, candy pastels | "moe anime, large round sparkling eyes, soft features, pastel colors" |

**Eye design is the #1 register signal.** Specifying eye style often triggers the broader register automatically.

### Anime Framing Grammar

| Convention | Prompt Language |
|-----------|----------------|
| Dramatic low angle | "low angle shot, camera looking up, dramatic perspective, imposing" |
| Contemplative wide | "extreme wide shot, character small in frame, vast landscape" |
| Pillow shot (cutaway) | "static wide shot of [environmental detail], held composition, no character" |
| Dutch angle | "Dutch angle, tilted camera, canted frame, disorienting" |
| Half-face shadow | "split lighting, one side illuminated one side dark" |

**Key insight:** Anime favors static compositions with cuts, not continuous camera movement. A held shot that suddenly moves is more "anime" than smooth tracking.

### Anime Motion — What Translates to AI Video

**Works well:** Wind-on-hair/clothing, slow pans across detailed scenes, stillness-to-movement contrast, general speed/dynamism.

**Does NOT work (editing, not generation):** Smear frames, impact frame insertion, framerate modulation, speed line overlays (inconsistent).

**Stillness as technique:** "Character standing still, hair flowing in wind, clothes rippling" — the static-character-with-environmental-movement is a signature anime technique and renders reliably.

### Anime Lighting Toolkit

| Technique | Prompt Language | Reliability |
|-----------|----------------|-------------|
| Rim lighting | "rim lighting, edge light on character, bright outline glow" | VERY HIGH |
| Dramatic backlighting | "dramatic backlighting, character silhouette against bright light" | VERY HIGH |
| Anime glow / bloom | "soft bloom on skin, gentle glow effect, warm bloom lighting" | HIGH |
| Neon on wet surfaces | "neon reflections on wet pavement, colored light in puddles" | VERY HIGH |
| Dappled light (komorebi) | "sunlight filtering through tree canopy, dappled light and shadow" | HIGH |
| Chiaroscuro | "high contrast light and shadow, dramatic shadow, stark illumination" | HIGH |

**Shadow color rule:** Anime shadows are never black. Use "colored shadows, blue-tinted shadow areas, no pure black shadows."

### Director-Specific Style Anchors

| Director/Studio | Use For | Key Prompt Elements |
|----------------|---------|---------------------|
| **Shinkai** | Atmospheric/romantic | Volumetric clouds, god rays, golden hour, lens flare, rain detail |
| **Ghibli** | Pastoral/whimsical | Watercolor warmth, hand-painted backgrounds, lived-in environments, wind through grass |
| **Cyberpunk anime** | Urban/night/neon | Neon-soaked streets, rain through neon, vertical density, steam, wet reflections |
| **Violet Evergarden** | Beautiful naturalistic | Soft golden natural light, delicate bloom |

---

## Part 4: Veo 3.1 Character-Specific Patterns

### Official Prompt Framework

Google's 5-part structure: **[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]**

**Optimal prompt length: 150-300 characters.** Below 100 = generic. Above 400 = model prioritizes unpredictably.

### Character Description — Front-Load It

Place character description BEFORE environment. Models weight earlier tokens more heavily.

**Character "DNA" template (reuse verbatim across shots):**
- Age/build: [specific]
- Face: [2-3 distinctive features]
- Hair: [specific cut, color, texture]
- Clothing: [exact outfit]
- Distinguishing accessory: [one anchor item]

### Breaking "Model Face" (Generic AI Look)

1. **Micro-expressions over emotion labels:** "Eyes squint thoughtfully, slight smile forming" not "looks happy"
2. **Component-level face description:** "Sharp cheekbones, thin scar across left eyebrow" not "attractive woman"
3. **Film grain/texture:** "slightly grainy, film-like quality" pushes away from too-clean AI aesthetic
4. **Visual identifiers:** "The woman in the red dress" not character names

### Known Failure Modes

| Failure | Severity | Mitigation |
|---------|----------|------------|
| Hand morphing | Severe | Describe "anatomically correct hands with five distinct fingers" or hide hands in framing |
| Face drift over time | Moderate-severe | Use reference images; lock character description verbatim |
| Proportion shift mid-clip | Moderate | Shorter clips (3-4s) chain better than 8s for complex motion |
| Temporal coherence collapse (3-7s) | Moderate | Error accumulation follows power law; quality drops 3-7s then plateaus |

### Consistency Techniques

1. **Reference images** (Ingredients to Video): Upload 2-3 angles of same character in neutral lighting
2. **Repeat character description verbatim** across shots — even small wording changes cause drift
3. **Limit motion complexity** — subtle movements maintain consistency far better than full-body action
4. **Lock the background** — stable background lets model focus on character
5. **Shorter clips, chained** — temporal attention caps at ~5 seconds

### Positive-Direction Prompting (Veo Has No Negative Prompt Field)

| Instead of (negative) | Use (positive) |
|----------------------|----------------|
| "no deformed hands" | "anatomically correct hands with five distinct fingers" |
| "no plastic skin" | "natural skin texture with pores and subtle imperfections" |
| "no dead eyes" | "eyes with natural light reflection and subtle moisture" |
| "no generic face" | "distinctive face with [specific feature], [specific feature]" |

### Style Impact on Character Quality

- **Pixar/3D:** Most consistent — strong model priors for 3D character geometry
- **Ghibli/watercolor:** More expressive but less anatomically stable; painterly quality forgives drift
- **Anime:** Strong face priors (large eyes, simplified features) but body proportions can drift
- **Photorealistic:** Highest ceiling but hardest to maintain — uncanny valley most visible

### Character vs Environment Attention Balance

- Front-load character description (before environment)
- Keep environment to 3-5 elements maximum when character is the focus
- When changing environment across shots, keep character description identical
- Reference images offload character identity so text prompt can focus on environment/action

---

## Part 5: Prompt Architecture — Putting It All Together

### The Optimal Character Prompt Template

```
[STYLE + register] + [CAMERA] + [CHARACTER: build + silhouette features + face + color palette] + [MOVEMENT QUALITY + ACTION: stimulus → processing → response] + [ENVIRONMENT: 3-5 elements max] + [LIGHTING/MOOD]
```

### Example — Applying All Research

**Before research (our v13 crafted prompt):**
> "Cinematography: slow dolly-in from medium-wide to medium close-up, slightly low angle looking up at bench, shallow depth of field with autumn trees softly blurred behind. Subject: small humanoid robot with a rounded dented metal body, mismatched bolts, one slightly flickering eye-light, seated on a worn wooden park bench with peeling green paint..."

**After research — what would change:**
1. **Shape language encoded:** "rounded body" is good (friendly), but could add secondary shape for interest
2. **Silhouette thinking:** Robot's distinctive feature (flickering eye-light) IS a good silhouette element
3. **Color 60-30-10:** Could be more intentional — what's the dominant/secondary/accent?
4. **Acting chain missing:** No stimulus → processing → response arc. Robot is just sitting.
5. **Object interaction underleveraged:** "tosses breadcrumb" is good but HOW reveals personality — gently? hesitantly? precisely?
6. **Movement quality unspecified:** Is the robot's movement jerky-mechanical or smooth-gentle? This IS its personality.
7. **Processing beat absent:** No visible thinking before the action.

**Revised prompt applying research:**
> "3D Pixar-style animation. Slow dolly-in, slightly low angle, shallow depth of field. A small round-bodied robot — matte white panels (60%), soft grey joints (30%), warm amber eye-light (10%) — sits on a weathered green park bench. It notices a pigeon approaching, tilts its head with a soft mechanical whir, then carefully reaches into a paper bag, pulls out a crumb, and extends its hand with slow gentle precision. The pigeon hops closer, pecks the crumb. The robot's eye-light brightens. Golden hour through autumn maples, leaves drifting."

**What changed:**
- 60-30-10 color encoded
- Acting chain: notices → processes (head tilt) → acts (reaches) → responds (eye brightens)
- Movement quality specified: "slow gentle precision" = personality
- Object interaction with manner: "carefully reaches," "extends with slow gentle precision"
- Tighter — under 400 chars of content
- Environment reduced to essentials (3 elements: bench, golden hour, autumn maples)

---

## Falsifiability & Limitations

**Untested hypotheses (need A/B verification):**
- Physical-descriptor prompts ("shoulders hunched") vs abstract labels ("sad") — theoretically strong, empirically unconfirmed for Veo specifically
- Laban movement quality descriptors — may or may not produce different outputs than simpler speed/weight words
- Processing beat in 8-second clips — model may compress it out
- Shape language in prompts — does "round-bodied" actually produce friendlier-reading characters than unspecified?

**Confirmed (official docs + community convergence):**
- Micro-action sequences > emotion labels (Google's own Veo 3.1 guide)
- Front-loading character description improves adherence
- 150-300 character sweet spot for Veo
- Style-register specificity (naming sub-register vs generic "anime") produces differentiated output
- Detailed character descriptions improve frame-to-frame consistency

**Shared assumptions across all sources:**
- Shape language associations (circles=friendly) are Western-culture-weighted
- AI models internalize design principles from training data statistically, not explicitly
- Proportion control through prompts is approximate, not precise

---

## Sources

Full source lists in individual research files. Key authoritative sources:
- Google DeepMind Veo Prompt Guide (official)
- Google Cloud Veo 3.1 Prompting Guide (official)
- Ed Hooks, "Acting for Animators" (industry standard)
- Frank Thomas & Ollie Johnston, "The Illusion of Life" (Disney 12 principles)
- Paul Ekman micro-expression research (peer-reviewed)
- Rudolf Laban Movement Analysis (established framework)
- Animation Mentor professional tutorials
- GitHub snubroot/Veo-3-Prompting-Guide (community, widely adopted)
- Sakugabooru analysis (anime production analysis)
- MIT CSAIL hand anatomy study (peer-reviewed)
