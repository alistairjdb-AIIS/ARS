"""
V5 Fix: Re-run failed queries (meme, reply_pattern, and others that used min_faves).
Also fixes reply collection and adds to existing v5 archive data.
"""

import urllib.request
import urllib.parse
import json
import time
import os
from datetime import datetime

BEARER = "AAAAAAAAAAAAAAAAAAAAAGkb8QEAAAAAxSnlvGZ5m0yI3IwW%2BkGjpf%2BamBY%3DsBbZa0mYmKkUq8gs3pYNcsVgiIlk29SqYXoZW9IhvaqQc7j67C"

request_count = 0

def api_get(url, max_retries=3):
    global request_count
    for attempt in range(max_retries):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {BEARER}"})
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            request_count += 1
            remaining = resp.headers.get('x-rate-limit-remaining', '?')
            if remaining != '?' and int(remaining) < 5:
                reset = resp.headers.get('x-rate-limit-reset', '?')
                wait = max(1, int(reset) - int(time.time()) + 1) if reset != '?' else 16
                print(f"  [Rate limit: {remaining} remaining, waiting {wait}s]")
                time.sleep(wait)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 429:
                wait = 16 * (attempt + 1)
                print(f"  [429, waiting {wait}s]")
                time.sleep(wait)
                continue
            elif e.code == 503:
                time.sleep(5)
                continue
            return {"error": e.code, "detail": body}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"error": str(e)}
    return {"error": "max_retries_exceeded"}

def search_all(query, max_results=100, next_token=None):
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,conversation_id",
        "sort_order": "relevancy",
    }
    if next_token:
        params["next_token"] = next_token
    url = f"https://api.x.com/2/tweets/search/all?{urllib.parse.urlencode(params)}"
    time.sleep(1.1)
    return api_get(url)

def get_users(user_ids):
    if not user_ids:
        return {}
    users = {}
    for i in range(0, len(user_ids), 100):
        chunk = user_ids[i:i+100]
        url = f"https://api.x.com/2/users?ids={','.join(chunk)}&user.fields=public_metrics,name,username"
        time.sleep(0.3)
        data = api_get(url)
        if "data" in data:
            for u in data["data"]:
                users[u["id"]] = {
                    "handle": u.get("username", ""),
                    "name": u.get("name", ""),
                    "followers": u.get("public_metrics", {}).get("followers_count", 0),
                }
    return users

def get_replies(conversation_id, max_results=50):
    params = {
        "query": f"conversation_id:{conversation_id} lang:en",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,in_reply_to_user_id",
        "sort_order": "relevancy",
    }
    url = f"https://api.x.com/2/tweets/search/all?{urllib.parse.urlencode(params)}"
    time.sleep(1.1)
    return api_get(url)

def categorize_reply(text):
    lower = text.lower()
    if '?' in text and any(w in lower for w in ['how', 'what', 'why', 'should', 'does', 'can', 'is it', 'which', 'where', 'when']):
        return "QUESTION"
    if any(w in lower for w in ['i tried', 'i use', 'my experience', 'i lost', 'my results', 'i did', 'i started', 'for me it']):
        return "EXPERIENCE"
    if any(w in lower for w in ['looking for', 'recommend', 'any tool', 'i wish', 'is there a', 'know of any']):
        return "REQUEST"
    if any(w in lower for w in ["that's not", 'wrong', 'incorrect', 'disagree', 'actually', 'not true', 'misleading']):
        return "DISAGREEMENT"
    return "OTHER"

def engagement_score(m):
    return m.get("like_count", 0) + (m.get("reply_count", 0) * 2) + (m.get("bookmark_count", 0) * 1.5)

# Queries that failed due to min_faves — rewritten without it, with higher engagement post-filtering
FIXED_QUERIES = [
    # Previously failed: health_data_surprise, health_viral_stat used min_faves in query
    ("health_data_surprise_fix", "health", "Surprising health data/stats",
     '("study found" OR "research shows" OR "data shows" OR "according to") (calories OR metabolism OR sleep OR exercise OR protein OR vitamin)',
     50),

    # finance_compressed_wisdom
    ("finance_compressed_wisdom", "finance", "Short financial wisdom",
     '("rich people" OR "wealthy people" OR "money is" OR "wealth is" OR "the best investment")',
     100),

    # dev_wisdom
    ("dev_wisdom", "dev", "Compressed developer wisdom",
     '("the best code" OR "senior developer" OR "junior vs senior" OR "years of experience" OR "coding is")',
     50),

    # fitness_advice_viral
    ("fitness_advice_viral", "fitness", "Viral fitness advice",
     '("best exercise" OR "only exercise you need" OR "most important" OR "if you only do one") (exercise OR lift OR workout OR movement OR stretch)',
     50),

    # productivity_hot_take
    ("productivity_hot_take", "productivity", "Controversial productivity opinions",
     '("hustle culture" OR "work life balance" OR "burnout" OR "overwork" OR "grind" OR "rise and grind")',
     50),

    # productivity_wisdom
    ("productivity_wisdom", "productivity", "Compressed productivity wisdom",
     '("time is" OR "busy is" OR "focus is" OR "saying no" OR "the best productivity")',
     50),

    # === ALL MEME QUERIES — rewritten without min_faves ===
    ("meme_relatable", "meme", "Relatable viral observations",
     '("no one:" OR "nobody:" OR "adults be like" OR "being an adult" OR "adulting is")',
     200),

    ("meme_one_liner", "meme", "Viral one-liners",
     '("the best part about" OR "the worst part about" OR "the thing about" OR "imagine being")',
     300),

    ("meme_universal_truth", "meme", "Universal observations that went mega-viral",
     '("nobody talks about" OR "the fact that" OR "can we talk about" OR "why does nobody")',
     300),

    ("meme_contrast", "meme", "Viral contrast/comparison format",
     '("expectation:" OR "reality:" OR "what I expected" OR "what I got" OR "me vs")',
     200),

    ("meme_hot_take_viral", "meme", "Hot takes that went viral (any topic)",
     '("hot take:" OR "unpopular opinion:" OR "I don\'t care what anyone says" OR "hear me out:")',
     200),

    ("meme_wholesome", "meme", "Wholesome viral content",
     '("friendly reminder" OR "in case nobody told you" OR "reminder that you")',
     200),

    ("meme_deadpan", "meme", "Deadpan humor viral tweets",
     '("literally just" OR "apparently" OR "turns out" OR "I simply")',
     300),

    ("meme_thread_starter", "meme", "Viral thread starters / engagement hooks",
     '("what\'s something" OR "name something" OR "what\'s your" OR "drop your")',
     200),

    # === ALL REPLY PATTERN QUERIES — rewritten without min_faves, using is:reply ===
    ("reply_helpful", "reply_pattern", "Helpful replies that got likes",
     '("actually" OR "the reason is" OR "here\'s why" OR "fun fact" OR "little known fact") is:reply',
     20),

    ("reply_correction", "reply_pattern", "Corrections that got engagement",
     '("that\'s not quite" OR "small correction" OR "to be fair" OR "important to note") is:reply',
     10),

    ("reply_addition", "reply_pattern", "Additive replies that got engagement",
     '("adding to this" OR "to add to this" OR "another thing" OR "don\'t forget") is:reply',
     10),

    ("reply_personal", "reply_pattern", "Personal experience replies that resonated",
     '("this happened to me" OR "can confirm" OR "same here" OR "I went through this" OR "my experience with this") is:reply',
     10),

    ("reply_reframe", "reply_pattern", "Replies that reframe the original",
     '("another way to think about" OR "the real question is" OR "what this really means" OR "put differently") is:reply',
     10),

    ("reply_data_evidence", "reply_pattern", "Replies adding data/evidence",
     '("the study" OR "the data" OR "the research shows" OR "according to" OR "the numbers show") is:reply',
     10),
]


def main():
    global request_count
    all_tweets = []
    seen_ids = set()
    query_stats = {}

    # Load existing v5 archive data to get seen IDs
    existing_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "twitter_demand_collection_v5_archive.json")
    if os.path.exists(existing_file):
        with open(existing_file) as f:
            existing = json.load(f)
        for t in existing.get("tweets", []):
            seen_ids.add(t["id"])
        print(f"Loaded {len(seen_ids)} existing tweet IDs to avoid duplicates")

    print(f"\nRunning {len(FIXED_QUERIES)} fixed queries...\n")

    for idx, (qid, vertical, desc, query_str, min_likes) in enumerate(FIXED_QUERIES):
        print(f"[{idx+1}/{len(FIXED_QUERIES)}] {vertical}/{qid}: {desc}")

        data = search_all(query_str, max_results=100)

        if "error" in data:
            print(f"  ERROR: {data}")
            query_stats[qid] = {"count": 0, "error": str(data)}
            continue

        author_ids = list(set(t.get("author_id", "") for t in data.get("data", []) if t.get("author_id")))
        users = get_users(author_ids) if author_ids else {}

        new_tweets = []
        for t in data.get("data", []):
            tid = t["id"]
            if tid in seen_ids:
                continue
            seen_ids.add(tid)

            metrics = t.get("public_metrics", {})
            likes = metrics.get("like_count", 0)
            replies = metrics.get("reply_count", 0)

            if likes < min_likes and replies < max(2, min_likes // 5):
                continue

            author_id = t.get("author_id", "")
            user = users.get(author_id, {})

            tweet = {
                "search_id": qid,
                "vertical": vertical,
                "id": tid,
                "conversation_id": t.get("conversation_id", ""),
                "text": t.get("text", ""),
                "created_at": t.get("created_at", ""),
                "handle": user.get("handle", ""),
                "name": user.get("name", ""),
                "followers": user.get("followers", 0),
                "likes": likes,
                "replies": replies,
                "reposts": metrics.get("retweet_count", 0),
                "quotes": metrics.get("quote_count", 0),
                "bookmarks": metrics.get("bookmark_count", 0),
                "impressions": metrics.get("impression_count", 0),
                "engagement_score": engagement_score(metrics),
                "ratio": round(likes / max(user.get("followers", 1), 1), 4),
                "word_count": len(t.get("text", "").split()),
                "reply_data": [],
            }
            new_tweets.append(tweet)

        # Pagination for low-yield queries
        next_token = data.get("meta", {}).get("next_token")
        if next_token and len(new_tweets) < 20:
            print(f"  Fetching page 2...")
            data2 = search_all(query_str, max_results=100, next_token=next_token)
            if "data" in data2:
                aids2 = list(set(t.get("author_id", "") for t in data2["data"] if t.get("author_id")))
                users2 = get_users(aids2)
                for t in data2["data"]:
                    tid = t["id"]
                    if tid in seen_ids:
                        continue
                    seen_ids.add(tid)
                    metrics = t.get("public_metrics", {})
                    likes = metrics.get("like_count", 0)
                    replies = metrics.get("reply_count", 0)
                    if likes < min_likes and replies < max(2, min_likes // 5):
                        continue
                    author_id = t.get("author_id", "")
                    user = users2.get(author_id, {})
                    tweet = {
                        "search_id": qid,
                        "vertical": vertical,
                        "id": tid,
                        "conversation_id": t.get("conversation_id", ""),
                        "text": t.get("text", ""),
                        "created_at": t.get("created_at", ""),
                        "handle": user.get("handle", ""),
                        "name": user.get("name", ""),
                        "followers": user.get("followers", 0),
                        "likes": likes,
                        "replies": replies,
                        "reposts": metrics.get("retweet_count", 0),
                        "quotes": metrics.get("quote_count", 0),
                        "bookmarks": metrics.get("bookmark_count", 0),
                        "impressions": metrics.get("impression_count", 0),
                        "engagement_score": engagement_score(metrics),
                        "ratio": round(likes / max(user.get("followers", 1), 1), 4),
                        "word_count": len(t.get("text", "").split()),
                        "reply_data": [],
                    }
                    new_tweets.append(tweet)

        all_tweets.extend(new_tweets)
        query_stats[qid] = {"vertical": vertical, "description": desc, "count": len(new_tweets), "error": None}
        print(f"  → {len(new_tweets)} tweets (running total: {len(all_tweets)})")

    # Fetch replies for top 40 new tweets
    if all_tweets:
        sorted_tw = sorted(all_tweets, key=lambda t: t["engagement_score"], reverse=True)
        top = sorted_tw[:40]
        print(f"\n--- Fetching replies for top {len(top)} new tweets ---")
        total_replies = 0
        for i, tweet in enumerate(top):
            cid = tweet.get("conversation_id", "")
            if not cid:
                continue
            print(f"  [{i+1}/{len(top)}] {tweet['id']} (score: {tweet['engagement_score']:.0f})...")
            data = get_replies(cid, max_results=50)
            if "data" not in data:
                continue
            reply_aids = list(set(r.get("author_id", "") for r in data["data"] if r.get("author_id")))
            reply_users = get_users(reply_aids) if reply_aids else {}
            replies = []
            for r in data["data"]:
                if r["id"] == tweet["id"]:
                    continue
                r_text = r.get("text", "")
                r_metrics = r.get("public_metrics", {})
                r_author = reply_users.get(r.get("author_id", ""), {})
                replies.append({
                    "text": r_text,
                    "category": categorize_reply(r_text),
                    "handle": r_author.get("handle", ""),
                    "followers": r_author.get("followers", 0),
                    "likes": r_metrics.get("like_count", 0),
                    "word_count": len(r_text.split()),
                })
                total_replies += 1
            tweet["reply_data"] = replies
        print(f"  Total new replies: {total_replies}")

    # Save as separate file
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "version": "v5_fix",
        "pass_type": "archive_fix",
        "description": "Fixed queries — meme vertical, reply patterns, and others that used invalid min_faves operator.",
        "total_tweets": len(all_tweets),
        "query_stats": query_stats,
        "api_requests": request_count,
        "tweets": sorted(all_tweets, key=lambda t: t["engagement_score"], reverse=True),
    }

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "twitter_demand_collection_v5_fix.json")
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(all_tweets)} tweets to {filepath}")
    print(f"API requests: {request_count}")

    # Summary
    for v in sorted(set(t['vertical'] for t in all_tweets)):
        vc = sum(1 for t in all_tweets if t['vertical'] == v)
        print(f"  {v}: {vc}")

if __name__ == "__main__":
    main()
