# Wiki Changelog

Append-only. Each entry documents what changed and why.

---

## 2026-04-06 — Initial compilation

**Source corpus:** 47 research .md files + 15 memory/feedback files from 25 sessions
**Articles created:** 47 (32 concepts + 5 tools + 4 registers + 5 findings + 1 vertical atlas)
**Total size:** 740KB, 9,168 lines
**Cross-references:** 209 total, 49 unique targets, 0 broken links
**Skipped sources:** `video_audio_api_landscape_2026.md` (corrupted JSON dump), 6 .json data collections (already synthesized), 8 .py scripts (operational code)

**Compilation method:** 8 parallel agents, each assigned a thematic cluster:
- Agent 1-A: Animation Craft (C01-C08)
- Agent 1-B: Visual Theory + Health Comms (C09-C14, C25)
- Agent 1-C: Content Strategy + Market (C19-C21, C23-C24, C26, C31-C32)
- Agent 2-A: Cross-Domain + Neuroscience (C27-C30)
- Agent 2-B: Vertical Whitespace Atlas (V01)
- Agent 3-A: Tool References (T01-T05)
- Agent 3-B: Style Registers (R01-R04)
- Agent 4: Findings + AI Prompting (C15-C18, C22, F01-F05)

**Quality notes:**
- 3 source files were JSON conversation dumps (storytelling, photoreal, cartoon) — research content extracted from assistant responses
- All claims tagged [TESTED], [VERIFIED], or [THEORETICAL]
- Every article follows the standard template (concept statement, core findings, operational rules, source files, related concepts, open questions)
- Spot-checked: narrative-coherence, photoreal register, progressive-disclosure-pacing — all faithful to sources

## 2026-04-07 — Compiled: continuity-editing-scene-flow (C33)

- **New articles:** `concepts/continuity-editing-scene-flow.md` (replaced prior `editorial-continuity-craft.md` with comprehensive research)
- **Updated articles:** `index.md` (updated C33 entry to new filename)
- **Confidence changes:** None
- **Research scope:** 25+ web sources across continuity editing rules, invisible cut techniques, overlap editing, J/L-cut audio bridges, Murch blink theory, master filmmaker transition techniques (Spielberg, Kubrick, Scorsese, Nolan, Miyazaki), Pixar color scripts, Disney layout finaling, AI video continuity (Kling/Runway/Veo first/last frame references, character consistency prompt patterns)
- **Key additions vs prior version:** Detailed invisible cut methods (5 techniques), explicit frame-level overlap guidance, comprehensive AI application notes per technique, ambient sound/room tone as continuity layer, motivated vs unmotivated cut framework, storyboard-vs-shotlist encoding gap analysis, "Five Biggest Levers" framework preserved from prior version
- **Tested findings preserved:** v27/v29/v31/v32 operator feedback on rest-to-rest transitions carried forward

## 2026-04-08 — Ingested: twitter_x_growth_mechanics_2026.md

- **New articles:** `concepts/twitter-x-growth-mechanics.md` (C34) — X algorithm signal weights, Premium vs free platform split, cold start strategy, engagement velocity mechanics, TweepCred reputation scoring, content format performance, community post discovery, build-in-public patterns for creative AI accounts
- **Updated articles:** `index.md` (added C34), `concepts/engagement-scoring-matrix.md` (added backlink to C34), `concepts/hook-first-half-second.md` (added backlink to C34), `concepts/reels-algorithm-signals.md` (added backlink to C34), `concepts/semantic-demand-patterns.md` (added backlink to C34)
- **Confidence changes:** None
- **Contradictions:** None
- **Research scope:** 25+ web sources — Buffer 18.8M post analysis, Sprout Social 2026 statistics, X open-source algorithm code analysis, PostEverywhere 700K post analysis, multiple practitioner case studies and growth strategy guides

## 2026-04-08 — Ingested: twitter_api_v2_capabilities_2026.md

- **New articles:** `tools/twitter-x-api.md` (T07) — X API v2 programmatic posting capabilities, pay-per-use pricing model, media upload specs, engagement metrics, authentication, Python library (tweepy)
- **Updated articles:** `index.md` (added T07), `concepts/engagement-scoring-matrix.md` (added backlink to T07), `concepts/reels-algorithm-signals.md` (added backlink to T07), `concepts/semantic-demand-patterns.md` (added backlink to T07)
- **Confidence changes:** None
- **Contradictions:** None
- **Research scope:** Official docs.x.com API documentation, developer community posts, 10+ third-party pricing/capability analyses, tweepy library documentation

## 2026-04-09 — Integrity audit + ingested: ai_tool_community_engagement_2026.md

- **Fixes applied:**
  - Removed broken `[[feedback-never-hardcode-secrets]]` cross-reference from `tools/runway-gen4.md` (memory file, not wiki article) + removed knowledge-map row
  - Deleted orphaned `research-data/video_audio_api_landscape_2026.md` (corrupted JSON, documented as skipped)
  - Copied `twitter_hashtags_and_tool_accounts_2026.md` and `ai_tool_community_engagement_2026.md` from twitter-pipeline to wiki/research-data/
  - Updated C34 Source Files paths from `twitter-pipeline/tools/research-data/` to `research-data/` (wiki-local)
- **Updated articles:** `concepts/twitter-x-growth-mechanics.md` (C34) — full 23-tool market engagement ranking, media-only methodology, platform-community mismatch analysis, high-engagement content archetypes, reshare behavior classification
- **Audit result:** 51 articles, 48 research files (1 deleted), 272 valid cross-references, 100% bidirectional, 100% index match, 100% schema compliance
- **Research files:** 48 active (was 49, minus 1 deleted orphan, plus 2 new = 49, minus 1 deleted = 48)

## 2026-04-09 — Ingested: twitter_hashtags_and_tool_accounts_2026.md

- **Updated articles:** `concepts/twitter-x-growth-mechanics.md` (C34) — expanded hashtag section from 1-line penalty note to full analysis with live data, added AI tool account handles and resharing behavior analysis, added AI community hashtag activity tiers, added 5 new operational rules (10-14)
- **New articles:** none
- **Contradictions:** none -- new findings EXTEND existing C34 content (the "3+ hashtags = ~40% penalty" was already present as a one-liner; new data adds depth, context, and the critical finding that hashtags are now near-irrelevant for algorithmic discovery)
- **Research method:** 15+ web sources (algorithm analyses, platform studies) + Twitter API v2 live data (7 account lookups, 20-100 tweet analysis per account, 21 hashtag activity searches, 5 @mention engagement queries)
- **Key additions:**
  - Hashtags are near-irrelevant for discovery (Grok reads content semantically)
  - 21 AI community hashtags measured: #AIartcommunity is highest-engagement, #MadeWithRunway is dead
  - 6 AI tool accounts verified with handles, follower counts, reshare rates
  - Kling AI has highest reshare rate (63%), Recraft second (25% via QTs)
  - @ElevenLabs is the correct handle (NOT @elevenlabsio)
  - No dedicated Google Veo Twitter account exists
  - Creator programs documented: Kling Elite Creators, NextGen Initiative, Runway Big Ad Contest
  - @mention engagement data: @recraftai mentions generate highest community engagement (535 likes/10-tweet sample)
- **Confidence changes:** Hashtag section upgraded from single-line to detailed analysis with live data backing; overall article confidence remains MEDIUM
- **New open questions added:** 3 (hashtag boost primary source, Kling reshare threshold for small accounts, Recraft QT quality threshold)

## 2026-04-09 — Ingested: ai_tool_community_engagement_2026.md

- **Updated articles:** `concepts/twitter-x-growth-mechanics.md` (C34) — massively expanded tool engagement section from 6 tools to 23 tools, replaced 10-tweet sample with 30-40 tweet media-only methodology (860+ tweets total), added bookmark rate analysis, high-engagement content archetypes, platform-community mismatch finding, updated operational rules 12-14 and added rules 15-16
- **New articles:** none
- **Contradictions:** [PARTIAL CONTRADICTION] Previous Kling AI reshare rate was reported as 52% RT + 11% QT = 63% (from 100-tweet sample). New 50-tweet sample shows 24% RT + 14% QT = 39%. The discrepancy may be temporal (sampling different weeks) or sample-size noise. Both agree Kling is among the highest resharers; the exact rate varies. Operational rules updated to use the more conservative 39% figure. Previous @recraftai engagement claim (535 likes in 10-tweet sample) was based on all-mentions; new media-only methodology confirms Recraft's #2 position (22.2 avg likes) with no contradiction.
- **Research method:** Twitter API v2 recent search, media-only filter (has:media), 23 tool accounts verified, 860+ tweets collected, resharing behavior analyzed from last 50 tweets per account
- **Key additions:**
  - 17 new tool accounts added: @pika_labs, @hailuo_ai, @minimax_ai, @LumaLabsAI, @PixVerse_, @wavespeed_ai, @LeonardoAi, @midjourney, @bfl_ml, @freepik, @NightcafeStudio, @openai, @suno_ai_, @udiomusic, @MeshyAI, @TripoAI, @StabilityAI
  - Media-only vs all-mentions distinction quantified: 4-33x engagement difference, media-only is the decision-relevant metric
  - Bookmark rate per tool: MeshyAI (17.6), Recraft (13.9), ElevenLabs (13.2) are extreme outliers
  - High-engagement content archetypes: utility/workflow demos (3-10x vs art showcases), institutional credibility, complete creative works, challenge entries, prompt sharing
  - Platform-community mismatch: tools with small follower counts + high @mention engagement (Recraft, MeshyAI, WaveSpeed) have Twitter-native communities; tools with massive followers + low engagement (OpenAI, Midjourney, DeepMind) have communities elsewhere
  - @openai and @GoogleDeepMind reshare rates (34% and 22%) are entirely internal content -- zero user creative content reshared by either
  - Correct handles verified: @pika_labs (NOT @PikaArtHQ), @LeonardoAi (NOT @LeonardoAi_), @TripoAI (NOT @tripo3d), @hailuo_ai is the product account, @minimax_ai is the corporate account
  - Suno AI has fragmented/negligible Twitter presence across multiple handles
  - Priority matrix with 4 tiers (high engagement + high reshare, high engagement OR reshare, moderate, do not prioritize)
- **Confidence changes:** Tool engagement section upgraded from LOW (6 tools, 10-tweet samples) to MEDIUM (23 tools, 30-40 tweet media-only samples with pagination)
- **New open questions added:** 4 (MeshyAI outlier sensitivity, utility-over-art temporal stability, Hailuo reshare rate stability, Kling reshare rate discrepancy between samples)
