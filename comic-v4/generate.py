"""
Comic v4 — THE CASCADE
Subject: AI solves coding → consequences cascade through 4 orders of magnitude.
Each order is bigger than the last. Most people are still looking at order 1.

3 formats:
  A — Newspaper front page (NB2 4:5) — inverted hierarchy, bottom story is biggest
  B — Domino strip (Recraft 1344x768) — 4 dominoes escalating, crowd looks backward
  C — Reaction split (NB2 1:1) — Spielberg principle: faces > spectacle

Wiki applied: C30 (Pixar "because of that" chain, Spielberg reaction, Parker/Stone
but/therefore, Hemingway restraint), C29 (pre-attentive processing, magnitude).
"""
import os, json, base64, requests

OUT = "/root/comic-v4"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")


# ═══════════════════════════════════════════════════════════════
# FORMAT A — NEWSPAPER FRONT PAGE (inverted hierarchy)
# Device: newspaper form = "this is major news" (proven in v3c).
# Twist: stories get BIGGER as you go down the page — the reader
# expects the top story to be the biggest, but the bottom one
# dwarfs everything above it. The form subverts itself.
# ═══════════════════════════════════════════════════════════════
NEWSPAPER_PROMPT = """A mock front page of a broadsheet newspaper. Ornate blackletter masthead reads "THE CASCADE TIMES" with "SPECIAL EDITION" in a red banner above and "APRIL 2026 — SAN FRANCISCO" in small caps below.

The page has FOUR stories stacked vertically, each one physically LARGER than the one above it, inverting normal newspaper hierarchy:

STORY 1 (top, smallest — takes up about 10% of page height): A tiny headline in modest type reads: "AI SYSTEM WRITES PRODUCTION CODE." Beneath it, a small paragraph of body text and a thumbnail image of a laptop screen with code on it. Calm, routine-looking. The way a paper reports a product launch.

STORY 2 (below, larger — about 20% of page height): A bigger headline reads: "SOFTWARE COSTS COLLAPSE TO NEAR ZERO." A medium-sized illustration shows an office building with a "FOR LEASE" sign. Wider columns, more alarming tone. A pull-quote reads: "The $500-per-hour contractor is now a $5 API call."

STORY 3 (below, larger still — about 25% of page height): A bold headline reads: "TECH GIANTS' MOATS CRUMBLE." A large illustration shows castle walls made of code dissolving into sand. Corporate logos (generic, not real) scattered in the rubble. Urgent editorial tone.

STORY 4 (bottom, ENORMOUS — takes up about 35% of page height): Massive headline in heavy condensed serif fills the width: "LABOR MARKET INVERTS." A dominant illustration shows a vast data center humming with light on the left, and on the right, a long line of people in business attire walking away from an office building carrying boxes. The scale of the illustration dwarfs everything above it.

Below story 4, a thin editorial slug line in italic reads: "See page 1 for the story everyone is discussing. See page 4 for the one that matters."

Design rules: classic broadsheet newspaper layout, ink-on-newsprint texture, yellowed paper, column rules, halftone dot texture on illustrations. The PHYSICAL SIZE of each story section on the page IS the message — the reader's eye naturally starts at the top (the small story everyone talks about) and arrives at the bottom (the massive story nobody's ready for). The form teaches the content."""


# ═══════════════════════════════════════════════════════════════
# FORMAT B — DOMINO STRIP (visual escalation)
# Device: 4 dominoes, each one dramatically larger than the last.
# A crowd of tiny people clusters around the first tiny domino
# with binoculars and cameras — while the fourth domino looms
# over a city skyline behind them.
# Passes Mamet silent-movie test: no text needed to get it.
# ═══════════════════════════════════════════════════════════════
DOMINO_PROMPT = """A wide-format editorial illustration. A single continuous landscape scene, viewed from the side like a cross-section diorama.

On the far left: a tiny white domino, about the height of a person, labeled "CODE" in small sans-serif. It has just been tipped over by an invisible finger and is falling to the right.

Next to it, slightly right: a second domino, three times taller (the height of a house), labeled "COST", already wobbling from the impact of the first.

Further right: a third domino, ten times taller than the first (the height of a skyscraper), labeled "MOATS", beginning to crack at its base as the second domino strikes it.

On the far right: a fourth domino so enormous it extends beyond the top of the frame, labeled "LABOR" in giant letters. It is perfectly still — it hasn't been hit yet. Behind it, visible through the gap between the third and fourth dominoes, a tiny city skyline sits in its shadow. The fourth domino, when it falls, will crush the city.

The key detail: a dense crowd of tiny people — journalists with cameras, executives in suits, politicians at podiums — are ALL clustered around the FIRST tiny domino on the far left, pointing at it, photographing it, arguing about it. They have their backs turned to the enormous fourth domino. Not a single person is looking right.

One lone figure, very small, stands in the middle of the scene between the second and third dominoes, facing right, looking up at the fourth domino. This figure is drawn with a simple, underdressed quality — no suit, no camera, just a person.

Color palette: muted newsprint tones — warm cream background, dominoes in stark black and white, city skyline in soft grey. The crowd is rendered in warm sepia tones. The lone figure is a single spot of desaturated blue.

The composition reads left to right like a sentence. No speech bubbles. No caption. The image is the argument. Editorial illustration style, clean confident linework, intelligent use of negative space between the dominoes to show escalating gaps."""


# ═══════════════════════════════════════════════════════════════
# FORMAT C — REACTION SPLIT (Spielberg principle)
# Device: "The reaction to the spectacle is more powerful than
# the spectacle itself." Two halves of the same boardroom.
# Left half: executives smiling at a laptop. Right half:
# the same room, but through the window, a tidal wave.
# The people facing the window are frozen.
# ═══════════════════════════════════════════════════════════════
REACTION_PROMPT = """An editorial cartoon of a corporate boardroom viewed from above at a slight angle, split into two emotional halves by a vertical compositional divide.

LEFT HALF of the room: Four executives in suits lean forward around a laptop on the conference table. The laptop screen shows a simple line of text: "AI WRITES CODE." Their faces are lit by the screen glow — they are BEAMING. One is pumping his fist. One is already on the phone. One is scribbling a number with many zeros on a napkin. Their body language radiates excitement, opportunity, money. Warm golden lighting from the laptop glow fills this half.

RIGHT HALF of the same room: The same boardroom table continues, but the chairs on this side face a floor-to-ceiling window. Through the window, the view reveals what's coming — a sequence of four events visible in the cityscape beyond:
- In the near distance, office buildings with "FOR LEASE" signs appearing on every floor
- In the middle distance, corporate headquarters with crumbling walls
- In the far distance, a massive dark data center complex glowing with blue light, dwarfing everything
- In the extreme distance, a long line of tiny human figures walking away from the city toward the horizon, carrying boxes

Two executives on this side of the table have turned their chairs to face the window. Their faces are ashen, frozen, mouths slightly open. One has her coffee cup stopped halfway to her lips, forgotten. The other has his glasses pushed up on his forehead, staring. Cold blue-grey light from the window fills this half.

The emotional contrast between the two halves IS the entire editorial: same room, same news, different time horizons. The left side sees order 1. The right side sees order 4.

Style: clean editorial illustration, slightly caricatured proportions (large heads, expressive faces), limited palette of warm gold (left) transitioning to cold slate blue (right). No text labels, no speech bubbles, no caption — the image must work as a silent editorial. The only text in the entire image is "AI WRITES CODE" on the laptop screen."""


def gen_nb2(prompt: str, filename: str, aspect: str):
    print(f"\n{'='*60}\nNB2 -> {filename} (aspect={aspect})\n{'='*60}")
    if not NB2_KEY:
        print("  SKIP -- no key"); return None
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
                    print(f"  saved {path} ({len(img)//1024}KB)")
                    return path
                elif "text" in part:
                    print(f"  text: {part['text'][:200]}")
        print(f"  no image: {json.dumps(data)[:400]}")
        return None
    except Exception as e:
        print(f"  EXC: {e}")
        return None


def gen_recraft(prompt: str, filename: str, size: str):
    print(f"\n{'='*60}\nRECRAFT V4 -> {filename} (size={size})\n{'='*60}")
    if not RECRAFT_KEY:
        print("  SKIP -- no key"); return None
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
        print(f"  saved {path} ({len(img)//1024}KB)")
        return path
    except Exception as e:
        print(f"  EXC: {e}")
        return None


if __name__ == "__main__":
    results = {}
    results["newspaper_nb2"] = gen_nb2(NEWSPAPER_PROMPT, "cascade_newspaper_nb2.png", "4:5")
    results["domino_recraft"] = gen_recraft(DOMINO_PROMPT, "cascade_domino_recraft.png", "1344x768")
    results["reaction_nb2"] = gen_nb2(REACTION_PROMPT, "cascade_reaction_nb2.png", "1:1")

    # Second pass: swap tools for comparison
    results["domino_nb2"] = gen_nb2(DOMINO_PROMPT, "cascade_domino_nb2.png", "16:9")
    results["newspaper_recraft"] = gen_recraft(NEWSPAPER_PROMPT, "cascade_newspaper_recraft.png", "768x1344")
    results["reaction_recraft"] = gen_recraft(REACTION_PROMPT, "cascade_reaction_recraft.png", "1024x1024")

    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        print(f"  {k}: {v}")
