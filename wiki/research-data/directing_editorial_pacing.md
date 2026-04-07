# Directing & Editorial Pacing: Craft of Sequencing Visual Information

**Date:** 2026-03-22
**Methodology:** Web search across 14 targeted queries. No primary sources consulted directly (WebFetch unavailable). All findings derived from secondary sources: StudioBinder, No Film School, MasterClass, Wikipedia, Backstage, media-studies.com, beverlyboy.com.
**Uncertainty level:** MODERATE — core principles well-documented across multiple sources; percentage weights for Murch's Rule confirmed across 3+ sources; UI applications are inferred by this research, not extracted from direct UI research literature.

---

## Purpose of This Document

Documents film directing and editorial pacing craft for application to:
1. Web animation sequencing (what to show, when, and for how long)
2. Product reveal design (calculator results, Pulse onboarding)
3. Twitter content structure (hook → tension → payoff)
4. Motion design editorial decisions

This is craft vocabulary, not technique rules. Every section includes a falsifiability note and a UI application inference.

---

## 1. Walter Murch's Rule of Six

**Source:** "In the Blink of an Eye" (1995, revised 2001), Walter Murch. Secondary: [StudioBinder](https://www.studiobinder.com/blog/walter-murch-rule-of-six/), [No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch), [Berkeley iSchool](https://blogs.ischool.berkeley.edu/i290-viznarr-s12/the-rule-of-six-walter-murch/)
**Verification:** [VERIFIED] — percentage weights confirmed across 3 independent sources citing Murch directly.

### The Six Criteria in Priority Order

| Priority | Criterion | Weight | Definition |
|----------|-----------|--------|------------|
| 1 | Emotion | 51% | Is the cut true to the emotion of the moment? |
| 2 | Story | 23% | Does the cut advance the story? |
| 3 | Rhythm | 10% | Does the cut occur at a rhythmically interesting, "right" moment? |
| 4 | Eye-trace | 7% | Does the cut respect where the audience's focus is within the frame? |
| 5 | 2D Plane (Planarity) | 5% | Does the cut respect the grammar of 3D space transposed to 2D? |
| 6 | 3D Space (Spatial continuity) | 4% | Does the cut respect the three-dimensional continuity of actual space? |

**Total: 100%. Emotion alone outweighs all other five criteria combined.**

### Core Principle

"What they finally remember is not the editing, not the camerawork, not the performances, not even the story — it's how they felt."

Murch's hierarchy means: if you must sacrifice something to make a cut, sacrifice your way up from the bottom. Give up spatial continuity before planarity, planarity before eye-trace, eye-trace before rhythm, rhythm before story — but never sacrifice emotion.

### The Murch Percentage Rule Applied to UI

If a UI transition, animation, or reveal satisfies emotional resonance but breaks spatial continuity (e.g., a panel expands from the wrong position), keep the emotional resonance. The spatial grammar violation costs 4%. The emotional disconnect costs 51%.

**[ASSUMED — inferred, not directly stated by Murch or any UI source]:** The weight hierarchy maps to web animation decisions: emotion-first means the speed, timing, and trigger of a reveal matters more than whether it's pixel-perfect in 3D transform space.

**Falsifiability:** If user testing showed that spatial disorientation in UI (scrolling position jumps, unexpected z-axis changes) reduced engagement more than emotional flatness, Murch's hierarchy would not generalize to UI. This has not been tested in available data.

---

## 2. Eisenstein's Five Methods of Montage

**Source:** "Film Form" and "The Film Sense" by Sergei Eisenstein (1920s). Secondary: [media-studies.com](https://media-studies.com/eisenstein-montage/), [StudioBinder](https://www.studiobinder.com/blog/soviet-montage-theory/), [Wikipedia](https://en.wikipedia.org/wiki/Soviet_montage_theory), [MasterClass](https://www.masterclass.com/articles/soviet-montage)
**Verification:** [VERIFIED] — five method names and definitions consistent across all sources.

### The Five Methods

**1. Metric Montage**
Cuts are made at fixed time intervals regardless of content. Like a metronome. Creates mechanical acceleration when intervals shorten. Tension comes from timing alone, not from what's in the frame.

Eisenstein: "Pieces are joined according to their lengths in a formula corresponding to a measure of music."

Application: Edit cuts every 2 seconds, then every 1.5s, then every 0.8s as a sequence builds. The shortening interval creates urgency before the content even changes. Equivalent: CSS animation `animation-duration` that accelerates across a sequence.

**2. Rhythmic Montage**
Cuts follow the motion and momentum within the frame. The content drives the cut, not the clock. Cutting on action (matching movement) creates continuity. This is what Kuleshov codified and what became standard Hollywood editing.

Equivalent: Cutting when a character's gesture completes, not before. In UI: triggering the next state when a user interaction completes (tap released, scroll threshold reached), not on a timer.

**3. Tonal Montage**
Cuts are made based on the emotional resonance (tone) of each shot, not length or motion. Two shots are joined because they carry similar or contrasting emotional weight. The dominant mood of each shot is the unit.

Example: A shot of still water cut to a shot of a sleeping face — both carry stillness. The tone rhymes.

Application in product design: Showing a "calm, authoritative" result card after an "uncertain, anxious" input form. The emotional register of each screen should be deliberate. The contrast or resonance is the message.

**4. Overtonal Montage**
The cumulative synthesis of metric + rhythmic + tonal. The effect on the audience is more complex and abstract than any single method can produce. Eisenstein described this as achieving "physiological" effects — making an audience physically feel something.

Application: When the timing (metric), the in-frame motion (rhythmic), and the emotional register (tonal) all align and build — the result transcends any single element. This is what makes great sequences feel inevitable rather than constructed.

**5. Intellectual Montage**
The juxtaposition of two shots to produce a third meaning that exists in neither shot alone. The meaning emerges only from collision.

The definitive example: In "Strike" (1925), Eisenstein intercut workers being massacred by machine guns with footage of cattle being slaughtered in a slaughterhouse. Neither shot alone makes the statement. Juxtaposed, they create the metaphor: "The workers were treated like cattle." This meaning is not in either image — it is generated by the sequence.

Eisenstein derived this from Japanese kanji: two separate ideograms combine to form a concept neither represents alone. (Eye + Water = Weeping. Mouth + Bird = Song.)

**UI/Product Application:**
A calculator result (your TDEE is 2,400) cut immediately to a consequence framing ("That's 3 fewer calories than you need to lose 1 lb/week") creates an intellectual montage. Neither the number alone nor the consequence alone makes the point. Their sequence produces understanding.

**Falsifiability:** Intellectual montage assumes the audience has the cultural/symbolic knowledge to complete the metaphor. If users lack the reference frame (e.g., they don't know what slaughter looks like), the third meaning never forms. In UI: if users don't understand what TDEE means yet, the consequence framing produces confusion, not insight. Sequence order matters — context before consequence.

---

## 3. The Six Types of Cuts and What Each Communicates

**Source:** [Adobe](https://www.adobe.com/creativecloud/video/post-production/cuts-in-film.html), [MasterClass](https://www.masterclass.com/articles/essential-film-cuts), [Backstage](https://www.backstage.com/magazine/article/types-of-cuts-in-film-75730/), [StudioBinder](https://www.studiobinder.com/blog/types-of-editing-transitions-in-film/)
**Verification:** [VERIFIED] — definitions consistent across sources; communicative intent is [ASSUMED/LLM-ESTIMATED] where sources gave technical definition without explicit communication meaning.

| Cut Type | Mechanism | What It Communicates | UI Equivalent |
|----------|-----------|----------------------|---------------|
| Hard Cut | Instantaneous switch between shots, no transition | Continuation, urgency, present moment, now | State change with no animation (0ms transition). Deliberate abruptness. Use when the new state is the entire point. |
| Dissolve | Two shots overlap briefly, one fades as the other rises | Passage of time, memory, dreamlike connection between moments | Crossfade between views. Implies the two states are related, one becomes the other. |
| Fade | Shot dissolves to (or from) black | Beginning, end, pause, gravity. Scripts open with FADE IN, close with FADE OUT | Full opacity fade used for section breaks, onboarding start/end, modal entrance. Signals: "this chapter is starting." |
| Wipe | New shot sweeps across screen, displacing old | Transition across location or time, often playful or declarative | Slide transitions, panels replacing panels. Direction of wipe implies direction of travel (left = back, right = forward). |
| Match Cut | Two different shots connected by visual/compositional similarity (shape, motion, framing) | Symbolic connection across time, space, or meaning. A = B in some essential dimension | Two UI states sharing a common anchor element that doesn't move (FLIP animation). The shared element IS the statement. |
| Jump Cut | The same shot with a section removed, causing a visual lurch forward in time | Disorientation, urgency, efficiency, instability, or intentional rawness (Godard) | Instagram Reels, TikTok jump cuts. Cuts between states of the same element. Can communicate speed or psychological fracture depending on context. |

### The Most Misused Cut

The jump cut is the most misused in web animation. Designers use it (no transition) expecting efficiency; audiences read it as broken. The hard cut (instantaneous, full swap) is different from a jump cut — a hard cut moves to a new scene/element; a jump cut lurches within the same scene. In UI: changing from a form view to a results view via a hard cut reads as intentional and decisive. Cutting between two states of the same button without transition reads as broken.

### The Match Cut as Design Language

The match cut is the highest-value technique for UI product reveals. When a button expands into a results card (FLIP animation), the button and the card share spatial identity — they are the "same object" across two states. This creates the cognitive message: "This result came from your input." The sequence produces causality. Without the match cut relationship, results feel disconnected from the action that generated them.

---

## 4. Cross-Cutting (Parallel Editing) and Tension

**Source:** [StudioBinder](https://www.studiobinder.com/blog/cross-cutting-parallel-editing-definition/), [Wikipedia](https://en.wikipedia.org/wiki/Cross-cutting), [Adobe](https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/cross-cut.html), [Skill Man](https://www.skillmanvideogroup.com/cross-cutting-and-parallel-editing/)
**Verification:** [VERIFIED] — mechanism and effect confirmed across sources. Godfather/Silence of the Lambs examples verified.

### Mechanism

Cross-cutting alternates between two or more simultaneous events occurring in different locations. The audience understands both events are happening at the same time.

### How Tension Is Generated — Two Variables

**Variable 1: The Gap**
The audience knows Event A and Event B are happening simultaneously. If the outcome of A depends on B arriving in time (rescue before execution, disarm the bomb before detonation), the gap between "where B is" and "where B needs to be" generates tension. Every cut back to A increases the gap's urgency.

**Variable 2: The Rhythm of the Cuts**
The speed at which cuts alternate sets the pace of tension. Long alternation = slow burn (The Silence of the Lambs). Short, accelerating alternation = spike (The Dark Knight ferry scene). Shortening the intervals is the mechanical equivalent of turning up volume — it communicates urgency regardless of content.

### The Multiplication Effect

From search results on "Inception": cross-cutting does not add suspense — it multiplies it. Suspense of Scene A × Suspense of Scene B, connected by causality. The multiplication only works if the audience understands the causal link between the two threads. Without causality, cross-cutting is just confusion.

### Film Examples

- "The Godfather" baptism/assassination sequence (Coppola): moral and dramatic irony. Michael declares faith while ordering murders. The juxtaposition is the statement.
- "The Silence of the Lambs" (Demme): Clarice storms the wrong house while Buffalo Bill stalks her in the dark. The audience knows; she doesn't. This information gap (Hitchcock's suspense principle applied to cross-cutting) is the mechanism.
- "Inception" (Nolan): four simultaneous dream layers, all causally connected. The cross-cutting creates a countdown clock across all four layers simultaneously.

### UI Application: Simultaneous State Revelation

Cross-cutting has a direct UI equivalent in "before/after" reveals and progress-based reveals. When a product shows two states simultaneously (input state + result state, side by side or alternating), it creates the same cognitive pressure: the user senses something is about to resolve. Alternating between "what you entered" and "what it means" is editorial cross-cutting applied to product design.

A loading state that shows two things happening simultaneously (data computing + user waiting) creates low-grade tension. Resolving both at once (result appears, loading stops) is the payoff cut.

---

## 5. The Kuleshov Effect: Sequence Creates Meaning

**Source:** [Wikipedia](https://en.wikipedia.org/wiki/Kuleshov_effect), [NFI](https://www.nfi.edu/kuleshov-effect/), [EditMentor](https://editmentor.com/blog/the-kuleshov-effect-the-magic-of-context-in-filmmaking/), [PMC NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299807/)
**Verification:** [VERIFIED] — original experiment documented in film theory literature; NIH citation confirms behavioral research.

### The Original Experiment

Lev Kuleshov intercut an identical expressionless shot of actor Ivan Mosjoukine's face with three different images:
- A bowl of soup (audiences attributed: hunger)
- A girl in a coffin (audiences attributed: grief)
- A woman on a divan (audiences attributed: desire)

The actor's expression was identical in all three sequences. Audiences believed they saw different expressions. The meaning was generated entirely by what came before and after the face — not by the face itself.

**The principle:** An image does not carry inherent meaning. Its meaning is constructed by the images adjacent to it in sequence.

### Applied to UI Sequences

Every screen a user sees is "cut" with the screen they just left. The meaning they derive from your current screen is partially constructed by their previous screen.

Concrete examples:

**Example A — The context contaminates the neutral:**
A BMI result shown immediately after a judgmental framing ("Are you overweight?") will read as accusatory even if the number and label are clinically neutral. The framing of the prior screen infects the next.

**Example B — The sequence changes the number's meaning:**
"Your TDEE is 2,400 calories."
Shown after: "Most people your age burn 2,000-2,200 calories"
Reader inference: "I'm above average. This is good."

"Your TDEE is 2,400 calories."
Shown after: "To lose 1 lb/week, you need to be in a 500-calorie deficit."
Reader inference: "I need to eat 1,900. That's restrictive."

Same number. Two different sequences. Two different emotional readings.

**Example C — The reveal controls the interpretation:**
In a calculator result, if you show the number BEFORE the interpretation, users form their own meaning (often negative, especially in health contexts). If you show the interpretation frame FIRST ("Here's what this tells us about your energy balance") and THEN the number, users receive the number inside a frame. The Kuleshov sequence is: interpretive frame → data → reinforcement.

### The Formal Principle for Product Design

The meaning a user assigns to any piece of data is not intrinsic to the data. It is constructed by:
1. What came just before it
2. What comes just after it
3. The emotional state they are in when they see it

This is not UX copywriting advice. It is a structural principle about sequence architecture.

**Falsifiability:** If users showed consistent interpretation of data independent of surrounding context (i.e., a BMI of 27 always read as "slightly overweight" regardless of framing), the Kuleshov effect would not apply. No research in available data supports this. The effect is considered well-established in behavioral psychology.

---

## 6. Shot/Reverse Shot and the Conversational Rhythm

**Source:** [Wikipedia](https://en.wikipedia.org/wiki/Shot/reverse_shot), [MasterClass](https://www.masterclass.com/articles/shot-reverse-shot), [StudioBinder](https://www.studiobinder.com/blog/shot-reverse-shot-cutaways-coverage/), [Backstage](https://www.backstage.com/magazine/article/what-is-shot-reverse-shot-film-examples-75550/)
**Verification:** [VERIFIED] — technique and 180-degree rule consistent across sources. UI application is [ASSUMED — inferred].

### The Technique

Shot/reverse shot alternates between two characters who are in dialogue. The canonical pattern:
1. Character A speaks (camera on A)
2. Cut to Character B reacting / listening
3. B responds (camera on B)
4. Cut to A reacting
5. Repeat

The 180-degree rule enforces spatial continuity: the camera stays on one side of an imaginary axis between the characters. Breaking the axis disorients the viewer — suddenly they can't tell who is "left" and who is "right" in the conversation.

### What It Communicates

Shot/reverse shot establishes:
- Two parties are in dialogue
- Each party has a perspective (their own frame)
- The relationship between them is defined by the cuts (rapid = tension, slow = intimacy)
- The power dynamic (whose shot is longer, who is shot from below vs. above, who gets the close-up vs. medium shot)

### The UI Equivalent: Input → Response

The conversational rhythm of shot/reverse shot maps directly to the input/response pattern in UI:

| Film | UI |
|------|----|
| Character A speaks | User enters data |
| Cut to B's reaction | System processes / loading state |
| B responds | Result appears |
| Cut to A's reaction | User reads result, forms next question |
| Repeat | User adjusts input, cycle continues |

The "180-degree rule" equivalent in UI: maintain spatial consistency. If input is on the left and response on the right, do not swap them. If the result appears below the input, it should always appear below the input. Breaking spatial consistency is the UI equivalent of crossing the axis — it disorients without purpose.

**The power dynamic equivalent:** The shot that gets more screen time and closer framing holds the power. In a calculator UI, if the result gets a full-screen reveal with visual weight while the input form is small and compressed, the result has the "power." If the form dominates and the result appears inline and small, the process (not the insight) has the power. Editorial choice.

**The rhythm equivalent:** Rapid shot/reverse shot = urgency, confrontation, pressure. Applied to UI: instant feedback (no delay between input and result acknowledgment) creates urgency and momentum. Deliberate delay (even 300ms with a subtle loading state) creates anticipation — the equivalent of a slow cut to the reaction shot. Both are valid; neither is neutral.

---

## 7. Hitchcock's Three Rules of Suspense and Product Reveals

**Source:** [No Film School](https://nofilmschool.com/screenwriting-lessons-on-suspense), [Medium — Nathan Baugh](https://medium.com/@nathan.baugh/the-bomb-under-the-table-12c83ce8259a), [The Script Lab](https://thescriptlab.com/features/screenwriting-101/9806-3-writing-lessons-on-suspense-from-alfred-hitchcock/), [Hitchcock's Rule — No Film School](https://nofilmschool.com/2015/11/hitchcock-rule-help-you-tell-better-visual-stories)
**Verification:** [VERIFIED] — bomb under the table analogy documented from Hitchcock's 1970 AFI interview and Truffaut interview transcripts across multiple sources.

### Rule 1: Give the Audience Information the Characters Don't Have

"In the surprise scenario, two people are talking at a table. A bomb explodes. The audience gets 15 seconds of shock.

In the suspense scenario, the audience sees the bomb placed under the table. Two people sit down to talk. Now the audience has 15 minutes of suspense."

The mechanism: **information asymmetry.** When the audience knows something is coming that a character doesn't, every mundane moment becomes charged. The scene has not changed — only what the audience knows has changed.

**Product application:** Reveal the stakes before the result. If a user knows their TDEE calculation will determine whether their current intake creates a surplus or deficit, every moment they spend entering data is charged with anticipation. If they don't know why the question matters, the data entry is just form-filling.

**Applied to Twitter content:** Post the conclusion in the hook. "Here's what happens when you take creatine at the wrong time." Now every tweet in the thread is the audience waiting for the bomb. The hook creates the bomb; the thread is the ticking clock.

### Rule 2: The Bomb Must Not Go Off

Hitchcock's constraint: if you build suspense and then release it without resolution or relief, the audience feels cheated and angry. The tension must resolve with payoff, not abandonment.

**Applied:** Do not create anticipation and then fail to deliver a meaningful result. A calculator that builds up to a result with a loading animation and then returns a vague or ambiguous number (e.g., "moderate risk") without explanation is the bomb going off on the audience. The contract is: suspense → resolution. Breaking it destroys trust.

The exception Hitchcock named: if the bomb's going off IS the twist (i.e., the unexpected ending is the point), then it works. Applied to content: a tweet thread that ends with "and this is exactly why most advice on this is wrong" can detonate the bomb if the detonation is the reveal.

### Rule 3: Scale the Object to Its Importance (Hitchcock's Rule)

Separate from suspense but related: "The size of an object in the frame should be proportional to its importance to the story at that exact moment."

A ticking clock dominates the frame. A key detail is shown in close-up. The bomb is small under a wide table — Hitchcock would argue this is the wrong composition. Show it large. Let the size communicate the stakes.

**Applied to product design:** If the key number in a calculator result (TDEE: 2,847 cal) is the most important element, it should occupy the most space. Not a supporting footnote. Not embedded in a paragraph. The visual hierarchy of the result screen should be proportional to information importance.

Hierarchy of a result that follows Hitchcock's Rule:
1. The number (largest, most prominent)
2. What it means in plain terms (second largest)
3. The details/methodology (smallest)

Hierarchy that violates it: a page with equal-weight sections for "How to calculate TDEE," "Your result," and "What is TDEE" — the result is buried in curriculum rather than foregrounded as the payoff.

---

## 8. Building a Sequence in Web Animation — Editorial Decisions

**Source:** [Google Animations Editorial Guidelines](https://creators.google/en-us/content-creation-guides/modern-storytelling-with-web-stories/animations-editorial-guidelines/), [CSS Animation Principles](https://cssanimation.rocks/principles/), [Smashing Magazine](https://www.smashingmagazine.com/2019/02/animation-design-system/), synthesis from all above sources.
**Verification:** [LLM-ESTIMATED] — synthesis across sources. Individual claims tagged inline.

### The Core Distinction: Transition vs. Sequence

A **transition** moves from State A to State B. It is a single edit.

A **sequence** is a series of editorial decisions about what to show, what to withhold, and in what order — with the same deliberateness a film editor uses to construct a scene.

Most web animation is built at the transition level. The craft of editorial pacing operates at the sequence level.

### The Eight Editorial Decisions in a Sequence

**Decision 1: What is the opening frame?**
What does the user see before they interact? The opening frame establishes the emotional register, the implied promise, and the context the Kuleshov effect will use to color everything that follows. This is not the same as "what is above the fold." It is the question: what does the user's eye land on first, and what does that establish?

**Decision 2: What is withheld from the opening?**
Hitchcock's bomb principle: suspense is generated by strategic withholding. A landing page that shows everything immediately gives 15 seconds of surprise. A landing page that reveals its most important element only after a scroll, an interaction, or a beat of anticipation builds suspense before the reveal. What is not yet visible at the moment of arrival?

**Decision 3: What triggers the next reveal?**
Scroll? Hover? A timed delay? Click? Each trigger has a different meaning. Scroll-triggered reveals say "you earned this by going deeper." Timed reveals say "wait for it." Click-triggered reveals say "you chose to see this." Hover reveals say "curiosity is rewarded." The trigger is an editorial statement about the relationship between user action and information access.

**Decision 4: What is the rhythm of reveals?**
Eisenstein's metric montage applied: if reveals happen at equal intervals, the pacing feels mechanical. If they accelerate, they create urgency. If they decelerate (slow down at the most important moment), they create gravity. Murch's Rule: rhythm is worth 10% — not nothing, but subordinate to emotion and story.

**Decision 5: What is the emotional register of each state?**
Eisenstein's tonal montage: each screen state carries an emotional tone. Form state = uncertain, anticipatory. Loading state = trust, patience. Result state = revelation, clarity (or shock). The sequence of tones is not incidental — it IS the emotional arc.

**Decision 6: What cut type connects each state?**
Choosing between a hard cut (instant), a dissolve (crossfade), a wipe (directional slide), or a match cut (FLIP) between UI states is the same decision a film editor makes. Each communicates something different. Hard cut = decisiveness. Dissolve = the new state grows from the old. Match cut = these are the same thing across two moments. [See Section 3]

**Decision 7: What is the payoff frame?**
Hitchcock's Rule: the most important element gets the most space. The payoff frame is the editorial climax — the shot the whole sequence has been building toward. In a calculator: the result number at full scale, with sufficient breathing room to register. In a Twitter video: the final frame that contains the re-tweetable insight.

**Decision 8: What is the exit state?**
Where does the sequence leave the user emotionally? Does it resolve (give them next steps)? Does it open a new question? Does it give them something to share? The exit is not the end of the user's story — it is where the next sequence begins. An editorial sequence that ends without an exit state has the equivalent of a film that stops before the final scene.

### The Kuleshov Trap in Web Animation

[ASSUMED — inferred from Kuleshov effect applied to UI sequences]

Every animation adds a contextual frame that colors the meaning of what follows. An animation that is visually exciting but tonally wrong (e.g., a celebratory particle effect on a BMI result that classifies a user as obese) does not just fail — it creates the wrong emotional sequence. The particle effect frames the result as cause for celebration. The Kuleshov effect means the user arrives at the number inside that celebratory frame, which reads as the product mocking them.

This is the editorial responsibility: every animation is a statement about what the surrounding content means. There are no neutral animations.

---

## 9. Synthesis: Directing Vocabulary for Web Product Sequences

A table mapping film techniques to web animation / product decisions:

| Film Craft Term | What It Controls | Web/Product Equivalent |
|----------------|-----------------|------------------------|
| The opening frame | Emotional register + audience expectation | Above-fold hero state before scroll or interaction |
| Information gap (Hitchcock) | Audience knowledge vs. character knowledge | What the user knows is coming vs. what they haven't seen yet |
| The cut type | How meaning bridges two states | CSS transition: none / fade / transform / FLIP |
| Metric montage | Timing of cuts regardless of content | Animation timing (duration, stagger, delay) as structural pacing |
| Rhythmic montage | Cuts driven by in-frame motion | Trigger on completion of user action, not on timer |
| Tonal montage | Emotional register of adjacent shots | Emotional arc of form → loading → result states |
| Intellectual montage | Third meaning from collision of two shots | Data → consequence sequence (number + interpretation = meaning) |
| Kuleshov effect | Context determines meaning of any single shot | Prior screen frames meaning of current screen |
| Cross-cutting | Two simultaneous events in tension | Before/after, progress + waiting, dual-state reveals |
| Shot/reverse shot | Conversational rhythm, power dynamic | Input → response cadence, visual weight of form vs. result |
| Hitchcock's Rule | Frame size proportional to importance | Visual hierarchy of result: number first, largest, most prominent |
| Murch's emotion (51%) | Preserve feeling over all other criteria | Animation serves emotional arc — never sacrifice it for technical correctness |
| Match cut | Symbolic connection across two states | FLIP animation: the input and the result are the same object |
| The exit state | What the sequence leaves the audience with | Next step CTA, share prompt, or new question after result |

---

## 10. Uncertainty and Gaps

**What is verified:**
- Murch's six criteria and weights [VERIFIED — cited in primary book, confirmed in 3+ secondary sources]
- Eisenstein's five montage methods and examples [VERIFIED — consistent across academic and film education sources]
- Cut types and their conventional meanings [VERIFIED]
- Hitchcock's suspense rules and bomb analogy [VERIFIED — sourced from documented AFI and Truffaut interviews]
- Kuleshov experiment [VERIFIED — documented in film theory literature, behavioral confirmation in PMC]
- Cross-cutting mechanism and examples [VERIFIED]

**What is inferred (not verified against UI research):**
- All UI applications of film techniques [ASSUMED — reasoned inference from film principles, not derived from UX research studies]
- The claim that "the Kuleshov effect applies to sequential UI screens" [ASSUMED — plausible from cognitive psychology of priming, not directly tested in UI research]
- The shot/reverse shot to input/response mapping [ASSUMED]

**What would disprove the core claims:**

| Claim | What Would Disprove It |
|-------|----------------------|
| Emotion should be preserved over rhythm and spatial continuity in UI | A/B test showing spatially disorienting animations (that felt emotional) underperformed smooth but emotionally flat ones |
| Prior screen context affects interpretation of data | User research showing consistent data interpretation independent of framing sequence |
| Matching input to result via FLIP animation increases perceived causality | Testing showing FLIP animations produced no difference in "I understand where this result came from" vs. no-animation transitions |
| Withholding creates anticipation in web sequences | Data showing immediate full-reveal outperforms progressive disclosure on engagement and trust |

---

## Sources

- [StudioBinder — Walter Murch Rule of Six](https://www.studiobinder.com/blog/walter-murch-rule-of-six/)
- [No Film School — 6 Rules for Good Cutting](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch)
- [Berkeley iSchool — Rule of Six](https://blogs.ischool.berkeley.edu/i290-viznarr-s12/the-rule-of-six-walter-murch/)
- [No Film School — Editing for Emotion with Murch's Rule](https://nofilmschool.com/editing-emotion-using-walter-murchs-rule-six-non-narrative-content)
- [media-studies.com — Eisenstein's Five Methods](https://media-studies.com/eisenstein-montage/)
- [StudioBinder — Soviet Montage Theory](https://www.studiobinder.com/blog/soviet-montage-theory/)
- [Wikipedia — Soviet Montage Theory](https://en.wikipedia.org/wiki/Soviet_montage_theory)
- [MasterClass — Soviet Montage](https://www.masterclass.com/articles/soviet-montage)
- [Adobe — Cuts in Film](https://www.adobe.com/creativecloud/video/post-production/cuts-in-film.html)
- [MasterClass — Essential Film Cuts](https://www.masterclass.com/articles/essential-film-cuts)
- [Backstage — Types of Cuts](https://www.backstage.com/magazine/article/types-of-cuts-in-film-75730/)
- [StudioBinder — Editing Transitions](https://www.studiobinder.com/blog/types-of-editing-transitions-in-film/)
- [StudioBinder — Cross-Cutting](https://www.studiobinder.com/blog/cross-cutting-parallel-editing-definition/)
- [Wikipedia — Cross-Cutting](https://en.wikipedia.org/wiki/Cross-cutting)
- [Adobe — Cross-Cut](https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/cross-cut.html)
- [Wikipedia — Kuleshov Effect](https://en.wikipedia.org/wiki/Kuleshov_effect)
- [NFI — Kuleshov Effect](https://www.nfi.edu/kuleshov-effect/)
- [PMC NIH — Kuleshov Effect Behavioral Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299807/)
- [Wikipedia — Shot/Reverse Shot](https://en.wikipedia.org/wiki/Shot/reverse_shot)
- [MasterClass — Shot Reverse Shot](https://www.masterclass.com/articles/shot-reverse-shot)
- [StudioBinder — Shot Reverse Shot](https://www.studiobinder.com/blog/shot-reverse-shot-cutaways-coverage/)
- [No Film School — 3 Lessons from Hitchcock](https://nofilmschool.com/screenwriting-lessons-on-suspense)
- [Medium — The Bomb Under the Table](https://medium.com/@nathan.baugh/the-bomb-under-the-table-12c83ce8259a)
- [The Script Lab — Hitchcock Suspense](https://thescriptlab.com/features/screenwriting-101/9806-3-writing-lessons-on-suspense-from-alfred-hitchcock/)
- [No Film School — Hitchcock's Rule](https://nofilmschool.com/2015/11/hitchcock-rule-help-you-tell-better-visual-stories)
- [No Film School — Kubrick directing actors](https://nofilmschool.com/how-stanley-kubrick-directed-actors)
- [StudioBinder — Kubrick directing style](https://www.studiobinder.com/blog/stanley-kubrick-directing-style/)
- [No Film School — 2001 bone cut](https://nofilmschool.com/2001-space-odyssey-greatest-cut-in-movie-history)
- [CSS Animation — Principles](https://cssanimation.rocks/principles/)
- [Smashing Magazine — Animation in Design Systems](https://www.smashingmagazine.com/2019/02/animation-design-system/)
- [Google Animations Editorial Guidelines](https://creators.google/en-us/content-creation-guides/modern-storytelling-with-web-stories/animations-editorial-guidelines/)
- [Fiveable — Techniques for Guiding the Viewer's Eye](https://fiveable.me/visual-storytelling/unit-4/techniques-guiding-viewers-eye/study-guide/O0I0y7KbDaLwd8bf)
- [Independent Film Arts — Silent Tension](https://independentfilmartsacademy.com/silent-tension-visual-sound-storytelling/)
