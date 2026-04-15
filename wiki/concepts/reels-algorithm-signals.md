# Reels Algorithm Signals

> The Instagram Reels ranking system uses a multi-stage funnel (Sourcing, Early-Stage Ranking, Late-Stage Ranking) that scores ~100 candidate reels using behavioral signals, content features, and user interest matching to determine distribution to both connected (follower) and unconnected (Explore/Reels tab) audiences.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 2 raw files, 0 memory files

---

## Core Findings

### Signal Hierarchy (Confirmed by Adam Mosseri, January 2025)

1. **Watch time** (duration + completion %) is the #1 signal for both connected and unconnected distribution. [VERIFIED]
2. **Sends/DM shares per reach** is the most powerful signal for reaching NEW (unconnected) audiences. [VERIFIED]
3. **Likes per reach** is slightly more important for connected (follower) distribution. [VERIFIED]

The hierarchy differs by context:
- For followers seeing your content: Likes > Sends [VERIFIED]
- For non-followers discovering your content: Sends > Likes [VERIFIED]
- Watch time is #1 in both contexts [VERIFIED]

### Extended Signal Weight Table

| Signal | Weight | Context | Source Quality |
|--------|--------|---------|---------------|
| Watch time (duration + completion %) | Highest | Both connected + unconnected | Mosseri confirmed |
| Sends/DM shares per reach | Very High | Strongest for unconnected reach | Mosseri confirmed |
| Likes per reach | High | Strongest for connected reach | Mosseri confirmed |
| Saves | High | Claimed 1.7x weight of likes; indicates reference value | Practitioner consensus, not Meta-confirmed |
| Substantive comments | Medium | Word count, questions, mentions weighted > emoji/generic | Multiple practitioner sources |
| Rewatches | Medium | Re-entering the reel signals deep interest | Practitioner sources |
| Profile visits after viewing | Medium | Signals content-to-creator curiosity | Buffer, Hootsuite analyses |

The 1.7x save weight over likes is a single-source claim (Social Tradia) and is NOT confirmed by Meta. [THEORETICAL]

### 3-Second Hold Rate Threshold

Instagram's analytics system measures retention at 3 seconds as a distribution threshold. [VERIFIED]
- >60% retention at 3 seconds correlates with 5-10x reach vs. <40% retention. [VERIFIED -- practitioner consensus across 10+ sources]
- This is the PLATFORM MEASUREMENT that the 1.7s creative advice maps to. [VERIFIED]

### Meta's Multi-Stage Ranking Architecture

The ranking funnel operates as: Sourcing (retrieval) -> Early-Stage Ranking (ESR) -> Late-Stage Ranking (LSR). [VERIFIED -- Meta Transparency Center system card]

Input signals include: reel length, similarity to previously engaged content, user behavior history (watch, like, skip, share, save), and 3-second watch threshold. [VERIFIED]

Instagram runs ~1000 models across the ranking funnel, with knowledge-sharing across Feed, Story, and Reels surfaces via Meta Lattice architecture. [VERIFIED -- Meta Engineering Blog, May 2025]

### True Interest (UTIS) Model

Meta's User True Interest Survey (UTIS) model goes beyond behavioral signals to capture "true interest" by asking random users "To what extent does this video match your interests?" on a 1-5 scale. [VERIFIED -- Meta Engineering Blog, January 2026]

Key insight: effective interest matching goes beyond topic alignment -- includes audio, production style, mood, and motivation. [VERIFIED]

Accuracy improved from 59.5% to 71.5%; precision from 48.3% to 63.2%. Deployed in both ESR and LSR stages. [VERIFIED]

This means production quality is not just a binary pass/fail -- it is matched to user preferences. A lo-fi aesthetic may score well with audiences who prefer that style. [VERIFIED]

### Originality Scoring

Instagram increased original content prevalence in US by 10 percentage points in Q4 2025. [VERIFIED]
- Reposted content is labeled and penalized. [VERIFIED]
- Aggregator accounts suppressed. [VERIFIED]
- Hashtags deprioritized as ranking signals in favor of interest/keyword-based relevance. Users can no longer follow hashtags. [VERIFIED]

### December 2025 Algorithm Updates

1. **"Your Algorithm" feature** (Dec 10, 2025): Users can review/edit topic preferences, add new interests, down-rank topics. Makes topical clarity in content more important for creators. [VERIFIED]
2. **AI content understanding improved**: Meta's AI now analyzes visuals, on-screen text, voiceover audio, and video clips to categorize content and match to users. [VERIFIED]

### March 2026 Update

- Stronger weight on relationship signals -- accounts that users interact with via DMs, comments, story replies ranked higher. [VERIFIED]
- Saves and repeat views gained importance relative to likes/comments. [VERIFIED]

### Algorithm Prediction Model

The system predicts BEFORE showing content, based on: [VERIFIED]
1. Probability of watching (will the user watch, and for how long?)
2. Probability of engagement (like, comment, share, save)
3. True interest alignment (UTIS model)
4. Negative signals (skip, "not interested", report)

These are combined into a relevance score using content features (visual, audio, text, length), user features (history, preferences, social graph), and context features (time of day, device, session state). [VERIFIED]

### What Instagram Penalizes (Confirmed)

- **Watermarks from competing platforms** (especially TikTok): confirmed down-ranking. Binary penalty. [VERIFIED]
- **Low resolution/blurry content**: high-quality video receives up to 30% more engagement. [VERIFIED]
- **Dynamic quality adjustment**: Instagram renders video at lower quality if it stops being watched, then re-renders at higher quality if views resume. Quality is a SIGNAL of expected engagement. [VERIFIED]

---

## Operational Rules

1. **When creating Reels, optimize for watch time first** -- it is the #1 signal in both connected and unconnected distribution, because Mosseri confirmed it publicly and no subsequent update has changed this.

2. **When designing for unconnected reach (discovery), optimize for DM sends** -- sends per reach is the strongest signal for reaching non-followers, because the algorithm weights content that generates active sharing effort higher than passive engagement.

3. **When evaluating early retention, target >60% hold at 3 seconds** -- this threshold correlates with 5-10x reach multiplier, because Instagram explicitly measures the 3-second mark as a distribution gate.

4. **When publishing, never include competing platform watermarks** -- this is a confirmed binary penalty that suppresses distribution regardless of content quality.

5. **When uploading, use 1080x1920 at 30fps in H.264/MP4** -- upload at highest quality and let Instagram compress, because the platform's dynamic quality adjustment uses resolution as a signal of expected engagement.

6. **When planning content strategy, prioritize originality** -- reposted and aggregated content is penalized with confirmed 10 percentage point reduction in prevalence, because Instagram's AI now detects reposted content and labels it.

7. **When producing content, ensure topical clarity** -- the "Your Algorithm" feature (Dec 2025) lets users edit topic preferences, meaning clearly categorizable content gets matched to interested users more accurately.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/reels_engagement_scoring_research_2026.md` | Full signal hierarchy, Meta system card details, UTIS model, engagement benchmarks, production quality signals |
| `research-data/instagram_reels_best_practices_2025.md` | 3-second hold rate practitioner data, algorithm context for dental/medical, music/audio findings, Mosseri confirmation cross-reference |

---

## Related Concepts

- [[hook-first-half-second]] — INFORMS: the 1.7s attention window is the creative input that maps to the algorithm's 3s measurement gate
- [[engagement-scoring-matrix]] — INFORMS: operationalizes these algorithm signals into a scoring framework
- [[reels-pacing-structure]] — INFORMS: pacing rules derived from these algorithmic requirements
- [[voiceover-audio-design]] — INFORMS: audio design choices that affect the UTIS model's content understanding
- [[competitive-landscape-animation]] — INFORMS: the five-tier market landscape shows how different providers optimize (or fail to optimize) for these algorithm signals, exposing the gap between template tools and crafted content
- [[vertical-whitespace-atlas]] — INFORMS: per-vertical whitespace analysis identifies saturated formats that the algorithm penalizes through low engagement signals, and whitespace formats that exploit algorithm signals competitors ignore
- [[twitter-x-growth-mechanics]] — CONTRASTS: X algorithm rewards replies and author engagement (150x a like) while Instagram rewards sends/DM shares for discovery; the signal hierarchies are inverted, requiring different optimization per platform
- [[twitter-x-api]] — EXTENDS: X's algorithm signals differ from Instagram's but share watch-time primacy; X's video quartile metrics (playback_25/50/75/100) provide granular retention data that maps to the same completion-rate analysis used here

---

## Deep Reference

- **When** deciding whether to optimize for sends vs likes for a specific Reel → **read** `research-data/reels_engagement_scoring_research_2026.md` §1A (Official Meta Sources) **for** Mosseri's stated hierarchy (sends > likes for non-follower reach, likes > sends for follower reach, watch time #1 in both), the 3-second watch threshold explicitly measured by Meta's system, and the multi-stage ranking funnel architecture (Sourcing → ESR → LSR on ~100 candidates)
- **When** evaluating whether a claim about algorithm signals is reliable or marketing noise → **read** `research-data/reels_engagement_scoring_research_2026.md` §(Uncertainty Register) **for** confidence ratings per finding (saves carry 1.7x weight of likes = LOW confidence single source, kinetic typography +42% = LOW unverifiable, 8-second attention span = DEBUNKED)
- **When** designing content for the UTIS (Unified Training Inference System) content understanding model → **read** `research-data/reels_engagement_scoring_research_2026.md` §(Meta Engineering Blog) **for** how Meta's AI analyzes audio, text, and visual features to match content to user interests beyond behavioral signals, and why "production style" matching is a separate signal from engagement

---

## Open Questions

- How exactly does the UTIS model weight "production style" matching vs. raw engagement signals? The model acknowledges behavioral signals are insufficient, but the relative weights are unpublished.
- Does the UTIS model, published for Facebook Reels, apply identically to Instagram Reels? Assumed but not confirmed.
- How does the "Your Algorithm" feature (Dec 2025) actually affect distribution for creators? Too new for performance data.
- What specific features does Meta's AI extract from visual, text, and audio content for categorization? Confirmed to exist but weights unpublished.
- Does absolute watch time or completion rate matter more? Multiple sources treat completion rate as primary, but Mosseri's statements support watch time broadly. These may differ by reel length.
