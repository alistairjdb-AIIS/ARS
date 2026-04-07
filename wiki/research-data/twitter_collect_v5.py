"""
Cross-Vertical Tweet Collection v5
Purpose: Collect 2000+ high-engagement tweets across 6 verticals for atomic decomposition.
Date: 2026-03-18

Verticals:
1. Health/wellness tools (extend existing v3/v4 dataset)
2. Personal finance tools (budgeting, investing, FIRE, tax)
3. Developer tools (coding tips, open source, dev productivity)
4. Fitness/quantified-self (workout tracking, body comp, running)
5. Productivity/SaaS (time management, workflow, tools)
6. Meme/entertainment (viral, humor, relatable — control group)

Two-pass approach:
- Pass 1: Full archive (search/all) — long-tail durable patterns
- Pass 2: Recent 7 days (search/recent) — short-tail current patterns

Engagement criteria: likes + replies combined, normalized by follower count where available.
Reply capture: Top 80 tweets by engagement get reply threads pulled.

Compatible with v3/v4 JSON schema, extended with:
- vertical (new): which of the 6 verticals
- pass_type: "archive" or "recent"
- engagement_score: likes + (replies * 2) — replies weighted 2x per algo research (75x signal)
"""

import urllib.request
import urllib.parse
import json
import time
import sys
import os
from datetime import datetime, timedelta

BEARER = "AAAAAAAAAAAAAAAAAAAAAGkb8QEAAAAAxSnlvGZ5m0yI3IwW%2BkGjpf%2BamBY%3DsBbZa0mYmKkUq8gs3pYNcsVgiIlk29SqYXoZW9IhvaqQc7j67C"

# --- ED Filter (carried from v3) ---
ED_SIGNALS = [
    'edtwt', 'wltwt', 'proana', 'thinspo', 'meanspo',
    'purging', 'purge', 'binge and purge',
    'restrict', 'restricting', 'restriction',
    'inpatient', ' ip ', 'anorex', 'wannarex', 'bulimi',
    'metabolism day', 'metab day', 'metab ',
    '600 cal', '500 cal', '400 cal', '300 cal', '200 cal',
    'body check', 'bodycheck', 'ugw', 'gw:', 'cw:',
    'eating disorder', 'my ed ', 'recovery ed',
]

def has_ed_signal(text):
    lower = text.lower()
    return any(sig in lower for sig in ED_SIGNALS)

# --- API Layer ---
request_count = 0
start_time = time.time()

def api_get(url, max_retries=3):
    global request_count
    for attempt in range(max_retries):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {BEARER}"})
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            request_count += 1
            # Rate limit headers
            remaining = resp.headers.get('x-rate-limit-remaining', '?')
            reset = resp.headers.get('x-rate-limit-reset', '?')
            if remaining != '?' and int(remaining) < 5:
                wait = max(1, int(reset) - int(time.time()) + 1) if reset != '?' else 16
                print(f"  [Rate limit: {remaining} remaining, waiting {wait}s]")
                time.sleep(wait)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 429:
                wait = 16 * (attempt + 1)
                print(f"  [429 rate limited, waiting {wait}s (attempt {attempt+1})]")
                time.sleep(wait)
                continue
            elif e.code == 503:
                print(f"  [503 service unavailable, waiting 5s]")
                time.sleep(5)
                continue
            return {"error": e.code, "detail": body}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"error": str(e)}
    return {"error": "max_retries_exceeded"}

def search_tweets(query, max_results=100, use_archive=True, next_token=None):
    """Search tweets. use_archive=True hits search/all (Pro tier)."""
    endpoint = "all" if use_archive else "recent"
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id,conversation_id",
        "sort_order": "relevancy",
    }
    if next_token:
        params["next_token"] = next_token
    url = f"https://api.x.com/2/tweets/search/{endpoint}?{urllib.parse.urlencode(params)}"
    time.sleep(1.1 if use_archive else 0.4)  # search/all has 1req/sec limit
    return api_get(url)

def get_users(user_ids):
    """Batch user lookup. Max 100 per call."""
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

def get_replies(conversation_id, max_results=30):
    """Fetch replies to a conversation."""
    query = f"conversation_id:{conversation_id} -is:retweet"
    params = {
        "query": f"{query} lang:en",
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,created_at,author_id",
    }
    url = f"https://api.x.com/2/tweets/search/all?{urllib.parse.urlencode(params)}"
    time.sleep(1.1)
    return api_get(url)

def categorize_reply(text):
    """Categorize reply type."""
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

# --- Query Definitions ---
# Each query: (id, vertical, description, query_string, min_likes)
# min_likes is the engagement floor for this query type

QUERIES = [
    # === VERTICAL 1: HEALTH/WELLNESS TOOLS ===
    # (Extending v3/v4 — new angles not covered before)
    ("health_reply_pattern", "health", "Replies to health posts that got engagement",
     '("your TDEE" OR "your BMI" OR "your calories" OR "your maintenance") (is OR are OR would)',
     10),
    ("health_tool_comparison", "health", "People comparing health tools/calculators",
     '("which calculator" OR "best calculator" OR "accurate calculator" OR "calculator says") (health OR calories OR BMI OR weight OR body fat)',
     5),
    ("health_number_sharing", "health", "People sharing their health numbers",
     '("my TDEE is" OR "my BMI is" OR "my body fat is" OR "my maintenance calories" OR "my resting metabolic")',
     3),
    ("health_frustration", "health", "Frustration with health tools/info",
     '("every calculator gives" OR "calculators are wrong" OR "doesn\'t account for" OR "one size fits all") (health OR diet OR calories OR weight)',
     5),
    ("health_aha_moment", "health", "Health insights that surprised people",
     '("I didn\'t know" OR "I just learned" OR "turns out" OR "nobody tells you" OR "no one told me") (calories OR protein OR metabolism OR sleep OR vitamin OR supplement)',
     10),
    ("health_advice_reply", "health", "Advice given in health reply threads",
     '("you should try" OR "what worked for me" OR "I recommend" OR "have you tried") (calories OR TDEE OR protein OR supplement OR workout OR sleep)',
     5),
    ("health_data_surprise", "health", "Surprising health data/stats",
     '("study found" OR "research shows" OR "data shows" OR "according to") (calories OR metabolism OR sleep OR exercise OR protein OR vitamin) min_faves:50',
     50),
    ("health_myth_busting", "health", "Debunking health myths",
     '("myth" OR "actually wrong" OR "not true" OR "misconception" OR "stop saying") (calories OR metabolism OR BMI OR weight loss OR muscle OR protein)',
     20),
    ("health_protocol", "health", "Health protocols/routines shared",
     '("my routine" OR "my protocol" OR "my stack" OR "every morning" OR "before bed") (supplement OR vitamin OR creatine OR protein OR magnesium OR sleep)',
     10),
    ("health_viral_stat", "health", "Viral health statistics",
     '("percent of" OR "% of" OR "average person" OR "most people don\'t") (sleep OR calories OR exercise OR water OR protein OR walk OR steps)',
     50),

    # === VERTICAL 2: PERSONAL FINANCE TOOLS ===
    ("finance_calculator", "finance", "People using/wanting finance calculators",
     '("compound interest" OR "retirement calculator" OR "savings calculator" OR "investment calculator" OR "net worth calculator")',
     10),
    ("finance_number_sharing", "finance", "People sharing financial numbers/milestones",
     '("my net worth" OR "my savings" OR "I finally hit" OR "my portfolio" OR "I saved") (k OR thousand OR million) -crypto -nft',
     20),
    ("finance_aha", "finance", "Financial insights that clicked",
     '("I didn\'t realize" OR "nobody tells you" OR "I just learned" OR "turns out" OR "mind blowing") (money OR savings OR investing OR compound OR interest OR taxes OR debt)',
     20),
    ("finance_comparison", "finance", "Financial comparisons/contrasts",
     '("vs" OR "versus" OR "compared to" OR "difference between") (renting OR owning OR investing OR saving OR ETF OR index OR stocks OR bonds)',
     10),
    ("finance_rule_of_thumb", "finance", "Financial rules/heuristics shared",
     '("rule of" OR "the formula" OR "the math" OR "simple math" OR "here\'s the math") (money OR investing OR retirement OR savings OR compound OR wealth)',
     20),
    ("finance_advice_reply", "finance", "Financial advice in replies",
     '("you should" OR "what I did" OR "here\'s what" OR "the trick is") (invest OR save OR budget OR debt OR retirement OR compound)',
     10),
    ("finance_frustration", "finance", "Frustration with financial systems",
     '("makes no sense" OR "is a scam" OR "rigged" OR "broken system" OR "nobody teaches") (money OR taxes OR insurance OR salary OR rent OR housing)',
     20),
    ("finance_compressed_wisdom", "finance", "Short financial wisdom",
     '("rich people" OR "wealthy people" OR "money is" OR "wealth is" OR "the best investment") min_faves:100',
     100),

    # === VERTICAL 3: DEVELOPER TOOLS ===
    ("dev_tool_rec", "dev", "Developer tool recommendations",
     '("best tool" OR "game changer" OR "switched to" OR "started using" OR "can\'t live without") (code OR coding OR developer OR programming OR IDE OR terminal OR git)',
     10),
    ("dev_tip", "dev", "Developer tips that went viral",
     '("TIL" OR "pro tip" OR "did you know" OR "most developers" OR "stop using") (code OR coding OR git OR CSS OR JavaScript OR Python OR API OR React)',
     20),
    ("dev_hot_take", "dev", "Controversial developer opinions",
     '("hot take" OR "unpopular opinion" OR "I said what I said" OR "fight me") (code OR developer OR programming OR engineer OR frontend OR backend OR startup)',
     20),
    ("dev_frustration", "dev", "Developer frustrations",
     '("why does" OR "who decided" OR "I hate" OR "drives me crazy" OR "pain") (code OR CSS OR JavaScript OR deployment OR production OR debugging OR merge)',
     15),
    ("dev_wisdom", "dev", "Compressed developer wisdom",
     '("the best code" OR "senior developer" OR "junior vs senior" OR "years of experience" OR "coding is") min_faves:50',
     50),
    ("dev_career", "dev", "Developer career insights",
     '("I quit" OR "I got fired" OR "I got hired" OR "salary" OR "interview tip" OR "career advice") (developer OR engineer OR programmer OR software OR tech)',
     20),
    ("dev_meme_wisdom", "dev", "Dev humor with insight",
     '("developers be like" OR "programmer:" OR "when the code" OR "git commit" OR "production") (😂 OR 💀 OR 😭 OR lmao OR lol)',
     30),
    ("dev_reply_help", "dev", "Helpful dev replies",
     '("try this" OR "the fix is" OR "you need to" OR "the issue is" OR "here\'s how") (code OR bug OR error OR deploy OR CSS OR JavaScript OR Python)',
     5),

    # === VERTICAL 4: FITNESS/QUANTIFIED SELF ===
    ("fitness_number_sharing", "fitness", "People sharing fitness numbers",
     '("my bench" OR "my squat" OR "my deadlift" OR "my PR" OR "new PR" OR "personal record" OR "personal best") (lbs OR kg OR pounds)',
     10),
    ("fitness_transformation", "fitness", "Body transformation/progress posts",
     '("month transformation" OR "year transformation" OR "before and after" OR "progress pic" OR "lost" OR "gained") (muscle OR weight OR lbs OR kg OR body fat)',
     20),
    ("fitness_protocol", "fitness", "Workout protocols shared",
     '("my split" OR "my routine" OR "my program" OR "workout split" OR "training split" OR "push pull legs" OR "upper lower")',
     10),
    ("fitness_science", "fitness", "Fitness science/studies shared",
     '("study shows" OR "research shows" OR "evidence" OR "science says" OR "data shows") (muscle OR strength OR hypertrophy OR protein OR training OR volume OR sets)',
     15),
    ("fitness_myth_bust", "fitness", "Fitness myths debunked",
     '("myth" OR "stop" OR "you don\'t need" OR "overrated" OR "actually wrong") (cardio OR abs OR toning OR spot reduce OR meal timing OR protein window)',
     15),
    ("fitness_advice_viral", "fitness", "Viral fitness advice",
     '("best exercise" OR "only exercise you need" OR "most important" OR "if you only do one") (exercise OR lift OR workout OR movement OR stretch) min_faves:50',
     50),
    ("fitness_comparison", "fitness", "Fitness comparisons",
     '("vs" OR "versus" OR "or" OR "better than") (creatine OR protein OR cardio OR lifting OR HIIT OR zone 2 OR running OR walking)',
     10),
    ("fitness_hot_take", "fitness", "Controversial fitness opinions",
     '("hot take" OR "unpopular opinion" OR "nobody wants to hear" OR "the truth about") (gym OR fitness OR workout OR training OR diet OR bulk OR cut)',
     20),

    # === VERTICAL 5: PRODUCTIVITY/SAAS ===
    ("productivity_tool", "productivity", "Productivity tool recommendations",
     '("game changer" OR "changed my life" OR "best tool" OR "switched from" OR "can\'t live without") (productivity OR workflow OR notes OR task OR calendar OR notion OR obsidian)',
     15),
    ("productivity_system", "productivity", "Productivity systems shared",
     '("my system" OR "my workflow" OR "my process" OR "how I organize" OR "morning routine" OR "daily routine") (work OR productive OR focus OR deep work OR time)',
     10),
    ("productivity_insight", "productivity", "Productivity insights",
     '("most productive" OR "time management" OR "the secret" OR "nobody tells you" OR "I stopped") (productive OR busy OR work OR focus OR meetings OR email)',
     20),
    ("productivity_hot_take", "productivity", "Controversial productivity opinions",
     '("hustle culture" OR "work life balance" OR "burnout" OR "overwork" OR "grind" OR "rise and grind") min_faves:50',
     50),
    ("productivity_wisdom", "productivity", "Compressed productivity wisdom",
     '("time is" OR "busy is" OR "focus is" OR "saying no" OR "the best productivity") min_faves:50',
     50),
    ("productivity_framework", "productivity", "Productivity frameworks/mental models",
     '("framework" OR "mental model" OR "the rule" OR "principle" OR "the 80/20" OR "pareto") (work OR productivity OR time OR focus OR decision)',
     15),
    ("productivity_anti", "productivity", "Anti-productivity/rest advocacy",
     '("rest is" OR "do nothing" OR "stop optimizing" OR "it\'s okay to" OR "you don\'t have to") (productive OR busy OR hustle OR grind OR optimize)',
     15),

    # === VERTICAL 6: MEME/ENTERTAINMENT (control group) ===
    ("meme_relatable", "meme", "Relatable viral observations",
     '("no one:" OR "nobody:" OR "me:" OR "everyone:" OR "adults be like" OR "being an adult") min_faves:500',
     500),
    ("meme_one_liner", "meme", "Viral one-liners",
     '("the best part about" OR "the worst part about" OR "the thing about" OR "imagine being") min_faves:1000',
     1000),
    ("meme_universal_truth", "meme", "Universal observations that went mega-viral",
     '("we all" OR "everyone has" OR "nobody talks about" OR "the fact that" OR "can we talk about") min_faves:1000',
     1000),
    ("meme_contrast", "meme", "Viral contrast/comparison format",
     '("vs" OR "but then" OR "expectation:" OR "reality:" OR "what I expected" OR "what I got") min_faves:500',
     500),
    ("meme_hot_take_viral", "meme", "Hot takes that went viral (any topic)",
     '("hot take" OR "unpopular opinion" OR "I don\'t care what anyone says" OR "hear me out") min_faves:500',
     500),
    ("meme_wholesome", "meme", "Wholesome viral content",
     '("reminder that" OR "friendly reminder" OR "in case nobody told you" OR "you are" OR "be kind") min_faves:500',
     500),
    ("meme_deadpan", "meme", "Deadpan humor viral tweets",
     '("simply" OR "just" OR "literally just" OR "apparently" OR "turns out") min_faves:1000',
     1000),
    ("meme_thread_starter", "meme", "Viral thread starters / engagement hooks",
     '("what\'s something" OR "name something" OR "what\'s your" OR "drop your" OR "tell me") min_faves:500',
     500),

    # === CROSS-VERTICAL: REPLY PATTERNS ===
    # These specifically target high-engagement REPLIES (not original posts)
    ("reply_helpful", "reply_pattern", "Helpful replies that got likes",
     '("actually" OR "the reason" OR "here\'s why" OR "fun fact" OR "little known") min_faves:50 is:reply',
     50),
    ("reply_correction", "reply_pattern", "Corrections that got engagement",
     '("that\'s not quite" OR "small correction" OR "to be fair" OR "important to note" OR "well actually") min_faves:20 is:reply',
     20),
    ("reply_addition", "reply_pattern", "Additive replies that got engagement",
     '("also" OR "adding to this" OR "to add" OR "another thing" OR "don\'t forget") min_faves:20 is:reply',
     20),
    ("reply_personal", "reply_pattern", "Personal experience replies that resonated",
     '("this happened to me" OR "can confirm" OR "same here" OR "I went through" OR "my experience") min_faves:20 is:reply',
     20),
    ("reply_reframe", "reply_pattern", "Replies that reframe the original",
     '("another way to think about" OR "the real question" OR "what this really means" OR "put differently") min_faves:15 is:reply',
     15),
    ("reply_data", "reply_pattern", "Replies adding data/evidence",
     '("study" OR "data" OR "research" OR "according to" OR "the numbers") min_faves:15 is:reply',
     15),
]

def compute_engagement_score(metrics):
    """Engagement score: likes + (replies * 2). Replies weighted 2x per algo research."""
    likes = metrics.get("like_count", 0)
    replies = metrics.get("reply_count", 0)
    bookmarks = metrics.get("bookmark_count", 0)
    return likes + (replies * 2) + (bookmarks * 1.5)

def process_tweets(raw_data, query_id, vertical, users, min_likes):
    """Process raw API response into structured tweets."""
    tweets = []
    if "data" not in raw_data:
        return tweets

    for t in raw_data["data"]:
        text = t.get("text", "")

        # ED filter (only for health/fitness verticals)
        if vertical in ("health", "fitness") and has_ed_signal(text):
            continue

        metrics = t.get("public_metrics", {})
        likes = metrics.get("like_count", 0)
        replies_count = metrics.get("reply_count", 0)

        # Engagement floor
        if likes < min_likes and replies_count < max(2, min_likes // 5):
            continue

        author_id = t.get("author_id", "")
        user = users.get(author_id, {})
        followers = user.get("followers", 0)

        tweet = {
            "search_id": query_id,
            "vertical": vertical,
            "id": t["id"],
            "conversation_id": t.get("conversation_id", ""),
            "text": text,
            "created_at": t.get("created_at", ""),
            "handle": user.get("handle", ""),
            "name": user.get("name", ""),
            "followers": followers,
            "likes": likes,
            "replies": replies_count,
            "reposts": metrics.get("retweet_count", 0),
            "quotes": metrics.get("quote_count", 0),
            "bookmarks": metrics.get("bookmark_count", 0),
            "impressions": metrics.get("impression_count", 0),
            "engagement_score": compute_engagement_score(metrics),
            "ratio": round(likes / max(followers, 1), 4),
            "word_count": len(text.split()),
        }
        tweets.append(tweet)

    return tweets

def collect_pass(pass_type="archive", target_queries=None):
    """
    Run one collection pass.
    pass_type: "archive" (search/all) or "recent" (search/recent, last 7 days)
    """
    use_archive = (pass_type == "archive")
    all_tweets = []
    seen_ids = set()
    query_stats = {}

    queries = QUERIES if target_queries is None else [q for q in QUERIES if q[0] in target_queries]

    print(f"\n{'='*60}")
    print(f"  PASS: {pass_type.upper()} | {len(queries)} queries | {'search/all' if use_archive else 'search/recent'}")
    print(f"{'='*60}\n")

    for idx, (qid, vertical, desc, query_str, min_likes) in enumerate(queries):
        print(f"[{idx+1}/{len(queries)}] {vertical}/{qid}: {desc}")

        # First page
        data = search_tweets(query_str, max_results=100, use_archive=use_archive)

        if "error" in data:
            print(f"  ERROR: {data}")
            query_stats[qid] = {"count": 0, "error": str(data.get("error", "unknown"))}
            continue

        # Collect author IDs for batch lookup
        author_ids = []
        if "data" in data:
            author_ids = list(set(t.get("author_id", "") for t in data["data"] if t.get("author_id")))

        # Look up users
        users = get_users(author_ids) if author_ids else {}

        # Process tweets
        tweets = process_tweets(data, qid, vertical, users, min_likes)

        # Pagination — get second page if available and we have few results
        next_token = data.get("meta", {}).get("next_token")
        if next_token and len(tweets) < 30:
            print(f"  Fetching page 2...")
            data2 = search_tweets(query_str, max_results=100, use_archive=use_archive, next_token=next_token)
            if "data" in data2:
                author_ids2 = list(set(t.get("author_id", "") for t in data2["data"] if t.get("author_id")))
                users2 = get_users(author_ids2)
                tweets.extend(process_tweets(data2, qid, vertical, users2, min_likes))

        # Dedup within this query and globally
        new_tweets = []
        for tw in tweets:
            if tw["id"] not in seen_ids:
                seen_ids.add(tw["id"])
                new_tweets.append(tw)

        all_tweets.extend(new_tweets)
        query_stats[qid] = {
            "vertical": vertical,
            "description": desc,
            "count": len(new_tweets),
            "error": None,
        }
        print(f"  → {len(new_tweets)} tweets (total: {len(all_tweets)})")

    return all_tweets, query_stats

def fetch_reply_data(tweets, top_n=80):
    """Fetch reply threads for the top N tweets by engagement score."""
    sorted_tweets = sorted(tweets, key=lambda t: t["engagement_score"], reverse=True)
    top_tweets = [t for t in sorted_tweets[:top_n] if t.get("conversation_id")]

    print(f"\n--- Fetching replies for top {len(top_tweets)} tweets ---")

    reply_count = 0
    for i, tweet in enumerate(top_tweets):
        cid = tweet["conversation_id"]
        print(f"  [{i+1}/{len(top_tweets)}] Replies for {tweet['id']} (score: {tweet['engagement_score']:.0f})...")

        data = get_replies(cid, max_results=30)

        if "data" not in data:
            tweet["reply_data"] = []
            continue

        # Get reply authors
        reply_author_ids = list(set(r.get("author_id", "") for r in data["data"] if r.get("author_id")))
        reply_users = get_users(reply_author_ids) if reply_author_ids else {}

        replies = []
        for r in data["data"]:
            if r["id"] == tweet["id"]:  # skip the original tweet
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
            reply_count += 1

        tweet["reply_data"] = replies

    # Add empty reply_data to tweets that didn't get fetched
    for tweet in tweets:
        if "reply_data" not in tweet:
            tweet["reply_data"] = []

    print(f"  Total replies collected: {reply_count}")
    return tweets

def save_results(tweets, query_stats, pass_type, filename):
    """Save collection results to JSON."""
    # Vertical summary
    vertical_summary = {}
    for t in tweets:
        v = t["vertical"]
        if v not in vertical_summary:
            vertical_summary[v] = {"count": 0, "avg_engagement": 0, "total_engagement": 0}
        vertical_summary[v]["count"] += 1
        vertical_summary[v]["total_engagement"] += t["engagement_score"]
    for v in vertical_summary:
        c = vertical_summary[v]["count"]
        vertical_summary[v]["avg_engagement"] = round(vertical_summary[v]["total_engagement"] / max(c, 1), 1)

    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "version": "v5",
        "pass_type": pass_type,
        "description": f"Cross-vertical tweet collection v5 — {pass_type} pass. 6 verticals + reply patterns.",
        "verticals": list(set(t["vertical"] for t in tweets)),
        "total_tweets": len(tweets),
        "vertical_summary": vertical_summary,
        "query_stats": query_stats,
        "api_requests": request_count,
        "tweets": sorted(tweets, key=lambda t: t["engagement_score"], reverse=True),
    }

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(tweets)} tweets to {filepath}")
    print(f"API requests used: {request_count}")
    return filepath

def main():
    global request_count

    # Parse args
    pass_type = "archive"
    if len(sys.argv) > 1:
        if sys.argv[1] in ("archive", "recent"):
            pass_type = sys.argv[1]
        else:
            print(f"Usage: python3 {sys.argv[0]} [archive|recent]")
            sys.exit(1)

    print(f"Twitter Collection v5 — {pass_type.upper()} pass")
    print(f"Queries: {len(QUERIES)} | Verticals: 6 + reply patterns")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Collect
    tweets, stats = collect_pass(pass_type=pass_type)

    if not tweets:
        print("No tweets collected. Check API access.")
        return

    # Fetch replies for top tweets
    tweets = fetch_reply_data(tweets, top_n=80)

    # Save
    filename = f"twitter_demand_collection_v5_{pass_type}.json"
    save_results(tweets, stats, pass_type, filename)

    # Summary
    print(f"\n{'='*60}")
    print(f"  COLLECTION COMPLETE")
    print(f"{'='*60}")
    print(f"  Pass: {pass_type}")
    print(f"  Total tweets: {len(tweets)}")
    print(f"  Tweets with replies: {sum(1 for t in tweets if t.get('reply_data'))}")
    for v in sorted(set(t['vertical'] for t in tweets)):
        vc = sum(1 for t in tweets if t['vertical'] == v)
        print(f"  {v}: {vc} tweets")
    print(f"  API requests: {request_count}")
    elapsed = time.time() - start_time
    print(f"  Elapsed: {elapsed/60:.1f} minutes")

if __name__ == "__main__":
    main()
