#!/usr/bin/env python3
"""v39 — 3-clip Veo 3.1 Fast chain test (Pulse waking up).

Goal: verify whether character + scene consistency holds across 3 sequential
image-to-video chains. Critical for 30s+ brand film architecture.

Pipeline:
  Clip 1 (text-to-video): sleeping Pulse baseline
  Clip 2 (i2v from clip1 last frame): Pulse waking up
  Clip 3 (i2v from clip2 last frame): Pulse sitting up

Each clip is 8s, so final concat = 24s.

Counter-check: does the character morph across chain steps? If ear shape,
fur color, halo, or wing structure drifts clip-to-clip, the chain architecture
has a character-consistency problem at the multi-step level.
"""

import os, json, base64, time, subprocess, requests

API_KEY = os.environ.get("VEO_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY env var required")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"
DURATION = 8
ASPECT = "16:9"

SHARED_NEGATIVE = (
    "text, watermarks, logos, deformed, extra limbs, blurry, jittery, "
    "camera shake, morphing, warping, flickering, static image"
)

# --- 3 sequential prompts ---
# Character anchor (repeated in each to fight drift):
CHAR_ANCHOR = (
    "a small fluffy yellow creature with round body, big brown eyes, "
    "triangular cat-like ears, a small gold halo floating above the head, "
    "small feathered wings, pink blush on cheeks"
)

PROMPTS = {
    1: (
        f"{CHAR_ANCHOR} lies curled up sleeping on a wooden table at dawn. "
        "Warm golden window light from the left. The creature's chest rises "
        "and falls with slow sleeping breath. Tail curled around body. "
        "Eyes closed. Body completely still except for the slow breathing. "
        "Audio: soft ambient dawn room tone, slow sleeping breath, distant "
        "birdsong."
    ),
    2: (
        f"{CHAR_ANCHOR} is waking up on a wooden table at dawn. Warm golden "
        "window light. The creature slowly opens its eyes, blinks twice, "
        "then lets out a small silent yawn. One paw stretches forward. "
        "Body otherwise still. Audio: soft ambient dawn room tone, a tiny "
        "creaking wood sound, the soft yawn."
    ),
    3: (
        f"{CHAR_ANCHOR} is now sitting up on a wooden table at dawn. Warm "
        "golden window light. The creature shakes its fur gently, looks "
        "left, then looks right, curious, fully awake. Small wing flutter. "
        "Halo sparkles faintly. Audio: soft fur ruffle, a tiny chirp, "
        "warm ambient room tone."
    ),
}


def load_image_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def _submit_with_retry(clip_num, payload):
    """POST to Veo API with 429 retry + backoff. Waits up to 4 × 60s."""
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    for attempt in range(5):
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            op = r.json().get("name")
            if op:
                print(f"[clip{clip_num}] submitted: {op}")
                return op
            print(f"[clip{clip_num}] 200 but no op name: {r.json()}")
            return None
        if r.status_code == 429:
            wait = 60 * (attempt + 1)
            print(f"[clip{clip_num}] 429 quota (attempt {attempt+1}/5), waiting {wait}s...")
            time.sleep(wait)
            continue
        print(f"[clip{clip_num}] SUBMIT ERROR {r.status_code}: {r.text[:400]}")
        return None
    print(f"[clip{clip_num}] Exceeded retry budget on 429")
    return None


def submit_text(clip_num, prompt):
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": ASPECT,
            "durationSeconds": DURATION,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }
    print(f"[clip{clip_num}] Submitting (text-to-video)...")
    return _submit_with_retry(clip_num, payload)


def submit_image(clip_num, prompt, image_path):
    img_b64 = load_image_b64(image_path)
    payload = {
        "instances": [
            {
                "prompt": prompt,
                "image": {
                    "bytesBase64Encoded": img_b64,
                    "mimeType": "image/jpeg",
                },
            }
        ],
        "parameters": {
            "aspectRatio": ASPECT,
            "durationSeconds": DURATION,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }
    print(f"[clip{clip_num}] Submitting (image-to-video from {image_path})...")
    return _submit_with_retry(clip_num, payload)


def poll_and_download(clip_num, op):
    out_path = os.path.join(OUT_DIR, f"v39-clip{clip_num}.mp4")
    start = time.time()
    while time.time() - start < 600:
        url = f"{BASE_URL}/{op}?key={API_KEY}"
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            time.sleep(15)
            continue
        d = r.json()
        if not d.get("done"):
            elapsed = int(time.time() - start)
            print(f"[clip{clip_num}] pending ({elapsed}s)...")
            time.sleep(15)
            continue
        err = d.get("error")
        if err:
            print(f"[clip{clip_num}] OPERATION ERROR: {json.dumps(err)[:500]}")
            return None
        samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
        if not samples:
            print(f"[clip{clip_num}] no samples: {json.dumps(d)[:300]}")
            return None
        uri = samples[0].get("video", {}).get("uri", "")
        if not uri:
            return None
        dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
        v = requests.get(dl, timeout=120, allow_redirects=True)
        if v.status_code != 200:
            return None
        with open(out_path, "wb") as f:
            f.write(v.content)
        print(f"[clip{clip_num}] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
        return out_path
    return None


def extract_last_frame(video_path, out_path):
    # Extract frame at duration - 0.1 to get the last visible frame
    cmd = [
        "ffmpeg", "-loglevel", "error", "-y",
        "-sseof", "-0.1", "-i", video_path,
        "-frames:v", "1", "-q:v", "2",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"  extracted last frame: {out_path}")
    return out_path


def concat_clips(clip_paths, out_path):
    concat_list = os.path.join(OUT_DIR, "v39-concat-list.txt")
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")
    cmd = [
        "ffmpeg", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"concatenated: {out_path}")
    return out_path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    clip_paths = []

    # Clip 1: text-to-video (baseline) — skip if already saved (resume support)
    clip1 = os.path.join(OUT_DIR, "v39-clip1.mp4")
    if os.path.exists(clip1):
        print(f"[clip1] already exists, skipping render")
    else:
        op1 = submit_text(1, PROMPTS[1])
        if not op1:
            raise SystemExit("Clip 1 submission failed")
        clip1 = poll_and_download(1, op1)
        if not clip1:
            raise SystemExit("Clip 1 download failed")
    clip_paths.append(clip1)

    # Extract last frame of clip 1 for clip 2 conditioning
    clip1_last = os.path.join(OUT_DIR, "v39-clip1-last.jpg")
    if not os.path.exists(clip1_last):
        extract_last_frame(clip1, clip1_last)

    # Clip 2: image-to-video from clip1 last — skip if already saved
    clip2 = os.path.join(OUT_DIR, "v39-clip2.mp4")
    if os.path.exists(clip2):
        print(f"[clip2] already exists, skipping render")
    else:
        op2 = submit_image(2, PROMPTS[2], clip1_last)
        if not op2:
            raise SystemExit("Clip 2 submission failed")
        clip2 = poll_and_download(2, op2)
        if not clip2:
            raise SystemExit("Clip 2 download failed")
    clip_paths.append(clip2)

    # Extract last frame of clip 2 for clip 3 conditioning
    clip2_last = os.path.join(OUT_DIR, "v39-clip2-last.jpg")
    if not os.path.exists(clip2_last):
        extract_last_frame(clip2, clip2_last)

    # Clip 3: image-to-video from clip2 last — skip if already saved
    clip3 = os.path.join(OUT_DIR, "v39-clip3.mp4")
    if os.path.exists(clip3):
        print(f"[clip3] already exists, skipping render")
    else:
        op3 = submit_image(3, PROMPTS[3], clip2_last)
        if not op3:
            raise SystemExit("Clip 3 submission failed")
        clip3 = poll_and_download(3, op3)
        if not clip3:
            raise SystemExit("Clip 3 download failed")
    clip_paths.append(clip3)

    # Concatenate into final
    final = os.path.join(OUT_DIR, "v39-chain-final.mp4")
    concat_clips(clip_paths, final)

    print("\n=== CHAIN TEST COMPLETE ===")
    print(f"Clip 1: {clip_paths[0]}")
    print(f"Clip 2: {clip_paths[1]}")
    print(f"Clip 3: {clip_paths[2]}")
    print(f"Concat: {final}")
    print(f"Duration: ~24s")


if __name__ == "__main__":
    main()
