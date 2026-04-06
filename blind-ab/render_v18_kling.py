#!/usr/bin/env python3
"""Blind A/B v18 — photoreal elderly man via Kling AI, research-informed crafted vs terse."""

import requests, json, time, os, jwt
from datetime import datetime

# Kling API auth
ACCESS_KEY = os.environ.get("KLING_ACCESS_KEY")
SECRET_KEY = os.environ.get("KLING_SECRET_KEY")
if not ACCESS_KEY or not SECRET_KEY:
    raise SystemExit("KLING_ACCESS_KEY and KLING_SECRET_KEY env vars required")

BASE_URL = "https://api.klingai.com"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "anime, cartoon, 3D render, Pixar, illustration, text, watermarks, logos, "
    "perfect skin, airbrushed, overly smooth, plastic, deformed hands, extra fingers"
)

# A=terse, B=research-informed crafted
PROMPTS = {
    "v18-output-a-raw": (
        "8-second cinematic scene. An elderly man with grey hair and a weathered "
        "brown jacket sits on a park bench. He opens a letter, reads it, and his "
        "expression slowly changes from neutral to a gentle smile. Autumn park, "
        "soft afternoon light. Shot on 35mm film. No dialogue."
    ),
    "v18-output-b-raw": (
        "Shot on 85mm lens, f/2.0, shallow depth of field, subtle handheld "
        "micro-shake. A man in his late seventies with thinning grey hair, deep "
        "laugh lines, age spots on his temples, and a slightly crooked nose sits "
        "on a weathered park bench. He wears a faded brown corduroy jacket with "
        "patched elbows. His weathered hands carefully unfold a letter — he squints "
        "at the handwriting, lips moving faintly. His brow furrows, then slowly "
        "softens. The corners of his mouth lift into an involuntary smile. His eyes "
        "glisten. Soft overcast afternoon light, autumn trees in background. Kodak "
        "Portra 400 film grain, natural skin texture with visible pores. No dialogue."
    ),
}


def get_token():
    now = int(datetime.now().timestamp())
    payload = {
        "iss": ACCESS_KEY,
        "exp": now + 1800,
        "nbf": now - 5,
        "iat": now,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256",
                      headers={"typ": "JWT", "alg": "HS256"})


def submit(key, prompt):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model_name": "kling-v2-master",
        "prompt": prompt,
        "negative_prompt": SHARED_NEGATIVE,
        "cfg_scale": 0.5,
        "mode": "std",
        "aspect_ratio": "16:9",
        "duration": "5",
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code != 200:
        print(f"[{key}] SUBMIT ERROR {r.status_code}: {r.text[:300]}")
        return None
    data = r.json()
    if data.get("code") != 0:
        print(f"[{key}] API ERROR: {data.get('message', 'unknown')}")
        return None
    task_id = data.get("data", {}).get("task_id")
    print(f"[{key}] submitted: task_id={task_id}")
    return task_id


def check_download(key, task_id):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        return None
    data = r.json()
    if data.get("code") != 0:
        print(f"[{key}] poll error: {data.get('message')}")
        return None
    task_data = data.get("data", {})
    status = task_data.get("task_status")
    if status == "succeed":
        videos = task_data.get("task_result", {}).get("videos", [])
        if not videos:
            print(f"[{key}] no videos in result")
            return False
        video_url = videos[0].get("url", "")
        if not video_url:
            return False
        v = requests.get(video_url, timeout=120)
        if v.status_code != 200:
            print(f"[{key}] download failed: {v.status_code}")
            return False
        out_path = os.path.join(OUT_DIR, f"{key}.mp4")
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[{key}] saved ({len(v.content)/1e6:.1f} MB)")
        return True
    elif status == "failed":
        print(f"[{key}] FAILED: {task_data.get('task_status_msg', 'unknown')}")
        return False
    return None  # still processing


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    ops = {}
    for key, prompt in PROMPTS.items():
        task_id = submit(key, prompt)
        if task_id:
            ops[key] = task_id

    if not ops:
        raise SystemExit("No operations submitted successfully")

    print(f"\n=== Polling {len(ops)} operations ===")
    results = {}
    pending = dict(ops)
    start = time.time()
    while pending and time.time() - start < 600:
        for k in list(pending):
            r = check_download(k, pending[k])
            if r is True:
                results[k] = "OK"
                del pending[k]
            elif r is False:
                results[k] = "FAIL"
                del pending[k]
        if pending:
            elapsed = int(time.time() - start)
            print(f"  {len(pending)} pending ({elapsed}s)...")
            time.sleep(15)

    for k in pending:
        results[k] = "TIMEOUT"

    print("\n=== RESULTS ===")
    for k in PROMPTS:
        print(f"  {k}: {results.get(k, '?')}")
