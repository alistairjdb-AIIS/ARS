# Semantic Demand Patterns

> Users interact with health content in two distinct modes -- Reference (save for later use, high bookmark-to-like ratio) and Validation (emotional engagement, low save rate) -- and the dominant question type across all health topics is comparison ("X vs Y"), not definition. Confusion about what's normal is the universal unmet emotion, but the form of clarity people seek differs by topic: dosage clarity, methodological clarity, emotional clarity, or authority clarity.

**Confidence:** MEDIUM
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### Two Distinct User Modes: Reference vs Validation

Bookmark-to-like ratio reveals user intent: [VERIFIED -- derived from 616 tweets across 8 topics]

| Topic | Bkmrk/Like | Mode |
|-------|-----------|------|
| Training | 0.33 | Reference (save for gym) |
| General | 0.34 | Reference (tool shopping) |
| Vitamin D | 0.29 | Reference (dosage, stacks) |
| Creatine | 0.25 | Reference (protocol, dosage) |
| TDEE | 0.12 | Mixed (some reference, some planning) |
| IVF | 0.11 | Mixed (tracking, emotional) |
| Ozempic | 0.07 | Engagement (debate, defense) |
| BMI | 0.05 | Validation (emotional, not saved) |

**Pattern:** High-bookmark topics (training, vitamin D, creatine) = people saving actionable information for later use. Low-bookmark topics (BMI, Ozempic) = people engaging emotionally but not saving. [VERIFIED]

**Design implication:** Content and calculator result displays need two configurable modes:
- **Reference mode:** Dense, saveable, data-rich (dosage tables, comparison charts, protocol steps). For creatine, vitamin D, training, TDEE. [VERIFIED]
- **Validation mode:** Emotional scaffolding, reassurance, "am I okay?" framing. For BMI, body composition. [VERIFIED]

### Five Universal Question Types

From 94 reply questions across all topics: [VERIFIED -- direct data from Twitter API pull]

| Question Type | Count | % | Example |
|--------------|-------|---|---------|
| Comparison ("X vs Y", "which is better") | 38 | 40% | "Why excluding steroids?" |
| Dosage/Amount ("how much", "how often") | 8 | 9% | "How many grams should a 175lb man take?" |
| Mechanism ("how does", "why does") | 6 | 6% | "How does creatine work?" |
| Personal Fit ("should I", "can I", "for me") | 6 | 6% | "What do I do with that level of toxicity?" |
| Safety ("is it safe", "side effects") | 2 | 2% | "Will taking vitamin D in heat be safe?" |

**Comparison is the dominant question type across ALL topics.** People don't ask "what is my X?" -- they ask "is X better than Y?" or "how does mine compare?" [VERIFIED]

**Implication:** Every calculator result should include a comparison/context layer: "Where do you fall?" / "How does this compare to [reference]?" The comparison targets change per topic but the pattern is universal. [VERIFIED]

### Content Format x Engagement Patterns

| Topic | Most Common Format | Highest Engagement Format |
|-------|-------------------|-------------------------|
| TDEE | Personal story | List/protocol (3,818 avg) |
| Ozempic | Other | Question (12,502 avg) |
| Vitamin D | Other | Data/study (8,440 avg) |
| Creatine | Other | Data/study (9,830 avg) |
| Training | Other | Personal story (1,102 avg) |
| BMI | Personal story | Question (622 avg) |

**Cross-topic patterns:** [VERIFIED]
1. **Data/study format** drives highest engagement in supplement topics (Vitamin D, Creatine) -- people trust and share research.
2. **List/protocol format** drives highest engagement in action topics (TDEE) -- "here's what to do, step by step."
3. **Questions** drive massive engagement in controversial topics (Ozempic, BMI) -- polarizing questions get replies.
4. **Personal stories** are the most common format but rarely the highest engagement format.

### Emotional State Map

| Topic | Primary Emotion | What They Want |
|-------|----------------|---------------|
| BMI | Frustrated (10%) | "Tell me BMI is wrong / my body is fine" |
| Creatine | Confused (10%) | "Give me the definitive answer on dosage" |
| Training | Seeking (18%) | "Tell me the optimal plan" |
| TDEE | Confused (6%) | "Which calculator do I trust?" |
| Vitamin D | Confused (6%) | "What do my levels mean?" |
| IVF | Confused (6%) | "Is my number normal?" |
| Ozempic | Skeptical (6%) | "Is this worth it / am I cheating?" |

**Universal: Confusion appears in 6/7 topics.** People don't know which tool to trust, what their number means, or how much to take. This is the universal unmet need. [VERIFIED]

**Corrected universal finding:** People want CLARITY -- but the form of clarity differs: [VERIFIED]
- BMI: emotional clarity ("am I okay?")
- TDEE: methodological clarity ("which calculator is right?")
- Creatine: dosage clarity ("how much, exactly?")
- Vitamin D: interpretation clarity ("what does my level mean?")
- Ozempic: social clarity ("is it okay to use this?")
- Training: authority clarity ("what's the optimal plan?")
- IVF: anxiety clarity ("is my number normal?")

### What Gets Saved (High Save-Rate Content)

Highest save-rate content across all topics (1.2-2.0% bookmark/impression ratio): [VERIFIED]
1. **Cheat sheets / reference lists** (supplement stacks, nutrient pairing rules)
2. **Specific protocols** ("reverse aging starter pack", "fat loss for IT professionals")
3. **Tool recommendations** ("I recommend this app to calculate your actual TDEE")
4. **Blood test / result interpretation guides**
5. **Data/study results with specific numbers**

**What does NOT get saved:** Hot takes, personal stories, memes, engagement farming. [VERIFIED]

### The Cortisol Content Demand Signal

The cortisol topic provides a case study in how health content demand manifests: [VERIFIED]

- "Cortisol spike" meme (Feb 2025) has been absorbed into identity and aesthetics language, not health language. "Low cortisol" = unbothered, elite. [VERIFIED -- KnowYourMeme, Daily Dot]
- #CortisolTok has 800M+ TikTok views, largely around "cortisol belly" and "cortisol face" -- body-image anxiety mapped onto cortisol. [VERIFIED]
- The highest-performing cortisol content pivots from assumed villain to misunderstood ally: "You think you have too much cortisol. Burned out people actually have too little." [THEORETICAL -- inferred from tension structure]
- Real people describe stress in physical and spatial terms: "shoulders near ears," "jaw clenched," "wired but tired." Not "I'm stressed." [VERIFIED -- aggregated from secondary sources describing Reddit discourse]

### Signal Quality Corrections

The v2 dataset was partially misleading. Corrections: [VERIFIED]

| Original Claim | Correction |
|----------------|-----------|
| "People want validation, not calculation" | TRUE for BMI only. For creatine, vitamin D, training, TDEE -- people want definitive reference answers. |
| "Am I overweight?" = top demand signal | This was engagement farming (63% of replies were compliments). Not genuine health demand. |
| "Nobody asks about formulas/methodology" | FALSE for TDEE -- confusion about which formula/calculator is accurate is a primary signal. |
| "Shallow input -> deep emotional output" | TRUE for BMI. FALSE for creatine/vitamin D where people want deep REFERENCE output. |

---

## Operational Rules

1. **When designing calculator result displays, set the reference/validation mode flag per topic** -- reference mode (dense, saveable) for supplement/action topics; validation mode (emotional, reassuring) for body composition topics, because bookmark-to-like ratio data shows fundamentally different user intent by topic.

2. **When creating any result display, include a comparison/context layer** -- "Where do you fall?" or "How does this compare to [reference]?" is the universal question type (40% of all questions), because users ask "X vs Y" not "what is X."

3. **When choosing distributable media format, match to the topic's highest-engagement format** -- data/study for supplement topics, list/protocol for action topics, provocative questions for controversial topics, because format-engagement mapping differs systematically by topic category.

4. **When designing content for save/bookmark behavior, use cheat sheets, specific protocols, and interpretation guides** -- these achieve 1.5-2.0% save rates while hot takes and memes do not get saved, because reference-mode users save actionable, dense information.

5. **When framing educational health content, lead with the confusion hook** -- confusion about what's normal is the universal unmet emotion (appears in 6/7 topics), and the specific form of confusion (dosage, methodology, interpretation, social, anxiety) should match the topic.

6. **When analyzing engagement data, distinguish genuine demand from engagement farming** -- "Am I overweight?" generated high reply counts but 63% were compliments, not genuine health questions, because surface-level engagement metrics can be misleading about actual user need.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/semantic_demand_findings_v1.md` | Two user modes, five question types, format x engagement, emotional state map, save-rate content analysis, signal quality corrections |
| `research-data/cortisol_animation_content_research.md` | Cortisol demand signals, meme vocabulary as cultural entry point, physical recognition language, confusion hook validation |

---

## Related Concepts

- [[hook-first-half-second]] — INFORMS: confusion hook is the recommended scroll-stopping mechanism for health content
- [[reels-pacing-structure]] — INFORMS: content format determines pacing structure (data visualization vs protocol steps vs question card)
- [[sme-buyer-psychology]] — EXTENDS: the reference vs validation mode split parallels SME buyer intent patterns
- [[engagement-scoring-matrix]] — INFORMS: engagement prediction dimension should account for format-topic matching
- [[twitter-x-growth-mechanics]] — EXTENDS: X bookmark behavior (20x a like, reference-value signal) maps directly to the reference vs validation mode split; high-bookmark X content matches high-bookmark-to-like health topics (cheat sheets, protocols, technique breakdowns)
- [[twitter-x-api]] — DEPENDS_ON: the Twitter/X search API and engagement metrics are the data collection substrate for all demand pattern findings; future real-time demand detection depends on continued API access and cost modeling

---

## Deep Reference

- **When** designing a calculator result page and need to choose between Reference mode (dense/saveable) and Validation mode (emotional scaffolding) → **read** `research-data/semantic_demand_findings_v1.md` §(Finding 1) **for** the bookmark-to-like ratio table per topic (Training 0.33 = reference, BMI 0.05 = validation), the configurable mode flag approach, and what each mode needs (reference = dosage tables/comparison charts, validation = "am I okay?" framing)
- **When** choosing content format for a health Reel and need the format-to-engagement mapping → **read** `research-data/semantic_demand_findings_v1.md` §(Finding 3) **for** which formats drive saves vs likes vs replies per topic, the comparison question dominance (40% of all reply questions are "X vs Y"), and the emotional state map showing confusion as the universal unmet need
- **When** building a hook for cortisol/stress content and need the cultural vocabulary → **read** `research-data/cortisol_animation_content_research.md` §1 (How Real People Talk) **for** the meme vocabulary ("spike my cortisol," "low cortisol era"), the physical-language pattern ("shoulders near my ears" not "I'm stressed"), and the body-image anxiety overlay (#CortisolTok, 800M+ views)

---

## Open Questions

- Is the comparison question dominance a Twitter artifact or universal user behavior? The dataset is Twitter-only (616 tweets). Reddit, forums, and Google search behavior may differ.
- Does the bookmark-to-like ratio hold on Instagram or only Twitter? Platform-specific behavior differences are unknown.
- Does the emotional state map hold across seasons/trends? Ozempic discourse shifts fast; the map was captured in March.
- IVF data is thin (71 tweets, only 15 replies) -- findings are directional only.
- Lurker demand (people who search but never tweet) is a known blind spot. Twitter captures vocal users, not silent tool-seekers.
