#!/usr/bin/env python3
"""Blind A/B v11 — anime character, prompt-depth test."""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "live-action, photorealistic, 3D render, CGI, text, readable characters, "
    "logos, watermarks, motion blur, warping, jitter, overexposure, "
    "deformed hands, extra fingers"
)

# A=crafted, B=terse (randomized assignment)
PROMPTS = {
    "v11-output-a-raw": (
        "Cinematography: medium shot, slow push-in from waist-level, shallow depth "
        "of field with city skyline softly defocused. Subject: anime-style young woman, "
        "dark hair past shoulders, casual clothes, sitting on concrete rooftop edge, "
        "legs dangling over the side. Action: wind blows through her hair with irregular "
        "gusts, loose strands drift across her face, she gazes toward the horizon without "
        "moving, fabric of her jacket shifts slightly in breeze. Context: golden hour dusk, "
        "warm orange-pink sky fading to deep blue above, city skyline silhouetted in "
        "mid-ground, rooftop has weathered concrete texture with a few scattered items "
        "behind her, warm rim light from setting sun on her hair and shoulder edges. "
        "Style & Ambiance: hand-drawn anime aesthetic with visible line work, warm sunset "
        "+ cool shadow palette, contemplative solitude mood, Makoto Shinkai-inspired "
        "atmospheric lighting. Audio: soft rooftop wind, distant city hum, faint wind chime."
    ),
    "v11-output-b-raw": (
        "8-second anime-style scene. Young woman sitting on a rooftop edge at dusk, "
        "legs dangling, wind blowing through her dark hair. City skyline in the background. "
        "She gazes at the horizon, contemplative. Warm sunset palette. Slow camera push-in. "
        "No dialogue."
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
