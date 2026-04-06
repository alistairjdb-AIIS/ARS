#!/usr/bin/env python3
"""Blind A/B v18 — photoreal elderly man, research-informed crafted vs terse."""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "anime, cartoon, 3D render, Pixar, illustration, text, watermarks, logos, "
    "perfect skin, airbrushed, overly smooth, plastic, uncanny valley, "
    "deformed hands, extra fingers"
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
