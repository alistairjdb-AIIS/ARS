"""
Loop Frame — Twitter/X posting pipeline.

Autonomous creative posting for @loopframe.
Posts text, images, video, polls. Reads engagement metrics.
All secrets from environment variables.
"""

import os
import sys
import json
import time
import tweepy
from pathlib import Path
from datetime import datetime, timezone


# --- Auth ---

def get_client():
    """Authenticated Tweepy v2 Client for tweet creation + reading."""
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
    )


def get_api():
    """Authenticated Tweepy v1.1 API for media upload + profile ops."""
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_SECRET"],
    )
    return tweepy.API(auth)


# --- Posting ---

def post_text(text, reply_to=None):
    """Post a text tweet. Returns tweet ID."""
    client = get_client()
    params = {"text": text}
    if reply_to:
        params["in_reply_to_tweet_id"] = reply_to
    resp = client.create_tweet(**params)
    tweet_id = resp.data["id"]
    print(f"Posted text tweet: {tweet_id}")
    return tweet_id


def post_image(text, image_path):
    """Post a tweet with an image. Returns tweet ID."""
    api = get_api()
    client = get_client()
    media = api.media_upload(filename=image_path)
    print(f"Uploaded image: media_id={media.media_id}")
    resp = client.create_tweet(text=text, media_ids=[media.media_id])
    tweet_id = resp.data["id"]
    print(f"Posted image tweet: {tweet_id}")
    return tweet_id


def post_images(text, image_paths):
    """Post a tweet with up to 4 images. Returns tweet ID."""
    if len(image_paths) > 4:
        raise ValueError("Twitter allows max 4 images per tweet")
    api = get_api()
    client = get_client()
    media_ids = []
    for path in image_paths:
        media = api.media_upload(filename=path)
        media_ids.append(media.media_id)
        print(f"Uploaded image: {path} → media_id={media.media_id}")
    resp = client.create_tweet(text=text, media_ids=media_ids)
    tweet_id = resp.data["id"]
    print(f"Posted multi-image tweet: {tweet_id}")
    return tweet_id


def post_video(text, video_path):
    """Post a tweet with a video (MP4, H.264+AAC, up to 140s). Returns tweet ID."""
    api = get_api()
    client = get_client()
    media = api.chunked_upload(
        filename=video_path,
        media_category="tweet_video",
    )
    # Wait for processing
    print(f"Uploaded video: media_id={media.media_id}, waiting for processing...")
    _wait_for_media_processing(api, media.media_id)
    resp = client.create_tweet(text=text, media_ids=[media.media_id])
    tweet_id = resp.data["id"]
    print(f"Posted video tweet: {tweet_id}")
    return tweet_id


def post_poll(text, options, duration_minutes=1440):
    """Post a poll tweet. Options: 2-4 choices. Duration: minutes (default 24h, max 7 days). Returns tweet ID."""
    if not 2 <= len(options) <= 4:
        raise ValueError("Polls need 2-4 options")
    if duration_minutes > 10080:
        raise ValueError("Max poll duration is 7 days (10080 minutes)")
    client = get_client()
    resp = client.create_tweet(
        text=text,
        poll_options=options,
        poll_duration_minutes=duration_minutes,
    )
    tweet_id = resp.data["id"]
    print(f"Posted poll tweet: {tweet_id}")
    return tweet_id


def post_thread(tweets):
    """Post a thread (list of dicts with 'text' and optional 'image'/'video'). Returns list of tweet IDs."""
    ids = []
    reply_to = None
    for i, tweet in enumerate(tweets):
        text = tweet["text"]
        if "image" in tweet:
            tid = post_image(text, tweet["image"])
        elif "video" in tweet:
            tid = post_video(text, tweet["video"])
        elif i == 0:
            tid = post_text(text)
        else:
            tid = post_text(text, reply_to=reply_to)
        ids.append(tid)
        reply_to = tid
        if i < len(tweets) - 1:
            time.sleep(1)
    print(f"Posted thread: {len(ids)} tweets")
    return ids


def _wait_for_media_processing(api, media_id, max_wait=120):
    """Wait for video processing to complete."""
    elapsed = 0
    while elapsed < max_wait:
        status = api.get_media_upload_status(media_id)
        state = status.processing_info.get("state", "succeeded")
        if state == "succeeded":
            print(f"Video processing complete ({elapsed}s)")
            return
        if state == "failed":
            raise RuntimeError(f"Video processing failed: {status.processing_info}")
        wait = status.processing_info.get("check_after_secs", 5)
        time.sleep(wait)
        elapsed += wait
    raise TimeoutError(f"Video processing timed out after {max_wait}s")


# --- Engagement Reading ---

def get_tweet_metrics(tweet_id):
    """Get public metrics for a tweet."""
    client = get_client()
    resp = client.get_tweet(
        tweet_id,
        tweet_fields=["public_metrics", "organic_metrics", "created_at"],
    )
    if resp and resp.data:
        return {
            "id": str(resp.data.id),
            "text": resp.data.text[:100],
            "created_at": str(resp.data.created_at),
            "metrics": resp.data.public_metrics,
        }
    return None


def get_all_metrics():
    """Get metrics for all our recent tweets."""
    client = get_client()
    me = client.get_me()
    tweets = client.get_users_tweets(
        id=me.data.id,
        max_results=100,
        tweet_fields=["public_metrics", "created_at"],
    )
    results = []
    if tweets and tweets.data:
        for t in tweets.data:
            results.append({
                "id": str(t.id),
                "text": t.text[:100],
                "created_at": str(t.created_at),
                "metrics": t.public_metrics,
            })
    return results


def get_engagement_summary():
    """Summarize engagement across all recent tweets."""
    metrics = get_all_metrics()
    if not metrics:
        return {"total_tweets": 0}

    total = {
        "total_tweets": len(metrics),
        "total_impressions": sum(m["metrics"].get("impression_count", 0) for m in metrics),
        "total_likes": sum(m["metrics"].get("like_count", 0) for m in metrics),
        "total_replies": sum(m["metrics"].get("reply_count", 0) for m in metrics),
        "total_retweets": sum(m["metrics"].get("retweet_count", 0) for m in metrics),
        "total_bookmarks": sum(m["metrics"].get("bookmark_count", 0) for m in metrics),
        "avg_impressions": 0,
        "avg_engagement_rate": 0,
        "tweets": metrics,
    }
    if total["total_tweets"] > 0:
        total["avg_impressions"] = total["total_impressions"] / total["total_tweets"]
        if total["total_impressions"] > 0:
            engagement = total["total_likes"] + total["total_replies"] + total["total_retweets"] + total["total_bookmarks"]
            total["avg_engagement_rate"] = engagement / total["total_impressions"]
    return total


# --- Profile ---

def update_profile(name=None, bio=None):
    """Update display name and/or bio."""
    api = get_api()
    kwargs = {}
    if name:
        kwargs["name"] = name
    if bio:
        kwargs["description"] = bio
    if kwargs:
        result = api.update_profile(**kwargs)
        print(f"Profile updated: name={result.name}, bio={result.description[:50]}...")
        return True
    return False


def update_profile_image(image_path):
    """Update profile picture."""
    api = get_api()
    api.update_profile_image(filename=image_path)
    print(f"Profile image updated from {image_path}")


def update_banner(image_path):
    """Update profile banner."""
    api = get_api()
    api.update_profile_banner(filename=image_path)
    print(f"Banner updated from {image_path}")


# --- Logging ---

LOG_DIR = Path(__file__).parent / "logs"


def log_post(tweet_id, post_type, text, media_path=None):
    """Log a post to the local log file."""
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tweet_id": str(tweet_id),
        "type": post_type,
        "text": text,
        "media": media_path,
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Logged to {log_file}")


# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python loopframe.py <command> [args]")
        print()
        print("Commands:")
        print("  text <message>           Post a text tweet")
        print("  image <message> <path>   Post with image")
        print("  video <message> <path>   Post with video")
        print("  poll <question> <opt1> <opt2> [opt3] [opt4]  Post a poll")
        print("  metrics                  Show engagement for all tweets")
        print("  metrics <tweet_id>       Show engagement for one tweet")
        print("  summary                  Engagement summary")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "text" and len(sys.argv) >= 3:
        text = " ".join(sys.argv[2:])
        tid = post_text(text)
        log_post(tid, "text", text)

    elif cmd == "image" and len(sys.argv) >= 4:
        text = sys.argv[2]
        path = sys.argv[3]
        tid = post_image(text, path)
        log_post(tid, "image", text, path)

    elif cmd == "video" and len(sys.argv) >= 4:
        text = sys.argv[2]
        path = sys.argv[3]
        tid = post_video(text, path)
        log_post(tid, "video", text, path)

    elif cmd == "poll" and len(sys.argv) >= 5:
        question = sys.argv[2]
        options = sys.argv[3:7]
        tid = post_poll(question, options)
        log_post(tid, "poll", question)

    elif cmd == "metrics":
        if len(sys.argv) >= 3:
            m = get_tweet_metrics(sys.argv[2])
            print(json.dumps(m, indent=2))
        else:
            metrics = get_all_metrics()
            for m in metrics:
                print(json.dumps(m, indent=2))

    elif cmd == "summary":
        s = get_engagement_summary()
        print(json.dumps(s, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
