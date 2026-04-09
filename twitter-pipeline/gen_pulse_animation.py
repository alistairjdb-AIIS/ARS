#!/usr/bin/env python3
"""Generate a fresh 8s animation from Pulse keyframe via Veo 3.1 on Runway."""

import os, base64, time, requests
from PIL import Image
from io import BytesIO
from runwayml import RunwayML

RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY")
if not RUNWAY_API_KEY:
    raise SystemExit("RUNWAY_API_KEY env var required")

# Use the joyful Pulse scene (scene 3 — light swirls, crystals, happiness)
IMAGE_PATH = "/root/blind-ab/v33b-scene3-keyframe.png"
OUT_PATH = "/root/twitter-pipeline/pulse-launch.mp4"

PROMPT = (
    "A small glowing golden orb character floats in a crystal cave, radiating warm light. "
    "It spins slowly with joy, arms outstretched. Golden light tendrils spiral outward from its body, "
    "intertwining with the cyan crystal formations. The crystals pulse and shimmer in response to the light. "
    "Tiny sparkles drift upward like fireflies. The character's expression shifts from wonder to pure delight, "
    "eyes closing in a happy squint. The cave walls catch the golden glow, creating dancing shadows. "
    "Anime style, soft lighting, particle effects, warm color palette."
)


def prepare_image_uri(path):
    """Resize to 1280x720, return data URI."""
    img = Image.open(path)
    w, h = img.size
    # Already 16:9-ish, just resize
    target_ratio = 16 / 9
    current_ratio = w / h
    if abs(current_ratio - target_ratio) > 0.1:
        target_h = int(w / target_ratio)
        top = (h - target_h) // 2
        img = img.crop((0, max(0, top), w, min(h, top + target_h)))
    img = img.resize((1280, 720), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def main():
    print("Preparing image...")
    data_uri = prepare_image_uri(IMAGE_PATH)
    print("Image ready: 1280x720")

    client = RunwayML(api_key=RUNWAY_API_KEY)

    print("Submitting to Runway (veo3.1) image-to-video...")
    task = client.image_to_video.create(
        model="veo3.1",
        prompt_image=data_uri,
        prompt_text=PROMPT,
        ratio="1280:720",
        duration=8,
    )
    print(f"Task ID: {task.id}")

    # Poll for completion
    while True:
        task_status = client.tasks.retrieve(task.id)
        status = task_status.status
        print(f"Status: {status}")

        if status == "SUCCEEDED":
            output_url = task_status.output[0]
            print(f"Output URL: {output_url}")

            # Download
            resp = requests.get(output_url)
            with open(OUT_PATH, "wb") as f:
                f.write(resp.content)
            print(f"Saved to {OUT_PATH} ({len(resp.content) / 1024 / 1024:.1f}MB)")
            break
        elif status == "FAILED":
            print(f"FAILED: {task_status.failure}")
            raise SystemExit(1)
        else:
            time.sleep(10)


if __name__ == "__main__":
    main()
