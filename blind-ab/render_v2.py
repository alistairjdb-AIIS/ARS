#!/usr/bin/env python3
"""
Blind A/B v2 — controlled brief, varying only prompt craft depth.
Both prompts target IDENTICAL brief. Only phrasing changes.
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
    "jitter, fast motion, busy frame"
)

OUTPUTS = {
    "v2-output-a-raw": {
        "prompt": (
            "8-second cinematic still-life. Handmade ceramic bowl on weathered oak surface. "
            "Morning window sidelight from frame-right at 45 degrees. Slow camera push-in. "
            "Steam rising from bowl interior, drifting in the sidelight. Warm palette."
        ),
        "negative": SHARED_NEGATIVE,
    },
    "v2-output-b-raw": {
        "prompt": (
            "Cinematography: 85mm lens, shallow depth of field f/2.0, slow dolly push-in 15%, "
            "locked horizontal at table height. Subject: handmade ceramic bowl, slightly "
            "off-center left composition. Action: steam rises from bowl interior, drifting "
            "slowly in the light beam. Context: weathered oak surface with visible grain, "
            "warm morning sidelight streams from frame-right window at 45 degrees, soft rim "
            "highlight on bowl, long shadow across oak. Style & Ambiance: slow contemplative "
            "artisan luxury, warm beige + honey-oak + cream palette, 35mm film grain, slight "
            "halation on rim highlights, quiet morning atmosphere. Audio: soft morning quiet, "
            "distant birdsong."
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
    for key in ["v2-output-a-raw", "v2-output-b-raw"]:
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
