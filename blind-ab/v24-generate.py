"""
Blind A/B v24 — Runway Gen-4.5 vs Kling AI for photoreal human
Cross-tool comparison with tool-optimized prompts.
"""
import os
import sys
import jwt
import time
import json
import requests
import urllib.request

# ---- Credentials from env ----
RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY")
KLING_ACCESS_KEY = os.environ.get("KLING_ACCESS_KEY")
KLING_SECRET_KEY = os.environ.get("KLING_SECRET_KEY")

if not all([RUNWAY_API_KEY, KLING_ACCESS_KEY, KLING_SECRET_KEY]):
    print("ERROR: Set RUNWAY_API_KEY, KLING_ACCESS_KEY, KLING_SECRET_KEY env vars")
    sys.exit(1)

OUTPUT_DIR = "/root/blind-ab"

# ---- Prompts (tool-optimized, same intent) ----

KLING_PROMPT = """A 75-year-old woman with white hair in a loose bun, reading glasses perched on her nose. Deep laugh lines around her eyes, age spots on her temples, slightly crooked smile. She wears a soft cream cardigan over a faded floral blouse. She sits at a worn wooden kitchen table, reading a handwritten letter held in weathered hands with visible veins.

0-4s: Her eyes move across the page, one finger tracing a line. Her lips press together softly, a quiet breath.

4-8s: She pauses. Looks up toward the window on her left. Morning sunlight catches fine white hairs at her temple. A faint asymmetric smile forms — slow, private, remembering something. Her eyes glisten slightly.

Soft window light from camera-left, gentle shadow falloff. Warm but restrained color grading. Visible pores on forehead. Fine facial hair catching the light. Shot on 35mm film, subtle grain."""

RUNWAY_PROMPT = """An elderly woman with white hair pulled into a loose bun, reading glasses balanced on her nose. Deep laugh lines, age spots at her temples, a slightly crooked smile. Cream cardigan over faded floral blouse. She sits at a scarred wooden kitchen table holding a handwritten letter in weathered hands.

Her eyes track slowly across the page. One finger drags along a line of ink. She draws a quiet breath, lips pressing together.

Then she stops. Her gaze lifts toward the window. Morning light catches the fine white hairs at her temple. Something lands — a memory settling behind her eyes. A slow, lopsided smile pulls at one corner of her mouth.

Soft window light from the left. Warm but muted tones. Visible pores, fine peach fuzz on her cheeks, faint under-eye circles. 35mm film texture, subtle grain."""


# ---- Kling API ----

def get_kling_token():
    now = int(time.time())
    payload = {
        "iss": KLING_ACCESS_KEY,
        "exp": now + 1800,
        "nbf": now - 5
    }
    return jwt.encode(payload, KLING_SECRET_KEY, algorithm="HS256")


def generate_kling():
    print("[Kling] Starting generation...")
    token = get_kling_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_name": "kling-v1-6",
        "prompt": KLING_PROMPT,
        "duration": "10",
        "aspect_ratio": "16:9",
        "mode": "std"
    }

    resp = requests.post(
        "https://api.klingai.com/v1/videos/text2video",
        headers=headers,
        json=payload
    )
    print(f"[Kling] Submit response: {resp.status_code}")
    data = resp.json()
    print(f"[Kling] Response: {json.dumps(data, indent=2)}")

    if resp.status_code != 200 or "data" not in data:
        print(f"[Kling] ERROR: {data}")
        return None

    task_id = data["data"]["task_id"]
    print(f"[Kling] Task ID: {task_id}")

    # Poll for completion
    for i in range(120):  # 10 min max
        time.sleep(5)
        token = get_kling_token()  # refresh token
        headers["Authorization"] = f"Bearer {token}"
        status_resp = requests.get(
            f"https://api.klingai.com/v1/videos/text2video/{task_id}",
            headers=headers
        )
        status_data = status_resp.json()
        task_status = status_data.get("data", {}).get("task_status", "unknown")

        if i % 6 == 0:  # Log every 30s
            print(f"[Kling] Poll {i}: status={task_status}")

        if task_status == "succeed":
            videos = status_data["data"].get("task_result", {}).get("videos", [])
            if videos:
                url = videos[0].get("url")
                print(f"[Kling] Done! URL: {url[:80]}...")
                return url
            print(f"[Kling] Succeeded but no video URL in response")
            print(f"[Kling] Full response: {json.dumps(status_data, indent=2)}")
            return None
        elif task_status == "failed":
            print(f"[Kling] FAILED: {json.dumps(status_data, indent=2)}")
            return None

    print("[Kling] TIMEOUT after 10 minutes")
    return None


# ---- Runway API ----

def generate_runway():
    print("[Runway] Starting generation...")
    from runwayml import RunwayML

    client = RunwayML(api_key=RUNWAY_API_KEY)

    task = client.text_to_video.create(
        model="gen4.5",
        prompt_text=RUNWAY_PROMPT,
        duration=10,
        ratio="1280:720"
    )
    print(f"[Runway] Task ID: {task.id}")

    # Poll for completion
    for i in range(120):  # 10 min max
        time.sleep(5)
        result = client.tasks.retrieve(task.id)

        if i % 6 == 0:  # Log every 30s
            print(f"[Runway] Poll {i}: status={result.status}")

        if result.status == "SUCCEEDED":
            # Get the output URL
            output = result.output
            if output and len(output) > 0:
                url = output[0]
                print(f"[Runway] Done! URL: {str(url)[:80]}...")
                return str(url)
            print(f"[Runway] Succeeded but no output URL")
            print(f"[Runway] Full result: {result}")
            return None
        elif result.status == "FAILED":
            print(f"[Runway] FAILED: {result.failure}")
            print(f"[Runway] Failure code: {result.failure_code}")
            return None

    print("[Runway] TIMEOUT after 10 minutes")
    return None


def download_video(url, filepath):
    print(f"Downloading to {filepath}...")
    urllib.request.urlretrieve(url, filepath)
    size = os.path.getsize(filepath)
    print(f"Downloaded: {size / 1024:.0f} KB")


if __name__ == "__main__":
    # Generate both
    print("=" * 60)
    print("Blind A/B v24: Runway Gen-4.5 vs Kling AI")
    print("Register: Photoreal human")
    print("=" * 60)

    kling_url = generate_kling()
    runway_url = generate_runway()

    # Download results
    # Mapping: A = Kling, B = Runway
    if kling_url:
        download_video(kling_url, os.path.join(OUTPUT_DIR, "v24-output-a.mp4"))
    else:
        print("WARNING: Kling generation failed")

    if runway_url:
        download_video(runway_url, os.path.join(OUTPUT_DIR, "v24-output-b.mp4"))
    else:
        print("WARNING: Runway generation failed")

    print("\n" + "=" * 60)
    print("Results:")
    print(f"  A (Kling):  {'OK' if kling_url else 'FAILED'}")
    print(f"  B (Runway): {'OK' if runway_url else 'FAILED'}")
    print("=" * 60)
