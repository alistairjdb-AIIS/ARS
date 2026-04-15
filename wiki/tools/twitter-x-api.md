# Twitter/X API v2

> The programmatic interface for posting content, reading engagement signals, and searching public conversation on X (formerly Twitter). Primary distribution and feedback channel for the autonomous posting loop.

**Confidence:** MEDIUM
**Last compiled:** 2026-04-08
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Pricing model — pay-per-use is the new default

As of February 6, 2026, X replaced its tiered pricing (Free/Basic/Pro) with pay-per-use for all new developers. [VERIFIED] Legacy tiers (Basic $200/mo, Pro $5,000/mo) remain available only to existing subscribers — closed to new signups.

| Operation | Cost |
|-----------|------|
| Post create | $0.01 |
| Post read | $0.005 |
| User lookup | $0.01 |
| User interaction (like/RT/follow) | $0.015 |

24-hour deduplication: requesting the same resource twice in one UTC day = single charge. [VERIFIED]

Monthly cap: 2 million post reads on pay-per-use. [VERIFIED]

For our projected use (5 posts/day + engagement reading + search): approximately $10-25/month. [VERIFIED — arithmetic from confirmed per-unit costs]

### Post creation capabilities

Endpoint: `POST https://api.x.com/2/tweets`. Supports text, media (1-4 images OR 1 video), polls (2-4 options, 5 min to 7 days), threads (reply chains), quote tweets, reply settings, AI labeling (`made_with_ai`), and geo tagging. [VERIFIED]

Critical mutual exclusivity: media cannot combine with polls or quote tweets. A poll post cannot have an image. [VERIFIED]

### Media upload

Endpoint: `POST https://api.x.com/2/media/upload`. Chunked upload for video (INIT/APPEND/FINALIZE/STATUS flow). [VERIFIED]

Video: MP4/MOV, H.264+AAC, up to 140 seconds and 512MB without Premium, up to 4 hours with Premium Plus. [VERIFIED]
Images: JPEG, PNG, WebP, BMP, up to 4 per post. [VERIFIED]

Requires `media.write` OAuth 2.0 scope or OAuth 1.0a user context. Bearer token NOT sufficient. [VERIFIED]

### Engagement metrics available

Public metrics (any auth): `like_count`, `retweet_count`, `quote_count`, `reply_count`, `impression_count`, `bookmark_count`. [VERIFIED]

Non-public metrics (own tweets, user auth, 30-day window): `url_link_clicks`, `user_profile_clicks`, `engagements`. [VERIFIED]

Video quartile metrics (own tweets, user auth): `playback_0_count` through `playback_100_count` at 0/25/50/75/100% completion. [VERIFIED] — These are the highest-signal metrics for content quality feedback.

### No native scheduling

X API v2 has no scheduling endpoint. Must build own scheduler (cron, APScheduler, GitHub Actions, etc.). [VERIFIED]

### Authentication

OAuth 1.0a: simpler, tokens don't expire, sufficient for single-account posting. We have all 4 credentials. [VERIFIED]

OAuth 2.0 with PKCE: required for some newer endpoints (v2 media upload needs `media.write` scope). Tokens expire after 2 hours without `offline.access` scope. [VERIFIED]

Common pattern: use OAuth 1.0a for v1.1 media upload, pass `media_id` to v2 tweet creation. [VERIFIED — documented in tweepy and developer tutorials]

---

## Operational Rules

- **When posting text + video:** Upload video via chunked upload first (INIT/APPEND/FINALIZE/STATUS), wait for processing to succeed, then create tweet with `media_ids`. Do not attempt to post before processing completes.
- **When wanting a poll with an image:** Cannot be done. Polls and media are mutually exclusive. Post the image as a reply to the poll, or vice versa.
- **When reading engagement on own posts:** Request `tweet.fields=public_metrics,non_public_metrics` with user auth. Non-public metrics only available for tweets less than 30 days old.
- **When choosing auth method:** Use OAuth 1.0a for posting and reading. Switch to OAuth 2.0 only if v2-exclusive endpoints require `media.write` scope.
- **When estimating costs:** $0.01/post + $0.005/read. At 5 posts/day + 200 reads/day, monthly cost is approximately $15. Budget $25/month for headroom.
- **When scheduling posts:** Build own scheduler. Simplest: cron job or Python `schedule` library calling the API at the target time. No API-native solution exists.
- **When uploading video from AI tools (Veo, Kling, Runway):** Output is natively MP4 H.264 — direct compatibility, no transcoding needed. Keep under 140 seconds and 512MB for non-Premium accounts.

---

## Deep Reference

- **When** deciding whether pay-per-use or legacy tier is more cost-effective for a specific posting volume → **read** `research-data/twitter_api_v2_capabilities_2026.md §1` **for** complete cost modeling table with breakpoints
- **When** constructing a `POST /2/tweets` request body → **read** `research-data/twitter_api_v2_capabilities_2026.md §2` **for** full parameter table including `made_with_ai`, `reply_settings`, `community_id`, and mutual exclusivity rules
- **When** debugging media upload failures → **read** `research-data/twitter_api_v2_capabilities_2026.md §3` **for** chunked upload 4-step flow, processing states, and auth requirements
- **When** choosing which engagement metrics to track → **read** `research-data/twitter_api_v2_capabilities_2026.md §6` **for** complete metric field names including video quartile completion metrics
- **When** writing the posting script → **read** `research-data/twitter_api_v2_capabilities_2026.md §8` **for** tweepy code patterns (OAuth 1.0a + v2 Client hybrid, media upload, thread creation)

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/twitter_api_v2_capabilities_2026.md` | Complete API capability audit: pricing, endpoints, media specs, auth, engagement metrics, Python libraries |
| `memory/project-twitter-learning-loop.md` | Vision and requirements for the autonomous posting loop |
| `memory/credentials.md` | All Twitter/X API credentials (@GetHealthC) |

---

## Related Concepts

- [[reels-algorithm-signals]] — INFORMS: X's algorithm signals differ from Instagram's but share watch-time primacy; video quartile metrics map to the same retention-curve analysis
- [[engagement-scoring-matrix]] — INFORMS: X engagement data (likes, RTs, bookmarks, video completion) feeds the same scoring dimensions but through different signal channels
- [[semantic-demand-patterns]] — DEPENDS_ON: the posting loop's content selection depends on demand patterns; X search API enables real-time demand detection

---

## Open Questions

- What is our account's current tier? Credentials obtained pre-Feb-2026. Need to verify via developer console whether we're on legacy free (migrated to pay-per-use with $10 voucher?), legacy basic, or pay-per-use.
- Is the v1.1 media upload endpoint (`upload.twitter.com/1.1/media/upload.json`) still functional or fully deprecated? Migration to v2 was scheduled for June 2025. Affects the tweepy `api.media_upload()` pattern.
- What are the exact per-15-minute and per-24-hour rate limits on pay-per-use? Not publicly documented.
- Is media upload charged separately or included in the $0.01/post-write cost?
