# Copywriting for Zero-Context Visitors: Research Findings
**Date:** 2026-03-22
**Scope:** Landing page and calculator copy for first-time visitors with no prior exposure to health metrics (BMR, TDEE, half-life, etc.)
**Sources:** MarketingExperiments A/B test database, CXL research, Copyhackers, cognitive fluency academic literature (Schwarz, Alter, Oppenheimer), CDC plain language research, landing page analysis of Calm/Headspace/Duolingo
**Method:** 8 targeted web searches, source triangulation, applied against 616-tweet semantic demand dataset already in collection
**Status:** Directional findings with verification levels tagged. Cites source material throughout.

---

## Core Problem Statement

A zero-context visitor arriving at `/tdee-calculator` does not know what TDEE means. They arrived via a search like "how many calories should I eat" or "why am I not losing weight." The mental gap between their question and our label ("TDEE Calculator") is a trust tax — every unit of confusion they experience reduces the probability of conversion and the probability of returning.

This document answers: how do you close that gap at the word level?

---

## Finding 1: The Given-New Contract

### What It Is

The given-new contract (also called the known-new contract) is a linguistic principle validated by text linguists and cognitive psychologists. Its rule: **put what the reader already knows at the start of a sentence, and introduce new information at the end.**

The purpose is to eliminate the cognitive cost of re-orienting. When new information arrives before the reader has established context, they must hold the new information in working memory while they locate the anchor. This increases cognitive load and increases the chance they quit reading.

Source: Carnegie Mellon University Writing Center; University of Colorado Denver Writing Center; Weissberg (1984) TESOL Quarterly research on given-new structures in scientific English.

### Application to Health Calculator Copy

**Wrong (new before given):**
> "TDEE is your Total Daily Energy Expenditure — how many calories you need."

The reader's first encounter is an acronym they've never seen. They must stop, decode the acronym, and then locate the concept. Three-step cognitive cost before the sentence is finished.

**Right (given before new):**
> "Your body burns a specific number of calories every day — just existing, moving, working. That number is called your TDEE."

The reader starts on known ground (bodies burn calories — they know this from experience). The new term arrives after context is established. The term becomes a label for something they already understood, not a gate they must pass through.

### Falsifiability

[ASSUMED] The given-new contract is validated for academic and technical writing. Its application to marketing copy is inferred, not directly tested in a controlled A/B setting on health calculator pages. The effect size in short copy (1-3 sentences) may be smaller than in long-form text.

What would disprove this: A/B test showing no conversion difference between jargon-first vs. plain-language-first headlines on calculator pages.

---

## Finding 2: Question-First vs. Answer-First Framing

### The Evidence

MarketingExperiments ran A/B tests on question vs. statement headlines. Key finding: **format matters less than whether the visitor can see the value of the offer quickly.**

Specific data points found:
- Question-style headline outperformed statement-style by 36.18% in one PPC clickthrough test [VERIFIED — MarketingExperiments cite]
- In a 6-headline test, the winning headline ("Identify Registered Sex Offenders Living Near You") converted 34% better than the next-best — it was a statement, not a question [VERIFIED — MarketingExperiments cite]
- CXL research: the more clarity a headline had, the more appealing it was. Number-based headlines had a 30% higher conversion rate than other formats [VERIFIED — CXL cite]
- Copyhackers: questions can generate curiosity but are "not the best method for converting site visitors" as a blanket rule

### The Synthesis

The research does not support "questions always win" or "statements always win." It supports: **whichever format gets the visitor to the value fastest wins.**

For health calculators, the relevant distinction is:

| Visitor entry state | Better format | Reason |
|---------------------|--------------|--------|
| Searching with a question ("how long does caffeine last?") | Question-first headline | Mirrors their search intent, creates immediate recognition |
| Searching with an outcome ("lose weight calculator") | Answer/benefit statement | They want the answer, not a question back |
| Browsing (no specific query) | Statement of value | Questions can feel rhetorical; benefits land faster |

### Application to This Product

Our 616-tweet dataset shows visitors arrive with questions, not with knowledge of our product. The dominant inbound query type is the question form: "How much creatine should I take?" "What is my TDEE?" "How long does caffeine stay in your system?"

**Implication [ASSUMED]:** For calculator pages that receive primarily question-driven organic traffic, leading with the user's own question ("How long does caffeine last in your body?") before introducing our answer ("Your half-life is X hours") is likely to outperform leading with the calculator name or our jargon.

This is an inference from the MarketingExperiments data + our tweet dataset. Not directly tested on this product.

---

## Finding 3: Cognitive Fluency — The Trust Mechanism

### The Research (Academic)

Cognitive fluency is the ease with which a person processes information. The core finding from Schwarz, Alter, Oppenheimer and others: **stimuli that are easier to process are judged as more true, more trustworthy, and more credible.**

Specific verified findings:
- Consumers perceived sellers with fluent (easy-to-say) names as more trustworthy, more likely to deliver products as advertised, and more likely to honor return policies [VERIFIED — Schwarz et al. consumer judgment research]
- "Incidental manipulations of processing fluency are sufficient to influence trust" [VERIFIED — direct quote from Schwarz et al. metacognitive experiences review, USC Dornsife]
- People asked to self-disclose in easy-to-read fonts were more willing to share than in hard-to-read fonts [VERIFIED — Alter & Oppenheimer 2009, Cognitive Science]
- PMC study on health information readability: higher readability in written health information directly increased self-efficacy in readers [VERIFIED — PMC article 7016314]

### The Line Between Simplicity and Oversimplification

[ASSUMED — no direct A/B data found] The research establishes that simpler = more trusted, but does not give a floor. The practical line for health calculators:

- **Too simple:** Strips precision users came for. "Your result is normal" without numbers gives no actionable data.
- **Too complex:** "Your basal metabolic rate adjusted for activity coefficient using the Mifflin-St Jeor equation yields 2,847 kcal/day." Reader exits.
- **Target:** Plain language container, precise number inside. "You burn about 2,847 calories per day just living your life — that's what your body needs to maintain its current weight."

The plain language container (given-new setup) absorbs the trust cost of the jargon. The precise number satisfies the reference-mode users who came for the data.

### What Breaks Fluency in Health Copy

From UX Bulletin / VWO readability research:
1. Dense acronym blocks (BMR, TDEE, VO2max on the same line)
2. Latin-root medical vocabulary ("attenuate," "exogenous," "hepatic")
3. Passive constructions ("calories are burned by the body")
4. Sentence length above 25 words
5. Conditional stacking ("if you are active, then depending on your weight, you may need...")

---

## Finding 4: The "So What?" Test

### What It Is

The "So What?" test is a copywriting filter: for every feature or fact you state, you ask "so what?" until you reach a benefit the reader viscerally understands.

Source: Multiple copywriting practitioners (Slobodan Dekanic Medium article, CopyEngineer, CarmineMastropierro). The technique appears consistently across independent copywriting sources.

### How to Apply It

Chain: **Feature → So what? → Benefit → So what? → Outcome**

| Feature | So what? | Benefit | So what? | Outcome |
|---------|----------|---------|----------|---------|
| "Caffeine has a 5-hour half-life" | So what? | "Half the caffeine is still in your body 5 hours after drinking" | So what? | "That afternoon coffee may be why you can't fall asleep at 11pm" |
| "Your TDEE is 2,400 kcal" | So what? | "That's how much you can eat without gaining weight" | So what? | "You can eat 400 fewer calories per day and lose about 1 pound per week" |
| "Your BMI is 27.3" | So what? | "That's slightly above the 'healthy' range" | So what? | "Your doctor may flag it, but BMI misses muscle mass — here's what else to check" |

The test is passed when a stranger could hear the final statement and know immediately why it matters to them.

### Where This Applies on Our Product

Every calculator result currently leads with the number. The number is the feature. The user has to supply the "so what?" themselves. Copy that provides the "so what?" directly — "here's what this means for you" — eliminates a cognitive step and replaces it with trust.

This is especially important for validation-mode users (BMI, body composition) who came with an emotional question, not a technical question.

---

## Finding 5: Jargon Handling — When to Use, When to Translate

### The Evidence

From copywriting research and health literacy sources:
- CDC Plain Language Materials: use "you" and common everyday words; strive for 20 words per sentence; limit each sentence to 1 idea [VERIFIED — CDC health literacy guidance]
- Agency for Healthcare Research and Quality provides a plain language word list for health materials [VERIFIED — AHRQ tool 4e]
- VWO readability research: readability lowers cognitive load, speeds comprehension, and "directly lifts satisfaction, conversions, and revenue" [VERIFIED — VWO 2026 readability guide]
- Medical jargon study (ScienceDirect, 2021): patients systematically misunderstood clinical terms; terms doctors considered "plain" were often opaque to patients [VERIFIED — ScienceDirect 2021]

### The Decision Rule

| Situation | Use jargon | Translate |
|-----------|-----------|-----------|
| The user searched using the jargon term | Yes — mirror their language | No — they know it |
| The user searched with plain language ("how many calories") | No | Yes — match their register |
| Result display (the number + label) | Label it both ways: "2,847 kcal — that's your TDEE" | — |
| Explanation of what the number means | Never jargon | Always translate |
| Trust signals / scientific basis | Acceptable in parenthetical | Lead with the translation |
| FAQ or deep-dive sections | Acceptable after establishing plain meaning | Always define on first use |

### Specific Translations for This Product

| Jargon term | Translation | When to use translation |
|-------------|-------------|------------------------|
| TDEE | "how many calories your body uses each day" | Any sentence that introduces the concept to a new user |
| BMR | "how many calories you'd burn doing nothing all day" | First use only |
| Half-life | "how long until half the [substance] is out of your system" | First use, then the term is established |
| Mifflin-St Jeor | Do not use in user-facing copy | Never in copy; footnote in methodology |
| ng/mL | "nanograms per milliliter (the unit your lab uses)" | Only if user input is in these units |
| Activity coefficient | "how active you are" | Always translate |

### The Dual-Label Pattern [ASSUMED]

No A/B data found for this specific approach on health calculators. The hypothesis: show both the translation and the jargon term together on first use, then drop the translation for subsequent mentions. This serves two audiences simultaneously — the zero-context visitor gets the translation, the research-mode visitor who knows the term gets signal that we're using it correctly.

Example: "Your body uses about 2,847 calories per day (your TDEE). To lose weight, eat below your TDEE."

---

## Finding 6: The "Bar Test" — Operational Definition

### What It Is

The bar test (sometimes called the "explain to a stranger" test) does not appear in academic literature by this name. It is a practitioner heuristic from the copywriting community. The principle: read your copy aloud as if explaining to someone sitting next to you at a bar who has no background in your product. If it sounds like a brochure, rewrite it. If they would say "wait, what does that mean?" — rewrite it.

[ASSUMED] No A/B data found for this specific heuristic. It is a qualitative filter, not a quantitative one.

### Why It Matters for Health Calculators

The problem with technical copy is that it passes the writer's internal filter (they know what everything means) but fails the zero-context reader's filter. The bar test forces the writer to simulate a different reader's state.

For our product specifically:
- "Enter your height, weight, age, and activity level to calculate your TDEE" — passes the writer's filter, fails the bar test (stranger asks: "what's a TDEE?")
- "Tell us about yourself and we'll show you exactly how many calories your body burns each day" — passes the bar test

### Running the Bar Test

For each block of copy, ask:
1. Would a 35-year-old non-fitness person who drinks coffee and goes for walks understand every word?
2. Would they know what to do with the result?
3. Would they trust the source based solely on this text?

If any answer is no, the copy has not passed the bar test. The fix is always: translate the jargon, run the "so what?" chain, apply the given-new structure.

---

## Finding 7: Real Examples — Health and Tech Products Explaining Complex Things Simply

### Calm

Headline: "Sleep more. Stress less. Live better."

Analysis: Three plain-language outcomes. No jargon. No feature description. Zero mention of "mindfulness," "meditation," "binaural audio," or any product mechanism. The product is invisible; the outcome is everything.

The zero-context visitor does not need to know what Calm is to understand why they might want it. [VERIFIED — from product landing page analysis in search results]

### Headspace

Approach: Sells the transformation, not the mechanism. Uses "Try" instead of "Subscribe" or "Sign Up" to reduce commitment anxiety.

Analysis: The zero-context visitor's first barrier is not understanding — it's commitment. Headspace's copy minimizes the barrier by minimizing the ask. [VERIFIED — from landing page analysis in search results]

### Duolingo

Approach: Shows the reward before the work. XP counters, streak badges, and achievement markers appear on the landing page before download, triggering reward anticipation.

Analysis: For a product that requires learning behavior (language learning), Duolingo does not explain the mechanism. It shows the emotional payoff — progress, completion, streaks. The zero-context visitor maps onto the emotional outcome, not the product feature. [VERIFIED — from landing page analysis in search results]

### TDEE Calculator (.net)

Current approach: Leads with "TDEE Calculator: Learn Your Total Daily Energy Expenditure." Jargon in the first line. Explanation buried in body copy.

Gap: A visitor searching "how many calories should I eat" lands on a page labeled with an acronym they didn't search for. The cognitive gap is immediate. [VERIFIED — direct observation of tdeecalculator.net in search results]

### Myprotein TDEE Article

Current approach: "BMR is the amount of energy needed while resting... like figuring out how much gas an idle car consumes while parked."

Analysis: This is the given-new contract applied correctly. Known concept (car, idle, gas) → new concept (BMR at rest). The analogy bridges the gap. [VERIFIED — from Myprotein search result content]

---

## Finding 8: Questions as Hooks — Why They Work Universally

### The Mechanism

From our 616-tweet dataset, the dominant question types users ask are:
- "How long does caffeine last?" (mechanism question)
- "How much creatine should I take?" (dosage question)
- "What does my BMI mean?" (interpretation question)
- "Is my vitamin D level normal?" (comparison question)

These questions are **universally understood** regardless of the user's fitness knowledge. You do not need to know what creatine is to understand the question "how much should I take?" — the question form itself carries enough context.

Contrast with "Every 5 hours, half" — the current mental model framing for caffeine half-life. This is correct and elegant as a summary, but it is an **answer without a question**. A zero-context visitor may read it and not know what it answers. The question "How long does caffeine last in your body?" is the given that makes "every 5 hours, half the caffeine is gone" land.

### What the Data Shows

MarketingExperiments: "In the mind of the customer, it is not a matter of a question headline or a statement headline, but rather how quickly they can see the value of the offer on the page." [VERIFIED — direct cite]

The question works when it mirrors the visitor's search intent. It fails when it's rhetorical or when the visitor didn't arrive with that question in mind.

### Applied Rule for This Product

For organic search traffic arriving via question queries: match the question first, then deliver the answer.

Structure:
1. **Hook:** The visitor's question, in their language ("How long does caffeine actually last?")
2. **Answer bridge:** Plain-language answer before any jargon ("It takes about 5 hours for your body to eliminate half the caffeine you drank")
3. **Mental model label:** Introduce the term after the concept is established ("That's called the half-life — and yours is probably different based on your weight and metabolism")
4. **Calculator CTA:** "Enter your weight and caffeine amount — we'll show you exactly when you'll be clear"

This sequence serves both audiences: the zero-context visitor gets a complete answer at step 2 and can stop; the engaged visitor proceeds to step 3-4.

---

## Synthesis: The Zero-Context Copy Stack

These principles compound. The full stack, in order of application:

| Layer | Principle | Test | Common failure |
|-------|-----------|------|---------------|
| 1. Entry | Given-new contract | Does the first line start with something they already know? | Leading with the product name or acronym |
| 2. Clarity | Bar test | Would a non-expert understand every word out loud? | Jargon that the writer no longer notices |
| 3. Value | "So what?" chain | Does every fact connect to a specific reader outcome? | Stopping at the feature without reaching the benefit |
| 4. Fluency | Cognitive fluency check | Is the reading level at or below 8th grade? Short sentences? | Conditional stacking, passive voice, Latin roots |
| 5. Jargon | Dual-label decision rule | Is the term necessary? If yes, is it translated on first use? | Using both jargon AND translation redundantly without structure |
| 6. Format | Question vs. statement | Does the format match the visitor's arrival state? | Using questions when visitor wants direct answers |

---

## Applied to Specific Calculators

### Caffeine Half-Life Calculator

Current mental model: "Every 5 hours, half"

Gap: Zero-context visitor does not know what "half" refers to or why it matters.

Copy stack applied:
- **Given:** "That afternoon coffee you're drinking right now — it'll still be in your system at midnight."
- **New:** "Caffeine has a half-life of about 5 hours. That means in 5 hours, half of it is still running through your bloodstream."
- **So what?:** "If you had a coffee at 3pm, half that caffeine is still active at 8pm — and a quarter of it at 1am."
- **Calculator CTA:** "Find your personal caffeine clearance time."

### TDEE Calculator

Current label: "TDEE Calculator"

Gap: Acronym first.

Copy stack applied:
- **Given:** "Your weight doesn't change based on willpower. It changes based on one number."
- **New:** "That number is how many calories your body burns every single day — we call it your TDEE."
- **So what?:** "Eat below that number, you lose weight. Eat above it, you gain. Eat exactly at it, you stay the same."
- **Bar test:** Would a stranger understand? Yes — every word is common.
- **Calculator CTA:** "Find your number."

### BMI Calculator

Current risk: BMI surfaces a number that can trigger negative emotion. Zero-context visitors often arrive in validation mode ("am I okay?").

The "so what?" chain for BMI has an extra step: the emotional "so what?" comes before the practical "so what?".

- **Given:** "BMI is the number your doctor uses to flag weight concerns."
- **New:** "Your BMI is [X]. That puts you [in/slightly above/well above] the range doctors call 'healthy.'"
- **Emotional so what?:** "That number doesn't account for muscle, age, or body type — here's what it actually tells you and what it misses."
- **Practical so what?:** "Doctors use BMI as a starting point. Here are three other numbers that give you a more complete picture."

---

## Falsifiability

| Finding | What would disprove it |
|---------|----------------------|
| Given-new contract improves comprehension in short marketing copy | A/B test showing no difference in time-on-page or conversion between jargon-first and plain-language-first calculator headlines |
| Questions match visitor intent better than statements for organic search traffic | Traffic analysis showing visitors arrive with outcome intent ("lose weight") more than question intent ("how many calories") across this site |
| Cognitive fluency increases trust in health copy | A/B test showing 8th-grade copy and 12th-grade copy perform equally on a health calculator page |
| "So what?" chaining improves conversion | A/B test showing result pages with and without outcome explanation convert equally |
| Dual-label pattern (jargon + translation) serves both audiences | A/B test showing pure-translation outperforms dual-label (suggesting the jargon label adds no value or adds confusion) |

---

## What This Research Did Not Find

1. **Direct A/B data on health calculator pages specifically.** All data is from adjacent domains (SaaS, e-commerce, general health marketing). The application to calculators is inferred. [FLAG for design agent]

2. **Quantified effect size for given-new contract in short copy.** The academic research is on long-form text. Headline-length application is logical but not empirically verified here. [FLAG]

3. **Where exactly the floor is for simplicity.** The research says simpler is more trusted, but does not establish at what reading level precision-seeking users (our reference-mode visitors) start to distrust because the copy feels dumbed-down. [FLAG]

4. **How the zero-context visitor distribution changes by traffic source.** Organic search visitors and social traffic visitors may have different context levels. A visitor coming from a tweet already knows the topic; an organic search visitor may not. Copy may need to adapt by traffic source — this is untested. [FLAG]

---

## Sources

- [MarketingExperiments — Do question headlines work?](https://marketingexperiments.com/copywriting/question-based-headlines)
- [MarketingExperiments — Optimizing Headlines](https://marketingexperiments.com/value-proposition/optimizing-headlines)
- [Copyhackers — Headline formulas and the science of high-converting copywriting](https://copyhackers.com/2012/09/headline-formulas-and-the-science-of-high-converting-copywriting/)
- [Copyhackers — Asking questions in your copy](https://copyhackers.com/2015/09/asking-questions/)
- [CXL — 5 characteristics of high-converting headlines](https://cxl.com/blog/5-characteristics-high-converting-headlines/)
- [Unbounce — Increase conversions by improving value proposition clarity](https://unbounce.com/landing-pages/increase-conversions-by-improving-the-clarity-of-your-value-proposition/)
- [Schwarz et al. — Processing fluency in consumer judgment and decision making](https://dornsife.usc.edu/norbert-schwarz/wp-content/uploads/sites/231/2023/12/21_CPR_Schwarz_et_al_Metacognitive_experiences_review.pdf)
- [Alter & Oppenheimer — Suppressing Secrecy Through Metacognitive Ease (2009)](https://journals.sagepub.com/doi/full/10.1111/j.1467-9280.2009.02461.x)
- [PMC — Influence of readability on self-efficacy in health information (article 7016314)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7016314/)
- [UX Bulletin — Processing Fluency in UX](https://www.ux-bulletin.com/processing-fluency-in-ux/)
- [VWO — 7 ways to improve website readability](https://vwo.com/blog/website-copy-readability/)
- [Carnegie Mellon University — Known-New Contract](https://www.cmu.edu/student-success/other-resources/resource-descriptions/known-new.html)
- [George Mason University Writing Center — Known/New Contract](https://writingcenter.gmu.edu/writing-resources/grammar-style/improving-cohesion-the-known-new-contract)
- [CDC — Plain Language Materials and Resources](https://www.cdc.gov/health-literacy/php/develop-materials/plain-language.html)
- [AHRQ — Plain Language Words for Health Communication](https://www.ahrq.gov/health-literacy/improve/precautions/tool4e.html)
- [Medium — So What? Test in copywriting](https://medium.com/@slobodandekanic.com/copywriting-so-what-test-advantages-and-disadvantages-with-examples-49aac4b3dba4)
- [CopyEngineer — How to translate features into benefits](https://copyengineer.com/post_translate_features_into_benefits/)
- [Landingi — Healthcare landing page best practices](https://landingi.com/blog/how-to-create-the-best-healthcare-landing-page/)
- [Lovable — Landing page best practices 2026](https://lovable.dev/guides/landing-page-best-practices-convert)
- [Shopify — Conversion copywriting](https://www.shopify.com/blog/conversion-copywriting)
- [ScienceDirect — Identifying and classifying medical jargon (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0738399121000537)
