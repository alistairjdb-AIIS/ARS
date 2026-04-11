"""
Comic v1 — Fact Lab Ep. 01 "THE 9-BRAIN OCTOPUS"
Generate the same 6-panel comic page with 3 tools: NB2, Recraft V4, Ideogram 3.0.
"""
import os, sys, json, base64, time, io
import requests

OUT = "/root/comic-v1"
os.makedirs(OUT, exist_ok=True)

# ── Credentials from env ──
NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")
IDEOGRAM_KEY = os.environ.get("IDEOGRAM_API_KEY")

for name, val in [("VEO_API_KEY", NB2_KEY), ("RECRAFT_API_KEY", RECRAFT_KEY), ("IDEOGRAM_API_KEY", IDEOGRAM_KEY)]:
    if not val:
        print(f"WARN: {name} not set")

# ── Master concept ──
CHAR_ANCHOR = (
    "Octavia: a bright coral-red octopus with large expressive black eyes, "
    "small plum-purple polka-dot pattern on her rounded head, friendly and curious, "
    "drawn in bold flat-color editorial cartoon style."
)

PALETTE = "warm cream background, limited palette of coral red, plum purple, and deep teal"

STYLE = (
    "bold modern editorial comic illustration, flat color with soft shading, "
    "2px clean black panel borders, generous whitespace, print-ready, "
    "reminiscent of The New Yorker editorial cartoons meets The Oatmeal"
)

# ── Master prompt (full, for NB2 + Recraft) ──
MASTER_PROMPT = f"""A single-page 6-panel comic book layout arranged in a 2 by 3 grid, {STYLE}, {PALETTE}.

{CHAR_ANCHOR}

Panel 1 (top-left): Bold title card. Large geometric sans-serif text at top reads "FACT LAB" in deep teal caps, small text below reads "No. 01", subtitle "9-BRAIN OCTOPUS" in smaller teal caps. Octavia peeks curiously up from the bottom edge of the panel.

Panel 2 (top-right): Octavia centered in a friendly pose, all eight arms curled playfully, large eyes looking forward with a small smile. Bold black caps caption at top reads "MEET OCTAVIA."

Panel 3 (middle-left): X-ray cutaway side view of Octavia showing one large glowing brain in her head plus eight smaller glowing brains, one at the base of each arm, connected by dotted nerve lines. Bold coral caption reads "9 BRAINS."

Panel 4 (middle-right): Three of Octavia's arms isolated, each doing a different task simultaneously — one holding a small brass key, one cradling a spiral shell, one waving hello to the reader. Bold teal caption at top reads "EACH ARM THINKS."

Panel 5 (bottom-left): A clean infographic donut chart. Two-thirds of the ring colored coral and labeled "ARMS", one-third colored teal and labeled "HEAD". Small nerve icons around it. Bold plum caption reads "2/3 OUTSIDE HEAD."

Panel 6 (bottom-right): Octavia drawn small in frame, waving one tentacle goodbye, plenty of negative space around her. Bold small teal caption at bottom reads "TOMORROW: TREES."

Visual hierarchy: titles prominent, character identity consistent across all six panels, warm and inviting tone, comic-book gutters visible, single unified page composition."""

# ── Compact Ideogram prompt (text-priority, shorter) ──
IDEOGRAM_PROMPT = """A 6-panel comic book page in a 2 by 3 grid. Bold editorial illustration, flat color, warm cream background, palette coral red plum purple deep teal. Octavia is a bright coral-red octopus with plum-purple polka-dot head and big black eyes, consistent across all panels.

Panel 1 top-left: Title card with bold geometric sans-serif text "FACT LAB" top, small "No. 01" below, subtitle "9-BRAIN OCTOPUS", Octavia peeks from bottom.

Panel 2 top-right: Octavia centered, all arms curled, friendly smile. Bold caption top "MEET OCTAVIA."

Panel 3 middle-left: X-ray side cutaway showing one large brain in head and eight small glowing brains in arms connected by dotted lines. Bold coral caption "9 BRAINS."

Panel 4 middle-right: Three arms isolated doing three tasks — holding brass key, holding spiral shell, waving. Bold teal caption top "EACH ARM THINKS."

Panel 5 bottom-left: Donut chart split 2/3 coral labeled "ARMS" and 1/3 teal labeled "HEAD". Bold plum caption "2/3 OUTSIDE HEAD."

Panel 6 bottom-right: Octavia small, waving goodbye, negative space. Bold small teal caption bottom "TOMORROW: TREES."

Clean 2px black panel borders. Style: flat editorial comic cartoon, generous whitespace."""


# ────────────────────────────────────────────────────────────
# Tool 1: Nano Banana 2 (gemini-3.1-flash-image-preview)
# ────────────────────────────────────────────────────────────
def gen_nb2():
    print("\n" + "="*60)
    print("TOOL 1: Nano Banana 2 (gemini-3.1-flash-image-preview)")
    print("="*60)
    if not NB2_KEY:
        print("SKIP — no key"); return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={NB2_KEY}"
    payload = {
        "contents": [{"parts": [{"text": MASTER_PROMPT}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "2:3"},
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=300)
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}")
            return None
        data = r.json()
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img = base64.b64decode(part["inlineData"]["data"])
                    path = os.path.join(OUT, "nb2.png")
                    with open(path, "wb") as f:
                        f.write(img)
                    print(f"  ✓ saved {path} ({len(img)//1024}KB)")
                    return path
                elif "text" in part:
                    print(f"  text: {part['text'][:200]}")
        print(f"  no image in response: {json.dumps(data)[:500]}")
        return None
    except Exception as e:
        print(f"  EXC: {e}")
        return None


# ────────────────────────────────────────────────────────────
# Tool 2: Recraft V4 (recraftv4)
# ────────────────────────────────────────────────────────────
def gen_recraft():
    print("\n" + "="*60)
    print("TOOL 2: Recraft V4 (recraftv4)")
    print("="*60)
    if not RECRAFT_KEY:
        print("SKIP — no key"); return None
    try:
        # Direct HTTP, OpenAI-compatible endpoint
        url = "https://external.api.recraft.ai/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {RECRAFT_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": MASTER_PROMPT,
            "model": "recraftv4",
            "size": "1024x1536",  # 2:3 portrait
            "n": 1,
            "response_format": "url",
        }
        r = requests.post(url, headers=headers, json=payload, timeout=180)
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}")
            # Try 1024x1024 fallback
            print("  retry with 1024x1024...")
            payload["size"] = "1024x1024"
            r = requests.post(url, headers=headers, json=payload, timeout=180)
            print(f"  HTTP {r.status_code}")
            if r.status_code != 200:
                print(f"  ERR: {r.text[:500]}")
                return None
        data = r.json()
        img_url = data["data"][0]["url"]
        img_bytes = requests.get(img_url, timeout=60).content
        path = os.path.join(OUT, "recraft.png")
        with open(path, "wb") as f:
            f.write(img_bytes)
        print(f"  ✓ saved {path} ({len(img_bytes)//1024}KB) from {img_url[:60]}...")
        return path
    except Exception as e:
        print(f"  EXC: {e}")
        return None


# ────────────────────────────────────────────────────────────
# Tool 3: Ideogram 3.0
# ────────────────────────────────────────────────────────────
def gen_ideogram():
    print("\n" + "="*60)
    print("TOOL 3: Ideogram 3.0")
    print("="*60)
    if not IDEOGRAM_KEY:
        print("SKIP — no key"); return None
    try:
        url = "https://api.ideogram.ai/v1/ideogram-v3/generate"
        headers = {"Api-Key": IDEOGRAM_KEY}
        # multipart/form-data with fields
        files = {
            "prompt": (None, IDEOGRAM_PROMPT),
            "aspect_ratio": (None, "2x3"),
            "rendering_speed": (None, "QUALITY"),
            "style_type": (None, "DESIGN"),
            "magic_prompt": (None, "OFF"),
            "num_images": (None, "4"),
            "negative_prompt": (None, "blurry text, misspelled words, illegible, low quality, distorted letters"),
        }
        r = requests.post(url, headers=headers, files=files, timeout=300)
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:600]}")
            return None
        data = r.json()
        # Save all 4 for text-accuracy selection
        paths = []
        for i, item in enumerate(data.get("data", [])):
            img_url = item.get("url")
            if not img_url:
                continue
            img_bytes = requests.get(img_url, timeout=60).content
            path = os.path.join(OUT, f"ideogram_v{i+1}.png")
            with open(path, "wb") as f:
                f.write(img_bytes)
            print(f"  ✓ variant {i+1} saved {path} ({len(img_bytes)//1024}KB)")
            paths.append(path)
        return paths
    except Exception as e:
        print(f"  EXC: {e}")
        return None


if __name__ == "__main__":
    results = {}
    results["nb2"] = gen_nb2()
    results["recraft"] = gen_recraft()
    results["ideogram"] = gen_ideogram()
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for k, v in results.items():
        print(f"  {k}: {v}")
