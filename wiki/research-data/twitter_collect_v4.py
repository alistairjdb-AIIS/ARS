"""
Twitter Semantic Demand Collection v4
Focus: User-centric language patterns — confusion, unmet needs, active problem-solving
6 targeted queries for natural language extraction (not topic-based)
Date: 2026-03-17

Queries:
1. Caffeine timing — "should I stop drinking coffee" / "when to stop caffeine"
2. Nutrition guidance — "how many calories should I eat" / "what should I eat to lose"
3. Health validation — "is this normal" health/body/symptoms
4. Unmet needs — "I wish there was" health/calculator/tool
5. Confusion about health data — "can someone explain" health/results/lab
6. Active problem-solving — "trying to figure out" diet/calories/workout/sleep

For each tweet:
- Exact text preserved
- Full engagement metrics
- Type classification: question / statement / complaint / wish
"""

import urllib.request
import urllib.parse
import json
import time

BEARER = "AAAAAAAAAAAAAAAAAAAAAGkb8QEAAAAAxSnlvGZ5m0yI3IwW%2BkGjpf%2BamBY%3DsBbZa0mYmKkUq8gs3pYNcsVgiIlk29SqYXoZW9IhvaqQc7j67C"


def api_get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {BEARER}"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        return {"error": e.code, "detail": body}
    except Exception as e:
        return {"error": "exception", "detail": str(e)}


def search_tweets(query, max_results=20, use_archive=True):
    endpoint = "all" if use_archive else "recent"
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,conversation_id",
        "sort_order": "relevancy",
    }
    url = f"https://api.x.com/2/tweets/search/{endpoint}?{urllib.parse.urlencode(params)}"
    return api_get(url)


def get_users(user_ids):
    if not user_ids:
        return {}
    users = {}
    for i in range(0, len(user_ids), 100):
        chunk = user_ids[i:i+100]
        url = f"https://api.x.com/2/users?ids={','.join(chunk)}&user.fields=public_metrics,name,username"
        data = api_get(url)
        if "error" not in data:
            for u in data.get("data", []):
                users[u["id"]] = u
        time.sleep(0.3)
    return users


def is_ed_content(text):
    t = text.lower()
    ed_signals = [
        'edtwt', 'wltwt', 'proana', 'thinspo', 'meanspo',
        'purging', 'purge', 'binge and purge',
        'restrict', 'restricting', 'restriction',
        'anorex', 'wannarex', 'bulimi',
        '600 cal', '500 cal', '400 cal', '300 cal', '200 cal',
        '600cal', '500cal', '400cal', '300cal', '200cal',
        'body check', 'bodycheck', 'ugw', 'gw:', 'cw:',
        'eating disorder', 'my ed ', 'recovery ed',
    ]
    return any(w in t for w in ed_signals)


def classify_tweet_type(text):
    t = text.lower()
    # Wish/unmet need
    if any(w in t for w in ["i wish", "wish there was", "wish i could", "wish someone", "wish we had", "wish they", "someone should make", "why isn't there", "why is there no", "why doesn't", "there should be"]):
        return "wish"
    # Complaint
    if any(w in t for w in ["i hate", "so frustrating", "frustrated", "annoying", "drives me crazy", "why is it so hard", "can't figure out", "can't understand", "still confused", "no idea", "makes no sense", "doesn't make sense"]):
        return "complaint"
    # Question
    if text.strip().endswith("?") or any(w in t for w in ["should i", "can i", "is this normal", "is it normal", "how many", "how much", "when should", "what should", "how do i", "how does", "can someone explain", "trying to figure out", "does anyone know", "anyone know"]):
        return "question"
    # Statement
    return "statement"


# ===== SEARCH QUERIES =====
# (search_id, query, description, use_archive)
searches = [
    (
        "caffeine_timing",
        '("should I stop drinking coffee" OR "when to stop caffeine" OR "stop drinking coffee" OR "cut off caffeine" OR "caffeine cutoff") -is:retweet',
        "People asking about when to stop caffeine — timing confusion",
        True
    ),
    (
        "nutrition_guidance",
        '("how many calories should I eat" OR "how many calories should I" OR "what should I eat to lose" OR "how many calories do I need" OR "how much should I eat") -is:retweet -edtwt',
        "People seeking nutrition/calorie guidance",
        True
    ),
    (
        "health_validation",
        '("is this normal" OR "is it normal") (health OR body OR symptoms OR sleep OR heart rate OR blood pressure OR weight OR pain OR tired OR fatigue) -is:retweet -edtwt',
        "People seeking validation about health experiences",
        True
    ),
    (
        "unmet_tool_need",
        '("I wish there was" OR "I wish there were" OR "wish there was a" OR "someone should make") (health OR calculator OR tool OR app OR tracker) -is:retweet',
        "People expressing unmet tool/calculator needs",
        True
    ),
    (
        "health_data_confusion",
        '("can someone explain" OR "can anyone explain" OR "help me understand") (health OR results OR lab OR blood OR test OR levels OR numbers OR reading) -is:retweet',
        "People confused by health data or test results",
        True
    ),
    (
        "active_problem_solving",
        '("trying to figure out" OR "trying to work out" OR "trying to understand") (diet OR calories OR workout OR sleep OR weight OR macros OR protein OR nutrition) -is:retweet -edtwt',
        "People in active problem-solving mode around health",
        True
    ),
]

# ===== COLLECTION =====
all_results = {}
all_author_ids = set()
all_tweets_flat = []

print(f"Running {len(searches)} searches (up to 20 tweets each)...\n")

for search_id, query, description, use_archive in searches:
    print(f"[{search_id}]...")
    data = search_tweets(query, max_results=20, use_archive=use_archive)

    if "error" in data:
        print(f"  ERROR {data['error']}: {data['detail'][:120]}")
        all_results[search_id] = {"error": data["error"], "tweets": []}
        time.sleep(1)
        continue

    tweets = data.get("data", [])
    clean = []
    ed_filtered = 0

    for t in tweets:
        if is_ed_content(t.get("text", "")):
            ed_filtered += 1
            continue
        t["_search_id"] = search_id
        all_author_ids.add(t["author_id"])
        clean.append(t)

    all_results[search_id] = {
        "description": description,
        "raw_count": len(tweets),
        "ed_filtered": ed_filtered,
        "tweets": clean,
    }
    all_tweets_flat.extend(clean)
    print(f"  {len(clean)} clean tweets ({ed_filtered} ED-filtered, {len(tweets)} raw)")
    time.sleep(1.0)

# ===== USER ENRICHMENT =====
print(f"\nFetching {len(all_author_ids)} user profiles...")
users = get_users(list(all_author_ids))
print(f"Got {len(users)} profiles")

# ===== BUILD FINAL DATASET =====
final_tweets = []
for t in all_tweets_flat:
    m = t.get("public_metrics", {})
    author = users.get(t["author_id"], {})
    followers = author.get("public_metrics", {}).get("followers_count", 0)
    likes = m.get("like_count", 0)
    replies = m.get("reply_count", 0)
    bookmarks = m.get("bookmark_count", 0)
    reposts = m.get("retweet_count", 0)
    impressions = m.get("impression_count", 0)
    text = t.get("text", "")
    tweet_type = classify_tweet_type(text)

    final_tweets.append({
        "search_id": t["_search_id"],
        "id": t["id"],
        "text": text,
        "type": tweet_type,
        "handle": author.get("username", "?"),
        "name": author.get("name", ""),
        "followers": followers,
        "likes": likes,
        "replies": replies,
        "bookmarks": bookmarks,
        "reposts": reposts,
        "impressions": impressions,
        "created_at": t.get("created_at", ""),
    })

final_tweets.sort(key=lambda x: x["likes"] + x["bookmarks"] * 2, reverse=True)

# ===== SAVE RAW DATA =====
output = {
    "date": "2026-03-17",
    "version": "v4",
    "description": "User-centric language pattern collection — 6 queries targeting confusion, unmet needs, active problem-solving. Natural language extraction, not topic-based.",
    "queries": [{"id": s[0], "description": s[2], "query": s[1]} for s in searches],
    "total_tweets": len(final_tweets),
    "by_search": {
        sid: {
            "description": r.get("description", ""),
            "count": len(r.get("tweets", [])),
            "ed_filtered": r.get("ed_filtered", 0),
            "error": r.get("error"),
        }
        for sid, r in all_results.items()
    },
    "tweets": final_tweets,
}

path = "/root/healthcalculators-full/tools/research-data/twitter_demand_collection_v4.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*60}")
print(f"COLLECTION COMPLETE")
print(f"Saved: {path}")
print(f"Total tweets: {len(final_tweets)}")
print(f"{'='*60}")

print(f"\n=== BY SEARCH ===")
for search_id, result in all_results.items():
    count = len(result.get("tweets", []))
    desc = result.get("description", "")
    err = result.get("error", None)
    status = f"ERROR: {err}" if err else f"{count} tweets"
    print(f"  {search_id:30s} — {status}")
    print(f"    {desc}")

print(f"\n=== TOP 30 BY ENGAGEMENT ===")
for t in final_tweets[:30]:
    bkl = round(t["bookmarks"] / max(t["likes"], 1), 2)
    print(f"\n  [{t['search_id']}] @{t['handle']} ({t['followers']:,} followers)")
    print(f"  {t['likes']} likes | {t['replies']} replies | {t['bookmarks']} bkmrk (B/L={bkl}) | type={t['type']}")
    print(f"  {t['text'][:300]}")

print(f"\n=== ALL TWEET TEXTS (for manual language analysis) ===")
for sid, _ in all_results.items():
    matching = [t for t in final_tweets if t["search_id"] == sid]
    if not matching:
        continue
    print(f"\n--- {sid.upper()} ({len(matching)} tweets) ---")
    for i, t in enumerate(matching, 1):
        print(f"\n{i}. [{t['type']}] @{t['handle']} | {t['likes']}L {t['bookmarks']}B")
        print(f"   {t['text']}")
