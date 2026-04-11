#!/usr/bin/env python3
"""Blind A/B v34 — Pulse quiet-realization beat. First-instinct vs post-dialogue.

Model held constant: kling-v1-6, std, 5s, 16:9, text-to-video.
Brief held constant: Pulse alone at a window, looking at a drawing, quiet realization.
Varies: prompt-writing process only.

Label assignment is randomized at submit time. The true mapping is written to
v34-labels.md only after both renders complete.
"""

import os, json, time, random, requests, jwt
from datetime import datetime

ACCESS_KEY = os.environ.get("KLING_ACCESS_KEY")
SECRET_KEY = os.environ.get("KLING_SECRET_KEY")
if not ACCESS_KEY or not SECRET_KEY:
    raise SystemExit("KLING_ACCESS_KEY and KLING_SECRET_KEY env vars required")

BASE_URL = "https://api.klingai.com"
OUT_DIR = "/root/blind-ab"

# --- Brief (constant) ---
BRIEF = (
    "Pulse, the round fluffy yellow angel, alone at a window at sunset, "
    "looking at a small paper drawing, having a quiet realization."
)

# --- Output 1: first instinct, no internal dialogue ---
PROMPT_FIRST_INSTINCT = (
    "Pulse the round yellow fluffy angel sits on a wooden windowsill at dusk. "
    "Warm evening light. Holding a small paper drawing. Looks down at it, then "
    "lifts head slowly, eyes lighting up with realization. Small happy smile "
    "forms. Anime style, Studio Ghibli mood, soft lighting."
)

# --- Output 2: after internal dialogue ---
# Dialogue notes (documented, not sent to model):
#   - No adjective-stack mood-board
#   - 1 clear beat + micro-support in 5s (not 3 beats)
#   - Realization → concrete physical proxy (eye-widen, mouth-part, smile-begin)
#   - NB2 character anchor: no external ears, brown eyes, halo, feathered wings, paw-hands
#   - No camera spec (director, not DP)
#   - Name what NOT to animate (body still, motion confined to face)
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
    "extra limbs, blurry, jittery, camera shake"
)

MODEL = "kling-v1-6"
MODE = "std"
DURATION = "5"
ASPECT = "16:9"


def get_token():
    now = int(datetime.now().timestamp())
    payload = {"iss": ACCESS_KEY, "exp": now + 1800, "nbf": now - 5, "iat": now}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256",
                      headers={"typ": "JWT", "alg": "HS256"})


def submit(label, prompt):
    token = get_token()
    url = f"{BASE_URL}/v1/videos/text2video"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "model_name": MODEL,
        "prompt": prompt,
        "negative_prompt": SHARED_NEGATIVE,
        "cfg_scale": 0.5,
        "mode": MODE,
        "aspect_ratio": ASPECT,
        "duration": DURATION,
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code != 200:
        print(f"[{label}] SUBMIT ERROR {r.status_code}: {r.text[:300]}")
        return None
    data = r.json()
    if data.get("code") != 0:
        print(f"[{label}] API ERROR: {data.get('message', 'unknown')}")
        return None
    task_id = data.get("data", {}).get("task_id")
    print(f"[{label}] submitted: task_id={task_id}")
    return task_id


def check_download(label, task_id):
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
        out_path = os.path.join(OUT_DIR, f"v34-output-{label}.mp4")
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[{label}] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
        return True
    elif status == "failed":
        print(f"[{label}] FAILED: {task_data.get('task_status_msg', 'unknown')}")
        return False
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Randomize label assignment (true mapping NOT written until after render)
    rng = random.SystemRandom()
    if rng.random() < 0.5:
        mapping = {"a": ("first_instinct", PROMPT_FIRST_INSTINCT),
                   "b": ("post_dialogue", PROMPT_POST_DIALOGUE)}
    else:
        mapping = {"a": ("post_dialogue", PROMPT_POST_DIALOGUE),
                   "b": ("first_instinct", PROMPT_FIRST_INSTINCT)}

    print("=== Submitting v34 blind A/B ===")
    ops = {}
    for label, (process, prompt) in mapping.items():
        task_id = submit(label, prompt)
        if task_id:
            ops[label] = task_id
    if len(ops) != 2:
        raise SystemExit(f"Only {len(ops)}/2 submissions succeeded — aborting")

    print(f"\n=== Polling {len(ops)} operations ===")
    results = {}
    pending = dict(ops)
    start = time.time()
    while pending and time.time() - start < 900:
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
    for k in sorted(mapping):
        print(f"  v34-output-{k}.mp4: {results.get(k, '?')} ({mapping[k][0]})")

    # Write sealed mapping AFTER render
    labels_path = os.path.join(OUT_DIR, "v34-labels.md")
    with open(labels_path, "w") as f:
        f.write("# v34 Blind A/B — Sealed Mapping\n\n")
        f.write(f"Session 36 blind test. Date: {datetime.utcnow().isoformat()}Z\n\n")
        f.write(f"**Model:** {MODEL} / mode={MODE} / duration={DURATION}s / aspect={ASPECT}\n\n")
        f.write(f"**Brief:** {BRIEF}\n\n")
        f.write("**Variable:** prompt-writing process only.\n\n")
        f.write("## Label → Process\n\n")
        for k in sorted(mapping):
            process, prompt = mapping[k]
            f.write(f"### v34-output-{k}.mp4 — **{process}**\n\n")
            f.write(f"Render status: {results.get(k, '?')}\n\n")
            f.write(f"Prompt:\n> {prompt}\n\n")
        f.write("## Task IDs\n\n")
        for k, tid in ops.items():
            f.write(f"- {k}: {tid}\n")
    print(f"\nSealed mapping written: {labels_path}")


if __name__ == "__main__":
    main()
