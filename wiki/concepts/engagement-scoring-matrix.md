# Engagement Scoring Matrix

> A six-dimension scoring framework (Hook, Pacing, Visual Motion, Typography, Production Quality, Engagement Prediction) that serves as a heuristic proxy for Meta's multi-stage ranking model. The first five dimensions are INPUT features (content attributes); the sixth (Engagement Prediction) is the OUTPUT (what the algorithm expects will happen based on those inputs).

**Confidence:** MEDIUM
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### The Six Dimensions and Their Upstream Evidence

| Dimension | Strongest Upstream Source | Evidence Quality |
|-----------|-------------------------|-----------------|
| Hook | Facebook 1.7s research + Instagram 3s hold metric + Kahneman System 1 | MEDIUM-HIGH |
| Pacing | Reading speed research (200-250 wpm) + video editing retention data + platform analytics | MEDIUM |
| Visual Motion | Pre-attentive processing (cognitive science) + format comparison data (Social Insider) | MEDIUM |
| Typography | Mayer multimedia learning + Paivio dual-coding + practitioner A/B data | MEDIUM-LOW |
| Production Quality | Meta watermark penalty (confirmed) + UTIS production style matching + resolution/engagement correlation | MEDIUM |
| Engagement Prediction | Meta ranking system architecture + completion rate benchmarks + signal hierarchy | HIGH for framework; LOW for specific thresholds |

### Dimension 1: Hook (First 1-2 Seconds)

**Scoring basis:**
- 1.7s mobile attention window (Facebook internal research, circa 2016). [VERIFIED -- original not publicly accessible but widely corroborated]
- 3-second hold rate: >60% retention = 5-10x reach multiplier. [VERIFIED -- practitioner consensus]
- Emplifi data (n=10,110): Face within 3s = +10% 10-second retention. Human speech within 3s = +25% retention, +5.6% engagement vs music-only. [VERIFIED]
- System 1 cognitive processing (Kahneman) is the mechanism: hooks must be immediate and pattern-interrupting. [VERIFIED]

### Dimension 2: Pacing

**Scoring basis:**
- Average silent reading: 200-250 wpm. Comfortable comprehension: 150-180 wpm. [VERIFIED]
- Text display minimum: 13 characters/second. [VERIFIED]
- High-performing shorts: one cut every 2-4 seconds (OpusClip). [VERIFIED]
- 3-5 seconds per shot before attention wavers (general video editing research). [VERIFIED]
- Static shot >4 seconds = danger zone for drop-off. [VERIFIED -- practitioner consensus]
- Build-and-release rhythm outperforms monotonous rhythm. [VERIFIED]

### Dimension 3: Visual Motion

**Scoring basis:**
- Movement triggers involuntary attention (pre-attentive processing) -- a survival mechanism. [VERIFIED -- cognitive science]
- Motion graphics generate ~2.5x more engagement than static alternatives. [THEORETICAL -- Jungl Studio; methodology unclear]
- Reels reach ~2.35x more people than single-image posts (2026 data). [VERIFIED -- Social Insider benchmarks]
- 80% of social videos watched on mute -- visual motion must communicate without audio. [VERIFIED]
- Looping animations boost watch time (rewatch trigger). [VERIFIED]
- Kinetic typography sees 42% higher completion rate vs static text overlays. [THEORETICAL -- influencers-time.com; original study not traceable]

**Critical gap:** There is very little CONTROLLED research comparing motion graphics Reels to filmed-content Reels with matched topics, lengths, and audiences. The 42% and 2.5x figures are widely cited but not traceable to published studies. [VERIFIED -- gap confirmed]

### Dimension 4: Typography

**Scoring basis:**
- Mayer's Cognitive Theory of Multimedia Learning (2001): multi-channel encoding superiority. [VERIFIED -- peer-reviewed]
- Paivio's Dual-Coding Theory (1971): visual + verbal encoding advantage. [VERIFIED -- peer-reviewed]
- Movement enhances recall by up to 40% compared to static presentation. [THEORETICAL -- likely derived from dual-coding theory, specific social media numbers unverified]
- Kinetic typography: 50-200% engagement increase over static alternatives. [THEORETICAL -- wide variance, practitioner-generated, no peer-reviewed source]
- Sans-serif fonts work best on mobile. [VERIFIED]
- ~55 characters per line optimal for reading comprehension. [VERIFIED]
- Minimum 42px font at 1080px width, 4.5:1 contrast ratio. [VERIFIED]
- Strategic animation outperforms static captions; BUT poor animation reduces retention. [VERIFIED]

**The evidence gap:** The 42% completion rate improvement and 50-200% engagement increase figures are widely cited in marketing content but none trace back to a peer-reviewed study or a controlled experiment with published methodology. These are practitioner-generated, likely from aggregated campaign data. [VERIFIED -- gap confirmed]

### Dimension 5: Production Quality

**Scoring basis:**
- Watermarks from competing platforms: confirmed binary penalty from Instagram. [VERIFIED]
- Low resolution/blurry content: high-quality video receives up to 30% more engagement. [VERIFIED]
- Dynamic quality adjustment: Instagram renders at lower quality if views drop, re-renders if views resume. [VERIFIED]
- UTIS model includes "production style" as a matching dimension -- production quality is matched to user preferences, not just a pass/fail gate. [VERIFIED -- Meta Engineering Blog, Jan 2026]

**Technical specs:**
| Parameter | Recommended | Source |
|-----------|------------|--------|
| Resolution | 1080 x 1920 pixels (9:16) | Instagram specs |
| Frame rate | 30 fps (29.97 fps) | Instagram specs |
| Codec | H.264 (MP4 container) | Universal recommendation |

### Dimension 6: Engagement Prediction

This dimension is fundamentally different from the other five. Hook, Pacing, Motion, Typography, and Quality are INPUT features -- attributes of the content itself. Engagement Prediction is the OUTPUT -- what the algorithm expects will happen. [VERIFIED]

**Completion rate benchmarks:**
- Short-form videos under 90 seconds: ~50% average viewer retention. [VERIFIED]
- Instagram Reels: 30-50% completion rate range (higher for shorter Reels). [VERIFIED]
- TikTok: 60-70% average completion (shorter average video length). [VERIFIED]
- "Excellent" threshold: >70% completion. [VERIFIED]
- 59% of short videos watched for 41-80% of duration. [VERIFIED]

**3-second hold rate benchmarks:**
- >60% hold rate = strong distribution signal (5-10x reach multiplier). [VERIFIED -- practitioner consensus]
- <40% hold rate = suppressed distribution. [VERIFIED -- practitioner consensus]

**Share rate benchmarks:**
- 694,000 Instagram Reels sent via DM per minute (Metricool data). [VERIFIED]
- Humor-driven Reels achieve 30% higher share rate. [VERIFIED]

**Engagement rates by format (Social Insider 2026):**
- Reels: ~1.23% per post. [VERIFIED]
- Carousels: ~0.99% per post. [VERIFIED]
- Photos: ~0.70% per post. [VERIFIED]

### The Prediction Loop Problem

A scoring matrix that includes engagement prediction is essentially trying to replicate what Meta's multi-stage ranking model does: predict engagement from content features. The difference is that Meta has billions of data points and the scoring matrix has heuristics. [VERIFIED]

Meta's system predicts: [VERIFIED]
1. Probability of watching (will the user watch, and for how long?)
2. Probability of engagement (like, comment, share, save)
3. True interest alignment (UTIS model)
4. Negative signals (skip, "not interested", report)

### Source Taxonomy

**Tier 1: Meta/Instagram Official** -- Adam Mosseri statements, Meta Transparency Center, Meta Engineering Blog. Highest reliability. [VERIFIED]

**Tier 2: Academic/Research** -- Kahneman, Mayer, Paivio, Nielsen, Emplifi (n=10,110). Peer-reviewed or large-sample. [VERIFIED]

**Tier 3: Industry/Practitioner** -- Social Insider (high), Hootsuite/Buffer (medium), OpusClip/Metricool (medium), influencers-time.com/Jungl Studio (low). Varying methodology. [VERIFIED]

**Tier 4: Derivative** -- "Instagram algorithm guide 2026" articles that aggregate from Tiers 1-3 without adding new data. [VERIFIED]

---

## Operational Rules

1. **When scoring content, weight Hook and Pacing highest** -- these two dimensions have the strongest upstream evidence (Mosseri-confirmed signals + Emplifi large-sample data), while Typography and Visual Motion rely on unverified practitioner claims.

2. **When evaluating visual motion claims, treat the 42% and 2.5x figures as directional, not precise** -- these numbers are not traceable to published studies and likely come from aggregated campaign data with confounded variables.

3. **When scoring production quality, treat watermark detection as binary (pass/fail) and everything else as continuous** -- watermarks are a confirmed penalty; resolution and style are matched to audience preferences via UTIS.

4. **When using the matrix for engagement prediction, compare against platform-specific benchmarks** -- Instagram Reels 30-50% completion range and >60% 3-second hold rate are the operational thresholds, because these derive from platform measurement data.

5. **When scoring typography, verify that text display times meet the 13 characters/second minimum** -- this is the one typography metric with solid cognitive science backing, unlike the engagement multiplier claims.

6. **When a piece scores well on inputs (dimensions 1-5) but performs poorly on engagement, investigate audience-content fit** -- the UTIS model shows Meta is moving beyond content quality to interest matching, meaning a well-made Reel can still underperform if served to the wrong audience.

---

## Deep Reference

- **When** weighting scoring dimensions → **read** `reels_engagement_scoring_research_2026.md` §Algorithm Signal Hierarchy **for** Mosseri-confirmed signal weights (watch time > sends > likes > saves > comments) + follower vs non-follower distinction
- **When** scoring text card timing → **read** `reels_engagement_scoring_research_2026.md` §Pacing **for** text timing formula (3s + 0.5-0.7s per word) + optimal total length (15-30s)
- **When** checking hook effectiveness → **read** `reels_engagement_scoring_research_2026.md` §Hook **for** specific hook types (motion in frame zero, triple hook visual+text+audio, contrarian/pattern-interrupt) + 1.7s/3s threshold reconciliation
- **When** accounting for 2025-2026 algorithm changes → **read** `reels_engagement_scoring_research_2026.md` §Algorithm Updates **for** original content boost (+10pp US Q4 2025), hashtag deprioritization, saves gaining weight (Mar 2026), "Your Algorithm" feature
- **When** scoring intentionally lo-fi content → **read** `reels_engagement_scoring_research_2026.md` §Production Quality **for** the lo-fi exception (lo-fi can score well if matched to audience preference)
- **When** evaluating motion vs filmed content → **read** `reels_engagement_scoring_research_2026.md` §Visual Motion **for** counterevidence that face+speech filmed content may outperform motion graphics (Emplifi 25%)

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/reels_engagement_scoring_research_2026.md` | All six dimensions with upstream evidence, uncertainty register, source taxonomy, gap analysis, benchmark data, Meta system architecture |

---

## Related Concepts

- [[reels-algorithm-signals]] — DEPENDS_ON: the algorithm signals that the scoring matrix attempts to proxy
- [[hook-first-half-second]] — DEPENDS_ON: detailed evidence for dimension 1 (Hook)
- [[reels-pacing-structure]] — DEPENDS_ON: detailed evidence for dimension 2 (Pacing)
- [[voiceover-audio-design]] — DEPENDS_ON: audio design rules that affect dimensions 1, 2, and 5
- [[competitive-landscape-animation]] — INFORMS: the competitive landscape reveals which market tiers actually optimize for these scoring dimensions and where the gap exists between generic template output and crafted content
- [[semantic-demand-patterns]] — INFORMS: format-topic matching from demand patterns should feed engagement prediction (dimension 6); reference vs validation mode affects which scoring dimensions matter most
- [[vertical-whitespace-atlas]] — INFORMS: per-vertical whitespace analysis identifies which content formats score well on the scoring matrix dimensions and which saturated formats score poorly despite high production quality
- [[twitter-x-api]] — INFORMS: X engagement data (likes, RTs, bookmarks, video completion) provides a second platform's signal channel to validate or challenge Instagram-derived scoring weights
- [[twitter-x-growth-mechanics]] — INFORMS: X algorithm signal weights (replies 150x, bookmarks 20x likes) provide a cross-platform comparison to Instagram-derived scoring, showing where signal hierarchies diverge (X rewards conversation depth; Instagram rewards sends)

---

## Open Questions

- How well do the six dimensions actually predict Instagram's ranking model output? No validation study exists comparing matrix scores to actual Reel performance.
- Should the Typography dimension be split into "kinetic typography" and "static text legibility"? The evidence base for these two sub-dimensions is very different (unverified for kinetic, solid for legibility).
- As Meta's UTIS model evolves, will content-side scoring become less predictive? The UTIS model explicitly acknowledges behavioral signals alone are insufficient, suggesting audience matching may eventually dominate content features.
- What is the interaction effect between dimensions? (e.g., Does strong motion compensate for weak hooks? Does voice quality affect pacing scores?) No research addresses dimension interactions.
