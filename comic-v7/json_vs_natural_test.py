"""
A/B test: JSON-structured prompt vs natural language prompt.
Same subject, same model (Veo 3.1 fast via Runway), same duration.
Subject: A single cargo ship passing through a narrow strait at sunset.
"""
import os, time, json, requests

os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

from runwayml import RunwayML

RUNWAY_KEY = os.environ.get("RUNWAY_API_KEY")
OUT = "/root/comic-v7"
client = RunwayML(api_key=RUNWAY_KEY)

# ─────────────────────────────────────
# PROMPT A: Natural language (prose)
# ─────────────────────────────────────
NATURAL = """A cinematic aerial shot of a single large cargo ship passing through a narrow ocean strait at golden hour. The camera starts behind the ship at a low angle, showing its massive wake cutting through dark teal water. Mountains rise on both sides of the strait. Warm golden sunlight catches the ship's hull. The camera slowly rises and pushes forward, revealing the full length of the narrow passage ahead. Atmospheric haze in the distance. Film grain. Anamorphic lens flare from the setting sun."""

# ─────────────────────────────────────
# PROMPT B: JSON-structured
# ─────────────────────────────────────
JSON_PROMPT = json.dumps({
    "shot": {
        "lens": "50mm anamorphic",
        "start": "Low angle behind a large cargo ship. Dark teal water, mountains both sides of narrow strait.",
        "camera": "Slow rise and push forward. Lifts from low behind ship to high wide angle revealing the strait ahead. Smooth, cinematic."
    },
    "subject": {
        "ship": "Single large cargo ship, massive wake, dark hull with rust, containers on deck.",
        "environment": "Narrow strait, mountainous coastlines, deep teal water, atmospheric haze."
    },
    "cinematography": {
        "lighting": "Golden hour, warm sunlight low angle from left, anamorphic lens flare from setting sun.",
        "look": "Film grain, anamorphic bokeh, dark teal water, warm golden highlights, blue-grey mountains."
    }
})

print(f"Natural prompt: {len(NATURAL)} chars")
print(f"JSON prompt: {len(JSON_PROMPT)} chars")

assert len(NATURAL) <= 1000, f"Natural too long: {len(NATURAL)}"
assert len(JSON_PROMPT) <= 1000, f"JSON too long: {len(JSON_PROMPT)}"


def generate(prompt, label):
    print(f"\n{'='*50}")
    print(f"Generating: {label}")
    print(f"{'='*50}")
    try:
        task = client.text_to_video.create(
            model="veo3.1_fast",
            prompt_text=prompt,
            duration=8,
            ratio="1920:1080",
        )
        task_id = task.id
        print(f"Task: {task_id}")

        for attempt in range(120):
            time.sleep(5)
            result = client.tasks.retrieve(task_id)
            status = result.status
            if attempt % 4 == 0:
                print(f"  Poll {attempt+1}: {status}")
            if status == "SUCCEEDED":
                url = result.output[0] if result.output else None
                if url:
                    r = requests.get(url, timeout=120)
                    path = os.path.join(OUT, f"ab_test_{label}.mp4")
                    with open(path, "wb") as f:
                        f.write(r.content)
                    print(f"  Saved: {path} ({len(r.content)//1024}KB)")
                    return path
                return None
            elif status == "FAILED":
                print(f"  FAILED: {result.failure}")
                return None
        print("  Timeout")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


if __name__ == "__main__":
    r1 = generate(NATURAL, "natural")
    r2 = generate(JSON_PROMPT, "json")

    print(f"\n{'='*50}")
    print("RESULTS")
    print(f"{'='*50}")
    print(f"  Natural: {r1}")
    print(f"  JSON:    {r2}")
