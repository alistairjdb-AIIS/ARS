"""
Comic v5 — THE CASCADE continued: format iteration round 2.
Same subject (AI solves coding → 4-order cascade), new formal devices.

6 variations exploring different ways to encode the cascade:

V5A — TIMELINE STRIP: horizontal left-to-right timeline, each era gets shorter
      but the disruption gets bigger. Time compression as magnitude device.
V5B — ICEBERG: above water = "AI writes code" (what everyone sees).
      Below water = the 3 deeper orders, each one a larger underwater layer.
V5C — MATRYOSHKA: nesting dolls where the OUTER doll is tiny "CODE" and
      each inner doll is progressively BIGGER (physics-breaking, surreal).
      The smallest shell contains the biggest consequence.
V5D — CEMETERY: headstones for things killed by each order. Row 1 (near): small
      stones for "junior dev jobs." Row 4 (far): massive mausoleum for
      "the labor market as we knew it." Forced perspective.
V5E — WEATHER MAP: mock TV weather forecast, but the "storm" is the cascade.
      Small rain cloud for order 1, category-5 hurricane for order 4.
      Everyone watching the rain cloud on the left of the map.
V5F — FRAME-BREAK: a 4-panel comic where each panel is bigger than the last,
      and panel 4 literally breaks out of the comic border, cracking the page.
      The content exceeding the form IS the point.
"""
import os, json, base64, requests

OUT = "/root/comic-v5"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")


# ═══════════════════════════════════════════════════════════════
# V5A — TIMELINE STRIP
# Device: time compression. Each era is shorter but the event is bigger.
# ═══════════════════════════════════════════════════════════════
TIMELINE_PROMPT = """A wide editorial illustration showing a horizontal timeline from left to right, drawn in the style of a scientific infographic crossed with a political cartoon.

The timeline spans the full width of the image. It is divided into four UNEQUAL sections, each dramatically shorter than the last but containing a taller, more dramatic event:

SECTION 1 (leftmost, takes up 40% of the width, tall event ~15% of height): A long, calm period labeled "2020-2025" at the bottom. Above the timeline, a modest office scene: developers at desks writing code on screens. Small, calm, routine. A gentle upward trend line.

SECTION 2 (next, takes up 25% of width, event ~30% of height): Labeled "2025-2026." Above: office buildings with "FOR LEASE" signs, a graph showing software costs plummeting. Medium disruption. Some people looking concerned.

SECTION 3 (next, takes up 20% of width, event ~50% of height): Labeled "2026-2027." Above: corporate castle walls crumbling, a wrecking ball labeled "FREE CODE" smashing through. Large disruption. Executives running.

SECTION 4 (rightmost, takes up only 15% of width but event extends to 100% of height): Labeled "2027-?" Above: an ENORMOUS tidal wave of servers and data centers crashing over a cityscape, tiny human figures scattered. The wave extends beyond the top of the frame. The disruption is so large it cannot be contained in the timeline format.

Below the timeline, a small caption reads: "Time to impact is shrinking. Scale of impact is not."

Color palette: clean white background, crisp linework, limited color — each section gets progressively more saturated (section 1 in light grey, section 2 in muted blue, section 3 in amber, section 4 in deep red). The color intensification mirrors the escalation. Editorial infographic style with personality — not cold data visualization but illustrated data storytelling."""


# ═══════════════════════════════════════════════════════════════
# V5B — ICEBERG
# Device: visible tip vs massive hidden structure below.
# What everyone discusses is the smallest part.
# ═══════════════════════════════════════════════════════════════
ICEBERG_PROMPT = """An editorial illustration of an iceberg floating in dark ocean water, viewed from the side in cross-section. The waterline divides the image horizontally at approximately the upper quarter.

ABOVE THE WATERLINE (small, visible, brightly lit):
A tiny tip of ice poking above calm blue water. On this small exposed surface, a cluster of miniature figures — journalists, tech executives, politicians — stand around a small glowing laptop. Above them, speech bubbles and headlines float: "AI WRITES CODE!" and "THE FUTURE IS HERE!" Bright sunshine, optimistic colors. This is what everyone can see and is talking about.

BELOW THE WATERLINE (massive, hidden, dark):
The iceberg expands dramatically downward in three distinct geological layers, each wider and deeper than the one above:

Layer 1 (just below surface, medium): Carved into the ice in rough text: "SOFTWARE COSTS → ZERO." Illustrations frozen into the ice: empty office floors, terminated contracts, "FOR LEASE" signs embedded like fossils.

Layer 2 (deeper, wider): Carved text: "COMPANY MOATS DISSOLVE." Frozen illustrations: crumbling corporate logos, shattered castle walls, boardroom tables cracking apart — all embedded in blue-white ice.

Layer 3 (deepest, widest, extending to the very bottom of the frame): Carved text: "LABOR MARKET INVERTS." Frozen at the base of the iceberg: an entire city in miniature, office towers and highways and suburbs, all encased in ice, with streams of tiny human figures frozen mid-walk carrying boxes. This bottom layer is wider than the entire visible portion above water.

A single tiny submarine or deep-sea diver floats at the bottom of the frame, shining a small flashlight beam at the lowest layer — the only observer who has gone deep enough to see it.

Style: cross-section illustration with precise geological layering, muted deep ocean blues and teals below water, warm sunlight above. The contrast between the cheerful tiny tip and the ominous massive base IS the editorial. Clean linework, intelligent negative space in the water surrounding the iceberg."""


# ═══════════════════════════════════════════════════════════════
# V5C — MATRYOSHKA (surreal/paradoxical)
# Device: the smallest shell contains the biggest consequence.
# Inverts the nesting-doll logic.
# ═══════════════════════════════════════════════════════════════
MATRYOSHKA_PROMPT = """A surrealist editorial illustration of four Russian nesting dolls (matryoshka) arranged in a row from left to right, but with an impossible paradox: the OUTER shells are small and the INNER contents are enormous.

DOLL 1 (leftmost, small, about 15% of frame height): A tiny, cheerful matryoshka doll painted with a simple laptop icon and labeled "CODE" on its belly. It is cracked open, revealing...

DOLL 2 (emerging from doll 1, but 2x its size — impossibly larger than the shell it came from): A medium matryoshka painted with dollar signs crumbling into dust, labeled "COST." The physically-impossible size relationship is the point. It is cracked open, revealing...

DOLL 3 (emerging from doll 2, but 3x the size of doll 1 — even more impossible): A large matryoshka painted with a crumbling castle/fortress, labeled "MOATS." Cracked open, revealing...

DOLL 4 (emerging from doll 3, ENORMOUS, taking up 60% of the frame): A massive matryoshka painted with a cityscape of people walking away from offices toward data centers, labeled "LABOR." This innermost doll dwarfs all three shells that supposedly contained it.

The visual paradox — small containers holding progressively larger contents — is rendered matter-of-factly, as if this is simply how these dolls work. No explanation. The impossibility IS the commentary: the thing everyone thought was small (AI writes code) contained something they couldn't have fit in their mental model.

A single small figure stands at the far left, looking at doll 1 with a magnifying glass, completely unaware of dolls 2-4 towering behind them.

Style: clean editorial illustration, cream/warm paper background, the dolls painted in traditional Russian folk-art patterns but with modern illustrations on each. Limited palette: warm red and gold for the doll patterns, cool blue-grey for the illustrations on each doll. Confident linework, surrealist composition treated with illustrative realism."""


# ═══════════════════════════════════════════════════════════════
# V5D — CEMETERY (memento mori)
# Device: forced perspective graveyard. What dies at each order.
# ═══════════════════════════════════════════════════════════════
CEMETERY_PROMPT = """An editorial cartoon showing a hillside cemetery viewed in forced perspective from the bottom of the hill looking up. Four rows of graves ascend the hill, each row containing larger and more elaborate monuments than the last.

ROW 1 (foreground, bottom of hill, small headstones): Simple flat headstones for specific, small casualties. Readable inscriptions: "Junior Dev Jobs," "Stack Overflow," "Coding Bootcamps," "Freelance Rates." Small, unremarkable. Fresh flowers on a few. A handful of mourners in casual clothes.

ROW 2 (middle-near, larger stones): Upright headstones and small obelisks. Inscriptions: "SaaS Margins," "The $500/Hour Contractor," "Software as Expensive." The stones are weathered — these deaths happened quietly, before anyone noticed. A few suited executives placing flowers.

ROW 3 (middle-far, large monuments): Grand marble monuments with carved angels and columns. Inscriptions: "The Engineering Moat," "Competitive Advantage via Code Quality," "The CTO as Kingmaker." Impressive tombs for impressive concepts. Corporate wreaths. Board members in dark coats.

ROW 4 (top of hill, ENORMOUS mausoleum): A single massive neoclassical mausoleum with pillars and a domed roof, dominating the hilltop skyline. Carved above its entrance in large serif letters: "THE KNOWLEDGE WORKER ECONOMY." No mourners at this grave — it's too far up the hill for anyone to have reached it yet. The path leading to it is empty. Dark storm clouds gather behind it.

The forced perspective means the enormous mausoleum at the top looks appropriately large despite being "farther away" — the eye reads it as truly monumental.

A groundskeeper with a shovel stands in the foreground between rows 1 and 2, looking at his clipboard, checking off names. He hasn't looked up the hill yet.

Style: pen-and-ink editorial cartoon with watercolor wash, muted palette of grey-green grass, grey stone, cream sky. Atmospheric perspective (hazier toward the top). The tone is darkly comic, not morbid — the specificity of the inscriptions provides the dark humor. Clean readable text on every headstone."""


# ═══════════════════════════════════════════════════════════════
# V5E — WEATHER MAP
# Device: familiar TV weather format recontextualized.
# ═══════════════════════════════════════════════════════════════
WEATHER_MAP_PROMPT = """A mock television weather forecast screen, designed to look exactly like a real TV weather broadcast graphic but with the "weather" being the AI disruption cascade.

At the top of the screen, a news channel chyron reads: "TECH FORECAST — DISRUPTION ADVISORY IN EFFECT"

The main image is a stylized map of a landscape (not a real geography — an abstract "industry map") showing four weather systems moving from left to right:

SYSTEM 1 (far left): A small rain cloud icon with light drizzle. Label: "CODE AUTOMATION — Light showers. Minor disruptions to entry-level positions. No action required."

SYSTEM 2 (center-left): A moderate thunderstorm icon with lightning. Label: "COST COLLAPSE — Thunderstorm warning. Software pricing models under pressure. Some companies advised to seek shelter."

SYSTEM 3 (center-right): A large red storm system with rotation. Label: "MOAT EROSION — Severe storm watch. Corporate competitive advantages at risk of structural failure. Evacuations recommended."

SYSTEM 4 (far right, ENORMOUS): A massive Category 5 hurricane spiral consuming the entire right side of the map, rendered in deep red and purple radar colors. Label: "LABOR MARKET INVERSION — CATASTROPHIC. All models exceed historical parameters. No precedent. Seek higher ground."

At the bottom of the screen, a scrolling ticker reads: "ADVISORY: Most analysts tracking System 1. Systems 3-4 not yet in mainstream forecast models."

A cartoon weather presenter stands at the left edge of the screen, pointing at System 1 with a cheerful smile, their back turned to the massive hurricane on the right.

Style: pixel-perfect recreation of a TV weather broadcast aesthetic — radar color gradients, sans-serif labels, chyron graphics, the blue-screen-map look. The humor comes from the deadpan application of weather-forecast visual language to economic disruption. Clean, broadcast-quality graphic design."""


# ═══════════════════════════════════════════════════════════════
# V5F — FRAME-BREAK (meta-formal)
# Device: panel 4 literally breaks out of the comic format.
# The content exceeding the form IS the meaning.
# ═══════════════════════════════════════════════════════════════
FRAMEBREAK_PROMPT = """A four-panel comic strip arranged in a 2x2 grid, where each panel is progressively larger and panel 4 breaks the format entirely.

PANEL 1 (top-left, small, contained neatly within its border): A simple office scene. A programmer at a desk. A laptop screen shows "AI: I can write your code now." The programmer shrugs. Small panel, small event, neat black border. Caption below: "Order 1: AI writes code."

PANEL 2 (top-right, slightly larger — its border bulges outward, pushing into panel 1's space): An office building with a "COSTS: $0" sign. Workers looking confused as their desks disappear. The panel border is stressed — hairline cracks visible in the black frame lines. Caption: "Order 2: Software becomes free."

PANEL 3 (bottom-left, noticeably larger — border warping, pushing panels 1 and 2 smaller): Corporate castle walls crumbling, executives scrambling, company logos falling. The panel border is buckling outward, cracking at the corners, pushing into neighboring panels' territory. Caption: "Order 3: Moats dissolve."

PANEL 4 (bottom-right, ENORMOUS — has completely shattered its border and is spilling across the entire page): A massive tidal wave of servers, data centers, and algorithmic patterns crashing over a cityscape. Tiny human figures scattered. The panel's content has BROKEN THROUGH the comic border — jagged cracks radiate outward from the frame, the illustration bleeds into the white margin, pieces of the broken border float like debris. The neat 2x2 grid is destroyed. Panel 4's content is literally too large for the format that was supposed to contain it. Caption (cracked, tilted, partially obscured): "Order 4: Everything changes."

At the very bottom of the page, outside all panels, tiny text reads: "The framework you used to understand panels 1-3 cannot contain panel 4."

Style: black-and-white ink comic with clean linework for panels 1-3, increasingly chaotic and detailed rendering as the panels progress. Panel 1 is simple ligne claire. Panel 4 is dense, dramatic, almost overwhelming. The meta-commentary is structural — the comic format itself fails under the weight of what it's trying to depict. This is the visual equivalent of 'the old categories are failing to contain what's actually happening.'"""


def gen_nb2(prompt, filename, aspect):
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


def gen_recraft(prompt, filename, size):
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

    # Each format on the tool best suited to it
    results["timeline_recraft"] = gen_recraft(TIMELINE_PROMPT, "cascade_timeline_recraft.png", "1344x768")
    results["iceberg_nb2"] = gen_nb2(ICEBERG_PROMPT, "cascade_iceberg_nb2.png", "9:16")
    results["matryoshka_recraft"] = gen_recraft(MATRYOSHKA_PROMPT, "cascade_matryoshka_recraft.png", "1344x768")
    results["cemetery_nb2"] = gen_nb2(CEMETERY_PROMPT, "cascade_cemetery_nb2.png", "4:5")
    results["weather_recraft"] = gen_recraft(WEATHER_MAP_PROMPT, "cascade_weather_recraft.png", "1344x768")
    results["framebreak_nb2"] = gen_nb2(FRAMEBREAK_PROMPT, "cascade_framebreak_nb2.png", "1:1")

    # Cross-tool: best concepts on opposite tool
    results["iceberg_recraft"] = gen_recraft(ICEBERG_PROMPT, "cascade_iceberg_recraft.png", "768x1344")
    results["framebreak_recraft"] = gen_recraft(FRAMEBREAK_PROMPT, "cascade_framebreak_recraft.png", "1024x1024")
    results["cemetery_recraft"] = gen_recraft(CEMETERY_PROMPT, "cascade_cemetery_recraft.png", "768x1344")
    results["weather_nb2"] = gen_nb2(WEATHER_MAP_PROMPT, "cascade_weather_nb2.png", "16:9")

    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        status = "OK" if v else "FAIL"
        print(f"  {status}: {k}")
