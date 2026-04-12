"""
Generate Strait of Hormuz cinematic explainer via Runway's Veo 3.1.
Runway promptText capped at 1000 chars — keep it tight.
"""
import os, time

# Runway SDK needs no SOCKS proxy
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

from runwayml import RunwayML

RUNWAY_KEY = os.environ.get("RUNWAY_API_KEY")
OUT = "/root/comic-v7"

client = RunwayML(api_key=RUNWAY_KEY)

# Tight prompt — under 1000 chars
PROMPT = """Dark cinematic aerial view of a narrow ocean strait at twilight. A single glowing cargo ship passes through calm deep navy water between two dark coastlines. Slow, deliberate camera movement. Then dozens more ships appear from all directions, their wake trails glowing orange as they converge on the narrow bottleneck. The water shifts from blue to deep red as the passage fills. Storm clouds roll in. Camera pulls back to reveal the full trapped fleet in the chokepoint. Atmospheric, moody, documentary cinematography. Dark color grading with teal and orange accents."""

print(f"Prompt length: {len(PROMPT)} chars")
assert len(PROMPT) <= 1000, f"Prompt too long: {len(PROMPT)}"

# Try Veo 3.1 fast first (cheaper)
print("\nSubmitting to Runway Veo 3.1 fast...")
try:
    task = client.text_to_video.create(
        model="veo3.1_fast",
        prompt_text=PROMPT,
        duration=8,
        ratio="1920:1080",
    )
    task_id = task.id
    print(f"Task ID: {task_id}")

    # Poll
    for attempt in range(120):
        time.sleep(5)
        result = client.tasks.retrieve(task_id)
        status = result.status
        print(f"Poll {attempt+1}: {status}")

        if status == "SUCCEEDED":
            output_url = result.output[0] if result.output else None
            if output_url:
                print(f"\nDownloading from: {output_url[:80]}...")
                import requests
                r = requests.get(output_url, timeout=120)
                path = os.path.join(OUT, "approach1_veo_runway.mp4")
                with open(path, "wb") as f:
                    f.write(r.content)
                print(f"Saved: {path} ({len(r.content)//1024}KB)")
            else:
                print(f"No output URL: {result}")
            break

        elif status == "FAILED":
            print(f"FAILED: {result.failure}")
            print(f"Full: {result}")
            break
    else:
        print("Timed out after 10 minutes")

except Exception as e:
    print(f"Error: {e}")
