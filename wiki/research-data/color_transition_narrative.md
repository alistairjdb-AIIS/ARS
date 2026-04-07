# Color Transitions as Emotional Narrative
## Research Document v1

**Date:** 2026-03-21
**Sources:** 18 web searches, 3 academic sources (Manchester Color Wheel / PMC / PubMed), 8 film/animation industry sources
**Purpose:** Feed brand film color arc design and calculator page emotional design
**Tags:** [VERIFIED] = directly cited in source | [LLM-ESTIMATED] = inferred from multiple consistent sources | [ASSUMED] = no direct evidence

---

## Section 1: Pixar's Color Script Technique

### What a color script is

A color script is a sequential series of paintings — typically small-format, quick studies — that map out the emotional arc of an entire film before a single frame is animated. Each panel represents a key scene or story beat. Together they show how color, light, saturation, and temperature evolve across the film's runtime.

Ralph Eggleston brought color scripts to Pixar for Toy Story (1995), working in pastel because it is fast and efficient. Since then every Pixar film has had one. [VERIFIED — Animated Views interview with Amid Amidi, author of "The Art of Pixar"]

The purpose is explicitly narrative, not aesthetic. Directors use color scripts to ensure the audience will feel the emotional weight of each beat without being told about it directly. [VERIFIED — StudioBinder, Prayan Animation]

### How Pixar maps beats to color

The color scheme varies to coincide with emotional beats and story arcs. The key operating principle: if the animator maintains consistent color-emotion relationships throughout the film, the audience will subconsciously connect the palettes with the emotion without conscious recognition. [VERIFIED — Prayan Animation]

**Specific documented examples:**

- **Up — opening sequence:** The wide-format color script shows the heartbreaking montage beat by emotional beat. Carl Fredricksen's palette centers on warm browns to signal grief rooted in memory and attachment. [VERIFIED — Hyperallergic review of "The Art of Pixar"]
- **Coco — Land of the Dead:** When the story crosses into the Land of the Dead, "it cranks up all the dials, colorwise." Scenes are described as "made out of neon, like a bio-organic version of Tokyo's Shinjuku District at night." The luminous orange marigolds are the connective tissue — the color of memory and crossing over. [VERIFIED — Pixar Coco color analysis, multiple sources]
- **Inside Out — Sadness:** Sadness (the character) has white in her palette. This white is specifically enhanced with blue-adjacent, desaturated tones per scene to deepen the emotional signal. [LLM-ESTIMATED — multiple Pixar color sources; specific scene-level HSL values not published]
- **Joker (non-Pixar but documented):** Progresses from muted greens and grays to bolder, more chaotic high-saturation colors as Arthur Fleck descends into madness. Color becomes louder as the character loses control. [VERIFIED — Filmustage blog, multiple film sources]

### The pre-animation constraint

Because computer animation is nonlinear in production — scenes are built out of sequence — the director needs the color script as a reference document to ensure the emotional temperature of any given scene matches where it falls in the story arc. [VERIFIED — Amy Moss Pre-Production Module citing Pixar internal process]

**Implication for web/brand film:** The same logic applies. If you build a brand film scene by scene without a color script, you will have locally acceptable scenes that are emotionally incoherent as a sequence.

---

## Section 2: Film Color Grading Rules

### The foundational warm/cool split

This is the most consistently documented finding across all sources. [VERIFIED across 6+ independent sources]

| Color Temperature | Kelvin Equivalent | Emotional Signal | Example Films |
|---|---|---|---|
| Warm (oranges, reds, amber) | 2,000K–3,500K | Safety, intimacy, belonging, nostalgia | Her (2013), Harry Potter interior Hogwarts scenes |
| Neutral (daylight) | 5,000K–5,500K | Normalcy, reality, no emotional loading | Documentary standard |
| Cool (blues, blue-greens) | 6,500K–10,000K+ | Isolation, tension, dread, clinical sterility | The Revenant, Black Hawk Down, most thrillers |

Specific documented citations:
- **Her (2013):** Warm reds, golds, oranges throughout. Signal: emotional intimacy and vulnerability between human and AI. Director Spike Jonze used the warmth of analog materials to contrast the digital world. [VERIFIED — multiple cinema color sources]
- **The Revenant:** Predominantly cool temperature. Mirrors protagonist's isolation in hostile landscape. Signal: the cold is not just weather, it is psychological abandonment. [VERIFIED — Backstage, NumberAnalytics]
- **Harry Potter:** Interior Hogwarts scenes use warm amber (2,800K range) to signal "finally home." The Deathly Hallows shifts to desaturated blue-gray to signal bleakness and dread as Voldemort's power rises. [VERIFIED — color temperature analysis sources]

### The saturation axis

Saturation and hue are separate variables that filmmakers use independently. [VERIFIED — PubMed study on color and emotion, Noam Kroll]

| Saturation Level | Emotional Signal | Physiological Effect |
|---|---|---|
| Highly desaturated (near grayscale) | Depression, boredom, sensory deprivation, passivity | Lower arousal, lower skin conductance response |
| Moderately desaturated | Calm, introspective, world-narrowing — viewer focuses on character, not environment | Moderate |
| Neutral saturation | Realism, credibility | Neutral |
| High saturation | Energy, excitement, climax, chaos | Measurably higher skin conductance (physical excitement response) |
| Oversaturated | Overwhelming, nauseating, surreal | Overstimulation |

Key finding from research: "While desaturation tends to emphasize the character (by focusing the viewer), saturation tends to emphasize the world by broadening the proverbial field of view. Dial your saturation up and you expand the world and stimulate the viewer's visual experience." [VERIFIED — Noam Kroll, Psychology of Color Grading]

Physiological evidence: Saturated and bright colors produce significantly stronger skin conductance responses — meaning the body physically reacts more intensely to vivid color. This is measurable, not subjective. [VERIFIED — PMC article 10867063, effects of color and saturation on enjoyment]

### The dark-to-warm arc

This is the specific arc relevant to the brand film ("dark to warm").

What it communicates:
- **Dark (desaturated + cool):** Confusion, isolation, uncertainty, the problem state. The user does not yet know the answer. They are in the fog.
- **Warm (saturated + warm):** Arrival, clarity, relief, trust, home. The user has the answer. The fog is gone.

This arc is the Hero's Journey collapsed into color. The dark is the ordinary world's dissolution; the warm is the return with the gift. [LLM-ESTIMATED — inferred from consistent film narrative pattern across sources; no single source states this formulation explicitly]

Alternative: **Dark → Cool → Warm** (three-beat arc)
- Dark: the problem state (desaturated, neutral-to-cool)
- Cool: active searching, unease, seeking (blue-dominant, moderate saturation)
- Warm: resolution, clarity, trust (amber-green, high saturation)

This three-beat version more closely mirrors the actual user experience of health anxiety. The "cool" phase maps to the moment of entering a calculator — not yet relieved, but actively doing something. The "warm" phase is the result. This arc has more emotional range and a cleaner emotional payoff. [LLM-ESTIMATED — inferred; not directly stated in any source]

---

## Section 3: Web Applications of Color Narrative

### What the web does differently

Film cuts or fades between scenes. Web design typically uses continuous gradients or scroll-triggered transitions. These are functionally different mechanisms. [VERIFIED — multiple web animation sources]

**Film approach:** Color shifts happen at story beat boundaries. The shift is the punctuation mark. It signals "something has changed." Abrupt swings serve dramatic or comedic purposes; gradual changes "fly under the radar of perception until a smooth change in mood is achieved." [VERIFIED — color script analysis sources]

**Web approach:** RGB interpolation via CSS transitions creates mathematically smooth gradients between states. This is continuous, not beat-driven.

### Beat-boundary vs. continuous gradient — which is more emotionally effective?

There is no direct head-to-head study comparing these approaches in web UX contexts. [ASSUMED — no source found]

The evidence from film suggests: beat-boundary transitions are more emotionally legible when you want the audience to register that a shift has occurred. Continuous gradients create mood, not punctuation. [LLM-ESTIMATED]

Practical implication for brand film:
- Use **continuous gradient** for the background environment (mood carrier — sets the emotional temperature of the moment)
- Use **beat-boundary shifts** at key narrative moments (the result appearing, the mental model clicking, the Pulse CTA)
- The gradient carries the audience toward the beat; the beat-boundary transition delivers the emotional punch

This is the approach NRK uses in scroll-driven journalism: continuous environmental changes (night falling, lights turning on) carry the reader between hard narrative beats (text revelations). [VERIFIED — Chrome Developers NRK case study]

### Scroll-driven color arc as a narrative device

Apple and NRK are the two best-documented examples of brands using scroll-driven background color transitions as narrative:

- **NRK:** Background visuals animate continuously as the user scrolls. Night falls progressively. Lights turn on in a building one by one. The color temperature shifts from day to night (warm to blue-dark) to tell the story without text. [VERIFIED — Chrome for Developers blog]
- **Apple:** Product pages use cinematic scrolling to reveal features. Background shifts from deep black to product-color-appropriate tones as each feature section scrolls in. [LLM-ESTIMATED — described in multiple sources but specific hex/temperature values not documented]

The CSS Scroll-driven Animations API (`animation-timeline: scroll()`) enables native synchronization of color transitions to scroll position without JavaScript. This is production-ready in 2025 Chromium and Safari. [VERIFIED — MDN Web Docs, Chrome for Developers]

---

## Section 4: Continuous Gradient vs. Beat-Boundary — Framework Recommendation

### Film evidence (beat-boundary is primary)

Pixar's color scripts show that "it's good to be decisive with how sudden and dramatic an adjustment in color and lighting is — abrupt swings can serve a comedic or dramatic purpose while more gradual changes can fly under the radar of perception until a smooth change in mood is achieved." [VERIFIED — color script sources]

The implication: gradual changes are **subconscious emotional carriers**; abrupt changes are **conscious narrative signals**.

### The hybrid model (recommended)

Neither approach alone is optimal. Film uses both:
- Continuous within a scene (mood maintenance)
- Beat-boundary between scenes (punctuation)

For a brand film or scroll-driven web experience, the model is:

```
[CONTINUOUS GRADIENT] ← carries emotional temperature across beats
      |
[BEAT-BOUNDARY SHIFT] ← fires at specific story moments
      |
[CONTINUOUS GRADIENT] ← new emotional temperature for next beat
```

Applied to our dark-to-warm brand film:

| Phase | Duration | Color State | Transition Type | Emotional Signal |
|---|---|---|---|---|
| Opening | 0–1.5s | Deep near-black, desaturated (HSL ~220, 15%, 8%) | — | Confusion, isolation |
| Problem state | 1.5–3s | Slow continuous drift toward cool dark blue (HSL ~215, 25%, 12%) | Continuous gradient | Searching, unease |
| Calculator appears | 3s | Beat-boundary snap — dark shifts fractionally warmer | Beat-boundary | "Something is happening" |
| Result loading | 3–5s | Slow gradient from cool to neutral (HSL ~190, 20%, 15%) | Continuous gradient | Anticipation building |
| Result reveals | 5s | Beat-boundary — warm pulse flash (HSL ~160, 60%, 25%) | Beat-boundary | Clarity arrives |
| Resolution | 5–8s | Slow gradient to warm-green resting state (HSL ~150, 40%, 18%) | Continuous gradient | Trust, relief, home |

[ASSUMED — specific HSL values are illustrative placeholders derived from our existing brand palette, not from external research]

---

## Section 5: Color Palettes for Specific Emotional States

### Research-backed mappings

The Manchester Color Wheel study (n=323: 105 healthy, 108 anxious, 110 depressed) is the most rigorous clinical source. [VERIFIED — PMC article 2829580, published BMC Medical Research Methodology]

Key findings:
- **Healthy mood → Yellow** (specifically "Yellow 14" on the Manchester scale). Yellow was the most-chosen "mood color" for healthy participants and the most "drawn to" color across all groups.
- **Anxious/depressed mood → Grey** ("Grey 35" and "Grey 36" dominated the top two slots for anxious and depressed participants)
- Yellow choice is significantly reduced in both depressed (p<0.001) and anxious (p=0.001) individuals compared to healthy controls
- Depressed people "feel more gray than blue" — the ScienceDaily headline directly summarizing this research

Design implication: Desaturated gray is clinically associated with low-mood states. The transition FROM gray/cool-desaturated TO warm-yellow-green is a literal color journey from anxiety to relief. This is not metaphor — it maps directly to what clinically anxious people report feeling. [VERIFIED source data; design implication is LLM-ESTIMATED]

### Emotional state → color mapping table

Compiled from: Manchester Color Wheel (clinical), film color psychology sources, wellness design literature.

| Emotional State | Hue Range | Saturation | Lightness | Notes | Confidence |
|---|---|---|---|---|---|
| Anxiety / dread | Cool gray to muted blue-gray | Very low (5–20%) | Low-mid (10–20%) | Manchester Wheel: Grey 35/36 dominant for anxious subjects | VERIFIED |
| Confusion / lost | Desaturated near-black | 0–15% | 5–12% | Film: opening act of horror/thriller — viewer feels protagonist's disorientation | LLM-ESTIMATED |
| Searching / seeking | Cool blue, low-mid saturation | 20–35% | 12–20% | Film: investigation sequences, detective genre | LLM-ESTIMATED |
| Anticipation | Neutral to slightly warm, mid-saturation | 25–40% | 15–22% | Tension before resolution — neither cold nor fully warm | LLM-ESTIMATED |
| Relief / clarity | Warm green to yellow-green | 40–60% | 20–35% | Manchester Wheel: Yellow dominant for healthy/positive mood | VERIFIED |
| Trust / safety | Warm green, mid-saturation, slightly desaturated from "relief" | 30–45% | 20–30% | Blue also scores for trust in UX literature, but our brand is green | LLM-ESTIMATED |
| Hope | Light green, yellow-adjacent | 35–55% | 30–45% | Multiple wellness design sources cite green for progress and hope | LLM-ESTIMATED |
| Intimacy / warmth | Amber-orange, warm | 50–70% | 20–35% | Film: Her, warm domestic scenes | VERIFIED |
| Energy / climax | High-saturation any hue | 70–100% | 30–50% | Skin conductance research confirms physiological arousal spike | VERIFIED |
| Depression / emptiness | Fully desaturated gray | 0–10% | 15–40% | Manchester Wheel: Grey dominant in depressed subjects | VERIFIED |

### Applied to our brand palette

Our brand green is approximately HSL(150, 60%, 45%) for the pulsing dot and accent. Our dark background is approximately HSL(220, 20%, 8%).

The emotional arc of our dark-to-warm film in HSL terms:
- Start: HSL(220, 15%, 8%) — anxiety/confusion register
- Mid: HSL(200, 20%, 12%) — searching register
- Near-end: HSL(170, 35%, 18%) — anticipation register
- End: HSL(150, 50%, 22%) — relief/trust register

This is a hue rotation of ~70 degrees (blue-dark to green-dark), combined with a saturation increase and modest lightness increase. The background never becomes light — it becomes warm-dark rather than light-warm. This preserves the brand's dark aesthetic while traversing the emotional arc. [ASSUMED — specific values are illustrative; verify against actual CSS values in the brand film]

---

## Section 6: Practical Framework — How to Plan a Color Arc

### Step-by-step process

**Step 1: List the story beats**
Write out every moment in the film/animation/page where something emotionally changes. Not plot events — emotional state changes. Example:
- User is lost / confused (BEFORE state)
- User discovers the calculator (recognition)
- User inputs their data (agency / participation)
- Result computes (anticipation)
- Result reveals (clarity arrives)
- User understands the mental model (comprehension)
- User feels equipped (trust / relief)
- User shares or acts (activation)

**Step 2: Assign an emotional state to each beat**
Use the table in Section 5. Be specific. "Positive" is not an emotional state. "Relief arriving after confusion" is.

**Step 3: Assign a color temperature + saturation to each emotional state**
Use the HSL ranges from Section 5 as starting points. Warm = high hue (orange-yellow-green direction in HSL). Cool = low/high hue with blue-dominant. Saturation = intensity of the emotion. Lightness = the amount of energy / activation.

**Step 4: Decide transition type for each beat boundary**
- Continuous gradient: mood carrier, subconscious
- Beat-boundary shift: conscious punctuation, marks that something changed
- Default rule: use beat-boundary only when the emotional state changes category (e.g., confusion → relief). Use continuous within a category (e.g., confusion deepening).

**Step 5: Build the color timeline**
Create a table mapping timestamp (for film) or scroll percentage (for web) to HSL values. Implement as CSS custom property animation, CSS `animation-timeline: scroll()`, or JavaScript-driven interpolation.

**Step 6: Test for legibility vs. subtlety**
Ask: would someone watching this without audio register that the emotional temperature changed at the right moments? Color arcs that require audio to be legible are failing. The visual arc should be independently readable. [LLM-ESTIMATED — inferred from film industry principle that color is a silent narrator]

---

## Falsifiability

| Finding | What would disprove it |
|---|---|
| Warm color = safety/intimacy in film | A rigorous cross-cultural study showing warm color evokes threat or aggression in >50% of participants from multiple cultures |
| Beat-boundary transitions are more emotionally legible than continuous gradients | A controlled UX study showing continuous gradients produce equal or stronger emotional recognition at beat moments |
| Manchester Color Wheel finding (yellow = healthy, gray = anxious) | Replication failure in a different cultural context; the original study was UK-based |
| Dark-to-warm arc communicates confusion-to-clarity | Viewer studies showing the arc reads as "danger to warmth" (threat-safety) rather than confusion-clarity — both are plausible interpretations |
| Saturation increase = emotional intensity | Contradiction in the PMC skin conductance data; the 2024 PMC study (10867063) is the primary evidence base |

---

## Shared Assumptions to Watch

1. **Western cultural baseline:** Most film and design color psychology research is conducted with Western audiences. Color associations are not fully universal. Warm colors signal danger in some cultural contexts.
2. **Dark backgrounds as "cool":** Our brand is dark-background dark-warm, not the light-warm of most "comfort" film palettes. We are inverting the typical lightness dimension. The emotional arc relies on hue and saturation shift, not lightness shift. This is an unusual approach without direct precedent in the sources.
3. **8-second film vs. multi-minute experience:** Pixar color scripts work over 90 minutes. Our brand film is 8 seconds. The pace of emotional travel must be compressed accordingly — the full arc happens in a fraction of the time. This may require the beat-boundary shifts to be more decisive and faster than film precedent suggests.

---

## Sources

- [Filmustage: Color Grading and Visual Narrative](https://filmustage.com/blog/enhancing-your-films-visual-narrative-color-grading-and-color-theory/)
- [Filmustage: Mastering Color in Filmmaking](https://filmustage.com/blog/mastering-color-in-filmmaking-an-essential-guide/)
- [Sohonet: Role of Color Grading in Cinematography](https://www.sohonet.com/article/the-powerful-role-of-color-grading-in-cinematography-enhancing-visual-storytelling)
- [No Film School: Color Psychology in Film](https://nofilmschool.com/color-psychology-in-film)
- [Noam Kroll: Psychology of Color Grading](https://noamkroll.com/the-psychology-of-color-grading-its-emotional-impact-on-your-audience/)
- [Backstage: Color Temperature in Film](https://www.backstage.com/magazine/article/what-is-color-temperature-75608/)
- [NumberAnalytics: Color Temperature in Film](https://www.numberanalytics.com/blog/ultimate-guide-color-temperature-film)
- [Brink Helsinki: Color Script in Animation](https://brinkhelsinki.com/logs/color-script-in-animation/)
- [Prayan Animation: Psychology of Color Theory in Animation](https://www.prayananimation.com/blog/psychology-of-color-theory-in-animation/)
- [StudioBinder: What Is a Color Script](https://www.studiobinder.com/blog/what-is-a-color-script-definition/)
- [FXGuide: Inside the Colorscript Process](https://www.fxguide.com/quicktakes/inside-the-colorscript-process-day-1-at-view/)
- [Munsell Color: Color Relationships in Film](https://munsell.com/color-blog/color-relationships-film/)
- [Manchester Color Wheel — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2829580/)
- [PubMed: Color and Emotion — Hue, Saturation, Brightness](https://pubmed.ncbi.nlm.nih.gov/28612080/)
- [PMC: Effects of Color and Saturation on Enjoyment](https://pmc.ncbi.nlm.nih.gov/articles/PMC10867063/)
- [ScienceDaily: Depressed People Feel More Gray Than Blue](https://www.sciencedaily.com/releases/2010/02/100208211926.htm)
- [Chrome for Developers: NRK Scroll-Driven Animation Case Study](https://developer.chrome.com/blog/nrk-casestudy)
- [UI Deploy: Complete Scrollytelling Guide 2025](https://ui-deploy.com/blog/complete-scrollytelling-guide-how-to-create-interactive-web-narratives-2025)
- [Fiction Horizon: Movies That Use Color Changes to Signal Emotional Shifts](https://fictionhorizon.com/movies-that-use-color-changes-to-signal-emotional-shifts/)
- [Hyperallergic: 25 Years of Pixar's Vibrant Color Palettes](https://hyperallergic.com/610771/the-art-of-pixar-chronicle-books/)
