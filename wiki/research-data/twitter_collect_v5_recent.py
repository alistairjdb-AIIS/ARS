"""
V5 Recent Pass: Collect last 7 days of tweets using search/recent.
Same queries as archive + fix, but against recent endpoint only.
Deduplicates against both v5_archive and v5_fix datasets.
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
                print(f"  [Rate limit: waiting {wait}s]")
                time.sleep(wait)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 429:
                time.sleep(16 * (attempt + 1))
                continue
            elif e.code == 402:
                print(f"  [CREDITS DEPLETED — stopping]")
                return {"error": 402, "detail": "CreditsDepleted"}
            return {"error": e.code, "detail": body}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"error": str(e)}
    return {"error": "max_retries_exceeded"}

def search_recent(query, max_results=100):
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,conversation_id",
        "sort_order": "relevancy",
    }
    url = f"https://api.x.com/2/tweets/search/recent?{urllib.parse.urlencode(params)}"
    time.sleep(0.4)
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

def categorize_reply(text):
    lower = text.lower()
    if '?' in text and any(w in lower for w in ['how', 'what', 'why', 'should', 'does', 'can', 'is it', 'which']):
        return "QUESTION"
    if any(w in lower for w in ['i tried', 'i use', 'my experience', 'i lost', 'i did', 'i started']):
        return "EXPERIENCE"
    if any(w in lower for w in ['looking for', 'recommend', 'any tool', 'i wish', 'is there a']):
        return "REQUEST"
    if any(w in lower for w in ["that's not", 'wrong', 'incorrect', 'disagree', 'not true']):
        return "DISAGREEMENT"
    return "OTHER"

def engagement_score(m):
    return m.get("like_count", 0) + (m.get("reply_count", 0) * 2) + (m.get("bookmark_count", 0) * 1.5)

ED_SIGNALS = [
    'edtwt', 'wltwt', 'proana', 'thinspo', 'meanspo', 'purging', 'purge',
    'restrict', 'restricting', 'restriction', 'anorex', 'bulimi',
    'metabolism day', 'metab day', 'body check', 'bodycheck', 'ugw', 'gw:', 'cw:',
    'eating disorder', 'my ed ', 'recovery ed',
]

# Combined query set — all queries from archive + fix, no min_faves
QUERIES = [
    # Health
    ("health_reply_pattern", "health", 5, '("your TDEE" OR "your BMI" OR "your calories" OR "your maintenance") (is OR are OR would)'),
    ("health_tool_comparison", "health", 3, '("which calculator" OR "best calculator" OR "accurate calculator") (health OR calories OR BMI OR weight)'),
    ("health_number_sharing", "health", 3, '("my TDEE is" OR "my BMI is" OR "my body fat is" OR "my maintenance calories")'),
    ("health_frustration", "health", 3, '("every calculator gives" OR "calculators are wrong" OR "doesn\'t account for") (health OR diet OR calories)'),
    ("health_aha_moment", "health", 5, '("I didn\'t know" OR "I just learned" OR "turns out" OR "nobody tells you") (calories OR protein OR metabolism OR sleep OR vitamin)'),
    ("health_advice_reply", "health", 3, '("you should try" OR "what worked for me" OR "I recommend") (calories OR TDEE OR protein OR supplement OR workout)'),
    ("health_data_surprise", "health", 10, '("study found" OR "research shows" OR "data shows" OR "according to") (calories OR metabolism OR sleep OR exercise OR protein)'),
    ("health_myth_busting", "health", 10, '("myth" OR "actually wrong" OR "not true" OR "misconception") (calories OR metabolism OR BMI OR weight loss OR protein)'),
    ("health_protocol", "health", 5, '("my routine" OR "my protocol" OR "my stack" OR "every morning") (supplement OR vitamin OR creatine OR protein OR magnesium)'),
    ("health_viral_stat", "health", 10, '("percent of" OR "% of" OR "average person" OR "most people don\'t") (sleep OR calories OR exercise OR water OR protein)'),
    # Finance
    ("finance_calculator", "finance", 5, '("compound interest" OR "retirement calculator" OR "savings calculator" OR "investment calculator")'),
    ("finance_number_sharing", "finance", 10, '("my net worth" OR "my savings" OR "I finally hit" OR "my portfolio") (k OR thousand OR million) -crypto -nft'),
    ("finance_aha", "finance", 10, '("I didn\'t realize" OR "nobody tells you" OR "turns out") (money OR savings OR investing OR compound OR taxes OR debt)'),
    ("finance_comparison", "finance", 5, '("vs" OR "versus" OR "compared to") (renting OR owning OR investing OR saving OR ETF OR index)'),
    ("finance_rule", "finance", 10, '("rule of" OR "the formula" OR "the math" OR "simple math") (money OR investing OR retirement OR savings OR wealth)'),
    ("finance_frustration", "finance", 10, '("makes no sense" OR "is a scam" OR "rigged" OR "nobody teaches") (money OR taxes OR insurance OR salary OR rent)'),
    ("finance_wisdom", "finance", 30, '("rich people" OR "wealthy people" OR "money is" OR "wealth is" OR "the best investment")'),
    # Dev
    ("dev_tool_rec", "dev", 5, '("best tool" OR "game changer" OR "switched to" OR "can\'t live without") (code OR developer OR programming OR IDE OR git)'),
    ("dev_tip", "dev", 10, '("TIL" OR "pro tip" OR "did you know" OR "most developers") (code OR git OR CSS OR JavaScript OR Python OR API)'),
    ("dev_hot_take", "dev", 10, '("hot take" OR "unpopular opinion" OR "I said what I said") (code OR developer OR programming OR engineer OR frontend)'),
    ("dev_frustration", "dev", 5, '("why does" OR "who decided" OR "I hate" OR "drives me crazy") (code OR CSS OR JavaScript OR deployment OR debugging)'),
    ("dev_wisdom", "dev", 15, '("the best code" OR "senior developer" OR "junior vs senior" OR "years of experience" OR "coding is")'),
    ("dev_career", "dev", 10, '("I quit" OR "I got fired" OR "I got hired" OR "salary" OR "interview tip") (developer OR engineer OR software OR tech)'),
    ("dev_meme", "dev", 10, '("developers be like" OR "programmer:" OR "when the code" OR "git commit" OR "production")'),
    # Fitness
    ("fitness_numbers", "fitness", 5, '("my bench" OR "my squat" OR "my deadlift" OR "my PR" OR "new PR" OR "personal record") (lbs OR kg)'),
    ("fitness_transformation", "fitness", 10, '("month transformation" OR "year transformation" OR "before and after" OR "progress") (muscle OR weight OR lbs OR body fat)'),
    ("fitness_protocol", "fitness", 5, '("my split" OR "my routine" OR "my program" OR "workout split" OR "training split" OR "push pull legs")'),
    ("fitness_science", "fitness", 5, '("study shows" OR "research shows" OR "evidence" OR "science says") (muscle OR strength OR hypertrophy OR protein OR volume)'),
    ("fitness_myth", "fitness", 5, '("myth" OR "stop" OR "you don\'t need" OR "overrated") (cardio OR abs OR toning OR spot reduce OR meal timing)'),
    ("fitness_comparison", "fitness", 5, '("vs" OR "versus" OR "better than") (creatine OR protein OR cardio OR lifting OR HIIT OR zone 2 OR running)'),
    ("fitness_hot_take", "fitness", 10, '("hot take" OR "unpopular opinion" OR "nobody wants to hear") (gym OR fitness OR workout OR training OR diet)'),
    # Productivity
    ("prod_tool", "productivity", 5, '("game changer" OR "changed my life" OR "best tool" OR "can\'t live without") (productivity OR workflow OR notes OR notion OR obsidian)'),
    ("prod_system", "productivity", 5, '("my system" OR "my workflow" OR "my process" OR "morning routine") (work OR productive OR focus OR deep work)'),
    ("prod_insight", "productivity", 10, '("most productive" OR "time management" OR "the secret" OR "I stopped") (productive OR busy OR work OR focus OR meetings)'),
    ("prod_hot_take", "productivity", 15, '("hustle culture" OR "work life balance" OR "burnout" OR "overwork" OR "grind")'),
    ("prod_wisdom", "productivity", 15, '("time is" OR "busy is" OR "focus is" OR "saying no" OR "the best productivity")'),
    ("prod_framework", "productivity", 5, '("framework" OR "mental model" OR "the rule" OR "the 80/20" OR "pareto") (work OR productivity OR time OR decision)'),
    # Meme
    ("meme_relatable", "meme", 50, '("no one:" OR "nobody:" OR "adults be like" OR "being an adult" OR "adulting is")'),
    ("meme_one_liner", "meme", 50, '("the best part about" OR "the worst part about" OR "the thing about" OR "imagine being")'),
    ("meme_universal", "meme", 50, '("nobody talks about" OR "the fact that" OR "can we talk about" OR "why does nobody")'),
    ("meme_contrast", "meme", 50, '("expectation:" OR "reality:" OR "what I expected" OR "what I got" OR "me vs")'),
    ("meme_hot_take", "meme", 50, '("hot take:" OR "unpopular opinion:" OR "hear me out:")'),
    ("meme_wholesome", "meme", 50, '("friendly reminder" OR "in case nobody told you" OR "reminder that you")'),
    ("meme_deadpan", "meme", 50, '("literally just" OR "apparently" OR "turns out" OR "I simply")'),
    ("meme_thread", "meme", 50, '("what\'s something" OR "name something" OR "what\'s your" OR "drop your")'),
    # Reply patterns
    ("reply_helpful", "reply_pattern", 5, '("actually" OR "the reason is" OR "here\'s why" OR "fun fact") is:reply'),
    ("reply_correction", "reply_pattern", 3, '("that\'s not quite" OR "small correction" OR "to be fair" OR "important to note") is:reply'),
    ("reply_addition", "reply_pattern", 3, '("adding to this" OR "to add to this" OR "another thing" OR "don\'t forget") is:reply'),
    ("reply_personal", "reply_pattern", 3, '("this happened to me" OR "can confirm" OR "same here" OR "my experience with this") is:reply'),
    ("reply_reframe", "reply_pattern", 3, '("another way to think about" OR "the real question is" OR "what this really means") is:reply'),
    ("reply_data", "reply_pattern", 3, '("the study" OR "the data" OR "the research shows" OR "the numbers show") is:reply'),
]

def main():
    global request_count
    basedir = os.path.dirname(os.path.abspath(__file__))

    # Load existing IDs from archive + fix
    seen_ids = set()
    for fname in ["twitter_demand_collection_v5_archive.json", "twitter_demand_collection_v5_fix.json"]:
        fpath = os.path.join(basedir, fname)
        if os.path.exists(fpath):
            with open(fpath) as f:
                for t in json.load(f).get("tweets", []):
                    seen_ids.add(t["id"])
    print(f"Loaded {len(seen_ids)} existing IDs")

    all_tweets = []
    query_stats = {}
    credits_depleted = False

    print(f"\nRunning {len(QUERIES)} queries against search/recent...\n")

    for idx, (qid, vertical, min_likes, query_str) in enumerate(QUERIES):
        if credits_depleted:
            break

        print(f"[{idx+1}/{len(QUERIES)}] {vertical}/{qid}")

        data = search_recent(query_str, max_results=100)

        if "error" in data:
            if data.get("error") == 402:
                credits_depleted = True
                break
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

            text = t.get("text", "")
            if vertical in ("health", "fitness") and any(s in text.lower() for s in ED_SIGNALS):
                continue

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
                "text": text,
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
                "word_count": len(text.split()),
                "reply_data": [],
            }
            new_tweets.append(tweet)

        all_tweets.extend(new_tweets)
        query_stats[qid] = {"vertical": vertical, "count": len(new_tweets), "error": None}
        print(f"  → {len(new_tweets)} tweets (total: {len(all_tweets)})")

    if credits_depleted:
        print(f"\n[CREDITS DEPLETED after {idx+1} queries]")

    # Save
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "version": "v5_recent",
        "pass_type": "recent",
        "description": "Recent 7-day pass — same queries as archive, search/recent endpoint.",
        "total_tweets": len(all_tweets),
        "queries_completed": sum(1 for v in query_stats.values() if v.get("error") is None),
        "queries_total": len(QUERIES),
        "credits_depleted": credits_depleted,
        "query_stats": query_stats,
        "api_requests": request_count,
        "tweets": sorted(all_tweets, key=lambda t: t["engagement_score"], reverse=True),
    }

    filepath = os.path.join(basedir, "twitter_demand_collection_v5_recent.json")
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(all_tweets)} tweets to {filepath}")
    print(f"API requests: {request_count}")
    for v in sorted(set(t['vertical'] for t in all_tweets)):
        print(f"  {v}: {sum(1 for t in all_tweets if t['vertical'] == v)}")

if __name__ == "__main__":
    main()
