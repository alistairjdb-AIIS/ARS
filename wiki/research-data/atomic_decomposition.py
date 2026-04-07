"""
Atomic Decomposition Engine v1
Reverse-engineered from the Jack Butcher writing profile methodology.

Approach:
1. Merge all v5 datasets into one unified corpus
2. Split 70/30 train/holdout
3. Group by vertical for cross-domain analysis
4. Feed batches to Claude API for atomic extraction
5. Cross-reference atoms across verticals (universal vs specific)
6. Validate discovered atoms against holdout set
7. Output: gethealthc.md

The Jack Butcher profile extracted these atom categories:
- Voice characteristics (directness, perspective, punctuation patterns)
- Statistical signatures (word count distribution, engagement sweet spots)
- Structural templates (sentence patterns, opening/closing patterns)
- Rhetorical devices (contrast frames, word-level mechanics)
- Absence patterns (what never appears)
- Vocabulary signatures (recurring words, banned words)
- Tone markers

We extend this with:
- Cross-vertical universal atoms vs vertical-specific atoms
- Reply-specific atoms (different from original post atoms)
- Temporal stability (archive vs recent overlap)
- Engagement correlation (which atoms correlate with highest engagement)
"""

import json
import os
import random
import time
import urllib.request
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
BASEDIR = os.path.dirname(os.path.abspath(__file__))

def load_all_tweets():
    """Load and merge all v5 datasets."""
    all_tweets = []
    seen_ids = set()

    files = [
        "twitter_demand_collection_v5_archive.json",
        "twitter_demand_collection_v5_fix.json",
        "twitter_demand_collection_v5_recent.json",
    ]

    for fname in files:
        fpath = os.path.join(BASEDIR, fname)
        if not os.path.exists(fpath):
            print(f"  Skipping {fname} (not found)")
            continue
        with open(fpath) as f:
            data = json.load(f)
        source = fname.replace("twitter_demand_collection_v5_", "").replace(".json", "")
        for t in data.get("tweets", []):
            if t["id"] not in seen_ids:
                seen_ids.add(t["id"])
                t["source_file"] = source
                all_tweets.append(t)
        print(f"  Loaded {fname}: {len(data.get('tweets', []))} tweets")

    print(f"\n  Total unique tweets: {len(all_tweets)}")
    return all_tweets

def split_train_holdout(tweets, train_ratio=0.7, seed=42):
    """Split into train (70%) and holdout (30%) sets."""
    random.seed(seed)
    shuffled = tweets.copy()
    random.shuffle(shuffled)
    split_idx = int(len(shuffled) * train_ratio)
    return shuffled[:split_idx], shuffled[split_idx:]

def group_by_vertical(tweets):
    """Group tweets by vertical."""
    groups = {}
    for t in tweets:
        v = t.get("vertical", "unknown")
        if v not in groups:
            groups[v] = []
        groups[v].append(t)
    return groups

def group_by_engagement_tier(tweets):
    """Split into high/medium/low engagement tiers."""
    sorted_tw = sorted(tweets, key=lambda t: t.get("engagement_score", 0), reverse=True)
    n = len(sorted_tw)
    return {
        "top_10pct": sorted_tw[:max(1, n // 10)],
        "top_25pct": sorted_tw[:max(1, n // 4)],
        "bottom_50pct": sorted_tw[n // 2:],
    }

def format_tweets_for_prompt(tweets, max_tweets=80):
    """Format tweets into a compact text block for the prompt."""
    # Sort by engagement score, take top N
    sorted_tw = sorted(tweets, key=lambda t: t.get("engagement_score", 0), reverse=True)[:max_tweets]

    lines = []
    for t in sorted_tw:
        likes = t.get("likes", 0)
        replies = t.get("replies", 0)
        bookmarks = t.get("bookmarks", 0)
        wc = t.get("word_count", 0)
        text = t.get("text", "").replace("\n", " | ")
        lines.append(f"[L:{likes} R:{replies} B:{bookmarks} W:{wc}] {text}")

    return "\n".join(lines)

def format_reply_data(tweets, max_tweets=40):
    """Format tweets with their reply data for reply-specific analysis."""
    # Only tweets with reply_data
    with_replies = [t for t in tweets if t.get("reply_data") and len(t["reply_data"]) > 0]
    sorted_tw = sorted(with_replies, key=lambda t: t.get("engagement_score", 0), reverse=True)[:max_tweets]

    blocks = []
    for t in sorted_tw:
        text = t.get("text", "").replace("\n", " | ")
        header = f"[L:{t.get('likes',0)} R:{t.get('replies',0)} B:{t.get('bookmarks',0)}] {text}"

        reply_lines = []
        for r in t["reply_data"][:10]:  # Top 10 replies per tweet
            r_text = r.get("text", "").replace("\n", " | ")
            reply_lines.append(f"  [{r.get('category','?')} L:{r.get('likes',0)}] {r_text}")

        blocks.append(header + "\n" + "\n".join(reply_lines))

    return "\n\n".join(blocks)

def call_claude(prompt, system="", max_tokens=8000):
    """Call Anthropic API."""
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"  API error: {e.code} — {body}")
        return f"ERROR: {e.code}"
    except Exception as e:
        print(f"  Exception: {e}")
        return f"ERROR: {e}"

SYSTEM_PROMPT = """You are a linguistic analyst specializing in social media writing patterns.
You extract the atomic structure of high-engagement writing — the smallest repeatable units
that make content resonate. You work with data, not opinion. Every pattern you identify must
be supported by multiple examples from the provided tweets.

Your analysis framework (based on the Jack Butcher writing profile methodology):

1. STATISTICAL SIGNATURES: Word count distributions, sentence counts, punctuation patterns,
   perspective ratios (you/I/we), engagement correlations with length.

2. STRUCTURAL TEMPLATES: Sentence patterns (single sentence, parallel, conditional, list,
   explicit contrast), opening patterns, closing patterns, how the tweet is architecturally built.

3. RHETORICAL DEVICES: Contrast frames (reframe, paradox, chiasmus, negation flip, etc.),
   word-level mechanics (alliteration, matched meter, internal rhyme, monosyllabic endings),
   colon as pivot, question deployment.

4. VOICE CHARACTERISTICS: Directness level, hedging presence/absence, perspective (who speaks
   to whom), tone (wry/earnest/confrontational/deadpan), register (formal/casual/locker room).

5. ABSENCE PATTERNS: What NEVER appears in high-engagement tweets. These define the voice
   as much as what's present. (Self-reporting emotions? Engagement begging? Clichés? Hedging?
   Diary content? Pop culture? News commentary?)

6. VOCABULARY SIGNATURES: Recurring power words, banned/absent words, domain-specific terms
   that signal insider knowledge.

7. ENGAGEMENT CORRELATIONS: Which specific atoms correlate with the highest engagement scores
   in this dataset? Not just what appears, but what PERFORMS.

Be specific. Use exact quotes from the tweets as evidence. Count frequencies where possible.
Distinguish between atoms that appear in >20% of high-engagement tweets (core) vs <5% (rare but powerful)."""

def analyze_vertical(vertical_name, tweets, tweet_count_label=""):
    """Run atomic analysis on a single vertical's tweets."""
    tweet_text = format_tweets_for_prompt(tweets, max_tweets=100)

    prompt = f"""Analyze these {len(tweets)} high-engagement tweets from the "{vertical_name}" vertical.

Extract the atomic structure using all 7 categories (statistical signatures, structural templates,
rhetorical devices, voice characteristics, absence patterns, vocabulary signatures, engagement correlations).

For each atom you identify:
- Quote 2-3 specific tweet examples
- Note frequency (how many of the provided tweets use this atom)
- Note engagement correlation (do tweets with this atom score higher or lower?)

Format your output as structured data, not prose. Use tables and lists.

TWEETS:
{tweet_text}"""

    print(f"\n  Analyzing {vertical_name} ({len(tweets)} tweets)...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=6000)
    time.sleep(2)  # Rate limit courtesy
    return result

def analyze_replies(tweets):
    """Analyze reply-specific patterns."""
    reply_text = format_reply_data(tweets, max_tweets=50)

    if not reply_text.strip():
        return "No reply data available for analysis."

    prompt = f"""Analyze these tweet-reply pairs. Focus specifically on REPLY patterns — what makes
a reply get engagement (likes) and what makes a reply provoke further responses.

Extract atoms specific to replies:
1. REPLY STRUCTURAL PATTERNS: How are high-engagement replies built differently from original posts?
2. REPLY RHETORICAL DEVICES: What devices work specifically in reply context?
3. REPLY VOICE: How does the voice shift when replying vs posting originally?
4. REPLY ENGAGEMENT HOOKS: What in a reply provokes the original author to respond back? (This is the 75x algorithm signal)
5. REPLY ABSENCE PATTERNS: What do high-engagement replies never do?

For each pattern, quote specific replies as evidence.

TWEET-REPLY PAIRS:
{reply_text}"""

    print(f"\n  Analyzing reply patterns...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=6000)
    time.sleep(2)
    return result

def analyze_cross_vertical(vertical_analyses):
    """Cross-reference atoms across verticals to find universals vs specifics."""
    # Combine all analyses into one prompt
    combined = ""
    for v, analysis in vertical_analyses.items():
        combined += f"\n\n=== {v.upper()} VERTICAL ===\n{analysis[:3000]}"  # Truncate each to fit context

    prompt = f"""You have atomic analyses from 7 different content verticals. Your job is to identify:

1. UNIVERSAL ATOMS: Patterns that appear in 4+ verticals. These are first principles of high-engagement writing.
2. VERTICAL-SPECIFIC ATOMS: Patterns unique to 1-2 verticals. These are domain adaptations.
3. CONTRADICTIONS: Where one vertical's high-performing atom directly contradicts another's.
4. ENGAGEMENT HIERARCHY: Rank the universal atoms by how consistently they correlate with engagement across verticals.

For each universal atom, state which verticals it appears in and quote one example from each.
For each vertical-specific atom, explain WHY it works in that vertical but not others.

VERTICAL ANALYSES:
{combined}"""

    print(f"\n  Cross-referencing across verticals...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=8000)
    time.sleep(2)
    return result

def analyze_temporal(archive_tweets, recent_tweets):
    """Compare archive vs recent patterns to find durable first principles."""
    archive_text = format_tweets_for_prompt(archive_tweets, max_tweets=60)
    recent_text = format_tweets_for_prompt(recent_tweets, max_tweets=60)

    prompt = f"""Compare these two sets of high-engagement tweets:

SET A — ARCHIVE (collected from full history, represents durable patterns):
{archive_text}

SET B — RECENT (last 7 days, represents current patterns):
{recent_text}

Identify:
1. DURABLE ATOMS: Patterns present in BOTH archive and recent. These are timeless first principles.
2. EMERGING ATOMS: Patterns in recent but NOT archive. These are trends or format evolution.
3. FADING ATOMS: Patterns in archive but NOT recent. These may be outdated or platform-shifted.
4. STABLE ENGAGEMENT PATTERNS: Which structural/rhetorical patterns consistently drive engagement across both time periods?

Be specific with examples from both sets."""

    print(f"\n  Analyzing temporal patterns...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=6000)
    time.sleep(2)
    return result

def validate_against_holdout(atoms_summary, holdout_tweets):
    """Validate discovered atoms against the holdout set."""
    holdout_text = format_tweets_for_prompt(holdout_tweets, max_tweets=80)

    prompt = f"""You have a set of "atoms" (writing patterns) extracted from a training set.
Now validate them against this HOLDOUT set of tweets that were NOT used in the analysis.

ATOMS TO VALIDATE:
{atoms_summary[:4000]}

HOLDOUT TWEETS:
{holdout_text}

For each major atom, report:
1. PRESENT: Found in holdout set? (Y/N, with count and examples)
2. ENGAGEMENT CORRELATION: Do holdout tweets using this atom score higher than those without?
3. FALSE POSITIVE: Any atoms that appeared strong in training but are absent/weak in holdout?
4. MISSED ATOMS: Any patterns in the holdout set that the training analysis didn't catch?

This is a validation exercise. Be honest about what doesn't hold up."""

    print(f"\n  Validating against holdout set...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=6000)
    time.sleep(2)
    return result

def synthesize_profile(all_analyses):
    """Final synthesis into gethealthc.md format."""
    combined = "\n\n".join(f"=== {k} ===\n{v[:2500]}" for k, v in all_analyses.items())

    prompt = f"""Synthesize all the following analyses into a single, definitive writing profile document.

Model it after the Jack Butcher writing profile format:
- Voice section (directness, perspective, punctuation)
- Statistical patterns (word counts, engagement sweet spots)
- Structural templates (with frequency percentages)
- Rhetorical devices (each with examples and frequency)
- Word-level mechanics (specific micro-devices)
- Absence patterns (what never appears)
- Vocabulary signatures
- Engagement correlations
- Reply-specific atoms (separate section)

CRITICAL: Separate into three tiers:
1. UNIVERSAL ATOMS — work across all verticals, validated against holdout, durable across time
2. HEALTH-SPECIFIC ATOMS — work specifically for health/fitness/wellness content
3. REPLY-SPECIFIC ATOMS — work specifically in reply context

For each atom, include:
- The pattern name
- What it does
- 2-3 example tweets demonstrating it
- Frequency in dataset
- Engagement correlation (higher/lower/neutral)
- What would disprove it (falsifiability)

The output should be a complete, actionable writing profile that someone could use to write
high-engagement tweets without any other guidance.

ANALYSES:
{combined}"""

    print(f"\n  Synthesizing final profile...")
    result = call_claude(prompt, system=SYSTEM_PROMPT, max_tokens=8000)
    time.sleep(2)
    return result


def main():
    print("=" * 60)
    print("  ATOMIC DECOMPOSITION ENGINE v1")
    print("=" * 60)

    # Step 1: Load all data
    print("\n[1/8] Loading all tweet data...")
    all_tweets = load_all_tweets()

    # Step 2: Split train/holdout
    print("\n[2/8] Splitting train/holdout (70/30)...")
    train, holdout = split_train_holdout(all_tweets)
    print(f"  Train: {len(train)} tweets")
    print(f"  Holdout: {len(holdout)} tweets")

    # Step 3: Group by vertical
    print("\n[3/8] Grouping by vertical...")
    vertical_groups = group_by_vertical(train)
    for v, tweets in sorted(vertical_groups.items()):
        print(f"  {v}: {len(tweets)} tweets")

    # Step 4: Analyze each vertical
    print("\n[4/8] Analyzing each vertical...")
    vertical_analyses = {}
    for v in sorted(vertical_groups.keys()):
        tweets = vertical_groups[v]
        if len(tweets) < 10:
            print(f"  Skipping {v} (only {len(tweets)} tweets)")
            continue
        analysis = analyze_vertical(v, tweets)
        vertical_analyses[v] = analysis

        # Save intermediate
        with open(os.path.join(BASEDIR, f"atoms_{v}.md"), 'w') as f:
            f.write(f"# Atomic Analysis: {v}\n\n{analysis}")
        print(f"  Saved atoms_{v}.md")

    # Step 5: Analyze reply patterns
    print("\n[5/8] Analyzing reply patterns...")
    tweets_with_replies = [t for t in train if t.get("reply_data") and len(t["reply_data"]) > 0]
    print(f"  Tweets with reply data: {len(tweets_with_replies)}")
    reply_analysis = analyze_replies(tweets_with_replies)
    vertical_analyses["_reply_patterns"] = reply_analysis
    with open(os.path.join(BASEDIR, "atoms_reply_patterns.md"), 'w') as f:
        f.write(f"# Reply Pattern Atoms\n\n{reply_analysis}")

    # Step 6: Cross-vertical analysis
    print("\n[6/8] Cross-referencing across verticals...")
    cross_analysis = analyze_cross_vertical(vertical_analyses)
    vertical_analyses["_cross_vertical"] = cross_analysis
    with open(os.path.join(BASEDIR, "atoms_cross_vertical.md"), 'w') as f:
        f.write(f"# Cross-Vertical Atom Analysis\n\n{cross_analysis}")

    # Step 7: Temporal analysis
    print("\n[7/8] Analyzing temporal patterns...")
    archive_tweets = [t for t in train if t.get("source_file") in ("archive", "archive_fix")]
    recent_tweets = [t for t in train if t.get("source_file") == "recent"]
    if recent_tweets:
        temporal_analysis = analyze_temporal(archive_tweets, recent_tweets)
        vertical_analyses["_temporal"] = temporal_analysis
        with open(os.path.join(BASEDIR, "atoms_temporal.md"), 'w') as f:
            f.write(f"# Temporal Atom Analysis\n\n{temporal_analysis}")
    else:
        print("  No recent tweets — skipping temporal analysis")

    # Step 8: Validate and synthesize
    print("\n[8/8] Validating and synthesizing...")

    # First validate
    # Use cross-vertical analysis as the atoms summary for validation
    validation = validate_against_holdout(cross_analysis, holdout)
    vertical_analyses["_validation"] = validation
    with open(os.path.join(BASEDIR, "atoms_validation.md"), 'w') as f:
        f.write(f"# Holdout Validation\n\n{validation}")

    # Final synthesis
    profile = synthesize_profile(vertical_analyses)
    with open(os.path.join(BASEDIR, "gethealthc.md"), 'w') as f:
        f.write(profile)
    print(f"\n  Saved gethealthc.md")

    # Summary
    print(f"\n{'='*60}")
    print(f"  DECOMPOSITION COMPLETE")
    print(f"{'='*60}")
    print(f"  Total tweets analyzed: {len(train)}")
    print(f"  Holdout validation set: {len(holdout)}")
    print(f"  Verticals analyzed: {len([v for v in vertical_analyses if not v.startswith('_')])}")
    print(f"  Output files:")
    for v in sorted(vertical_analyses.keys()):
        name = v.replace("_", "") if v.startswith("_") else v
        print(f"    atoms_{name}.md")
    print(f"    gethealthc.md (final profile)")

if __name__ == "__main__":
    main()
