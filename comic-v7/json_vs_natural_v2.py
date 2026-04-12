"""
Controlled A/B: JSON vs natural language. SAME creative intent, ONLY format differs.

Creative brief (held constant):
- Subject: cargo ship in narrow strait, golden hour
- Camera: 50mm anamorphic, low behind ship, slow rise forward
- Lighting: golden hour, sun low left, anamorphic lens flare
- Look: film grain, anamorphic bokeh, teal water, golden highlights
- Environment: mountains both sides, atmospheric haze
"""
import os, time, json, requests

os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

from runwayml import RunwayML

RUNWAY_KEY = os.environ.get("RUNWAY_API_KEY")
OUT = "/root/comic-v7"
client = RunwayML(api_key=RUNWAY_KEY)

# ─────────────────────────────────────
# PROMPT A: Natural language — SAME content as JSON
# ─────────────────────────────────────
NATURAL = """50mm anamorphic lens. Camera starts low behind a large cargo ship with containers and a dark rusted hull, moving through a narrow strait with mountains on both sides. Deep teal water, massive white wake behind the ship, atmospheric haze in the distance. Camera slowly rises and pushes forward, revealing the full strait passage ahead. Golden hour lighting, warm sunlight from the low left, anamorphic lens flare from the setting sun. Film grain, anamorphic bokeh, dark teal water, warm golden highlights, blue-grey mountains."""

# ─────────────────────────────────────
# PROMPT B: JSON — SAME content as natural
# ─────────────────────────────────────
JSON_PROMPT = json.dumps({
    "shot": {
        "lens": "50mm anamorphic",
        "start": "Low behind a large cargo ship. Mountains both sides of narrow strait.",
        "camera": "Slowly rises and pushes forward, revealing full strait passage ahead."
    },
    "subject": {
        "ship": "Large cargo ship, containers on deck, dark rusted hull, massive white wake.",
        "environment": "Narrow strait, mountains both sides, deep teal water, atmospheric haze."
    },
    "cinematography": {
        "lighting": "Golden hour, warm sunlight from low left, anamorphic lens flare from setting sun.",
        "look": "Film grain, anamorphic bokeh, dark teal water, warm golden highlights, blue-grey mountains."
    }
})

print(f"Natural: {len(NATURAL)} chars")
print(f"JSON: {len(JSON_PROMPT)} chars")
assert len(NATURAL) <= 1000
assert len(JSON_PROMPT) <= 1000


def generate(prompt, label):
    print(f"\n{'='*50}\n{label}\n{'='*50}")
    task = client.text_to_video.create(
        model="veo3.1_fast",
        prompt_text=prompt,
        duration=8,
        ratio="1920:1080",
    )
    print(f"Task: {task.id}")
    for attempt in range(120):
        time.sleep(5)
        result = client.tasks.retrieve(task.id)
        if attempt % 4 == 0:
            print(f"  Poll {attempt+1}: {result.status}")
        if result.status == "SUCCEEDED":
            url = result.output[0]
            r = requests.get(url, timeout=120)
            path = os.path.join(OUT, f"ab2_{label}.mp4")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  Saved: {path} ({len(r.content)//1024}KB)")
            return path
        elif result.status == "FAILED":
            print(f"  FAILED: {result.failure}")
            return None
    return None


if __name__ == "__main__":
    r1 = generate(NATURAL, "natural")
    r2 = generate(JSON_PROMPT, "json")
    print(f"\nNatural: {r1}\nJSON: {r2}")
