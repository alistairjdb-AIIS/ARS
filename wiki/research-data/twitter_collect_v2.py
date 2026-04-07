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
        return {"error": e.code, "detail": e.read().decode()[:200]}

def search_tweets(query, max_results=50, use_archive=False):
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
    if not user_ids: return {}
    users = {}
    for i in range(0, len(user_ids), 100):
        chunk = user_ids[i:i+100]
        url = f"https://api.x.com/2/users?ids={','.join(chunk)}&user.fields=public_metrics,name,username"
        data = api_get(url)
        for u in data.get("data", []):
            users[u["id"]] = u
        time.sleep(0.3)
    return users

def get_replies(conversation_id, max_results=30):
    params = {
        "query": f"conversation_id:{conversation_id} lang:en",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,author_id,created_at",
        "sort_order": "relevancy",
    }
    url = f"https://api.x.com/2/tweets/search/recent?{urllib.parse.urlencode(params)}"
    return api_get(url)

def categorize_reply(text):
    t = text.lower()
    if "?" in text and any(w in t for w in ["how", "what", "why", "is it", "should", "can i", "does", "where", "when", "which"]):
        return "QUESTION"
    if any(w in t for w in ["i tried", "i use", "i found", "my experience", "i've been", "i started", "i lost", "i gained", "i was", "mine is", "my doctor", "i weigh", "i eat", "i'm currently", "i did"]):
        return "EXPERIENCE"
    if any(w in t for w in ["is there", "can someone", "need a", "looking for", "recommend", "any tool", "any app", "wish there", "link", "where can"]):
        return "REQUEST"
    if any(w in t for w in ["actually", "that's not", "wrong", "incorrect", "disagree", "not true", "false", "misleading"]):
        return "DISAGREEMENT"
    return "OTHER"

# ===== SEARCHES =====
# Using full archive for broader data + recent for freshness
searches = [
    # Round 1 — Calculator demand (archive for volume)
    ("TDEE calculator", "TDEE calculator", True),
    ("calorie calculator", "calorie calculator -ad -promo -download", True),
    ("BMI frustration", "BMI (wrong OR inaccurate OR stupid OR doesn't account OR muscle)", True),
    ("macro help", "macro calculator (help OR confused)", True),
    
    # Round 2 — Natural language health demand
    ("how much should I eat", '"how much should I eat" OR "how many calories should I eat"', True),
    ("is my weight normal", '"is my weight" OR "am I overweight" OR "is my BMI normal"', True),
    ("calorie confusion", '"I don\'t know" (calories OR how much to eat OR macros)', True),
    ("doctor said calculate", '"my doctor" (calculate OR told me OR said I should) (weight OR calories OR BMI)', True),
    ("health numbers help", '"what does my" (mean OR number) (health OR result OR lab OR test)', True),
    ("TDEE frustration", "TDEE (confusing OR wrong OR accurate OR trust OR how do I)", True),
    
    # Round 3 — High-engagement health (use archive, broader queries)
    ("health viral text", "health (tip OR fact OR myth) -filter:links", False),
    ("fitness engagement", "fitness (changed my life OR game changer OR wish I knew)", False),
    ("nutrition hot take", "nutrition (controversial OR unpopular opinion OR hot take)", False),
    ("weight loss real talk", '"weight loss" (honest OR truth OR nobody tells you OR real)', False),
    ("body composition", '"body fat" OR "body composition" (surprised OR shocked OR learned)', False),
]

all_tweets = []
all_author_ids = set()

print(f"Running {len(searches)} searches...\n")

for name, query, use_archive in searches:
    print(f"[{name}]...", end=" ", flush=True)
    data = search_tweets(query, max_results=30, use_archive=use_archive)
    
    if "error" in data:
        print(f"ERROR {data['error']}: {data['detail'][:80]}")
        continue
    
    tweets = data.get("data", [])
    for t in tweets:
        t["_search"] = name
        all_author_ids.add(t["author_id"])
    all_tweets.extend(tweets)
    print(f"{len(tweets)} tweets")
    time.sleep(0.8)

# Deduplicate
seen = set()
unique = []
for t in all_tweets:
    if t["id"] not in seen:
        seen.add(t["id"])
        unique.append(t)

print(f"\nTotal: {len(all_tweets)}, unique: {len(unique)}, authors: {len(all_author_ids)}")

# Get authors
print(f"Fetching {len(all_author_ids)} user profiles...")
users = get_users(list(all_author_ids))
print(f"Got {len(users)} profiles")

# Enrich and filter — lower threshold, keep anything with engagement
enriched = []
for t in unique:
    m = t.get("public_metrics", {})
    author = users.get(t["author_id"], {})
    followers = author.get("public_metrics", {}).get("followers_count", 0)
    likes = m.get("like_count", 0)
    replies = m.get("reply_count", 0)
    bookmarks = m.get("bookmark_count", 0)
    
    # Keep if any meaningful engagement
    if likes >= 5 or replies >= 3 or bookmarks >= 5:
        enriched.append({
            "search": t["_search"],
            "id": t["id"],
            "conversation_id": t.get("conversation_id", t["id"]),
            "text": t["text"],
            "created_at": t.get("created_at", ""),
            "handle": author.get("username", "?"),
            "name": author.get("name", ""),
            "followers": followers,
            "likes": likes,
            "reposts": m.get("retweet_count", 0),
            "replies": replies,
            "quotes": m.get("quote_count", 0),
            "bookmarks": bookmarks,
            "impressions": m.get("impression_count", 0),
            "ratio": round(likes / max(followers, 1), 3),
            "reply_data": [],
        })

enriched.sort(key=lambda t: t["replies"] + t["likes"], reverse=True)
print(f"\nEnriched tweets with engagement: {len(enriched)}")

# Get replies for top 40 by reply count
top_for_replies = sorted(enriched, key=lambda t: t["replies"], reverse=True)[:40]
print(f"\nFetching replies for top {len(top_for_replies)} tweets...")

for i, t in enumerate(top_for_replies):
    if t["replies"] < 2:
        continue
    reply_data = get_replies(t["conversation_id"], max_results=30)
    replies = reply_data.get("data", [])
    
    # Get reply author info
    new_ids = [r["author_id"] for r in replies if r["author_id"] not in users]
    if new_ids:
        new_users = get_users(list(set(new_ids)))
        users.update(new_users)
    
    for r in replies:
        ra = users.get(r["author_id"], {})
        t["reply_data"].append({
            "text": r["text"],
            "category": categorize_reply(r["text"]),
            "handle": ra.get("username", "?"),
            "followers": ra.get("public_metrics", {}).get("followers_count", 0),
            "likes": r.get("public_metrics", {}).get("like_count", 0),
        })
    
    if replies:
        print(f"  [{i+1}] {len(replies)} replies for @{t['handle']} ({t['replies']} reply count)")
    time.sleep(0.5)

# Save
output = {
    "date": "2026-03-15",
    "searches": [s[0] for s in searches],
    "total_unique": len(unique),
    "with_engagement": len(enriched),
    "tweets": enriched,
}

path = "/tmp/claude-0/twitter_health_collection_v2.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*60}")
print(f"COLLECTION COMPLETE")
print(f"Saved: {path}")
print(f"Tweets: {len(enriched)}")
print(f"With replies: {sum(1 for t in enriched if t['reply_data'])}")
print(f"{'='*60}")

# Summary by search
print(f"\n=== BY SEARCH ===")
by_search = {}
for t in enriched:
    s = t["search"]
    by_search[s] = by_search.get(s, 0) + 1
for s, c in sorted(by_search.items(), key=lambda x: -x[1]):
    print(f"  {c:3d} tweets — {s}")

# Top tweets
print(f"\n=== TOP 15 BY ENGAGEMENT ===")
for t in enriched[:15]:
    print(f"\n  @{t['handle']} ({t['followers']:,} followers) — {t['likes']} likes, {t['replies']} replies, {t['bookmarks']} bookmarks")
    print(f"  Search: {t['search']}")
    print(f"  {t['text'][:200]}")
    if t["reply_data"]:
        cats = {}
        for r in t["reply_data"]:
            cats[r["category"]] = cats.get(r["category"], 0) + 1
        print(f"  Reply breakdown: {cats}")

