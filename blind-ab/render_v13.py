#!/usr/bin/env python3
"""Blind A/B v13 — 3D Pixar-style robot, prompt-depth test."""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "live-action, photorealistic, anime, hand-drawn, 2D, text, readable characters, "
    "logos, watermarks, motion blur, warping, jitter, overexposure, "
    "deformed hands, extra fingers, uncanny valley"
)

# A=crafted, B=terse (flipped from v12)
PROMPTS = {
    "v13-output-a-raw": (
        "Cinematography: slow dolly-in from medium-wide to medium close-up, slightly "
        "low angle looking up at bench, shallow depth of field with autumn trees softly "
        "blurred behind. Subject: small humanoid robot with a rounded dented metal body, "
        "mismatched bolts, one slightly flickering eye-light, seated on a worn wooden "
        "park bench with peeling green paint. Action: robot reaches into a small paper "
        "bag on the bench, pulls out a breadcrumb, and tosses it gently toward three "
        "pigeons on the ground — pigeons hop and peck, one flutters its wings briefly, "
        "robot tilts its head watching them with subtle mechanical whir. Context: quiet "
        "city park in late afternoon, golden hour light filtering through canopy of maple "
        "trees, orange and red leaves scattered on the ground and drifting slowly through "
        "the air, empty path behind the bench, distant park lamp. Style & Ambiance: 3D "
        "Pixar-style rendering, warm saturated autumn palette, gentle whimsical mood, "
        "slight melancholy in the robot's solitude contrasted with the pigeons' liveliness. "
        "Audio: soft wind rustling leaves, distant birds chirping, subtle mechanical servo "
        "sounds when robot moves, pigeon cooing, gentle ambient park atmosphere."
    ),
    "v13-output-b-raw": (
        "8-second 3D Pixar-style animated scene. A small dented robot sits on a park "
        "bench feeding breadcrumbs to pigeons. Warm golden hour afternoon light, autumn "
        "leaves on the ground and falling gently. Whimsical and slightly melancholic mood. "
        "Camera slowly moves closer. No dialogue."
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
