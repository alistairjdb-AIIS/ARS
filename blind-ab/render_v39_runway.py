#!/usr/bin/env python3
"""v39 — Chain test continuation via Runway Veo 3.1 Fast.

Google Gemini API hit daily quota on Veo 3.1 Fast after ~11 renders today.
Switching to Runway for clips 2 + 3. Clip 1 already exists (from Google direct).

Runway Veo 3.1 Fast supports image-to-video per SDK:
  model='veo3.1_fast', prompt_image={uri, position}, ratio='1280:720',
  duration=8, audio=True (native audio preserved).

IMPORTANT: `env -u ALL_PROXY -u all_proxy` is required OR unset in env
before running — runwayml SDK crashes on SOCKS proxy per session-start context.
"""

import os, base64, time
from runwayml import RunwayML

API_KEY = os.environ.get("RUNWAY_API_KEY") or os.environ.get("RUNWAYML_API_SECRET")
if not API_KEY:
    raise SystemExit("RUNWAY_API_KEY env var required")

OUT_DIR = "/root/blind-ab"
MODEL = "veo3.1_fast"
RATIO = "1280:720"
DURATION = 8

CHAR_ANCHOR = (
    "a small fluffy yellow creature with round body, big brown eyes, "
    "triangular cat-like ears, a small gold halo floating above the head, "
    "small feathered wings, pink blush on cheeks"
)

PROMPTS = {
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


def image_to_data_uri(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def extract_last_frame(video_path, out_path):
    import subprocess
    cmd = [
        "ffmpeg", "-loglevel", "error", "-y",
        "-sseof", "-0.1", "-i", video_path,
        "-frames:v", "1", "-q:v", "2",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"  extracted last frame: {out_path}")


def run_clip(client, clip_num, prompt, image_path):
    print(f"\n[clip{clip_num}] Submitting via Runway Veo 3.1 Fast (i2v)...")
    print(f"[clip{clip_num}] prompt_image: {image_path}")
    data_uri = image_to_data_uri(image_path)

    task = client.image_to_video.create(
        model=MODEL,
        prompt_image=[{"uri": data_uri, "position": "first"}],
        prompt_text=prompt,
        ratio=RATIO,
        duration=DURATION,
    )
    task_id = task.id
    print(f"[clip{clip_num}] task_id: {task_id}")

    # Poll
    start = time.time()
    while time.time() - start < 900:
        t = client.tasks.retrieve(task_id)
        status = t.status
        elapsed = int(time.time() - start)
        print(f"[clip{clip_num}] status={status} ({elapsed}s)")
        if status == "SUCCEEDED":
            # Download
            output_urls = t.output
            if not output_urls:
                print(f"[clip{clip_num}] SUCCEEDED but no output URLs: {t}")
                return None
            url = output_urls[0] if isinstance(output_urls, list) else output_urls
            import requests
            r = requests.get(url, timeout=120)
            if r.status_code != 200:
                print(f"[clip{clip_num}] download HTTP {r.status_code}")
                return None
            out_path = os.path.join(OUT_DIR, f"v39-clip{clip_num}.mp4")
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"[clip{clip_num}] saved: {out_path} ({len(r.content)/1e6:.1f} MB)")
            return out_path
        if status == "FAILED":
            print(f"[clip{clip_num}] FAILED: {t}")
            return None
        time.sleep(10)
    print(f"[clip{clip_num}] TIMEOUT")
    return None


def main():
    client = RunwayML(api_key=API_KEY)

    clip1 = os.path.join(OUT_DIR, "v39-clip1.mp4")
    if not os.path.exists(clip1):
        raise SystemExit(f"Clip 1 missing at {clip1} — run Google direct first")

    clip1_last = os.path.join(OUT_DIR, "v39-clip1-last.jpg")
    if not os.path.exists(clip1_last):
        extract_last_frame(clip1, clip1_last)

    # Clip 2 from clip 1 last
    clip2 = os.path.join(OUT_DIR, "v39-clip2.mp4")
    if not os.path.exists(clip2):
        clip2 = run_clip(client, 2, PROMPTS[2], clip1_last)
        if not clip2:
            raise SystemExit("Clip 2 failed")
    else:
        print(f"[clip2] already exists, skipping")

    clip2_last = os.path.join(OUT_DIR, "v39-clip2-last.jpg")
    if not os.path.exists(clip2_last):
        extract_last_frame(clip2, clip2_last)

    # Clip 3 from clip 2 last
    clip3 = os.path.join(OUT_DIR, "v39-clip3.mp4")
    if not os.path.exists(clip3):
        clip3 = run_clip(client, 3, PROMPTS[3], clip2_last)
        if not clip3:
            raise SystemExit("Clip 3 failed")
    else:
        print(f"[clip3] already exists, skipping")

    # Concat
    import subprocess
    concat_list = os.path.join(OUT_DIR, "v39-concat-list.txt")
    with open(concat_list, "w") as f:
        for p in [clip1, clip2, clip3]:
            f.write(f"file '{p}'\n")
    final = os.path.join(OUT_DIR, "v39-chain-final.mp4")
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", concat_list, "-c", "copy", final],
        check=True,
    )

    print("\n=== CHAIN TEST COMPLETE ===")
    print(f"Clip 1 (Google direct text-to-video): {clip1}")
    print(f"Clip 2 (Runway Veo 3.1 Fast i2v): {clip2}")
    print(f"Clip 3 (Runway Veo 3.1 Fast i2v): {clip3}")
    print(f"Concat: {final}")


if __name__ == "__main__":
    main()
