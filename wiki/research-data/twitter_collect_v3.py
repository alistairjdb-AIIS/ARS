"""
Expanded Twitter Semantic Demand Collection v3
Focus: Genuine health tool/calculator demand across multiple topics
Filters: Exclude ED community signals, engagement farming
Date: 2026-03-15

Topics covered:
- TDEE / Calories (existing top traffic)
- Ozempic / GLP-1 (existing top traffic)
- IVF / Fertility (existing top traffic)
- Vitamin D (existing top traffic)
- Creatine (existing top traffic)
- Training Volume / Workout (existing top traffic)
- BMI / Body Composition (reference implementation)
- General health calculator demand
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
    if any(w in t for w in ["i tried", "i use", "i found", "my experience", "i've been", "i started", "i lost", "i gained", "i was", "mine is", "my doctor", "i weigh", "i eat", "i'm currently", "i did", "my results", "i take", "i got"]):
        return "EXPERIENCE"
    if any(w in t for w in ["is there", "can someone", "need a", "looking for", "recommend", "any tool", "any app", "wish there", "link", "where can", "what app", "what tool"]):
        return "REQUEST"
    if any(w in t for w in ["actually", "that's not", "wrong", "incorrect", "disagree", "not true", "false", "misleading"]):
        return "DISAGREEMENT"
    return "OTHER"

def is_ed_content(text):
    """Filter out eating disorder community content"""
    t = text.lower()
    ed_signals = [
        'edtwt', 'wltwt', 'proana', 'thinspo', 'meanspo',
        'purging', 'purge', 'binge and purge',
        'restrict', 'restricting', 'restriction',
        'inpatient', ' ip ', 'anorex', 'wannarex', 'bulimi',
        'metabolism day', 'metab day', 'metab ',
        '600 cal', '500 cal', '400 cal', '300 cal', '200 cal',
        '600cal', '500cal', '400cal', '300cal', '200cal',
        'body check', 'bodycheck', 'ugw', 'gw:', 'cw:',
        'eating disorder', 'my ed ', 'recovery ed',
    ]
    return any(w in t for w in ed_signals)

# ===== SEARCH STRATEGY =====
# Each tuple: (topic_category, search_name, query, use_archive)
# Queries designed to capture genuine tool demand, not ED or engagement farming

searches = [
    # === TDEE / CALORIES (genuine tool demand) ===
    ("tdee", "tdee_tool_demand", "TDEE (calculator OR calculate OR app OR tool OR accurate) -restrict -restricting -edtwt", True),
    ("tdee", "tdee_results_sharing", "\"my TDEE\" (is OR was OR says OR shows) -edtwt -restrict", True),
    ("tdee", "tdee_confusion", "TDEE (confusing OR confused OR different OR which one OR accurate OR trust) -edtwt -restrict", True),
    ("tdee", "calorie_deficit_how", "calorie deficit (how much OR how to OR calculate OR start) -edtwt -restrict -purge", True),

    # === OZEMPIC / GLP-1 (top traffic calculator) ===
    ("ozempic", "ozempic_dosing", "ozempic (dose OR dosing OR pen OR click OR inject OR mg) -spam -ad", True),
    ("ozempic", "ozempic_weight_loss", "ozempic (lost OR losing OR weight loss OR results OR progress) -spam -ad", True),
    ("ozempic", "ozempic_questions", "ozempic (how long OR when does OR side effects OR plateau OR stall)", True),
    ("ozempic", "glp1_calculator", "(ozempic OR mounjaro OR wegovy OR zepbound) (calculator OR calculate OR track OR dose)", True),

    # === IVF / FERTILITY (top traffic calculator) ===
    ("ivf", "ivf_due_date", "IVF (due date OR transfer date OR weeks pregnant OR how far along)", True),
    ("ivf", "ivf_hcg_levels", "(IVF OR fertility) (hCG OR beta OR levels OR doubling OR numbers)", True),
    ("ivf", "fertility_tracking", "(fertility OR TTC OR trying to conceive) (calculator OR tracker OR app OR tool)", True),

    # === VITAMIN D (top traffic calculator) ===
    ("vitamind", "vitamin_d_levels", "vitamin D (levels OR deficient OR deficiency OR low OR test results OR blood test)", True),
    ("vitamind", "vitamin_d_dosage", "vitamin D (how much OR dosage OR supplement OR IU OR nmol OR ng/ml)", True),
    ("vitamind", "vitamin_d_conversion", "vitamin D (conversion OR convert OR nmol OR ng OR units)", True),

    # === CREATINE (top traffic calculator) ===
    ("creatine", "creatine_dosage", "creatine (how much OR dosage OR dose OR grams OR loading OR maintenance)", True),
    ("creatine", "creatine_water", "creatine (water OR hydration OR how much water OR dehydrat)", True),
    ("creatine", "creatine_questions", "creatine (should I OR does it OR is it OR worth it OR safe)", True),

    # === TRAINING VOLUME (top traffic calculator) ===
    ("training", "training_volume", "training volume (too much OR optimal OR how many sets OR overtraining OR recovery)", True),
    ("training", "sets_per_week", "(sets per week OR weekly volume) (muscle OR growth OR hypertrophy)", True),
    ("training", "workout_split", "workout split (best OR optimal OR how many days OR push pull)", True),

    # === BMI / BODY COMPOSITION (reference implementation) ===
    ("bmi", "bmi_accuracy", "BMI (accurate OR inaccurate OR doesn't account OR muscle mass OR outdated OR stupid) -edtwt", True),
    ("bmi", "body_fat_percentage", "body fat percentage (how to OR measure OR calculate OR estimate OR what is)", True),
    ("bmi", "healthy_weight", "healthy weight (for my height OR range OR chart OR what is) -edtwt -restrict", True),

    # === GENERAL HEALTH CALCULATOR DEMAND ===
    ("general", "health_calculator_demand", "health calculator (need OR wish OR looking for OR want OR recommend)", True),
    ("general", "fitness_tool_demand", "fitness (calculator OR tool OR app) (recommend OR best OR accurate OR free)", True),
    ("general", "macro_calculator", "macro calculator (help OR confused OR which one OR recommend OR accurate)", True),

    # === CROSS-TOPIC: WHAT PEOPLE SHARE (content format signals) ===
    ("sharing", "health_results_sharing", "\"my results\" (health OR fitness OR TDEE OR BMI OR body fat OR blood test)", True),
    ("sharing", "health_numbers_viral", "health (shocked OR surprised OR blown away) (number OR result OR test)", False),
]

all_tweets = []
all_author_ids = set()

print(f"Running {len(searches)} searches...\n")

for topic, name, query, use_archive in searches:
    print(f"[{topic}/{name}]...", end=" ", flush=True)
    data = search_tweets(query, max_results=50, use_archive=use_archive)

    if "error" in data:
        print(f"ERROR {data['error']}: {data['detail'][:80]}")
        continue

    tweets = data.get("data", [])
    # Pre-filter ED content
    clean_tweets = []
    ed_filtered = 0
    for t in tweets:
        if is_ed_content(t.get("text", "")):
            ed_filtered += 1
        else:
            t["_search"] = name
            t["_topic"] = topic
            all_author_ids.add(t["author_id"])
            clean_tweets.append(t)

    all_tweets.extend(clean_tweets)
    print(f"{len(clean_tweets)} tweets ({ed_filtered} ED-filtered)")
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

# Enrich — keep anything with engagement
enriched = []
for t in unique:
    m = t.get("public_metrics", {})
    author = users.get(t["author_id"], {})
    followers = author.get("public_metrics", {}).get("followers_count", 0)
    likes = m.get("like_count", 0)
    replies = m.get("reply_count", 0)
    bookmarks = m.get("bookmark_count", 0)

    if likes >= 3 or replies >= 2 or bookmarks >= 3:
        enriched.append({
            "topic": t["_topic"],
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

enriched.sort(key=lambda t: t["bookmarks"] + t["replies"] + t["likes"], reverse=True)
print(f"\nEnriched tweets with engagement: {len(enriched)}")

# Get replies for top 60 by reply+bookmark count
top_for_replies = sorted(enriched, key=lambda t: t["replies"] + t["bookmarks"], reverse=True)[:60]
print(f"\nFetching replies for top {len(top_for_replies)} tweets...")

for i, t in enumerate(top_for_replies):
    if t["replies"] < 2:
        continue
    reply_data = get_replies(t["conversation_id"], max_results=30)
    replies_list = reply_data.get("data", [])

    new_ids = [r["author_id"] for r in replies_list if r["author_id"] not in users]
    if new_ids:
        new_users = get_users(list(set(new_ids)))
        users.update(new_users)

    for r in replies_list:
        # Filter ED content from replies too
        if is_ed_content(r.get("text", "")):
            continue
        ra = users.get(r["author_id"], {})
        t["reply_data"].append({
            "text": r["text"],
            "category": categorize_reply(r["text"]),
            "handle": ra.get("username", "?"),
            "followers": ra.get("public_metrics", {}).get("followers_count", 0),
            "likes": r.get("public_metrics", {}).get("like_count", 0),
        })

    if replies_list:
        print(f"  [{i+1}] {len(t['reply_data'])} clean replies for @{t['handle']} [{t['topic']}]")
    time.sleep(0.5)

# Save
output = {
    "date": "2026-03-15",
    "version": "v3",
    "description": "Expanded semantic demand collection — 8 topic categories, ED-filtered, genuine tool demand focus",
    "topics": list(set(t["_topic"] for t in unique)),
    "searches": [s[1] for s in searches],
    "total_raw": len(all_tweets),
    "total_unique": len(unique),
    "ed_filtering": "Applied — edtwt, restrict, purge, and related terms excluded",
    "with_engagement": len(enriched),
    "tweets": enriched,
}

path = "tools/research-data/twitter_demand_collection_v3.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*60}")
print(f"COLLECTION COMPLETE")
print(f"Saved: {path}")
print(f"Tweets: {len(enriched)}")
print(f"With replies: {sum(1 for t in enriched if t['reply_data'])}")
print(f"{'='*60}")

# Summary by topic
print(f"\n=== BY TOPIC ===")
by_topic = {}
for t in enriched:
    tp = t["topic"]
    if tp not in by_topic:
        by_topic[tp] = {"count": 0, "likes": 0, "replies": 0, "bookmarks": 0}
    by_topic[tp]["count"] += 1
    by_topic[tp]["likes"] += t["likes"]
    by_topic[tp]["replies"] += t["replies"]
    by_topic[tp]["bookmarks"] += t["bookmarks"]

for tp, stats in sorted(by_topic.items(), key=lambda x: -x[1]["count"]):
    print(f"  {stats['count']:3d} tweets | {stats['likes']:6,} likes | {stats['replies']:5,} replies | {stats['bookmarks']:5,} bkmrk | {tp}")

# Summary by search
print(f"\n=== BY SEARCH ===")
by_search = {}
for t in enriched:
    s = t["search"]
    by_search[s] = by_search.get(s, 0) + 1
for s, c in sorted(by_search.items(), key=lambda x: -x[1]):
    print(f"  {c:3d} tweets — {s}")

# Top 20 tweets
print(f"\n=== TOP 20 BY ENGAGEMENT ===")
for t in enriched[:20]:
    print(f"\n  [{t['topic']}] @{t['handle']} ({t['followers']:,} followers)")
    print(f"  {t['likes']} likes | {t['replies']} replies | {t['bookmarks']} bkmrk")
    print(f"  {t['text'][:200]}")
    if t["reply_data"]:
        cats = {}
        for r in t["reply_data"]:
            cats[r["category"]] = cats.get(r["category"], 0) + 1
        print(f"  Reply categories: {cats}")
