#!/usr/bin/env python3
"""Blind A/B v16 — seinen anime train scene, research-informed (tight chain) vs terse."""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "live-action, photorealistic, 3D render, CGI, Pixar, text, readable characters, "
    "logos, watermarks, motion blur, warping, jitter, overexposure, "
    "deformed hands, extra fingers"
)

# A=terse, B=research-informed crafted
PROMPTS = {
    "v16-output-a-raw": (
        "8-second seinen anime scene. A teenage boy in a school uniform sits by a "
        "rain-streaked train window. He watches the rain, then notices his reflection "
        "and his expression softens. Muted blue-grey palette, evening light. "
        "Contemplative and melancholic. No dialogue."
    ),
    "v16-output-b-raw": (
        "Seinen anime. A teenage boy in a dark school uniform sits alone by a train "
        "window, chin resting on his hand, watching raindrops race down the glass. "
        "The city lights outside blur into streaks of amber and blue. He catches his "
        "own reflection in the window — pauses — then his tense jaw loosens, eyes "
        "soften. Muted blue-grey palette with warm amber window reflections, evening "
        "overcast light, gentle train sway. Shallow depth of field."
    ),
}


def submit(key, prompt):
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[{key}] SUBMIT ERROR {r.status_code}: {r.text[:300]}")
        return None
    op = r.json().get("name")
    print(f"[{key}] submitted: {op}")
    return op


def check_download(key, op):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d.get("done"):
        return None
    samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
    if not samples:
        print(f"[{key}] no samples: {json.dumps(d)[:300]}")
        return False
    uri = samples[0].get("video", {}).get("uri", "")
    if not uri:
        return False
    dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
    v = requests.get(dl, timeout=120, allow_redirects=True)
    if v.status_code != 200:
        return False
    out_path = os.path.join(OUT_DIR, f"{key}.mp4")
    with open(out_path, "wb") as f:
        f.write(v.content)
    print(f"[{key}] saved ({len(v.content)/1e6:.1f} MB)")
    return True


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    ops = {}
    for key, prompt in PROMPTS.items():
        op = submit(key, prompt)
        if op:
            ops[key] = op

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
