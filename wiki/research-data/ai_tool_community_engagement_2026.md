# AI Tool Community Engagement on Twitter/X -- @Mention Engagement Analysis

**Date:** 2026-04-09
**Methodology:** Twitter API v2 recent search (7-day window). Two search strategies per tool: (1) all @mention tweets excluding tool's own account and retweets, max 30-40 per tool; (2) media-only @mention tweets (has:media filter) to isolate showcase content from reply chatter. Resharing behavior analyzed from each tool account's last 50 tweets.
**Source count:** 23 tool accounts verified, 20 with engagement data, 860+ individual tweets analyzed
**API tier:** Basic (recent search, 7-day window only)

---

## Master Ranking: Engagement per @Mention (Media-Only Tweets)

This is the primary ranking. "Media-only" means the tweet contains an image or video -- these are showcase tweets where a user is tagging the tool to credit it for their creation. This filters out reply noise and isolates the signal that matters: **"I made this with [tool], look."**

| Rank | Handle | Tool Name | Category | N | Avg Likes | Median Likes | P90 Likes | Avg RT | Avg Reply | Avg Bookmarks | Avg Impressions | Max Likes | Followers | Reshare Rate | Reshares User Content? |
|------|--------|-----------|----------|---|-----------|-------------|-----------|--------|-----------|---------------|-----------------|-----------|-----------|-------------|----------------------|
| 1 | @MeshyAI | Meshy | 3D | 31 | 25.2 | 1 | 19 | 1.7 | 2.5 | 17.6 | 3,137 | 533 | 14,651 | 23% | Yes (RT+QT) |
| 2 | @recraftai | Recraft | image | 29 | 22.2 | 2 | -- | 3.5 | 1.4 | 13.9 | -- | 376 | 15,313 | 20% | Yes (QT w/ editorial) |
| 3 | @ElevenLabs | ElevenLabs | audio | 40 | 20.6 | 3 | 28 | 2.4 | 2.2 | 13.2 | 1,792 | 370 | 173,706 | 20% | Yes (selective RT) |
| 4 | @wavespeed_ai | WaveSpeed | video | 11 | 15.4 | 6 | 41 | 0.7 | 1.5 | 3.7 | 358 | 55 | 6,328 | 2% | No |
| 5 | @LumaLabsAI | Luma AI | video | 40 | 14.5 | 1 | 31 | 1.8 | 3.4 | 2.8 | 754 | 115 | 195,140 | 23% | Yes (RT+QT) |
| 6 | @pika_labs | Pika Labs | video | 38 | 11.0 | 1 | 23 | 2.5 | 0.8 | 1.4 | 389 | 270 | 146,836 | 4% | No (reply-only) |
| 7 | @hailuo_ai | Hailuo AI | video | 38 | 10.3 | 3 | 19 | 1.8 | 2.6 | 2.0 | 2,329 | 116 | 72,510 | 52% | Yes (heaviest RT) |
| 8 | @Kling_ai | Kling AI | video | 40 | 10.0 | 2 | -- | -- | -- | 0.3 | -- | 60 | 129,616 | 39% | Yes (RT+QT, "Creative Partners") |
| 9 | @StabilityAI | Stability AI | video/image | 14 | 8.9 | 3 | 17 | 0.6 | 1.6 | 0.6 | 645 | 70 | 252,219 | 8% | Rare |
| 10 | @LeonardoAi | Leonardo AI | image | 40 | 7.8 | 3 | 21 | 0.3 | 1.9 | 1.9 | 337 | 87 | 60,884 | 6% | Rare (QT only) |
| 11 | @ideogram_ai | Ideogram | image | 19 | 7.4 | 3 | 26 | 0.9 | 0.7 | 3.0 | 680 | 50 | 65,130 | 14% | Selective (RT+QT) |
| 12 | @bfl_ml | Black Forest Labs / Flux | image | 26 | 7.1 | 2 | 29 | 1.7 | 1.9 | 0.3 | 509 | 44 | 41,749 | 14% | Yes (RT only) |
| 13 | @runwayml | Runway | video | 40 | 6.8 | 1 | -- | -- | -- | 1.3 | -- | 68 | 272,549 | 12% | Selective (contest-driven) |
| 14 | @midjourney | Midjourney | image | 38 | 6.0 | 1 | 20 | 0.5 | 1.4 | 0.3 | 86 | 58 | 414,221 | 2% | No |
| 15 | @PixVerse_ | PixVerse | video | 39 | 6.2 | 1 | 9 | 1.0 | 1.8 | 0.5 | 97 | 126 | 26,572 | 42% | Yes (heavy QT) |
| 16 | @freepik | Freepik | image | 40 | 6.2 | 1 | 20 | 1.4 | 1.8 | 1.9 | 1,147 | 89 | 80,726 | 2% | No |
| 17 | @minimax_ai | MiniMax | video | 40 | 5.0 | 1 | 9 | 0.4 | 1.1 | 1.9 | 406 | 88 | 82,203 | 35% | Yes (QT-heavy) |
| 18 | @TripoAI | Tripo AI | 3D | 21 | 5.1 | 1 | 13 | 0.2 | 1.6 | 0.2 | 168 | 41 | 13,982 | 19% | Yes (QT) |
| 19 | @GoogleDeepMind | Google DeepMind / Veo | video | 40 | 3.5 | 0 | 7 | 0.7 | 0.8 | 1.4 | 378 | 74 | 1,393,472 | 22% | No (internal only) |
| 20 | @udiomusic | Udio | audio | 4 | 2.5 | 1 | 8 | 0.8 | 0.0 | 0.5 | 85 | 8 | 35,932 | 13% | Occasional RT |
| 21 | @NightcafeStudio | NightCafe | image | 40 | 1.2 | 1 | 3 | 0.0 | 0.0 | 0.0 | 14 | 4 | 22,670 | 0% | No |
| 22 | @openai | OpenAI / DALL-E | image | 40 | 0.9 | 0 | 3 | 0.1 | 0.2 | 0.2 | 71 | 12 | 4,708,633 | 34% | No (internal only) |
| 23 | @suno_ai_ | Suno AI | audio | 11 | 0.1 | 0 | 0 | 0.0 | 0.8 | 0.0 | 6 | 1 | 2,081 | -- | Unknown (no tweets) |

**Note:** Cells marked "--" indicate data collected in a separate batch where that specific metric was not captured; the primary metrics (avg likes, max likes, bookmarks) are complete for all tools.

---

## Finding 1: Tier Classification by Engagement-per-Tag

### Tier 1 -- HIGH engagement return per @mention (avg likes >= 10)

| Tool | Category | Avg Likes | Key Driver | Action |
|------|----------|-----------|------------|--------|
| @MeshyAI | 3D | 25.2 | Vibe-coding crossover (533-like top tweet was ThreeJS + Meshy). Bookmark rate is extreme (17.6/tweet) -- people save 3D workflows. | Tag on any 3D asset showcase. Bookmark-bait. |
| @recraftai | image | 22.2 | Curatorial QT culture. Recraft QTs user work with design commentary. Bookmark rate 13.9/tweet. | Tag with high-craft design work. They will QT. |
| @ElevenLabs | audio | 20.6 | Institutional attention (Stanford lecture = 370 likes). Bookmark rate 13.2/tweet. Engineering/product crossover. | Tag with novel integrations, not simple TTS demos. |
| @wavespeed_ai | video | 15.4 | Small but engaged community. Median likes = 6 (highest of any tool). Seedance content performing well. | Tag when using Seedance. Small community = less noise. |
| @LumaLabsAI | video | 14.5 | Uni-1 launch driving discussion. QTs happening. | Tag with Luma video showcases. |
| @pika_labs | video | 11.0 | Music video content drives top engagement (270 likes). | Tag with creative/music video content. |
| @hailuo_ai | video | 10.3 | Heaviest resharer (52% of their tweets are user RTs). Guaranteed amplification. | Tag everything. They will RT. |
| @Kling_ai | video | 10.0 | "Creative Partners" program. 39% reshare rate. | Tag and apply to Creative Partners. |

### Tier 2 -- MODERATE engagement return (avg likes 5-10)

| Tool | Category | Avg Likes | Key Pattern |
|------|----------|-----------|-------------|
| @StabilityAI | video/image | 8.9 | Low reshare (8%). Engagement comes from brand recognition. |
| @LeonardoAi | image | 7.8 | Moderate community. Low reshare (6%). |
| @ideogram_ai | image | 7.4 | Product innovation drives spikes (Layerize = 50 likes). |
| @bfl_ml | image | 7.1 | Flux community is technical. RT rate 14%. |
| @runwayml | video | 6.8 | Contest-driven amplification. Low organic reshare (12%). |
| @midjourney | image | 6.0 | Massive community but no resharing (2%). Engagement is purely organic. |
| @PixVerse_ | video | 6.2 | Heavy QT resharing (42%) but small community. Challenge entries spike. |
| @freepik | image | 6.2 | Surprisingly engaged community. No resharing. |

### Tier 3 -- LOW engagement return (avg likes < 5)

| Tool | Category | Avg Likes | Why Low |
|------|----------|-----------|---------|
| @minimax_ai | video | 5.0 | Moderate. QT-heavy resharing (35%). |
| @TripoAI | 3D | 5.1 | Small community. QT resharing (19%). |
| @GoogleDeepMind | video | 3.5 | Corporate research account. Does not engage with user creative content. |
| @udiomusic | audio | 2.5 | Very small Twitter presence (4 media tweets in 7 days). |
| @NightcafeStudio | image | 1.2 | Dead community. Zero resharing. |
| @openai | image | 0.9 | Massive account but DALL-E is not the community driver. All reshares are internal. |
| @suno_ai_ | audio | 0.1 | Wrong/fragmented handle. Suno's Twitter presence is negligible. |

---

## Finding 2: Resharing Behavior Classification

### Who reshares user content and how?

| Behavior | Accounts | Reshare % | Implication |
|----------|----------|-----------|-------------|
| **Heavy RT** (retweet user content frequently) | @hailuo_ai (52%), @Kling_ai (39%), @MeshyAI (23%) | 23-52% | Highest probability of amplification. Just tag and post good work. |
| **Heavy QT** (quote-tweet with commentary) | @PixVerse_ (42%), @minimax_ai (35%), @LumaLabsAI (23%), @recraftai (20%), @TripoAI (19%) | 19-42% | QTs add their editorial voice. Better for credibility. |
| **Mixed RT+QT** | @ElevenLabs (20%), @bfl_ml (14%), @ideogram_ai (14%), @runwayml (12%), @udiomusic (13%) | 12-20% | Moderate. Selective about what they amplify. |
| **No resharing / Internal only** | @GoogleDeepMind (22% but all internal), @openai (34% but all internal), @pika_labs (4%), @midjourney (2%), @freepik (2%), @wavespeed_ai (2%), @NightcafeStudio (0%), @StabilityAI (8%) | 0-8% effective | Tagging will not produce amplification. Engagement is purely organic. |

### Key distinctions

- **@openai reshares 34%** but it is all internal (Codex team, executives, product accounts). ZERO user creative content reshared.
- **@GoogleDeepMind reshares 22%** but it is all research/internal (Gemma, AlphaProof, Nature papers). ZERO user Veo content reshared.
- **@pika_labs is 96% replies.** They respond to users in replies but do not reshare to their timeline.
- **@hailuo_ai is the single most active resharer of user creative content.** 52% of their tweets are user RTs.

---

## Finding 3: Bookmark Rate as Signal of Utility Value

The bookmark metric is a strong signal of "save for later" / reference value. Tools where mention tweets have high bookmark rates indicate the community treats tagged content as workflow reference, not just entertainment.

| Tool | Avg Bookmarks/Tweet | Interpretation |
|------|-------------------|----------------|
| @MeshyAI | 17.6 | Extremely high. 3D asset workflows are saved as references. |
| @recraftai | 13.9 | High. Design work is saved for inspiration/technique. |
| @ElevenLabs | 13.2 | High. Voice/audio integration content saved as how-to. |
| @wavespeed_ai | 3.7 | Moderate. Video generation prompts being saved. |
| @ideogram_ai | 3.0 | Moderate. Text-in-image technique saved. |
| @LumaLabsAI | 2.8 | Moderate. |
| @hailuo_ai | 2.0 | Moderate. |
| @LeonardoAi | 1.9 | Moderate. |
| @minimax_ai | 1.9 | Moderate. |
| @freepik | 1.9 | Moderate. |
| @pika_labs | 1.4 | Low-moderate. |
| @GoogleDeepMind | 1.4 | Research content bookmarked. |
| @runwayml | 1.3 | Low. |
| All others | <1.0 | Low -- content consumed but not saved. |

---

## Finding 4: High-Engagement Tweet Patterns

Analysis of the top 30 tweets by likes across all tools reveals these content archetypes:

| Pattern | Examples | Typical Likes | What Makes It Work |
|---------|----------|---------------|-------------------|
| **Vibe-coding + AI tool** | "Vibe coding with threeJS and @MeshyAI" (533 likes) | 100-500+ | Developer audience + AI tool crossover. Practical demo, not just art showcase. |
| **Institutional/academic credibility** | Stanford lecture featuring @ElevenLabs (370 likes) | 100-300+ | Authority figure or institution using the tool = legitimacy signal. |
| **Music/narrative creative work** | "Right Here, Right Now" music video with @pika_labs (270 likes) | 100-300 | Complete creative projects, not isolated clips. Finished work with emotional payload. |
| **Challenge/contest entries** | PixVerse KitKat challenge entry (126 likes) | 50-150 | Contest mechanic creates community attention. PixVerse, Kling, and Runway all run these. |
| **Game/product prototype** | "Mafia themed GTA-style game" with @MeshyAI (156 likes) | 50-150 | "I built a real thing with this tool" > "Look at this pretty output." |
| **Prompt sharing + result** | "TV Stickers by Nano Banana" on @hailuo_ai (99 likes) | 30-100 | Prompts included = bookmarks. People save what they can reproduce. |
| **Product feature announcements by users** | "Layerize from @ideogram_ai is up on Replicate" (50 likes) | 30-80 | User announcing tool feature = more trusted than tool's own announcement. |
| **Artistic showcase (solo)** | Various @midjourney, @LeonardoAi showcase posts | 5-50 | Lowest ceiling. "Look what I made" without utility or narrative underperforms. |

### The utility-vs-art gradient

Tweets that demonstrate a **workflow** or **build something functional** using the AI tool get 3-10x more engagement than tweets that simply showcase AI-generated art. The top 3 tweets across all tools (533, 370, 270 likes) all involve the tool being used for a PURPOSE (game development, university lecture, music video), not just visual generation.

---

## Finding 5: Platform-Community Mismatch

Some tools have large Twitter followings but minimal community engagement on @mentions. This indicates the community lives elsewhere (Discord, Reddit, the tool's own platform).

| Tool | Followers | Avg Likes on @Mention | Engagement-to-Follower Ratio | Where Community Likely Lives |
|------|-----------|----------------------|------------------------------|------------------------------|
| @openai | 4,708,633 | 0.9 | 0.000019% | ChatGPT itself, Reddit, HN |
| @GoogleDeepMind | 1,393,472 | 3.5 | 0.00025% | Research community, arXiv |
| @midjourney | 414,221 | 6.0 | 0.0014% | Discord (primary community) |
| @runwayml | 272,549 | 6.8 | 0.0025% | Platform (runway.ml), YouTube |
| @StabilityAI | 252,219 | 8.9 | 0.0035% | GitHub, HuggingFace, Reddit |
| @recraftai | 15,313 | 22.2 | 0.14% | **Twitter IS the community** |
| @MeshyAI | 14,651 | 25.2 | 0.17% | **Twitter IS the community** |
| @wavespeed_ai | 6,328 | 15.4 | 0.24% | **Twitter IS the community** |

**Key insight:** The highest engagement-per-tag ratios come from tools where **Twitter is the primary community platform**, not a secondary channel. Recraft (15K followers, 22.2 avg likes), Meshy (14K followers, 25.2 avg likes), and WaveSpeed (6K followers, 15.4 avg likes) all have small-but-engaged Twitter-native communities. Contrast with OpenAI (4.7M followers, 0.9 avg likes) where Twitter is a broadcast channel, not a community.

---

## Finding 6: Engagement Comparison -- All Mentions vs. Media-Only

The "media-only" filter dramatically changes rankings because it removes reply threads, complaints, and non-creative mentions.

| Tool | All Mentions Avg Likes | Media-Only Avg Likes | Multiplier | Interpretation |
|------|----------------------|---------------------|------------|----------------|
| @Kling_ai | 0.3 | 10.0 | 33x | Almost all engagement is on showcase content; reply mentions get near zero. |
| @runwayml | 1.2 | 6.8 | 5.7x | Big difference -- lots of low-engagement reply chatter. |
| @midjourney | 0.8 | 6.0 | 7.5x | Same pattern. |
| @openai | 0.1 | 0.9 | 9x | Still low even for media tweets. |
| @recraftai | 5.6 | 22.2 | 4x | Even non-media mentions get engagement. Community is consistently engaged. |
| @MeshyAI | 4.7 | 25.2 | 5.4x | Strong baseline + massive media spike. |

---

## Handles Not Found / Fragmented

| Intended Tool | Handles Tried | Result |
|---------------|--------------|--------|
| Pika Labs | @PikaArtHQ, @pika_art | **Correct: @pika_labs** (146,836 followers) |
| MiniMax / Hailuo | @minimax_global | **Correct: @minimax_ai** (82,203 followers) for MiniMax, **@hailuo_ai** (72,510 followers) for Hailuo product |
| Leonardo AI | @LeonardoAi_, @LeonardoAI_ | **Correct: @LeonardoAi** (60,884 followers) |
| Tripo | @tripo3d | **Correct: @TripoAI** (13,982 followers) |
| Haiper | @HaiperOfficial | Handle exists (1 follower) -- appears to be a shell/placeholder. No community activity. |
| Genmo | @genmo_ai | Handle exists (12 followers) -- effectively dead on Twitter. |
| Suno AI | @suno_ai_, @SunoMusic | Fragmented. @suno_ai_ has 2,081 followers, @SunoMusic has 2,047. Neither is active. Suno's community is NOT on Twitter. |
| Playground AI | @playground_ai | Exists (20,368 followers) but zero mention tweets found in 7-day window. |

---

## Strategic Recommendations: Tag Priority Matrix

Combining engagement data, resharing behavior, and bookmark rate into a single priority ranking for which tools to tag when posting content.

| Priority | Tool | Why | Expected Return per Tag |
|----------|------|-----|------------------------|
| **1** | @MeshyAI | Highest avg likes (25.2), extreme bookmarks (17.6), 23% reshare rate. 3D content is bookmark-bait. | High engagement + bookmarks + reshare probability |
| **2** | @recraftai | Second highest likes (22.2), extreme bookmarks (13.9), 20% QT rate with editorial commentary. | High engagement + bookmarks + curatorial QT |
| **3** | @ElevenLabs | Third highest likes (20.6), high bookmarks (13.2), 20% reshare rate. Novel integrations get amplified. | High engagement + bookmarks + selective reshare |
| **4** | @hailuo_ai | 52% reshare rate (highest of any tool). Avg 10.3 likes. Guaranteed amplification. | Guaranteed RT. Reliable distribution. |
| **5** | @Kling_ai | 39% reshare rate. "Creative Partners" program for ongoing relationship. | High reshare probability + program entry |
| **6** | @LumaLabsAI | 14.5 avg likes, 23% reshare rate. Luma Uni-1 driving current attention. | Good engagement + moderate reshare |
| **7** | @wavespeed_ai | Small community but highest median (6). Seedance 2 content performing. Less noise to compete with. | Consistent moderate engagement. Low competition. |
| **8** | @pika_labs | 11.0 avg likes but only 4% reshare. Good organic engagement. | Organic engagement only. No amplification. |
| **9** | @PixVerse_ | 42% QT reshare rate (second highest). 6.2 avg likes. Good for amplification on challenge content. | Moderate engagement + high QT probability |
| **10** | @ideogram_ai | 7.4 avg likes, 3.0 bookmarks. 14% reshare. Text-in-image work valued. | Moderate engagement + bookmarks |
| **11** | @bfl_ml | 7.1 avg likes, technical audience. 14% reshare. | Moderate engagement |
| **12** | @minimax_ai | 5.0 avg likes, 35% reshare rate. Overlaps with @hailuo_ai. | Moderate. Tag if using MiniMax specifically. |

### Do NOT prioritize tagging:

| Tool | Why Not |
|------|---------|
| @openai | 0.9 avg likes. Corporate broadcast account. Zero user content resharing. |
| @GoogleDeepMind | 3.5 avg likes. Research account. Zero user content resharing. |
| @midjourney | 6.0 avg likes but 2% reshare, community lives on Discord. |
| @NightcafeStudio | 1.2 avg likes. Dead community. |
| @suno_ai_ | 0.1 avg likes. Twitter presence is negligible. |

---

## Falsifiability Section

| Finding | What Would Disprove It |
|---------|----------------------|
| "MeshyAI has highest avg engagement" | If the 533-like tweet is a one-time outlier. Removing it drops avg from 25.2 to ~8.3 -- still top 5 but not #1. **The median (1) suggests heavy skew.** |
| "Recraft's community lives on Twitter" | If Recraft's engagement drops when they stop QTing user content (their QTs amplify the original). Test: compare engagement on Recraft mentions that were NOT QT'd by @recraftai. |
| "Hailuo resharing is guaranteed" | If @hailuo_ai changes their resharing strategy. The 52% rate is current behavior, not policy. Monitor monthly. |
| "Utility content > art showcase" | If pure art showcases start outperforming workflow demos in future samples. The current finding is based on top-30 analysis only. |
| "Small tools have higher engagement-per-tag" | Could be survivorship bias -- small communities are self-selected engaged users. As tools grow, engagement-per-tag may decline (dilution). |
| "Bookmark rate indicates workflow value" | Bookmarks could indicate intent-to-engage-later rather than reference-saving. No way to verify without internal data. |

## Shared Assumptions

1. **7-day window bias.** All data covers the last 7 days only (Basic API tier limitation). Product launches, contests, or viral moments in this window skew results. The Luma Uni-1 launch, PixVerse challenge, and Kling Creative Partners program were all active during this window.

2. **Outlier sensitivity.** Small sample sizes (10-40 tweets) mean a single viral tweet dominates averages. MeshyAI's avg (25.2) is driven by one 533-like tweet; removing it drops to ~8.3. The median metric is more robust but shows most tools at 0-3 likes, suggesting the "typical" @mention gets minimal engagement everywhere.

3. **Causal direction unknown.** Tools with high reshare rates (Hailuo 52%, Kling 39%) show high @mention engagement -- but we cannot determine whether: (a) the tool reshares because users post good content, or (b) users post because they know the tool will reshare. Both likely compound.

4. **Reply contamination.** Even with `-is:retweet` filter, many "mention" tweets are reply threads, not showcase posts. The `has:media` filter helps but imperfectly -- media tweets can still be replies. A perfect filter would require checking `in_reply_to` status.

5. **Missing Discord/Reddit communities.** Midjourney (Discord), Stability AI (GitHub/HuggingFace), and Suno (in-platform) have large communities that do not appear in Twitter data. This analysis only measures Twitter engagement, which is one channel.

## Alternative Interpretations

**Interpretation A: Small tools are better to tag because their communities are more engaged.**
Evidence: Recraft (15K followers, 22.2 avg likes), MeshyAI (14K followers, 25.2 avg likes) dramatically outperform larger tools.
This would mean: Prioritize niche tools over mainstream ones.

**Interpretation B: Small tools appear better because their audience self-selects for Twitter engagement, but large tools deliver more total reach even at lower per-tweet metrics.**
Evidence: OpenAI mentions still reach 71 avg impressions despite 0.9 avg likes. ElevenLabs reaches 1,792 avg impressions per mention tweet. Impressions != engagement, but they indicate eyeballs.
This would mean: Large tools have hidden value in impression counts that doesn't convert to likes but may convert to profile visits.

**Weight assessment:** Interpretation A is stronger for our use case (building community engagement, getting reshared) because likes and reshares compound into follower growth. Impressions without engagement do not compound. However, Interpretation B has merit for brand awareness plays.

---

## Data Files

- Raw JSON (all mentions): `/root/twitter-pipeline/tools/research-data/tool_engagement_raw_2026.json`
- Raw JSON (media-only): `/root/twitter-pipeline/tools/research-data/tool_engagement_media_2026.json`
- Raw JSON (additional tools): `/root/twitter-pipeline/tools/research-data/tool_engagement_additional_2026.json`
- Raw JSON (keyword searches): `/root/twitter-pipeline/tools/research-data/tool_engagement_keywords_2026.json`
- Collection script: `/root/twitter-pipeline/tools/research-data/collect_tool_engagement.py`
