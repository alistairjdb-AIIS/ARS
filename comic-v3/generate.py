"""
Comic v3 — Anthropic mythos, MAGNITUDE SEMANTICS
3 mockups. Each encodes the WEIGHT of the announcement through a distinct formal device.
Subject: Oracle speaks "SAFETY," pilgrims hear opportunity.

V3A — MONOLITH (scale disparity + sublime, NB2 9:16)
V3B — TYPOGRAPHIC SHOUT (headline-as-image, Recraft V4 1:1)
V3C — NEWSPAPER EXTRA (front-page form = shorthand for major news, NB2 4:5)
"""
import os, json, base64, requests

OUT = "/root/comic-v3"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")


# ═══════════════════════════════════════════════════════════════
# V3A — MONOLITH (scale disparity, architectural sublime)
# Magnitude device: tiny human vs enormous object
# Dark, desaturated, low angle, vertical. Amygdala-level weight.
# ═══════════════════════════════════════════════════════════════
MONOLITH_PROMPT = """A single cinematic wide shot in the visual tradition of 2001: A Space Odyssey and Caspar David Friedrich's "Wanderer Above the Sea of Fog." A colossal, impossibly tall matte-black obsidian monolith rises from a mountaintop above San Francisco, stretching far beyond the top of the frame into a brooding grey storm sky. The word "CLAUDE" is carved vertically into the monolith in severe sans-serif engraved letters, each letter ten meters tall, glowing with a faint cold blue inner light.

At the base of the monolith, dwarfed to the size of an ant, stands a single robed figure with arms raised — the Oracle — rendered so small that the viewer must search to find him. Four even tinier pilgrim figures kneel on the stone steps below him, barely visible.

The scale ratio between the monolith and the human figure is approximately 500:1. Heavy atmospheric perspective. Desaturated palette dominated by cold slate, graphite, and bruised blue-grey. A sliver of cold dawn light catches the monolith's edge. Below the cliff, the miniature San Francisco skyline is visible — skyscrapers rendered smaller than the monolith's base.

At the very bottom of the frame, in heavy bold condensed slab serif capitals, one word in white: "SAFETY." No other text. No speech bubbles. No explanatory caption.

Compositional rules: extreme low-angle perspective looking up the monolith, implied loom toward the viewer, the human figures positioned at the lower third intersection for scale reference, generous negative space filled with storm sky. Shot on a cinematic wide lens, volumetric mist, high dynamic range, stark contrast. Semantic weight: the viewer should feel the magnitude before reading the word."""


# ═══════════════════════════════════════════════════════════════
# V3B — TYPOGRAPHIC SHOUT (word-as-image)
# Magnitude device: single word dominates 90% of frame; nested icons tell the rest
# ═══════════════════════════════════════════════════════════════
SHOUT_PROMPT = """An editorial graphic design composition. The entire image is dominated by ONE enormous word: "SAFETY" rendered in massive bold heavy-weight condensed slab serif capitals, filling approximately 85% of the frame. The letters are carved in deep obsidian black on a warm cream newsprint background, as if chiseled from stone.

Inside each letterform, tiny intricate illustrations are nested, each visually hidden within the negative space of that letter:
- Inside the "S": a small rocket taking off with dollar-sign exhaust
- Inside the "A": a tiny gavel and a senate bench with a worried senator
- Inside the "F": a laptop with a vertically-rising GitHub contribution graph
- Inside the "E": a journalist's recorder with a viral headline flying out
- Inside the "T": a small mushroom cloud and a skull (existential worry)
- Inside the "Y": a question mark made of circuit-board traces

Above the word, a small caption in thin tracked-out uppercase reads: "THE ORACLE SPOKE ONE WORD." Below the word, a small caption in italic lowercase reads: "here is what each pilgrim heard."

At the very bottom-right corner, tiny credit line: "— THE ANTHROPIC MYTHOS, VOL. I"

Design rules: Swiss editorial design discipline, massive typographic dominance, generous margin around the word, the hidden illustrations are subtle enough that they reward close looking but obvious enough to read within 2 seconds. Limited palette: obsidian black type, cream paper background, single accent color of ember orange on the rocket + laptop graph + headline. The composition enforces magnitude through typographic scale alone — the word is the subject, not a label."""


# ═══════════════════════════════════════════════════════════════
# V3C — NEWSPAPER EXTRA EDITION
# Magnitude device: front-page layout = universal "this is major news"
# ═══════════════════════════════════════════════════════════════
NEWSPAPER_PROMPT = """A mock front page of an evening extra-edition newspaper in the classic broadsheet tradition. At the top, an ornate masthead reads "THE SILICON CHRONICLE" in heavy blackletter serif, with "EXTRA EDITION" in red banner caps above it and the date "APRIL 11, 2026" + "SAN FRANCISCO" in small caps below.

The entire page is dominated by a single massive three-line headline in enormous bold condensed serif display type, stacked in a dramatic hierarchy:

Line 1: "ORACLE"
Line 2: "SPEAKS ONE"
Line 3: "WORD."

Each line takes up roughly 18% of the page height. Below the headline, a smaller subheading reads: "SILICON VALLEY REACTS — SEE FOUR INTERPRETATIONS BELOW."

Below the subheading, the central hero image: a grainy black-and-white newsprint-style photo of a tiny robed figure atop a mountaintop, arms raised in silhouette against a bright sky, a huge obelisk behind him labeled "CLAUDE". The photo has newsprint halftone dot texture.

Beneath the photo, a 4-column grid of tiny boxed reaction quotes, each with a small pen-and-ink portrait of a single pilgrim and a one-line quote in italics:
- Column 1: A senator. Quote: "We must regulate this immediately."
- Column 2: A venture capitalist in a vest. Quote: "I'm wiring two billion tomorrow."
- Column 3: A journalist with glasses. Quote: "The headline writes itself."
- Column 4: A hooded developer with a laptop. Quote: "I'm forking the repo tonight."

At the bottom, a thin slug line in small italic caps: "THE ORACLE SPEAKS OF SAFETY. THE PILGRIMS HEAR OPPORTUNITY."

Classical newspaper design rules: ink-on-newsprint texture, slightly yellowed paper, column rules, drop caps, tombstone-free hierarchy, traditional broadsheet grid. The FORM of the newspaper front page itself communicates that this is a story of enormous cultural significance — the viewer recognizes "extra edition broadsheet layout" as a century-old shorthand for "an event so important the paper stopped the presses."""


def gen_nb2(prompt: str, filename: str, aspect: str):
    print(f"\n{'='*60}\nNB2 → {filename} (aspect={aspect})\n{'='*60}")
    if not NB2_KEY:
        print("  SKIP — no key"); return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={NB2_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect},
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
                    path = os.path.join(OUT, filename)
                    with open(path, "wb") as f:
                        f.write(img)
                    print(f"  ✓ saved {path} ({len(img)//1024}KB)")
                    return path
                elif "text" in part:
                    print(f"  text: {part['text'][:200]}")
        print(f"  no image: {json.dumps(data)[:400]}")
        return None
    except Exception as e:
        print(f"  EXC: {e}")
        return None


def gen_recraft(prompt: str, filename: str, size: str):
    print(f"\n{'='*60}\nRECRAFT V4 → {filename} (size={size})\n{'='*60}")
    if not RECRAFT_KEY:
        print("  SKIP — no key"); return None
    url = "https://external.api.recraft.ai/v1/images/generations"
    headers = {"Authorization": f"Bearer {RECRAFT_KEY}", "Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "model": "recraftv4",
        "size": size,
        "n": 1,
        "response_format": "url",
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=180)
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  ERR: {r.text[:500]}")
            return None
        data = r.json()
        img_url = data["data"][0]["url"]
        img = requests.get(img_url, timeout=60).content
        path = os.path.join(OUT, filename)
        with open(path, "wb") as f:
            f.write(img)
        print(f"  ✓ saved {path} ({len(img)//1024}KB)")
        return path
    except Exception as e:
        print(f"  EXC: {e}")
        return None


if __name__ == "__main__":
    results = {}
    results["monolith_nb2"] = gen_nb2(MONOLITH_PROMPT, "oracle_monolith_nb2.png", "9:16")
    results["shout_recraft"] = gen_recraft(SHOUT_PROMPT, "oracle_shout_recraft.png", "1024x1024")
    results["newspaper_nb2"] = gen_nb2(NEWSPAPER_PROMPT, "oracle_newspaper_nb2.png", "4:5")
    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        print(f"  {k}: {v}")
