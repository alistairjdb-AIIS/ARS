# Twitter/X API v2 Capabilities Reference — April 2026

**Date:** 2026-04-08
**Method:** Official docs (docs.x.com), developer community posts, third-party pricing analyses, web search verification
**Purpose:** Determine what @GetHealthC can do programmatically for the autonomous posting loop
**Confidence tags:** VERIFIED = confirmed against official docs or multiple independent sources. ASSUMING = training knowledge or single-source. UNVERIFIED = conflicting signals.

---

## 1. Pricing Model (CRITICAL CHANGE)

**As of February 6, 2026, X replaced tiered pricing with pay-per-use as the default.**

| Operation | Cost per request | Source |
|-----------|-----------------|--------|
| Post create (write tweet) | $0.01 | VERIFIED — official docs, multiple sources |
| Post read (fetch tweet) | $0.005 | VERIFIED |
| User profile lookup | $0.01 | VERIFIED |
| User interaction (follow, like, retweet) | $0.015 | VERIFIED |
| DM event read | $0.01 | VERIFIED |
| DM interaction create | $0.015 | VERIFIED |
| Media upload | NOT ITEMIZED separately | UNVERIFIED — no source lists media upload cost independently |
| Search (recent, 7-day) | Likely $0.005/post read | ASSUMING — search returns posts, likely charged per post returned |

### Monthly caps (pay-per-use)
- 2 million post reads maximum
- No stated cap on writes (cost-limited only)
- 24-hour deduplication: same resource requested twice in one UTC day = single charge

### xAI credit rebates
- $200+ cumulative spend/billing cycle: 10% back as xAI API credits
- $500+: 15% back
- $1,000+: 20% back

### Legacy tiers (CLOSED to new signups)
| Tier | Price | Post writes | Post reads | Search | Streaming |
|------|-------|-------------|-----------|--------|-----------|
| Free | $0 | DISCONTINUED (was 500/mo) | DISCONTINUED | N/A | No |
| Basic | $200/mo | ~50,000/mo | ~10,000-15,000/mo | 7-day | No |
| Pro | $5,000/mo | ~300,000/mo | 1,000,000/mo | Full archive | Yes |
| Enterprise | $42,000+/mo | Custom | 50,000,000+/mo | Full archive | Yes |

**Our situation:** The project-twitter-learning-loop.md references "$50 Twitter API credit for reading/analysis." This aligns with the pay-per-use model. At $0.01/post write, $50 buys 5,000 posts. At $0.005/read, $50 buys 10,000 reads. The economics are favorable for a posting + engagement-reading loop.

### Cost modeling for our use case
| Activity | Volume/month | Cost/month |
|----------|-------------|------------|
| Post 2x/day | 60 posts | $0.60 |
| Post 5x/day | 150 posts | $1.50 |
| Read own post metrics | 150 reads | $0.75 |
| Read engagement (likes, replies) | 500 reads | $2.50 |
| Search for trending content | 1,000 reads | $5.00 |
| **Total (moderate)** | | **~$10/month** |
| **Total (aggressive)** | | **~$25/month** |

---

## 2. Post Types — What Can Be Posted Programmatically

**Endpoint:** `POST https://api.x.com/2/tweets`

| Feature | Supported | Parameter | Constraints |
|---------|-----------|-----------|-------------|
| Text post | Yes | `text` | 280 chars (standard), 25,000 chars (Premium subscribers) |
| Image attachment | Yes | `media.media_ids` | 1-4 images per post |
| Video attachment | Yes | `media.media_ids` | 1 video per post (upload separately) |
| GIF attachment | Yes | `media.media_ids` | 1 GIF per post |
| Poll | Yes | `poll` | 2-4 options, 5-10,080 min duration |
| Thread (reply chain) | Yes | `reply.in_reply_to_tweet_id` | Post first tweet, reply to it with second, etc. |
| Quote tweet | Yes | `quote_tweet_id` | Mutually exclusive with media, poll |
| Reply settings | Yes | `reply_settings` | `following`, `mentionedUsers`, `subscribers`, `verified` |
| AI label | Yes | `made_with_ai` | Boolean — labels post as AI-generated |
| Paid partnership | Yes | `paid_partnership` | Boolean — discloses promotion |
| Geo tagging | Yes | `geo` | Place ID |
| Community post | Yes | `community_id` | Target specific community |

### Mutual exclusivity (VERIFIED)
- `media` is mutually exclusive with `poll`, `quote_tweet_id`, and `card_uri`
- `poll` is mutually exclusive with `media`, `quote_tweet_id`, and `card_uri`
- This means: you CANNOT attach an image to a poll, or quote-tweet with media

---

## 3. Media Upload

### Endpoint (v2, current)
`POST https://api.x.com/2/media/upload`

### Simple upload (images)
- Single multipart/form-data POST
- Returns `media_id` to use in `create_tweet`

### Chunked upload (video, large files)
Four-step process:
1. **INIT** — `POST /2/media/upload` with `command=INIT`, `total_bytes`, `media_type`, `media_category`
2. **APPEND** — `POST /2/media/upload/{id}/append` with chunk data (recommended 1MB chunks)
3. **FINALIZE** — `POST /2/media/upload/{id}/finalize`
4. **STATUS** — `GET /2/media/upload/{id}` to poll processing state

### Authentication
- Requires OAuth 2.0 with `media.write` scope, or OAuth 1.0a user context
- App-only (Bearer token) NOT sufficient for uploads

### Image specifications (VERIFIED)
| Property | Value |
|----------|-------|
| Formats | JPEG, PNG, WebP, BMP, PJPEG, TIFF |
| Max per post | 4 |
| Max file size | 5MB (ASSUMING — standard Twitter limit, not explicitly confirmed in v2 docs) |

### Video specifications (VERIFIED from multiple sources)
| Property | Non-Premium | Premium Plus |
|----------|-------------|-------------|
| Formats | MP4, MOV | MP4, MOV |
| Codec | H.264 video, AAC audio | H.264 video, AAC audio |
| Max file size | 512 MB | 16 GB (web/iOS) |
| Max duration | 140 seconds (2:20) | 4 hours (web/iOS), 10 min (Android) |
| Resolution | Up to 1920x1080 | Up to 1920x1080 (1080p < 2hr), 720p for 2-4hr |
| Aspect ratios | 16:9, 9:16, 1:1 | 16:9, 9:16, 1:1 |
| Frame rate | 30 fps (60 fps supported) | 30 fps (60 fps supported) |
| Max per post | 1 | 1 |

**Critical note for our use case:** Our Reels-style content will be 8-60 seconds, well within the 140-second non-premium limit. Video files from Veo/Kling/Runway are typically MP4 H.264 — native compatibility.

### Media upload rate limits (pay-per-use)
UNVERIFIED for pay-per-use tier specifically. One developer community source reports free tier limits of 17 INIT+FINALIZE/24hr and 85 APPEND/24hr. Pay-per-use limits are likely higher but not documented publicly.

---

## 4. Polls (VERIFIED)

Created via `POST /2/tweets` with `poll` parameter:

```json
{
  "text": "Which animation style do you prefer?",
  "poll": {
    "duration_minutes": 1440,
    "options": ["Anime", "Pixar 3D", "Cartoon", "Photoreal"]
  }
}
```

| Constraint | Value |
|------------|-------|
| Min options | 2 |
| Max options | 4 |
| Min duration | 5 minutes |
| Max duration | 10,080 minutes (7 days) |
| Max chars per option | 25 |
| With media? | NO — mutually exclusive |
| With quote tweet? | NO — mutually exclusive |

---

## 5. Scheduling

**There is NO native scheduling endpoint in the X API v2.** (VERIFIED — confirmed via docs sitemap, developer community, and multiple third-party analyses.)

The X Ads API has a `scheduled_tweets` endpoint, but this requires advertiser access and is designed for ad campaigns, not organic posting.

**For our use case:** We must build our own scheduler. Options:
1. Cron job / scheduled task that calls `POST /2/tweets` at the desired time
2. Python `schedule` library or `APScheduler`
3. GitHub Actions scheduled workflow
4. Cloud function (AWS Lambda, Google Cloud Functions) with CloudWatch/Cloud Scheduler trigger

This is straightforward — no API limitation, just infrastructure.

---

## 6. Engagement Reading (VERIFIED)

### Public metrics (any authentication)
Available on any tweet by requesting `tweet.fields=public_metrics`:

| Metric | Field |
|--------|-------|
| Likes | `like_count` |
| Retweets | `retweet_count` |
| Quote tweets | `quote_count` |
| Replies | `reply_count` |
| Impressions | `impression_count` |
| Bookmarks | `bookmark_count` |

### Non-public metrics (user context, own tweets only, 30-day window)
Requires OAuth 1.0a or OAuth 2.0 user token for tweets you authored:

| Metric | Field |
|--------|-------|
| URL link clicks | `url_link_clicks` |
| Profile clicks | `user_profile_clicks` |
| Total engagements | `engagements` |

### Video-specific metrics (user context, own tweets)
| Metric | Field |
|--------|-------|
| Video views | `view_count` (public) |
| Playback started | `playback_0_count` |
| 25% watched | `playback_25_count` |
| 50% watched | `playback_50_count` |
| 75% watched | `playback_75_count` |
| 100% watched | `playback_100_count` |

**These video quartile metrics are extremely valuable for our learning loop.** They tell us not just "did someone see it" but "did they watch to the end" — direct signal for content quality.

### Organic vs. promoted breakdown
For promoted posts, metrics split into `organic_metrics` and `promoted_metrics` to separate paid vs. organic reach. Not relevant for us initially.

### How to request metrics
Add `tweet.fields=public_metrics,non_public_metrics` to any tweet lookup/search request. Non-public metrics require user context auth.

---

## 7. Authentication

### Two methods, both supported

| Method | Use case | What we have |
|--------|----------|-------------|
| OAuth 1.0a | Server-to-server, single-account posting | Consumer Key + Secret, Access Token + Secret (all in credentials.md) |
| OAuth 2.0 with PKCE | Multi-user, scoped access, newer endpoints | Client ID + Secret (in credentials.md), requires auth flow |

### For our autonomous posting loop: OAuth 1.0a is simpler and sufficient

OAuth 1.0a advantages for us:
- No token refresh needed (tokens don't expire unless revoked)
- Single account (@GetHealthC) — no multi-user complexity
- Already have all 4 credentials
- Works with both `POST /2/tweets` and media upload

OAuth 2.0 would be needed if:
- We wanted users to authorize our app to post on their behalf
- We needed specific scopes (e.g., `media.write` for v2 media upload)
- Token expiry: OAuth 2.0 tokens expire after 2 hours unless `offline.access` scope used

**IMPORTANT NOTE:** The v2 media upload endpoint (`/2/media/upload`) requires `media.write` scope, which means OAuth 2.0 user token. However, many developers still use the v1.1 media upload endpoint with OAuth 1.0a for uploading, then use the returned `media_id` with the v2 tweet creation endpoint. This hybrid approach is common and documented. (VERIFIED — tweepy docs, developer tutorials)

### Our credentials status (from credentials.md)
- App permissions: Read and write (VERIFIED configured)
- Bearer Token: present (read-only operations)
- OAuth 1.0a: all 4 tokens present (read + write)
- OAuth 2.0: Client ID + Secret present (would need auth flow for user token)

---

## 8. Python Libraries

### Tweepy (RECOMMENDED)
- **Version:** 4.14.0 (latest stable as of research date)
- **Status:** Actively maintained, widely used, well-documented
- **v2 support:** Full — `tweepy.Client` class for API v2
- **Key methods:**
  - `client.create_tweet(text=..., media_ids=[...], poll=...)` — post tweets
  - `client.get_tweet(id, tweet_fields=["public_metrics"])` — read metrics
  - `client.search_recent_tweets(query)` — search
  - `api.media_upload(filename)` — upload media (uses v1.1 under the hood)
- **Auth:** Supports both OAuth 1.0a (via `OAuthHandler`) and OAuth 2.0 (via `OAuth2UserHandler`)
- **Media upload pattern:** Use `tweepy.API` (v1.1) for `media_upload()`, get `media_id`, pass to `tweepy.Client.create_tweet(media_ids=[id])`

### Alternatives considered
| Library | Status | Notes |
|---------|--------|-------|
| python-twitter-v2 | Listed on official X tools page | Simpler wrapper, less community |
| twikit | Free/scraping approach | Unofficial, breaks frequently, not recommended for production |
| requests + oauth | DIY | More control, more code, good for learning the raw API |

### Tweepy installation
```
pip install tweepy
```

### Minimal posting example (OAuth 1.0a)
```python
import tweepy

# OAuth 1.0a — for posting + media upload
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)  # v1.1 — for media upload

# v2 Client — for creating tweets
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Text-only post
client.create_tweet(text="Hello world")

# Post with image
media = api.media_upload("image.png")
client.create_tweet(text="Check this out", media_ids=[media.media_id])

# Post with video (chunked upload)
media = api.chunked_upload("video.mp4", media_category="tweet_video")
client.create_tweet(text="Watch this", media_ids=[media.media_id])

# Thread
first = client.create_tweet(text="Thread 1/3")
second = client.create_tweet(text="Thread 2/3", in_reply_to_tweet_id=first.data["id"])
third = client.create_tweet(text="Thread 3/3", in_reply_to_tweet_id=second.data["id"])
```

---

## 9. Summary: What We Can and Cannot Do

### CAN DO
- Post text tweets programmatically
- Attach up to 4 images per tweet
- Attach 1 video per tweet (up to 140s / 512MB without Premium)
- Create polls (2-4 options, up to 7 days)
- Post threads (reply chains)
- Quote tweet other posts
- Read public engagement metrics (likes, RTs, replies, impressions, bookmarks)
- Read private metrics on own tweets (link clicks, profile clicks, video quartile completion)
- Search recent tweets (7-day window)
- Control reply settings
- Label posts as AI-generated

### CANNOT DO
- Schedule posts natively (must build own scheduler)
- Attach media to polls
- Search full archive (pay-per-use is 7-day only; needs Pro legacy tier)
- Stream in real-time (pay-per-use has no streaming; needs Pro legacy tier)
- Read non-public metrics on other people's tweets
- Non-public metrics on tweets older than 30 days

### OPEN QUESTIONS
1. **Media upload cost on pay-per-use** — Is it a separate charge or included in the $0.01/post write? No source itemizes it separately. UNVERIFIED.
2. **Exact rate limits on pay-per-use** — Per-15-minute and per-24-hour limits are not publicly documented for the new pricing model. The Basic tier had specific numbers (100 creates/15min per user, 10,000/24hr per app). Pay-per-use limits are unknown.
3. **Our account tier status** — Credentials were obtained pre-Feb-2026 with "Premium" mentioned. Need to verify in developer console whether we're on legacy free, legacy basic, or auto-migrated to pay-per-use.
4. **v1.1 media upload deprecation** — Was scheduled for June 2025. If completed, the tweepy `api.media_upload()` pattern may need updating to v2 endpoints. Need to test.

---

## 10. Falsifiability

| Finding | What would disprove it |
|---------|----------------------|
| Pay-per-use is the only option for new devs | Finding that Free/Basic/Pro signups are still open (check developer console) |
| $0.01/post write | Official pricing page showing different number (check console.x.com) |
| No native scheduling API | Discovery of a `scheduled_at` parameter in POST /2/tweets |
| Video limit is 140s without Premium | Successful upload of a 3-minute video without Premium |
| OAuth 1.0a sufficient for posting | POST /2/tweets returning auth error with our OAuth 1.0a tokens |
| Tweepy is best Python library | Another library with better v2 coverage, active maintenance, and community |
| Poll max 4 options | Successful creation of a 5-option poll |

---

## 11. Recommended Next Steps

1. **Verify account tier** — Log into developer console, check whether @GetHealthC is on pay-per-use or legacy tier
2. **Test basic post** — Send a test tweet via OAuth 1.0a to confirm credentials still work
3. **Test media upload** — Upload a test image and video to confirm the pipeline
4. **Test engagement reading** — Fetch public_metrics on an existing tweet
5. **Build scheduler** — Simple cron-based approach, not dependent on API
6. **Estimate monthly budget** — Based on posting frequency and engagement reading needs
