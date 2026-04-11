#!/usr/bin/env python3
"""v36 — Post-dialogue prompt on Kling v3 (Kling 3.0), best-effort config.

Single render (not A/B — the post-dialogue prompt already won on Veo 3.1 Fast
in v35). Goal: close the 3-way tool comparison.
  - v34: kling-v1-6 std → still + camera pan (fail)
  - v35-b: veo-3.1-fast 8s → real character animation (win)
  - v36 (this): kling-v3 pro 10s → ???

Config strategy: try Kling's BEST text-to-video config first (pro mode,
10s duration, cfg_scale 0.7). Fall back on API rejection.
Prompt: IDENTICAL to v35-b post-dialogue (the winner).
"""

import os, json, time, requests, jwt
from datetime import datetime

ACCESS_KEY = os.environ.get("KLING_ACCESS_KEY")
SECRET_KEY = os.environ.get("KLING_SECRET_KEY")
if not ACCESS_KEY or not SECRET_KEY:
    raise SystemExit("KLING_ACCESS_KEY and KLING_SECRET_KEY env vars required")

BASE_URL = "https://api.klingai.com"
OUT_DIR = "/root/blind-ab"
MODEL = "kling-v3"

# Prompt: IDENTICAL to v34/v35 post-dialogue (the winner)
PROMPT_POST_DIALOGUE = (
    "Pulse — round fluffy yellow body, no external ears, big brown eyes, small "
    "halo floating above head, small feathered wings, small paw-hands. Standing "
    "on wooden floorboards beside a window at sunset, holding a small crumpled "
    "paper drawing in both paws. Holding completely still, staring at the "
    "drawing. Then: eyes widen slowly, mouth parts just slightly, a small smile "
    "begins. Warm golden window light across the fur. Hand-drawn anime, soft "
    "line-weight, gentle atmospheric haze. Body remains still — motion confined "
    "to the face."
)

SHARED_NEGATIVE = (
    "live-action, photorealistic, text, watermarks, logos, deformed, "
    "extra limbs, blurry, jittery, camera shake, camera zoom, camera pan, "
    "static image, still image, slideshow"
)

# Config fallback ladder — try best first, fall back on rejection
CONFIG_LADDER = [
    {"mode": "pro", "duration": "10", "cfg_scale": 0.7, "label": "pro-10s-cfg07"},
    {"mode": "pro", "duration": "5",  "cfg_scale": 0.7, "label": "pro-5s-cfg07"},
    {"mode": "std", "duration": "10", "cfg_scale": 0.7, "label": "std-10s-cfg07"},
    {"mode": "std", "duration": "5",  "cfg_scale": 0.7, "label": "std-5s-cfg07"},
    {"mode": "std", "duration": "5",  "cfg_scale": 0.5, "label": "std-5s-cfg05"},
]


def get_token():
    now = int(datetime.now().timestamp())
    payload = {"iss": ACCESS_KEY, "exp": now + 1800, "nbf": now - 5, "iat": now}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256",
                      headers={"typ": "JWT", "alg": "HS256"})


def submit(config):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "model_name": MODEL,
        "prompt": PROMPT_POST_DIALOGUE,
        "negative_prompt": SHARED_NEGATIVE,
        "cfg_scale": config["cfg_scale"],
        "mode": config["mode"],
        "aspect_ratio": "16:9",
        "duration": config["duration"],
    }
    print(f"[v36] trying {config['label']}: mode={config['mode']} dur={config['duration']} cfg={config['cfg_scale']}")
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code != 200:
        print(f"[v36] HTTP {r.status_code}: {r.text[:300]}")
        return None, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    if data.get("code") != 0:
        err = data.get("message", "unknown")
        print(f"[v36] API rejected: {err}")
        return None, f"API: {err}"
    task_id = data.get("data", {}).get("task_id")
    print(f"[v36] submitted: task_id={task_id}")
    return task_id, None


def check_download(task_id, label):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        return None
    data = r.json()
    if data.get("code") != 0:
        return None
    task_data = data.get("data", {})
    status = task_data.get("task_status")
    if status == "succeed":
        videos = task_data.get("task_result", {}).get("videos", [])
        if not videos:
            return False
        video_url = videos[0].get("url", "")
        if not video_url:
            return False
        v = requests.get(video_url, timeout=120)
        if v.status_code != 200:
            return False
        out_path = os.path.join(OUT_DIR, f"v36-kling-v3.mp4")
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[v36] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
        return True
    elif status == "failed":
        print(f"[v36] FAILED: {task_data.get('task_status_msg', 'unknown')}")
        return False
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Walk the fallback ladder
    task_id = None
    used_config = None
    attempts = []
    for config in CONFIG_LADDER:
        tid, err = submit(config)
        attempts.append({"config": config, "error": err, "task_id": tid})
        if tid:
            task_id = tid
            used_config = config
            break

    if not task_id:
        print("\n=== ALL CONFIGS REJECTED ===")
        for a in attempts:
            print(f"  {a['config']['label']}: {a['error']}")
        raise SystemExit("No config accepted by Kling v3 text2video")

    print(f"\n=== Polling (config: {used_config['label']}) ===")
    start = time.time()
    result = None
    while time.time() - start < 900:
        r = check_download(task_id, used_config["label"])
        if r is True:
            result = "OK"
            break
        elif r is False:
            result = "FAIL"
            break
        elapsed = int(time.time() - start)
        print(f"  pending ({elapsed}s)...")
        time.sleep(15)
    if result is None:
        result = "TIMEOUT"

    print(f"\n=== RESULT: {result} ===")

    # Write labels file
    labels_path = os.path.join(OUT_DIR, "v36-labels.md")
    with open(labels_path, "w") as f:
        f.write("# v36 — Post-dialogue prompt on Kling v3 (single render)\n\n")
        f.write(f"Session 36. Date: {datetime.now().isoformat()}\n\n")
        f.write(f"**Model:** {MODEL}\n")
        f.write(f"**Config used:** {used_config['label']} (mode={used_config['mode']}, duration={used_config['duration']}s, cfg_scale={used_config['cfg_scale']})\n")
        f.write(f"**Aspect:** 16:9\n")
        f.write(f"**Task ID:** {task_id}\n")
        f.write(f"**Render status:** {result}\n\n")
        f.write(f"**Prompt (identical to v35-b post-dialogue winner):**\n> {PROMPT_POST_DIALOGUE}\n\n")
        f.write(f"**Negative prompt:**\n> {SHARED_NEGATIVE}\n\n")
        f.write("## Config ladder attempts\n\n")
        for a in attempts:
            status = "OK" if a["task_id"] else f"REJECTED ({a['error']})"
            f.write(f"- {a['config']['label']}: {status}\n")
    print(f"\nLabels: {labels_path}")


if __name__ == "__main__":
    main()
