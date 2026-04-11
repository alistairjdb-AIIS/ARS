#!/usr/bin/env python3
"""v37 RETRY — re-submit only the 3 renders that hit 429 on first pass.

Sealed mapping is preserved from v37-labels.md; this script just re-submits
the same (brief, label, prompt) tuples to overwrite the ? status rows.
"""

import os, json, time, requests
from datetime import datetime

API_KEY = os.environ.get("VEO_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY env var required")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"
DURATION = 8
ASPECT = "16:9"

SHARED_NEGATIVE = (
    "text, watermarks, logos, deformed, extra limbs, extra fingers, "
    "blurry, jittery, camera shake, morphing, warping, flickering, "
    "overexposure, static noise"
)

# --- Retry queue: (output_label, prompt) ---
# From v37-labels.md, preserving the sealed mapping:
#   patagonia/b -> post_dialogue
#   apple/a     -> post_dialogue
#   apple/b     -> first_instinct

RETRIES = {
    "patagonia-b": (
        "A figure in a weathered black wetsuit seen from three-quarters behind, "
        "holding a surfboard tucked under one arm, other hand trailing in the "
        "water, standing waist-deep in cold steel-grey Pacific water at "
        "pre-dawn. The water is still except for distant swell building on the "
        "horizon. Warm first-light just catching the eastern edge of low "
        "clouds. The figure holds completely still, watching the horizon, "
        "breath fogging visibly in the cold air. Then takes one long slow "
        "exhale -- a visible plume of breath in the air. Muted warm-cool color "
        "grading, natural light only, weathered texture on the wetsuit. Audio: "
        "slow wave wash, low wind, one distant gull call, the soft exhale. No "
        "dialogue, no music, no wave breaking."
    ),
    "apple-a": (
        "Extreme macro shot, shallow focus. A matte white wireless earbud case "
        "sits alone on a pale linen cloth. Warm morning light from one "
        "direction catches a soft rim along the hinge edge. Only the hinge is "
        "in perfect focus; the rest of the case softens into bokeh. A hand "
        "enters from frame edge -- just fingertips, no palm, no wrist -- and "
        "gently presses the case seam. The lid clicks open with a precise "
        "magnetic sound. The lid lifts in one smooth unhurried arc. Inside, "
        "the chrome stem of an earbud reveals itself, catching the warm "
        "light. Hold on the open case. Soft dust particles drift in the "
        "morning beam. Audio: silence, then the exact magnetic CLICK, the "
        "soft hiss of the hinge opening, a single low warm sustained tone. "
        "No music, no voice. Linen texture visible in the foreground."
    ),
    "apple-b": (
        "Extreme close-up of hands holding a matte white AirPods case on a warm "
        "sunlit marble surface. The case clicks open, one earbud lifts out, "
        "chrome catches the light, then the case clicks shut. Minimal, clean, "
        "Apple aesthetic, shallow depth of field, warm color grading. Audio: "
        "magnetic click, soft ambient hum, single chime."
    ),
}


def submit(label, prompt):
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": ASPECT,
            "durationSeconds": DURATION,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[{label}] SUBMIT ERROR {r.status_code}: {r.text[:300]}")
        return None
    op = r.json().get("name")
    print(f"[{label}] submitted: {op}")
    return op


def check_download(label, op):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d.get("done"):
        return None
    err = d.get("error")
    if err:
        print(f"[{label}] ERROR: {json.dumps(err)[:300]}")
        return False
    samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
    if not samples:
        return False
    uri = samples[0].get("video", {}).get("uri", "")
    if not uri:
        return False
    dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
    v = requests.get(dl, timeout=120, allow_redirects=True)
    if v.status_code != 200:
        return False
    out_path = os.path.join(OUT_DIR, f"v37-{label}.mp4")
    with open(out_path, "wb") as f:
        f.write(v.content)
    print(f"[{label}] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
    return True


def main():
    print(f"=== v37 RETRY ({len(RETRIES)} renders) ===")
    ops = {}
    failed_submit = []
    for label, prompt in RETRIES.items():
        op = submit(label, prompt)
        if op:
            ops[label] = op
        else:
            failed_submit.append(label)
        time.sleep(2)  # small gap to avoid burst limit

    if not ops:
        raise SystemExit("All retries failed submit")

    print(f"\n=== Polling {len(ops)} ops ===")
    results = {}
    for l in failed_submit:
        results[l] = "SUBMIT_FAIL"
    pending = dict(ops)
    start = time.time()
    while pending and time.time() - start < 900:
        for l in list(pending):
            r = check_download(l, pending[l])
            if r is True:
                results[l] = "OK"
                del pending[l]
            elif r is False:
                results[l] = "FAIL"
                del pending[l]
        if pending:
            elapsed = int(time.time() - start)
            print(f"  {len(pending)} pending ({elapsed}s)...")
            time.sleep(15)
    for l in pending:
        results[l] = "TIMEOUT"

    print("\n=== RETRY RESULTS ===")
    for l in RETRIES:
        print(f"  v37-{l}.mp4: {results.get(l, '?')}")


if __name__ == "__main__":
    main()
