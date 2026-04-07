# Semantic Demand Research Findings v1
**Date:** 2026-03-15
**Source:** Twitter/X API — 616 tweets across 8 topic categories, ED-filtered
**Status:** Directional findings. Single source (Twitter). Not finalized.

## Dataset Summary
- **v2 collection:** 91 tweets, 12 searches, heavy ED contamination (59%)
- **v3 collection:** 616 tweets, 28 searches, 8 topic categories, ED-filtered
- **Topics covered:** TDEE (62), Ozempic (115), IVF (71), Vitamin D (84), Creatine (124), Training (49), BMI (69), General (15), Sharing (27)
- **Reply data:** 1,008 replies across 48 tweets, 94 categorized as questions

---

## Finding 1: Two Distinct User Modes — Reference vs Validation

**Bookmark-to-like ratio reveals user intent:**

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

**Pattern:** High-bookmark topics (training, vitamin D, creatine) = people saving actionable information for later use. Low-bookmark topics (BMI, ozempic) = people engaging emotionally but not saving.

**Implication for config:** The calculator result display needs two modes:
- **Reference mode:** Dense, saveable, data-rich (dosage tables, comparison charts, protocol steps). For creatine, vitamin D, training, TDEE.
- **Validation mode:** Emotional scaffolding, reassurance, "am I okay?" framing. For BMI, body composition.

This is **configurable per calculator** — a mode flag that determines result presentation style.

---

## Finding 2: Five Universal Question Types (cross-topic)

From 94 reply questions across all topics:

| Question Type | Count | Example | Topics Present |
|--------------|-------|---------|---------------|
| Comparison ("X vs Y", "which is better") | 38 (40%) | "Why excluding steroids?" | ALL |
| Dosage/Amount ("how much", "how often") | 8 (9%) | "How many grams should a 175lb man take?" | Creatine, VitD, TDEE |
| Mechanism ("how does", "why does") | 6 (6%) | "How does creatine work?" | Creatine, VitD |
| Personal Fit ("should I", "can I", "for me") | 6 (6%) | "What do I do with that level of toxicity?" | VitD, Ozempic, Creatine |
| Safety ("is it safe", "side effects") | 2 (2%) | "Will taking vitamin D in heat be safe?" | VitD, Ozempic |

**Universal: Comparison is the dominant question type across ALL topics.** People don't ask "what is my X?" — they ask "is X better than Y?" or "how does mine compare?"

**Implication for config:** Every calculator result should include a comparison/context layer: "Where do you fall?" / "How does this compare to [reference]?" This is configurable — the comparison targets change per topic but the pattern is universal.

---

## Finding 3: Content Format × Engagement (what drives replies)

| Topic | Most Common Format | Highest Engagement Format |
|-------|-------------------|-------------------------|
| TDEE | Personal story (27) | List/protocol (3,818 avg) |
| Ozempic | Other (67) | Question (12,502 avg) |
| IVF | Other (42) | Other (711 avg) |
| Vitamin D | Other (37) | Data/study (8,440 avg) |
| Creatine | Other (48) | Data/study (9,830 avg) |
| Training | Other (26) | Personal story (1,102 avg) |
| BMI | Personal story (44) | Question (622 avg) |

**Cross-topic patterns:**
1. **Data/study format** drives highest engagement in supplement topics (Vitamin D, Creatine) — people trust and share research.
2. **List/protocol format** drives highest engagement in action topics (TDEE) — "here's what to do, step by step."
3. **Questions** drive massive engagement in controversial topics (Ozempic, BMI) — polarizing questions get replies.
4. **Personal stories** are the most common format across most topics but rarely the highest engagement.

**Implication for media pipeline:** The distributable media format should match the topic's highest-engagement format:
- Supplement topics → data visualization / study result infographic
- Action topics → step-by-step protocol visual
- Controversial topics → provocative question card that invites replies
- This is **configurable per calculator topic category**.

---

## Finding 4: Emotional State Map

| Topic | Primary Emotion | Secondary | What They Want |
|-------|----------------|-----------|---------------|
| BMI | Frustrated (10%) | Confused (7%) | "Tell me BMI is wrong / my body is fine" |
| Creatine | Confused (10%) | Skeptical (2%) | "Give me the definitive answer on dosage" |
| Training | Seeking (18%) | — | "Tell me the optimal plan" |
| TDEE | Confused (6%) | Frustrated (5%) | "Which calculator do I trust?" |
| Vitamin D | Confused (6%) | Frustrated (4%) | "What do my levels mean?" |
| IVF | Confused (6%) | Seeking (4%) | "Is my number normal?" |
| Ozempic | Skeptical (6%) | Confused (2%) | "Is this worth it / am I cheating?" |

**Universal emotional pattern:** Confusion appears in 6/7 topics. People don't know which tool to trust, what their number means, or how much to take. This is the universal unmet need.

**Topic-specific emotions:**
- BMI: frustration at the metric itself
- Ozempic: defensiveness about using medication
- IVF: anxiety about numbers being "normal"
- Training: desire for authority/optimal plan
- Creatine: skepticism about whether it even works

**Implication for config:** The emotional tone of results is configurable:
- Confused users → "Here's the clear answer" framing
- Frustrated users → "You're right to question this, here's the full picture" framing
- Anxious users → "Your number is [normal/actionable], here's what it means" framing
- Seeking users → "Here's the optimal approach" framing

---

## Finding 5: What Gets Saved (Bookmark/Impression Ratio)

The highest save-rate content across all topics:

1. **Cheat sheets / reference lists** (supplement stacks, nutrient pairing rules) — 1.5-2.0% save rate
2. **Specific protocols** ("reverse aging starter pack", "fat loss for IT professionals") — 1.2-1.7% save rate
3. **Tool recommendations** ("I recommend this app to calculate your actual TDEE") — 1.3-1.5% save rate
4. **Blood test / result interpretation guides** — 1.5-2.0% save rate
5. **Data/study results with specific numbers** — 1.2-1.5% save rate

**What does NOT get saved:** Hot takes, personal stories, memes, engagement farming.

**Implication for media pipeline:** The distributable media should be designed to be SAVED, not just liked:
- Result cards with interpretation ("Your vitamin D is 32 ng/mL — here's what that means")
- Dosage reference cards ("Creatine: 5g daily, no loading needed")
- Comparison cards ("TDEE Calculator A vs B vs C — here's why they differ")

---

## Finding 6: Signal Quality Correction

**The v2 dataset was misleading.** Our original conclusions were partially wrong:

| Original Claim | Correction |
|----------------|-----------|
| "People want validation, not calculation" | TRUE for BMI only. For creatine, vitamin D, training, TDEE — people want definitive reference answers. |
| "Am I overweight?" = top demand signal | This was engagement farming (63% of replies were compliments). Not genuine health demand. |
| "Nobody asks about formulas/methodology" | FALSE for TDEE — confusion about which formula/calculator is accurate is a primary signal. |
| "Shallow input → deep emotional output" | TRUE for BMI. FALSE for creatine/vitamin D where people want deep REFERENCE output, not emotional output. |

**Corrected universal finding:** People want CLARITY — but the form of clarity differs:
- BMI → emotional clarity ("am I okay?")
- TDEE → methodological clarity ("which calculator is right?")
- Creatine → dosage clarity ("how much, exactly?")
- Vitamin D → interpretation clarity ("what does my level mean?")
- Ozempic → social clarity ("is it okay to use this?")
- Training → authority clarity ("what's the optimal plan?")
- IVF → anxiety clarity ("is my number normal?")

---

## Configurable vs Logic-Driven: Summary

### CONFIGURABLE (universal across 4+ topics)
1. **Result comparison layer** — "Where do you fall?" / "How does this compare?" (appears in ALL topics)
2. **Emotional tone flag** — confused/frustrated/anxious/seeking/skeptical (set per calculator)
3. **Result display mode** — reference (dense, saveable) vs validation (emotional, reassuring) (set per calculator)
4. **Follow-up question patterns** — "Should I?", "How much?", "Is it safe?" (configurable prompts)
5. **Share mechanic** — "What's yours?" / comparison-inviting framing (universal)
6. **Demand capture** — "Have another question? Tell Pulse." (universal)
7. **Citation/trust signals** — study references, source badges (universal, content varies)
8. **Media output format flag** — data visualization / protocol steps / comparison card / question card (per topic category)

### LOGIC-DRIVEN (topic-specific, requires research per calculator)
1. The actual calculation/formula
2. Medical safety caveats (vary dramatically by topic)
3. Result interpretation text (what does THIS number mean in THIS context)
4. Controversy/nuance framing (BMI accuracy, Ozempic ethics, creatine skepticism)
5. Recommended actions after results
6. Comparison reference points (population averages, clinical thresholds)

### WHAT WE'RE NOT SURE ABOUT (needs more data)
1. Whether the reference/validation mode split maps cleanly to categories or is more granular
2. Whether the emotional state map holds across seasons/trends (Ozempic discourse shifts fast)
3. Whether the comparison question dominance is a Twitter artifact or universal user behavior
4. IVF data is thin (71 tweets, only 15 replies) — findings are directional only

---

## What This Means for the Media Pipeline

The distributable media format should match topic category:

| Category | Media Format | Content Pattern | Save Intent |
|----------|-------------|----------------|-------------|
| Supplement (VitD, Creatine) | Data infographic + dosage card | Study result + protocol | HIGH |
| Action (TDEE, Training) | Step-by-step protocol visual | List format + comparison | HIGH |
| Validation (BMI, Body Comp) | Result card with emotional framing | "You vs average" comparison | LOW |
| Medical (Ozempic, IVF) | Q&A card addressing common fears | Question + clear answer | MEDIUM |

All formats should be:
- Self-contained (no link needed — the media IS the value)
- Saveable (designed for bookmarks)
- Reply-inviting ("What's yours?" / "Agree or disagree?")
- 1200x675 for static, 3-8s for video

---

## Falsifiability

- If expanded research (Reddit, forums) shows different question type distribution, the "comparison dominates" finding may be a Twitter bias
- If the bookmark/like ratio doesn't hold on our own content, the reference/validation mode split needs revision
- If BMI users on non-Twitter platforms DO ask about methodology, the "validation only" conclusion for BMI is wrong
- The emotional state map is crude (keyword matching) — could misclassify ironic or complex tweets

## What We Might Be Missing

1. **Lurker demand** — people who search but never tweet. Twitter captures vocal users, not silent tool-seekers. This is a known blind spot.
2. **Seasonal variation** — creatine/training demand likely spikes Jan-Mar (New Year's resolutions). We collected in March.
3. **Platform-specific behavior** — Twitter users may behave differently from Google searchers who land on our calculators. The overlap is unclear.
4. **The "I already have a tool" population** — we're seeing unmet demand, but not satisfaction with existing tools. We don't know what's good enough.
