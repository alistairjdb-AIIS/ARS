#!/usr/bin/env python3
"""
Blind A/B render — 2026-04-05
Test: reaching exemplar craft level on Veo 3.1.

Subject: 8s cinematic still-life — handmade ceramic bowl, morning window light, oak surface.

Output A: first-instinct, minimal prompt → raw Veo output
Output B: after internal dialogue, crafted shot-list prompt → Veo + typographic overlay (applied separately via ffmpeg)

Both renders are 8s, 16:9, veo-3.1-fast-generate-preview.
Cost: 2 x $0.15 x 8 = $2.40
"""

import requests
import json
import time
import os
import sys

API_KEY = "AIzaSyDWDdnEGEXGuaJGoY0cMku5QFK6hkTSTow"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"

OUTPUTS = {
    "output-a": {
        "prompt": "A handmade ceramic bowl on a wooden table with morning window light, 8 seconds, cinematic.",
        "negative": "faces, hands, people, text, logos, watermarks"
    },
    "output-b-raw": {
        "prompt": (
            "Slow dolly push-in toward a handmade clay-colored ceramic bowl sitting slightly "
            "off-center left on a weathered oak surface, 85mm lens, shallow depth of field. "
            "Warm morning sidelight enters from frame-right window at 45 degrees, casting soft "
            "golden glow across the bowl's surface and rim highlight while leaving the bowl's "
            "interior in deep contemplative shadow. Dust motes drift visibly in the diagonal "
            "light rays. Soft bokeh on wood grain texture in background. Steam rises slowly "
            "from bowl interior. Palette: warm beige, deep walnut brown, cream highlight, muted "
            "ochre. 35mm film grain throughout, slight halation on rim highlights, natural "
            "vignette. Subtle breath-like camera micro-movement. Quiet contemplative register. "
            "Audio: soft morning quiet, distant birdsong, faint kettle in distance."
        ),
        "negative": (
            "faces, hands, people, text, readable characters, logos, watermarks, motion blur, "
            "warping, morphing, bright backgrounds, overexposure, jitter, fast motion, busy frame"
        )
    }
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
            "negativePrompt": p["negative"]
        }
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
            print(f"  poll error {r.status_code}")
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
                print(f"  no video URI: {json.dumps(samples[0])[:500]}")
                return False
            dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
            print(f"  downloading...")
            v = requests.get(dl, timeout=120, allow_redirects=True)
            if v.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(v.content)
                print(f"  saved {out_path} ({len(v.content)/1e6:.1f} MB)")
                return True
            print(f"  download failed: {v.status_code}")
            return False
        elapsed = int(time.time() - start)
        print(f"  waiting ({elapsed}s)...")
        time.sleep(15)
    print(f"  timed out after {max_wait}s")
    return False


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = {}
    for key in ["output-a", "output-b-raw"]:
        op = generate(key)
        if op:
            out = os.path.join(OUT_DIR, f"{key}.mp4")
            ok = poll_download(op, out)
            results[key] = "OK" if ok else "FAIL"
        else:
            results[key] = "SUBMIT_FAIL"
    print()
    print("=== RESULTS ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
