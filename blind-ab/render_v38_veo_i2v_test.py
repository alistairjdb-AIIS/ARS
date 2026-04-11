#!/usr/bin/env python3
"""v38 — Veo 3.1 image-to-video capability test.

Query: does veo-3.1-fast-generate-preview accept an image in instances[] for
first-frame conditioning?

Structure (per CLAUDE.md "Construct Specific Structure Before Starting"):
  - Test image: v36-frames/f5.jpg (final frame of kling-v3 Pulse render)
  - Prompt: simple character-only motion
  - Success: clip returned AND first frame resembles input image
  - Counter-check: if clip is produced but looks nothing like input, image was ignored

Reference: wiki/tools/veo-3-1.md notes i2v is THEORETICAL for this pipeline.
Google's Gemini API conventionally accepts:
  instances: [{prompt: "...", image: {bytesBase64Encoded: "...", mimeType: "image/jpeg"}}]
  -- this is the convention we're trying first.
"""

import os, json, base64, time, requests

API_KEY = os.environ.get("VEO_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY env var required")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"
IMAGE_PATH = "/root/blind-ab/v36-frames/f5.jpg"

PROMPT = (
    "The small fluffy round creature blinks slowly, then tilts its head "
    "gently to the side. Soft warm breeze ruffles its fur. Warm window "
    "light. Camera stays locked. Audio: soft ambient hum, gentle breath."
)

SHARED_NEGATIVE = (
    "text, watermarks, logos, deformed, extra limbs, blurry, jittery, "
    "camera shake, morphing, warping, flickering"
)


def load_image_b64():
    with open(IMAGE_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def submit():
    img_b64 = load_image_b64()
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"

    # Attempt 1: conventional Google image-conditioning format
    payload = {
        "instances": [
            {
                "prompt": PROMPT,
                "image": {
                    "bytesBase64Encoded": img_b64,
                    "mimeType": "image/jpeg",
                },
            }
        ],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }

    print("[v38] Attempting image-to-video with conventional image field...")
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[v38] ATTEMPT 1 FAILED: HTTP {r.status_code}")
        print(f"[v38] Response: {r.text[:800]}")
        return None, "attempt1_failed"

    op = r.json().get("name")
    if not op:
        print(f"[v38] No operation name: {r.json()}")
        return None, "no_op_name"
    print(f"[v38] submitted: {op}")
    return op, "attempt1_ok"


def poll_and_download(op):
    print(f"\n[v38] Polling {op}...")
    start = time.time()
    while time.time() - start < 600:
        url = f"{BASE_URL}/{op}?key={API_KEY}"
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            print(f"  Poll HTTP {r.status_code}")
            time.sleep(15)
            continue
        d = r.json()
        if not d.get("done"):
            elapsed = int(time.time() - start)
            print(f"  pending ({elapsed}s)...")
            time.sleep(15)
            continue
        err = d.get("error")
        if err:
            print(f"[v38] OPERATION ERROR: {json.dumps(err)[:500]}")
            return None
        samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
        if not samples:
            print(f"[v38] no samples: {json.dumps(d)[:400]}")
            return None
        uri = samples[0].get("video", {}).get("uri", "")
        if not uri:
            return None
        dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
        v = requests.get(dl, timeout=120, allow_redirects=True)
        if v.status_code != 200:
            return None
        out_path = os.path.join(OUT_DIR, "v38-veo-i2v-test.mp4")
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[v38] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
        return out_path
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"[v38] Test image: {IMAGE_PATH}")
    print(f"[v38] Model: {MODEL}")
    print(f"[v38] Prompt: {PROMPT[:100]}...")

    op, status = submit()
    if not op:
        print(f"\n=== RESULT: IMAGE-TO-VIDEO NOT SUPPORTED via conventional format ===")
        print(f"Status: {status}")
        print("Next: try alternative formats (lastFrame, firstFrame, etc.) OR confirm i2v is not yet supported on veo-3.1-fast.")
        return

    result = poll_and_download(op)
    if result:
        print(f"\n=== RESULT: IMAGE-TO-VIDEO ACCEPTED ===")
        print(f"Saved: {result}")
        print("\nCounter-check needed: extract first frame of output and compare against input image.")
        print("If first frame resembles input → i2v works → chain architecture viable.")
        print("If first frame is unrelated → image was ignored → false pass.")
    else:
        print(f"\n=== RESULT: SUBMIT OK BUT DOWNLOAD FAILED ===")


if __name__ == "__main__":
    main()
