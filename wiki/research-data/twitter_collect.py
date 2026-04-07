import urllib.request
import urllib.parse
import json
import time
import sys

BEARER = "AAAAAAAAAAAAAAAAAAAAAGkb8QEAAAAAxSnlvGZ5m0yI3IwW%2BkGjpf%2BamBY%3DsBbZa0mYmKkUq8gs3pYNcsVgiIlk29SqYXoZW9IhvaqQc7j67C"

def api_get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {BEARER}"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": e.code, "detail": body[:200]}

def search_tweets(query, max_results=15, use_archive=False):
    """Search recent or full archive tweets."""
    endpoint = "all" if use_archive else "recent"
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,conversation_id",
    }
    url = f"https://api.x.com/2/tweets/search/{endpoint}?{urllib.parse.urlencode(params)}"
    return api_get(url)

def get_users(user_ids):
    """Batch lookup users by ID."""
    if not user_ids:
        return {}
    # API allows up to 100 per request
    chunks = [user_ids[i:i+100] for i in range(0, len(user_ids), 100)]
    users = {}
    for chunk in chunks:
        ids_str = ",".join(chunk)
        url = f"https://api.x.com/2/users?ids={ids_str}&user.fields=public_metrics,name,username"
        data = api_get(url)
        if "data" in data:
            for u in data["data"]:
                users[u["id"]] = u
        time.sleep(0.5)
    return users

def get_replies(conversation_id, max_results=30):
    """Get replies to a tweet via conversation_id."""
    params = {
        "query": f"conversation_id:{conversation_id}",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,author_id,created_at",
    }
    url = f"https://api.x.com/2/tweets/search/recent?{urllib.parse.urlencode(params)}"
    return api_get(url)

def categorize_reply(text):
    """Simple heuristic reply categorization."""
    t = text.lower()
    if "?" in text and any(w in t for w in ["how", "what", "why", "is it", "should", "can i", "does", "do you", "where"]):
        return "QUESTION"
    if any(w in t for w in ["i tried", "i use", "i found", "my experience", "i've been", "i started", "i lost", "i gained", "i was", "mine is", "my doctor"]):
        return "EXPERIENCE"
    if any(w in t for w in ["is there", "can someone", "need a", "looking for", "recommend", "any tool", "any app", "wish there"]):
        return "REQUEST"
    if any(w in t for w in ["actually", "that's not", "wrong", "incorrect", "disagree", "but", "no,", "nope", "false"]):
        return "DISAGREEMENT"
    return "OTHER"

# ===== SEARCH QUERIES =====
searches = {
    # Round 1 — Calculator-specific
    "TDEE calculator": {"q": "TDEE calculator", "archive": False},
    "calorie calculator": {"q": "calorie calculator -ad -sponsored", "archive": False},
    "BMI calculator": {"q": "BMI calculator", "archive": False},
    "macro calculator": {"q": "macro calculator OR macros calculator", "archive": False},
    
    # Round 2 — Problem-framed (semantic demand)
    "how much should I eat": {"q": '"how much should I eat" OR "how many calories should"', "archive": False},
    "is my weight normal": {"q": '"is my weight normal" OR "am I overweight" OR "is my BMI"', "archive": False},
    "don't know calories": {"q": '"I don\'t know how many calories" OR "no idea how many calories"', "archive": False},
    "doctor told me": {"q": '"my doctor told me" (calculate OR calculator OR calories OR weight)', "archive": False},
    "understand results": {"q": '"help me understand" (results OR labs OR numbers) health', "archive": False},
    
    # Round 3 — High-engagement health patterns
    "health high replies": {"q": "health min_replies:50 -filter:links lang:en", "archive": False},
    "health high engagement": {"q": "(fitness OR nutrition OR health) min_faves:500 -filter:links lang:en", "archive": False},
    "small account breakout": {"q": "(calculator OR health OR fitness) min_faves:200 -filter:links lang:en", "archive": False},
}

all_results = []
all_author_ids = set()

print(f"Running {len(searches)} searches...\n")

for name, config in searches.items():
    print(f"[{name}]...", end=" ", flush=True)
    data = search_tweets(config["q"], max_results=15, use_archive=config.get("archive", False))
    
    if "error" in data:
        print(f"ERROR {data['error']}: {data['detail'][:100]}")
        continue
    
    tweets = data.get("data", [])
    print(f"{len(tweets)} tweets")
    
    for t in tweets:
        t["_search_query"] = name
        all_author_ids.add(t["author_id"])
        all_results.append(t)
    
    time.sleep(1)  # Be nice to rate limits

# Deduplicate by tweet ID
seen_ids = set()
unique_results = []
for t in all_results:
    if t["id"] not in seen_ids:
        seen_ids.add(t["id"])
        unique_results.append(t)

print(f"\nTotal tweets: {len(all_results)}, unique: {len(unique_results)}")
print(f"Unique authors: {len(all_author_ids)}")

# Fetch author data
print(f"\nFetching user data for {len(all_author_ids)} authors...")
users = get_users(list(all_author_ids))
print(f"Got {len(users)} user profiles")

# Filter by engagement threshold
high_engagement = []
for t in unique_results:
    m = t.get("public_metrics", {})
    likes = m.get("like_count", 0)
    replies = m.get("reply_count", 0)
    bookmarks = m.get("bookmark_count", 0)
    author = users.get(t["author_id"], {})
    followers = author.get("public_metrics", {}).get("followers_count", 0)
    
    # Engagement threshold from the framework
    ratio = likes / max(followers, 1)
    passes = (
        ratio > 1.0 or  # likes > followers
        replies > 50 or  # high conversation
        bookmarks > 100 or  # high save intent
        (followers < 5000 and likes > 100)  # small account breakout
    )
    
    t["_author"] = author
    t["_followers"] = followers
    t["_like_ratio"] = round(ratio, 2)
    t["_passes_threshold"] = passes
    
    if passes or likes > 20 or replies > 10:  # Also keep moderately engaging tweets for analysis
        high_engagement.append(t)

print(f"\nHigh engagement tweets: {len(high_engagement)} (of {len(unique_results)})")

# Get replies for top tweets (limit to top 30 to conserve API calls)
top_tweets = sorted(high_engagement, key=lambda t: t["public_metrics"]["reply_count"], reverse=True)[:30]

print(f"\nFetching replies for top {len(top_tweets)} tweets...")
for i, t in enumerate(top_tweets):
    conv_id = t.get("conversation_id", t["id"])
    reply_data = get_replies(conv_id, max_results=30)
    replies = reply_data.get("data", [])
    
    # Categorize and store
    categorized = []
    reply_author_ids = [r["author_id"] for r in replies if r["author_id"] not in users]
    if reply_author_ids:
        reply_users = get_users(reply_author_ids)
        users.update(reply_users)
    
    for r in replies:
        cat = categorize_reply(r["text"])
        r_author = users.get(r["author_id"], {})
        categorized.append({
            "text": r["text"],
            "category": cat,
            "handle": r_author.get("username", "unknown"),
            "followers": r_author.get("public_metrics", {}).get("followers_count", 0),
            "likes": r.get("public_metrics", {}).get("like_count", 0),
        })
    
    t["_replies"] = categorized
    print(f"  [{i+1}/{len(top_tweets)}] {len(categorized)} replies for tweet {t['id'][:10]}...")
    time.sleep(1)

# ===== OUTPUT =====
output_path = "/tmp/claude-0/twitter_health_collection.json"
output = {
    "collection_date": "2026-03-15",
    "searches_run": list(searches.keys()),
    "total_tweets_found": len(unique_results),
    "high_engagement_count": len(high_engagement),
    "tweets": []
}

for t in high_engagement:
    author = t.get("_author", {})
    m = t.get("public_metrics", {})
    output["tweets"].append({
        "search_query": t.get("_search_query", ""),
        "id": t["id"],
        "text": t["text"],
        "created_at": t.get("created_at", ""),
        "handle": author.get("username", "unknown"),
        "display_name": author.get("name", ""),
        "followers": t.get("_followers", 0),
        "likes": m.get("like_count", 0),
        "reposts": m.get("retweet_count", 0),
        "replies": m.get("reply_count", 0),
        "quotes": m.get("quote_count", 0),
        "bookmarks": m.get("bookmark_count", 0),
        "impressions": m.get("impression_count", 0),
        "like_ratio": t.get("_like_ratio", 0),
        "passes_threshold": t.get("_passes_threshold", False),
        "reply_data": t.get("_replies", []),
    })

# Sort by reply count (conversation signal)
output["tweets"].sort(key=lambda t: t["replies"], reverse=True)

with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n=== COLLECTION COMPLETE ===")
print(f"Saved to: {output_path}")
print(f"Total tweets collected: {len(output['tweets'])}")
print(f"Tweets with replies captured: {sum(1 for t in output['tweets'] if t['reply_data'])}")

# Quick summary
print(f"\n=== TOP 10 BY REPLIES ===")
for t in output["tweets"][:10]:
    print(f"  [{t['replies']} replies, {t['likes']} likes] @{t['handle']} ({t['followers']} followers)")
    print(f"    {t['text'][:120]}...")
    if t["reply_data"]:
        cats = {}
        for r in t["reply_data"]:
            cats[r["category"]] = cats.get(r["category"], 0) + 1
        print(f"    Reply categories: {cats}")
    print()

