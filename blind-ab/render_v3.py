#!/usr/bin/env python3
"""
Blind A/B v3 — olive oil bottle photoreal still-life.
Tests if crafted shot-list consistently beats terse on photoreal (new subject).
Craft fix: no "35mm film grain" language (caused literal filmstrip artifacts in v2).
"""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "faces, hands, people, text, readable characters, logos, watermarks, "
    "motion blur, warping, morphing, bright backgrounds, overexposure, "
    "jitter, fast motion, busy frame, filmstrip edges, sprocket holes, film burns"
)

OUTPUTS = {
    "v3-output-a-raw": {
        "prompt": (
            "8-second cinematic photoreal still-life. Clear glass bottle of olive oil on "
            "polished marble surface. Warm morning window sidelight from frame-right at 45 "
            "degrees. Slow camera orbit 20 degrees around bottle. Golden-green liquid visible "
            "through glass with light refraction. Shallow depth of field. Warm amber palette."
        ),
        "negative": SHARED_NEGATIVE,
    },
    "v3-output-b-raw": {
        "prompt": (
            "Cinematography: 85mm lens, shallow depth of field f/2.0, slow camera orbit 20 "
            "degrees around subject, locked vertical at bottle mid-height. Subject: clear glass "
            "bottle of olive oil, slightly off-center, golden-green liquid visible through glass, "
            "subtle light refraction through bottle glass. Action: liquid shifts slowly as camera "
            "orbits, catching highlights at varying angles. Context: polished marble surface "
            "with subtle gray veining, warm morning light streams from frame-right window at 45 "
            "degrees, soft rim highlight on glass bottle edge, light refracts through liquid "
            "creating warm amber glow on marble beneath. Style & Ambiance: slow contemplative "
            "artisan luxury, warm amber + golden-green + muted marble palette, soft organic "
            "noise texture, subtle halation on glass highlights, quiet morning atmosphere. "
            "Audio: soft morning quiet, distant birdsong."
        ),
        "negative": SHARED_NEGATIVE,
    },
}


def generate(key):
    p = OUTPUTS[key]
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": p["prompt"]}],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "sampleCount": 1,
            "negativePrompt": p["negative"],
        },
    }
    print(f"[{key}] submitting...")
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"  ERROR {r.status_code}: {r.text[:500]}")
        return None
    op = r.json().get("name")
    print(f"  operation: {op}")
    return op


def poll_download(op, out_path, max_wait=600):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    start = time.time()
    while time.time() - start < max_wait:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            time.sleep(10)
            continue
        d = r.json()
        if d.get("done"):
            samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
            if not samples:
                print(f"  no samples: {json.dumps(d)[:500]}")
                return False
            uri = samples[0].get("video", {}).get("uri", "")
            if not uri:
                return False
            dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
            print(f"  downloading...")
            v = requests.get(dl, timeout=120, allow_redirects=True)
            if v.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(v.content)
                print(f"  saved {out_path} ({len(v.content)/1e6:.1f} MB)")
                return True
            return False
        elapsed = int(time.time() - start)
        print(f"  waiting ({elapsed}s)...")
        time.sleep(15)
    return False


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = {}
    for key in ["v3-output-a-raw", "v3-output-b-raw"]:
        op = generate(key)
        if op:
            out = os.path.join(OUT_DIR, f"{key}.mp4")
            ok = poll_download(op, out)
            results[key] = "OK" if ok else "FAIL"
        else:
            results[key] = "SUBMIT_FAIL"
    print("\n=== RESULTS ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
