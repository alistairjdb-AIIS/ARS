"""
Comic v7 — LLM NEWS explainer: 3 parallel approaches.
Approach 1: Veo 3.1 (native video + audio from prompt)
Approach 2: Kling v3 (cinematic video, no audio)
Approach 3: NB2 scene-by-scene → sequenced with transitions

Content: Strait of Hormuz — visual metaphor approach, not infographic.
"""
import os, json, base64, time, hmac, hashlib, struct, requests

OUT = "/root/comic-v7"

# Keys
VEO_KEY = os.environ.get("VEO_API_KEY", "AIzaSyBPr_-MJ0PGihDVpbQL666iHBfNFqvlLnM")
KLING_ACCESS = "ANRfHmR8PYdM9PeQtgm48CnL8bDHByB3"
KLING_SECRET = "aLAnPFbGBfMhmpMQTdE8bkbMdHF4ykHP"
NB2_KEY = VEO_KEY

# ════════════════════════════════════════
# PROMPTS — visual metaphor, not infographic
# ════════════════════════════════════════

# Veo 3.1: full narrated video with native audio
VEO_PROMPT = """A cinematic documentary-style explainer about the Strait of Hormuz ceasefire trap.
Clean, minimal visual style on dark navy background. Calm, authoritative male narrator voice.

Scene 1: A single white dot representing an oil tanker moves smoothly through a narrow passage between two dark landmasses. The passage glows soft green. The narrator says: "Iran reopened the Strait of Hormuz. A two-week ceasefire. Oil prices dropped four percent. The headline looked like good news."

Scene 2: More white dots appear — dozens of ships — all converging on the same narrow passage from different directions. Orange trail lines show their paths. The narrator says: "So shipping companies did the rational thing. They abandoned the long route around Africa and sent their ships back through the Strait. Eight hundred thousand dollars saved per voyage."

Scene 3: The passage turns red. The green glow dies. The dots are now trapped inside — the passage narrows visually. A countdown timer appears: 14 DAYS. The narrator says: "But here's what they missed. In fourteen days, the ceasefire expires. And now every ship that went back in... is trapped inside the bottleneck."

Scene 4: Camera pulls way back. The entire region pulses deep purple. The narrow passage is a tiny chokepoint in a vast dark ocean. Text fades in: "The Strait is now a weapon. Even when it's open." The narrator says: "This is system four. The Strait isn't just a shipping lane anymore. It's a permanent geopolitical weapon. Maritime insurance reprices forever. The option to close has been demonstrated. And nobody has a model for what that means."

End card: "LLM NEWS" logo, clean white on dark navy. Subtitle: "The patterns humans miss."

Style: Vox documentary meets Bloomberg terminal. Minimal, data-driven, dark background with bright accent colors. Camera movements are slow and deliberate. Typography is bold sans-serif, appearing and disappearing with purpose."""

# Kling v3: cinematic short, no audio
KLING_PROMPT = """Cinematic aerial view of a narrow ocean strait between two dark mountainous coastlines at dusk. Golden light on the water. A single cargo ship sails through the calm narrow passage. The water shimmers. The camera slowly pulls back to reveal dozens more ships converging from all directions toward the same narrow gap, their wake trails forming orange-white lines on the dark water. The peaceful golden light gradually shifts to deep red as the passage seems to narrow. Dark storm clouds roll in from the edges. The ships are caught in the bottleneck — too many vessels in too small a space. Cinematic, atmospheric, documentary photography style, dark moody color grading, 4K quality."""

# NB2 scenes — distinct images for each beat
NB2_SCENES = [
    {
        "name": "scene1_passage",
        "prompt": """Minimalist illustration on off-white background. A clean black curved line forms a narrow horizontal passage — like a river between two landmasses seen from above. A single small red dot sits at the left entrance of the passage. Bold black text upper-left reads "The Ceasefire." Clean, modern, editorial style. Only 3 elements: the passage, the dot, the text. Lots of whitespace. Style: motion.so explainer, Vox documentary graphics.""",
    },
    {
        "name": "scene2_convergence",
        "prompt": """Minimalist illustration on off-white background. Same narrow black curved passage from above, but now 30+ small red dots are converging on it from all directions — streams of dots flowing toward the bottleneck with orange trail lines behind them. The passage entrance is getting crowded. Small text: "$800K saved per voyage." Bold black text reads "The Re-routing." Clean editorial style, lots of whitespace around the central action. Style: motion.so explainer, data visualization aesthetic.""",
    },
    {
        "name": "scene3_trap",
        "prompt": """Minimalist illustration on off-white background. The narrow passage is now colored deep red. The dots inside are trapped — the passage walls have visually tightened. Outside the passage, a few dots that stayed away are colored green with a curved dotted line showing the long route around. A bold countdown reads "14 DAYS" in red. Bold black text: "The Trap." Stark contrast between the trapped red cluster and the safe green dots outside. Style: motion.so explainer, urgent but clean.""",
    },
    {
        "name": "scene4_permanent",
        "prompt": """Minimalist illustration on off-white background. Zoomed way out — the passage is now tiny in the center of a vast space. A massive deep purple gradient radiates outward from it, covering most of the frame — it has no edges, it extends beyond the borders. The passage itself pulses like a wound. Bold text center: "The Strait is now a weapon." Smaller text below: "Even when it's open." At the very bottom in muted red: "the invisible risk finally made visible." Style: motion.so explainer finale, dramatic but minimal.""",
    },
    {
        "name": "scene5_endcard",
        "prompt": """Minimalist end card. Dark navy (#0F172A) background. Center: "LLM NEWS" in bold white modern sans-serif. Below in smaller muted blue-grey text: "The patterns humans miss." Clean, professional, simple. Nothing else on screen. Brand card style.""",
    },
]


# ════════════════════════════════════════
# APPROACH 1: Veo 3.1
# ════════════════════════════════════════
def run_veo():
    print("\n" + "=" * 60)
    print("APPROACH 1: Veo 3.1 (native video + audio)")
    print("=" * 60)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning?key={VEO_KEY}"
    payload = {
        "instances": [{"prompt": VEO_PROMPT}],
        "parameters": {
            "sampleCount": 1,
            "durationSeconds": 8,
            "aspectRatio": "16:9",
            "personGeneration": "dont_allow",
            "generateAudio": True,
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        print(f"  Submit: HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}")
            return None
        op = r.json()
        op_name = op.get("name", "")
        print(f"  Operation: {op_name}")

        # Poll for completion
        for attempt in range(60):
            time.sleep(10)
            poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={VEO_KEY}"
            pr = requests.get(poll_url, timeout=30)
            if pr.status_code != 200:
                print(f"  Poll err: {pr.status_code}")
                continue
            status = pr.json()
            done = status.get("done", False)
            print(f"  Poll {attempt+1}: done={done}")
            if done:
                # Extract video
                resp = status.get("response", {})
                videos = resp.get("generatedSamples", [])
                if videos:
                    video_uri = videos[0].get("video", {}).get("uri", "")
                    if video_uri:
                        vr = requests.get(f"{video_uri}&key={VEO_KEY}", timeout=120)
                        if vr.status_code == 200:
                            path = os.path.join(OUT, "approach1_veo.mp4")
                            with open(path, "wb") as f:
                                f.write(vr.content)
                            print(f"  Saved: {path} ({len(vr.content)//1024}KB)")
                            return path
                    # Try inline data
                    for v in videos:
                        vid = v.get("video", {})
                        if "bytesBase64Encoded" in vid:
                            data = base64.b64decode(vid["bytesBase64Encoded"])
                            path = os.path.join(OUT, "approach1_veo.mp4")
                            with open(path, "wb") as f:
                                f.write(data)
                            print(f"  Saved: {path} ({len(data)//1024}KB)")
                            return path
                print(f"  No video in response: {json.dumps(status)[:500]}")
                return None
        print("  Timed out after 10 minutes")
        return None
    except Exception as e:
        print(f"  EXC: {e}")
        return None


# ════════════════════════════════════════
# APPROACH 2: Kling v3
# ════════════════════════════════════════
def kling_jwt():
    """Generate Kling API JWT token."""
    import jwt
    now = int(time.time())
    payload = {
        "iss": KLING_ACCESS,
        "exp": now + 1800,
        "nbf": now - 5,
        "iat": now,
    }
    return jwt.encode(payload, KLING_SECRET, algorithm="HS256")


def run_kling():
    print("\n" + "=" * 60)
    print("APPROACH 2: Kling v3 (cinematic video)")
    print("=" * 60)

    try:
        token = kling_jwt()
    except ImportError:
        print("  PyJWT not installed, trying manual JWT...")
        try:
            # Manual JWT
            import hmac, hashlib
            header = base64.urlsafe_b64encode(json.dumps({"alg":"HS256","typ":"JWT"}).encode()).rstrip(b'=').decode()
            now = int(time.time())
            payload_data = json.dumps({"iss":KLING_ACCESS,"exp":now+1800,"nbf":now-5,"iat":now})
            payload_b64 = base64.urlsafe_b64encode(payload_data.encode()).rstrip(b'=').decode()
            sig_input = f"{header}.{payload_b64}".encode()
            sig = base64.urlsafe_b64encode(hmac.new(KLING_SECRET.encode(), sig_input, hashlib.sha256).digest()).rstrip(b'=').decode()
            token = f"{header}.{payload_b64}.{sig}"
        except Exception as e:
            print(f"  JWT failed: {e}")
            return None

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "model_name": "kling-v3",
        "prompt": KLING_PROMPT,
        "duration": "10",
        "mode": "pro",
        "aspect_ratio": "16:9",
        "cfg_scale": 0.7,
    }

    try:
        r = requests.post("https://api.klingai.com/v1/videos/text2video",
                          headers=headers, json=payload, timeout=30)
        print(f"  Submit: HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}")
            return None
        data = r.json()
        task_id = data.get("data", {}).get("task_id", "")
        print(f"  Task: {task_id}")

        # Poll
        for attempt in range(60):
            time.sleep(10)
            pr = requests.get(f"https://api.klingai.com/v1/videos/text2video/{task_id}",
                              headers=headers, timeout=30)
            if pr.status_code != 200:
                continue
            status = pr.json()
            task_status = status.get("data", {}).get("task_status", "")
            print(f"  Poll {attempt+1}: {task_status}")
            if task_status == "succeed":
                videos = status.get("data", {}).get("task_result", {}).get("videos", [])
                if videos:
                    vid_url = videos[0].get("url", "")
                    if vid_url:
                        vr = requests.get(vid_url, timeout=120)
                        path = os.path.join(OUT, "approach2_kling.mp4")
                        with open(path, "wb") as f:
                            f.write(vr.content)
                        print(f"  Saved: {path} ({len(vr.content)//1024}KB)")
                        return path
                return None
            elif task_status == "failed":
                print(f"  FAILED: {json.dumps(status)[:500]}")
                return None
        print("  Timed out")
        return None
    except Exception as e:
        print(f"  EXC: {e}")
        return None


# ════════════════════════════════════════
# APPROACH 3: NB2 scene-by-scene
# ════════════════════════════════════════
def gen_nb2_scene(prompt, filename):
    """Generate a single scene image with NB2."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={NB2_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "16:9"},
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=300)
        if r.status_code != 200:
            print(f"    ERR {r.status_code}: {r.text[:300]}")
            return None
        data = r.json()
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img = base64.b64decode(part["inlineData"]["data"])
                    path = os.path.join(OUT, filename)
                    with open(path, "wb") as f:
                        f.write(img)
                    print(f"    Saved: {filename} ({len(img)//1024}KB)")
                    return path
        return None
    except Exception as e:
        print(f"    EXC: {e}")
        return None


def run_nb2_scenes():
    print("\n" + "=" * 60)
    print("APPROACH 3: NB2 scene-by-scene → sequenced video")
    print("=" * 60)

    paths = []
    for i, scene in enumerate(NB2_SCENES):
        print(f"  Scene {i+1}/{len(NB2_SCENES)}: {scene['name']}")
        path = gen_nb2_scene(scene["prompt"], f"approach3_{scene['name']}.png")
        paths.append(path)

    # Sequence into video: each scene 4 seconds with 0.5s crossfade
    valid = [p for p in paths if p]
    if len(valid) < 3:
        print(f"  Only {len(valid)} scenes generated, need at least 3")
        return None

    print(f"\n  Sequencing {len(valid)} scenes into video...")

    # Build ffmpeg filter for crossfade transitions
    inputs = " ".join(f'-loop 1 -t 5 -i "{p}"' for p in valid)

    # Simple concat with crossfades
    n = len(valid)
    filter_parts = []

    # Scale all to 1920x1080
    for i in range(n):
        filter_parts.append(f'[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}]')

    # Crossfade chain
    if n == 1:
        filter_parts.append(f'[v0]null[outv]')
    else:
        # First xfade
        filter_parts.append(f'[v0][v1]xfade=transition=fade:duration=0.8:offset=4.2[x1]')
        for i in range(2, n):
            prev = f'x{i-1}'
            offset = 4.2 + (i - 1) * 4.2
            filter_parts.append(f'[{prev}][v{i}]xfade=transition=fade:duration=0.8:offset={offset:.1f}[x{i}]')
        filter_parts.append(f'[x{n-1}]null[outv]')

    filter_str = ";".join(filter_parts)
    output_path = os.path.join(OUT, "approach3_nb2_scenes.mp4")

    cmd = (
        f'ffmpeg -y {inputs} '
        f'-filter_complex "{filter_str}" '
        f'-map "[outv]" -c:v libx264 -pix_fmt yuv420p -crf 18 "{output_path}"'
    )

    os.system(cmd)
    if os.path.exists(output_path):
        mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Output: {output_path} ({mb:.1f}MB)")
        return output_path
    else:
        print("  ffmpeg FAILED")
        return None


# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════
if __name__ == "__main__":
    results = {}

    # Run all three approaches
    results["veo"] = run_veo()
    results["kling"] = run_kling()
    results["nb2_scenes"] = run_nb2_scenes()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for k, v in results.items():
        status = "OK" if v else "FAIL"
        print(f"  {status}: {k} → {v}")
