#!/usr/bin/env python3
"""Blind A/B v19 — photoreal coffee shop woman via Kling AI. /animate vs crafted-only."""

import requests, json, time, os, jwt
from datetime import datetime

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

# A=/animate-designed, B=crafted-without-animate
PROMPTS = {
    "v19-output-a-raw": (
        "A woman in her late twenties with dark curly hair tucked behind one ear, "
        "light freckles, warm brown eyes, sits alone in a window seat of a quiet "
        "coffee shop. She wears an oversized cream knit sweater. Rain traces lines "
        "down the glass beside her. She cradles a ceramic mug in both hands, steam "
        "curling, watching the rain — still, unhurried. Her phone buzzes once on "
        "the wooden table. She glances down. Her hands lower the mug slowly. She "
        "picks up the phone. Her brow draws together — she reads, lips barely "
        "moving. A beat. Then something shifts — her brow releases, her eyes "
        "soften, and the smallest smile pulls at the corner of her mouth before "
        "she can stop it. Soft overcast window light, shallow depth of field, "
        "Kodak Portra 400 grain. No dialogue."
    ),
    "v19-output-b-raw": (
        "A woman in her late twenties with dark curly hair, light freckles across "
        "her nose, and warm brown eyes sits in a window seat of a quiet coffee shop. "
        "She wears an oversized cream knit sweater, hands wrapped around a ceramic "
        "mug. Her phone buzzes on the table. She glances down — her lips part "
        "slightly, eyebrows lift. She sets the mug down slowly, picks up the phone "
        "with both hands, and a slow disbelieving smile spreads across her face. "
        "Soft window light from camera-left, steam rising from the mug, rain-streaked "
        "glass behind her. Kodak Portra 400, natural skin texture. No dialogue."
    ),
}


def get_token():
    now = int(datetime.now().timestamp())
    payload = {"iss": ACCESS_KEY, "exp": now + 1800, "nbf": now - 5, "iat": now}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256",
                      headers={"typ": "JWT", "alg": "HS256"})


def submit(key, prompt):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
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
        out_path = os.path.join(OUT_DIR, f"{key}.mp4")
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[{key}] saved ({len(v.content)/1e6:.1f} MB)")
        return True
    elif status == "failed":
        print(f"[{key}] FAILED: {task_data.get('task_status_msg', 'unknown')}")
        return False
    return None


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
