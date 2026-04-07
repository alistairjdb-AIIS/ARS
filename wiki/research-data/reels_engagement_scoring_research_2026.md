# Reels Engagement Scoring: Primary Source Research

**Date:** 2026-03-30
**Method:** Web search (18 targeted queries across Meta official sources, academic research, industry data, creator/agency publications). No primary data collected.
**Purpose:** Reverse-engineer the upstream sources that inform a Reels engagement scoring matrix with six dimensions: Hook, Pacing, Visual Motion, Typography, Production Quality, Engagement Prediction.
**Consumer:** Agent on animation scoring tasks; user for scoring matrix calibration.
**Status:** Secondary source synthesis. Each section identifies primary sources, derivative sources, and gaps.

---

## Uncertainty Register

| Finding | Confidence | Why |
|---------|-----------|-----|
| Watch time is #1 signal | HIGH | Adam Mosseri confirmed publicly, Jan 2025; corroborated by Meta Transparency Center system cards |
| Sends > Likes for unconnected reach | HIGH | Mosseri confirmed Jan 2025; consistent across 10+ independent analyses |
| 1.7s mobile attention window | MEDIUM | Attributed to Facebook internal research (circa 2016); original study not publicly accessible; widely cited but primary doc unverifiable |
| 3-second hold rate threshold | MEDIUM | Multiple practitioner sources cite >60% hold = 5-10x reach; no official Meta confirmation of exact threshold |
| Saves carry 1.7x weight of likes | LOW | Single source claim (Social Tradia); not confirmed by Meta; plausible but unverified multiplier |
| Kinetic typography +42% completion | LOW | Cited by influencers-time.com; original study not traceable; likely aggregated from multiple contexts |
| Motion graphics 2.5x engagement vs static | LOW | Jungl Studio claim; methodology unclear; "engagement" definition varies |
| 8-second attention span | DEBUNKED | Microsoft Canada 2015 report cited Statistic Brain, not their own research; widely debunked |

---

## Part 1: Instagram's Algorithm Signal Hierarchy

### 1A. Official Meta Sources

**Adam Mosseri, January 2025 — Three Confirmed Ranking Signals:**

1. **Watch time** — #1 signal for both connected (follower) and unconnected (Explore/Reels tab) distribution
2. **Sends per reach** — How often content is shared via DM; most powerful signal for reaching NEW audiences
3. **Likes per reach** — Percentage of viewers who like; slightly more important for connected (follower) distribution

Source hierarchy stated by Mosseri:
- For followers seeing your content: Likes > Sends
- For non-followers discovering your content: Sends > Likes
- Watch time is #1 in both contexts

**Meta Transparency Center — Reels Chaining AI System Card:**
- Multi-stage ranking funnel: Sourcing (retrieval) -> Early-Stage Ranking (ESR) -> Late-Stage Ranking (LSR)
- ~100 candidate reels scored at final stage
- Input signals: reel length, similarity to previously engaged content, user behavior history (watch, like, skip, share, save)
- 3-second watch threshold explicitly measured: "how many times users watched at least 3 seconds of the reel anywhere on Instagram"
- Integrity filters applied to remove non-recommendable content
- System is dynamic — models, predictions, and input signals change frequently

**Meta Engineering Blog — Key Technical Publications:**

1. *"Adapting the Facebook Reels RecSys AI Model Based on User Feedback"* (Jan 2026)
   - User True Interest Survey (UTIS) model: asks random users "To what extent does this video match your interests?" on 1-5 scale
   - UTIS goes beyond likes/watch time to capture "true interest"
   - Accuracy improved from 59.5% to 71.5%; precision from 48.3% to 63.2%
   - Deployed in both ESR and LSR stages
   - Key insight: effective interest matching goes beyond topic alignment — includes audio, production style, mood, and motivation

2. *"Journey to 1000 Models: Scaling Instagram's Recommendation System"* (May 2025)
   - Instagram runs ~1000 models across the ranking funnel
   - Each layer progressively filters candidates with more expensive operations
   - Knowledge-sharing across Feed, Story, and Reels surfaces (Meta Lattice architecture)

3. *"Friend Bubbles: Enhancing Social Discovery on Facebook Reels"* (Mar 2026)
   - Social signals (friend interactions) used to expand top-of-funnel sourcing
   - Continuous feedback loop for ranking friend-adjacent content

**December 2025 Algorithm Updates:**

1. **"Your Algorithm" feature** (Dec 10, 2025): Users can review/edit topic preferences, add new interests, down-rank topics. Makes topical clarity in content more important for creators.
2. **Hashtag deprioritization continued**: Users can no longer follow hashtags; hashtags deprioritized as ranking signals in favor of interest/keyword-based relevance.
3. **Original content boost**: Reposted content labeled and penalized; aggregator accounts suppressed. Instagram increased original content prevalence in US by 10 percentage points in Q4 2025.
4. **AI content understanding improved**: Meta's AI now analyzes visuals, on-screen text, voiceover audio, and video clips to categorize content and match to users.

**March 2026 Update:**
- Stronger weight on relationship signals — accounts that users interact with via DMs, comments, story replies ranked higher
- Saves and repeat views gained importance relative to likes/comments

### 1B. Engagement Signal Weight Hierarchy (Synthesized)

Based on all sources, the operational hierarchy from most to least algorithmic weight:

| Signal | Weight | Context | Source Quality |
|--------|--------|---------|---------------|
| Watch time (duration + completion %) | Highest | Both connected + unconnected | Mosseri confirmed |
| Sends/DM shares per reach | Very High | Strongest for unconnected reach | Mosseri confirmed |
| Likes per reach | High | Strongest for connected reach | Mosseri confirmed |
| Saves | High | Claimed 1.7x likes; indicates reference value | Practitioner consensus, not Meta-confirmed |
| Substantive comments | Medium | Word count, questions, mentions weighted > emoji/generic | Multiple practitioner sources |
| Rewatches | Medium | Re-entering the reel signals deep interest | Practitioner sources, aligns with UTIS logic |
| Profile visits after viewing | Medium | Signals content-to-creator curiosity | Buffer, Hootsuite analyses |

### 1C. What Would Disprove This Hierarchy

If Meta published an updated system card showing saves or comments outweigh sends, or if UTIS survey data showed that "true interest" diverges significantly from watch time (e.g., users report high interest in content they watch briefly), the hierarchy would need revision. The UTIS model itself represents Meta's acknowledgment that behavioral signals alone are insufficient.

---

## Part 2: Hook (First 1-2 Seconds) — Sources and Benchmarks

### 2A. Where "hooks need to land in X seconds" comes from

**The 1.7-second figure:**
- Origin: Facebook internal research, circa 2016, published on facebook.com/business
- Finding: Average attention span on Facebook video = ~2 seconds (2.5s desktop, 1.7s mobile)
- Original study not publicly accessible as a standalone document; referenced in Facebook Business blog post "Capturing Attention in Feed: The Science Behind Effective Video Creative"
- This is the UPSTREAM source that most "hook in 1-2 seconds" advice derives from

**The 3-second hold rate:**
- Origin: Instagram's own analytics system; the platform measures retention at 3 seconds as a distribution threshold
- Practitioner consensus: >60% retention at 3 seconds correlates with 5-10x reach vs. <40% retention
- This is the PLATFORM MEASUREMENT that the 1.7s creative advice maps to

**Nielsen sub-2-second effectiveness data:**
- Nielsen research found that sub-2-second video impressions still drive 38% brand recall, 23% brand awareness, 25% purchase intent
- This validates that even brief attention capture has measurable impact

**The reconciliation:** Content has ~1.7s to stop the scroll (user decision window), but Instagram measures at 3s (platform threshold). The hook must WORK at 1.7s but HOLD to 3s.

### 2B. Eye-Tracking and Attention Research

- **Tandfonline (2025):** "Measuring Gaining and Holding Attention to Social Media Ads with Viewport Logging" — validated eye-tracking against viewport logging; key metrics are time-to-first-fixation and minimum fixation thresholds
- **Kahneman, "Thinking, Fast and Slow":** Hooks work because they target System 1 (fast, emotional, automatic processing) before System 2 (deliberate, logical) engages. This is the cognitive science foundation for why hooks must be immediate and pattern-interrupting.
- **EyeQuant research:** Website attention capture measured in seconds; video content in feed even more compressed
- **UC Irvine + Microsoft:** Screen attention dropped from 2.5 minutes (2004) to 47 seconds (recent); within-content attention even shorter

### 2C. What Specifically Makes Hooks Work (Research-Backed)

| Mechanism | Source | Evidence Level |
|-----------|--------|---------------|
| Motion in frame zero | Emplifi (10,110 Reels analyzed) | Medium — single large study |
| Face within 3 seconds | Emplifi — +10% 10-second retention | Medium |
| Human speech within 3 seconds | Emplifi — +25% 10-second retention, +5.6% engagement vs music-only | Medium |
| Visual + text + audio triple hook | OpusClip, Social Media Examiner | Practitioner consensus |
| Contrarian/pattern-interrupt opening | Planable, Buffer, multiple agencies | Widely replicated pattern |

### 2D. What Would Disprove Hook Doctrine

If Instagram's AI content understanding becomes sophisticated enough to evaluate content quality independent of early retention (e.g., UTIS-style "true interest" surveys override 3-second hold rates), the hook-first paradigm could shift. Meta's January 2026 UTIS paper is the first evidence this might happen — they explicitly acknowledge behavioral signals alone are insufficient.

---

## Part 3: Pacing — Timing for Human Reading/Processing Speed

### 3A. Primary Sources

**Reading speed research (cognitive science):**
- Average silent reading: 200-250 words per minute (3.3-2.4 words/second)
- Comfortable comprehension for mixed audiences: 150-180 wpm
- Minimum text display time: 13 characters per second (i.e., 30 characters needs ~2.3 seconds)
- ACM research (2022): "Towards Individuated Reading Experiences" — reading speed varies significantly by individual and font

**Text card timing formula (practitioner-derived):**
- Base display time = 3 seconds + 0.5-0.7 seconds per average word
- Example: 10-word card = ~9 seconds (3 + 10 x 0.6)
- Platform adjustment: TikTok/Reels favor shorter cards with lower multipliers vs. YouTube/educational content

**Video pacing research:**
- High-performing shorts average one cut every 2-4 seconds (OpusClip data)
- 3-5 seconds per shot before attention wavers (general video editing research)
- Visual novelty resets attention: each visual change buys a few more seconds of engagement
- "Build-and-release" rhythm: alternating fast-paced and slower sections maintains engagement
- Monotonous rhythm (same clip length throughout) reduces emotional impact and retention
- For short-form: 15-30 seconds total length maximizes retention and algorithmic distribution

### 3B. Where Pacing Benchmarks Come From

The "2-4 second cuts" benchmark is a DERIVATIVE of:
1. Reading speed research (how long text needs to be visible)
2. Attention decay research (3-5 seconds per visual before wandering)
3. Platform-specific retention curves (where dropoff happens in analytics)

No single study established this as a rule. It emerged from convergent evidence across cognitive science and platform analytics.

### 3C. What Would Disprove Pacing Rules

If longer-form Reels (60-90s) with slower pacing consistently outperformed fast-cut Reels in reach and engagement, the "fast cuts = better" assumption would need revision. There is some early evidence that Instagram is testing longer-form content distribution (up to 3 minutes for Reels), which could shift optimal pacing.

---

## Part 4: Visual Motion — Kinetic Energy, Moving Elements

### 4A. Research on Motion vs Static Content

**Performance claims (varying evidence quality):**
- Motion graphics generate ~2.5x more engagement than static alternatives (Jungl Studio — methodology unclear)
- Instagram Reels (1.23% engagement) beat photos (0.70%) and carousels (0.99%) (Social Insider benchmarks)
- Reels reach ~2.35x more people than single-image posts (2026 data)
- Social videos shared 1,200% more than text+image combined (widely cited; original source unclear)

**Cognitive science basis:**
- Movement triggers involuntary attention (pre-attentive processing) — the brain literally cannot ignore motion in the visual field the way it can ignore static elements
- Peripheral motion detection is a survival mechanism repurposed for media consumption
- This is the UPSTREAM mechanism that all "add motion" advice derives from

**Platform-specific:**
- 80% of social videos watched on mute — visual motion must communicate without audio
- Instagram's AI now analyzes visual elements, motion, and on-screen text for content categorization
- Looping animations boost watch time (rewatch trigger), which boosts algorithmic distribution

### 4B. Motion Graphics Specifically (Not Just Filmed Content)

- Kinetic typography sees 42% higher completion rate vs static text overlays (influencers-time.com; original study not traceable)
- Character animation and motion elements drive more social sharing (practitioner consensus)
- Short-form animation delivers messages quickly with higher watch-to-end rates (Spiel Creative)
- Motion graphics' visual-first approach aligns with mute-viewing behavior

**Gap:** There is very little CONTROLLED research comparing motion graphics Reels to filmed-content Reels with matched topics, lengths, and audiences. Most claims are either cross-format comparisons (video vs photo) or anecdotal. The 42% completion rate claim for kinetic typography is widely cited but the original study is not traceable.

### 4C. What Would Disprove Motion Doctrine

If "talking head" filmed Reels consistently outperformed equivalent motion graphics Reels in the same niche (controlled for topic and audience), it would challenge the motion graphics advantage. The Emplifi finding that face+speech within 3 seconds boosts retention by 25% suggests filmed content has its own advantages that motion graphics may not replicate.

---

## Part 5: Typography — Kinetic vs Static Text

### 5A. Primary Sources

**Cognitive psychology:**
- Movement enhances recall by up to 40% compared to static presentation (cited across multiple sources; likely derived from dual-coding theory, Paivio 1971, and multimedia learning research, Mayer 2001)
- Information presented through multiple channels (visual + kinetic) encodes more deeply than single-channel (Mayer's Cognitive Theory of Multimedia Learning)
- Average person exposed to 4,000-10,000 brand messages per day; motion text breaks through where static cannot

**Performance data:**
- Kinetic typography: 50-200% engagement increase over static alternatives (influencers-time.com range; wide variance suggests context-dependence)
- Video completion rates improve with kinetic typography vs voiceover alone
- Content types that benefit most: explainers, testimonials, list-based, tutorials
- Strategic animation outperforms static captions; BUT poor animation reduces retention

**Text display requirements (from Part 3, applies here):**
- Text must be visible long enough to read at 150-180 wpm for mixed audiences
- Sans-serif fonts work best on mobile
- ~55 characters per line optimal for reading comprehension
- High contrast required: white on dark, or text with drop shadow
- Must be legible without audio (>50% watch silently)

### 5B. The Kinetic Typography Evidence Gap

The 42% completion rate improvement and 50-200% engagement increase figures are widely cited in marketing content but none trace back to a peer-reviewed study or a controlled experiment with published methodology. These are likely derived from:
1. A/B tests run by agencies or tools (not published)
2. Aggregated platform analytics from multiple campaigns
3. Confounded by other variables (content quality, topic, posting time)

**What exists upstream:** Mayer's multimedia learning principles (2001) and Paivio's dual-coding theory (1971) provide the cognitive science foundation. The specific performance numbers for social media kinetic typography are practitioner-generated, not academically validated.

---

## Part 6: Production Quality — Professional Feel

### 6A. What Instagram Penalizes (Confirmed)

- **Watermarks from competing platforms** (especially TikTok): Instagram has confirmed they down-rank content with visible watermarks. This is a BINARY penalty.
- **Low resolution/blurry content**: High-quality video receives up to 30% more engagement; Instagram's algorithm favors content that keeps viewers watching rather than scrolling past degraded frames
- **Dynamic quality adjustment**: Instagram renders video at lower quality if it stops being watched, then re-renders at higher quality if views resume. Quality is a SIGNAL of expected engagement, not just a viewer experience issue.

### 6B. Technical Specifications (Instagram Recommended)

| Parameter | Recommended | Source |
|-----------|------------|--------|
| Resolution | 1080 x 1920 pixels (9:16) | Instagram specs |
| Frame rate | 30 fps (29.97 fps) | Instagram specs; 60fps optional |
| Codec | H.264 (MP4 container) | Universal recommendation |
| Bitrate | Platform-dependent; upload at highest quality and let Instagram compress | Multiple sources |

### 6C. Quality Signals the Algorithm Likely Uses

Based on Meta's AI content understanding capabilities (confirmed in 2026):
- Visual clarity / resolution detection
- On-screen text legibility
- Audio quality analysis
- Watermark detection (confirmed)
- Content originality assessment (repost detection confirmed)
- Production style matching to user preferences (UTIS model, Jan 2026)

**Important:** Meta's UTIS model explicitly includes "production style" as a dimension of user interest matching. This means production quality is not just a binary pass/fail — it is matched to user preferences. A lo-fi aesthetic may score well with audiences who prefer that style.

### 6D. What Would Disprove Production Quality as a Signal

If lo-fi, "authentic" content consistently outperformed polished production in algorithmic distribution (not just engagement rate), it would suggest the algorithm doesn't favor production quality per se, but rather audience-content fit. The UTIS model's inclusion of "production style" as a matching dimension supports this more nuanced view.

---

## Part 7: Engagement Prediction — Watch-Through, Share, Save

### 7A. Benchmark Data (2025-2026)

**Completion rates:**
- Short-form videos under 90 seconds: ~50% average viewer retention
- Instagram Reels: 30-50% completion rate range (higher for shorter Reels)
- TikTok: 60-70% average completion (shorter average video length)
- "Excellent" threshold: >70% completion
- TikTok algorithmic boost threshold: 75%+ completion
- 59% of short videos watched for 41-80% of duration
- 30% of short videos have average watch rate >81%

**3-second hold rate:**
- >60% hold rate = strong distribution signal (5-10x reach multiplier, practitioner consensus)
- <40% hold rate = suppressed distribution

**Share rates:**
- 694,000 Instagram Reels sent via DM per minute (Metricool data)
- Humor-driven Reels achieve 30% higher share rate
- Share-through-DM represents active effort — stronger signal than passive engagement

**Engagement rates by format (Social Insider 2026):**
- Reels: ~1.23% per post
- Carousels: ~0.99% per post
- Photos: ~0.70% per post

### 7B. What the Algorithm Predicts (Meta's Model)

Based on Meta's published architecture, the Reels ranking system predicts:
1. **Probability of watching** (will the user watch, and for how long?)
2. **Probability of engagement** (like, comment, share, save)
3. **True interest alignment** (UTIS model — does content match user's stated interests?)
4. **Negative signals** (skip, "not interested", report)

These predictions are combined into a relevance score. The system predicts BEFORE showing the content, based on:
- Content features (visual, audio, text, length, similarity to other content)
- User features (history, preferences, social graph)
- Context features (time of day, device, session state)

### 7C. The Prediction Loop

The engagement prediction dimension of a scoring matrix is fundamentally different from the other five dimensions (Hook, Pacing, Motion, Typography, Quality). Those five are INPUT features — attributes of the content itself. Engagement prediction is the OUTPUT — what the algorithm expects will happen based on those inputs.

A scoring matrix that includes engagement prediction is essentially trying to replicate what Meta's multi-stage ranking model does: predict engagement from content features. The difference is that Meta has billions of data points and the scoring matrix has heuristics.

---

## Part 8: Source Taxonomy — Where Scoring Criteria Come From

### Tier 1: Meta/Instagram Official Sources

| Source | What It Provides | URL |
|--------|-----------------|-----|
| Adam Mosseri public statements (Jan 2025) | Top 3 ranking signals confirmed | Various (Instagram, interviews) |
| Meta Transparency Center — Reels Chaining AI System Card | Multi-stage ranking process, signal categories | transparency.meta.com |
| Meta Engineering Blog — UTIS Model (Jan 2026) | True interest beyond behavioral signals; production style as matching dimension | engineering.fb.com |
| Meta Engineering Blog — Instagram 1000 Models (May 2025) | Ranking funnel architecture | engineering.fb.com |
| Facebook Business — "Capturing Attention in Feed" | 1.7s mobile / 2.5s desktop attention window | facebook.com/business |
| Instagram algorithm "Your Algorithm" launch (Dec 2025) | Topic clarity, user control over recommendations | TechCrunch reporting |

### Tier 2: Academic/Research Sources

| Source | What It Provides |
|--------|-----------------|
| Kahneman, "Thinking, Fast and Slow" | System 1/System 2 cognitive framework for why hooks work |
| Mayer, Cognitive Theory of Multimedia Learning (2001) | Multi-channel encoding superiority (foundation for kinetic typography claims) |
| Paivio, Dual-Coding Theory (1971) | Visual+verbal encoding advantage |
| Nielsen attention effectiveness research | Sub-2-second video impression impact data |
| Emplifi (10,110 Reels study) | Face/speech within 3s retention data |
| Microsoft Canada attention span report (2015) | DEBUNKED as primary source; cited Statistic Brain, not their own research |
| UC Irvine + Microsoft screen attention study | Screen attention decline from 2.5 min to 47 seconds |
| Tandfonline viewport logging study (2025) | Eye-tracking validation for social media attention measurement |

### Tier 3: Industry/Practitioner Sources

| Source | What It Provides | Reliability |
|--------|-----------------|-------------|
| Social Insider | Engagement benchmarks by format | High (large dataset) |
| Hootsuite | Algorithm analysis, best practices | Medium (aggregator) |
| Buffer | Algorithm guide, creator tips | Medium |
| OpusClip | Hook formulas, pacing data | Medium |
| Metricool | Share rate data (694K DMs/minute) | Medium |
| Influencers-time.com | Kinetic typography performance claims | Low (unverified numbers) |
| Jungl Studio | Motion graphics 2.5x engagement claim | Low (methodology unclear) |

### Tier 4: Derivative/Aggregated Sources

Most "Instagram algorithm guide 2026" articles (Clixie, SocialBotify, OrangeMonke, etc.) aggregate from Tiers 1-3 without adding new data. They are useful for cross-referencing but not as primary sources.

---

## Part 9: Gap Analysis — What We Don't Know

1. **No controlled studies** comparing motion graphics Reels to filmed-content Reels with matched variables. All comparisons are cross-format (video vs photo) or anecdotal.

2. **Kinetic typography performance numbers** (42% completion boost, 50-200% engagement increase) are not traceable to published studies. They are practitioner-generated, likely from aggregated campaign data.

3. **Exact algorithmic weights** for saves vs likes vs shares are not published by Meta. The 1.7x save weight is a single-source claim.

4. **UTIS model impact on organic content ranking** is unclear. Published research covers Facebook Reels; applicability to Instagram Reels is assumed but not confirmed in published papers.

5. **"Your Algorithm" feature impact** on content distribution is too new (Dec 2025) for performance data to exist.

6. **Production style matching** — Meta's UTIS model includes this, but how "production quality" interacts with audience preference (does polished content always win, or does the algorithm match lo-fi to lo-fi-preferring users?) is unknown.

7. **AI content understanding specifics** — Meta confirmed their AI analyzes visuals, on-screen text, voiceover, and video clips, but the specific features extracted and their weights in ranking are not published.

---

## Part 10: Implications for Scoring Matrix Design

A scoring matrix with the six dimensions (Hook, Pacing, Visual Motion, Typography, Production Quality, Engagement Prediction) maps to upstream sources as follows:

| Dimension | Strongest Upstream Source | Evidence Quality |
|-----------|-------------------------|-----------------|
| Hook | Facebook 1.7s research + Instagram 3s hold metric + Kahneman System 1 | MEDIUM-HIGH (Facebook source not fully public; 3s metric is practitioner-derived) |
| Pacing | Reading speed research (200-250 wpm) + video editing retention data + platform analytics | MEDIUM (convergent evidence, no single study) |
| Visual Motion | Pre-attentive processing (cognitive science) + format comparison data (Social Insider) | MEDIUM (mechanism is strong; performance numbers are weak) |
| Typography | Mayer multimedia learning + Paivio dual-coding + practitioner A/B data | MEDIUM-LOW (theory is strong; social media specific numbers are unverified) |
| Production Quality | Meta watermark penalty (confirmed) + UTIS production style matching + resolution/engagement correlation | MEDIUM (binary penalties confirmed; quality-as-signal is indirect) |
| Engagement Prediction | Meta ranking system architecture + completion rate benchmarks + signal hierarchy | HIGH for the framework; LOW for specific thresholds |

The scoring matrix is essentially a heuristic proxy for Meta's multi-stage ranking model. Its accuracy depends on how well the six dimensions capture the features Meta's models actually use. The UTIS model (Jan 2026) suggests Meta is moving BEYOND purely behavioral signals toward stated user interest, which a content-side scoring matrix cannot directly measure.
