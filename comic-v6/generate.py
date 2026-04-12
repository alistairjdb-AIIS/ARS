"""
Comic v6 — LIVE HEADLINES, second-order consequences made visual.
3 subjects from today's news (April 12, 2026), each pushed past the hedging point.
Best format per subject, NB2 primary (operator preference this session).

Subject 1: Strait of Hormuz ceasefire — "The Trap"
Subject 2: Hottest March + El Nino — "The Stack"
Subject 3: Emperor Penguin endangered — "The Canary"
"""
import os, json, base64, requests

OUT = "/root/comic-v6"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")


# ═══════════════════════════════════════════════════════════════
# STRAIT OF HORMUZ — WEATHER MAP FORMAT
# "The Trap": the ceasefire reopening is more dangerous than the closure.
# ═══════════════════════════════════════════════════════════════
STRAIT_WEATHER = """A mock television weather forecast screen. At the top, a news chyron reads: "STRAIT FORECAST — GEOPOLITICAL ADVISORY IN EFFECT"

The main display shows a stylized map of the Persian Gulf region with the Strait of Hormuz prominently visible as a narrow chokepoint. Four weather systems are overlaid:

SYSTEM 1 (over the Strait, small sun icon breaking through clouds): "CEASEFIRE — Temporary clearing. Strait reopens. Oil prices ease. 2-week window." Bright yellow, optimistic icon. Small text: "ALL CLEAR."

SYSTEM 2 (over shipping lanes, moderate wind arrows): "RE-ROUTING — Moderate. Vessels returning to Strait from Cape of Good Hope routes. Cost savings drive traffic back through the bottleneck." Orange arrows showing ships converging on the narrow passage.

SYSTEM 3 (building storm over the Strait, red): "TRAP FORMATION — Severe. When ceasefire expires, every vessel inside the Strait is exposed. Companies that re-routed back are caught. Those who stayed on long routes are safe." Dark red storm cell forming directly over the chokepoint, with ship icons caught inside.

SYSTEM 4 (massive permanent weather system covering the entire Gulf, deep purple): "PERMANENT WEAPONIZATION — UNPRECEDENTED. The Strait is now a weapon even when open. Maritime insurance permanently reprices. Every Strait-dependent economy lives under perpetual closure risk. The option to close is demonstrated. Geography is now geopolitics." Enormous dark purple system covering the entire map, no clear edges.

A cartoon weather presenter in a suit stands at the left, pointing cheerfully at System 1 (the sun). Behind her back, System 4 covers the entire right side of the screen.

Bottom ticker: "ADVISORY: Markets pricing System 1. Systems 3-4 not in any shipping company's forecast model."

Style: pixel-perfect TV weather broadcast aesthetic, radar gradients, sans-serif labels, chyron graphics, broadcast-blue background. Deadpan application of weather format to geopolitical risk."""


# ═══════════════════════════════════════════════════════════════
# STRAIT OF HORMUZ — ICEBERG FORMAT
# Above water: the ceasefire. Below: what it actually means.
# ═══════════════════════════════════════════════════════════════
STRAIT_ICEBERG = """An editorial illustration of an iceberg in dark ocean water, cross-section view. The waterline divides the image at the upper quarter.

ABOVE THE WATERLINE (small, bright, optimistic):
A tiny tip of ice shaped like a white dove. On it, miniature figures shake hands — diplomats in suits. Small flags (US, Iran). A headline floats above: "CEASEFIRE! STRAIT REOPENS!" Bright sunshine, blue sky. Oil barrel icons with downward arrows. Celebration.

BELOW THE WATERLINE (massive, dark, escalating):

Layer 1 (just below surface): Text carved in ice: "SHIPS RETURN TO THE STRAIT." Illustrations frozen in ice: cargo vessels and oil tankers turning back from the long Cape of Good Hope route, funneling into a narrow passage. The passage narrows ominously.

Layer 2 (deeper, wider): Text: "THE 2-WEEK TRAP." The narrow passage from Layer 1 is now a bottleneck filled with ship icons, and the ice around them is cracking — fissures spreading. A countdown clock frozen in the ice reads "14 DAYS." Ships that re-entered cannot turn around in time.

Layer 3 (deepest, widest, extending to bottom): Text: "THE STRAIT IS NOW A WEAPON. FOREVER." At the base, the entire Persian Gulf is frozen in miniature — a permanent fixture of geopolitical risk. Maritime insurance documents, energy security reports, and naval maps are all embedded in the ice. Even when the surface is sunny and the dove is perched on top, THIS layer never melts. A small submarine at the very bottom shines a light on text carved into the base of the iceberg: "The option to close is now priced in permanently."

Style: cross-section illustration, deep ocean blues and teals below, warm sunshine above. The contrast between the diplomatic celebration on top and the permanent structural change below IS the editorial."""


# ═══════════════════════════════════════════════════════════════
# HOTTEST MARCH + EL NINO — NEWSPAPER FORMAT (inverted hierarchy)
# "The Stack": two anomalies stacking multiplies, not adds.
# ═══════════════════════════════════════════════════════════════
ELNINO_NEWSPAPER = """A mock front page of a broadsheet newspaper. Ornate blackletter masthead reads "THE CLIMATE STACK" with "SPECIAL EDITION" in red banner above and "APRIL 2026" in small caps below.

Four stories stacked vertically, each LARGER than the one above:

STORY 1 (top, smallest — 10% of page): Small headline: "MARCH 2026: HOTTEST ON RECORD." A tiny thermometer icon. Brief body text. The way a paper reports weather data. Routine.

STORY 2 (below, larger — 20%): Headline: "EL NINO INCOMING ON TOP OF RECORD HEAT." A medium illustration showing two weather maps overlapping — one showing current heat, one showing El Nino formation. Pull-quote: "Two anomalies don't add. They multiply." Maps of breadbaskets shaded red: US Midwest, India, Australia. All simultaneously stressed.

STORY 3 (below, larger — 25%): Bold headline: "REINSURERS REPRICE THE PLANET." Large illustration showing a boardroom at Munich Re or Swiss Re, executives staring at screens showing maps covered in red. Documents on the table labeled "SOVEREIGN RISK ADJUSTMENT." The ripple: when reinsurers reprice, governments borrow at higher rates, every public service downstream is affected. A pull-quote: "The insurance industry sees the future 18 months before the market does."

STORY 4 (bottom, ENORMOUS — 35%): Massive headline: "THE BASELINE IS GONE." Dominant illustration: a graph showing temperature records over decades, but the X-axis itself is bending upward — the baseline from which records are measured is rising. A scientist stands next to the graph looking not at the latest data point but at the curving axis itself. The point: we're not setting records in a stable system. The system is moving. Next year's normal is this year's record. The concept of "record" has lost meaning.

Bottom slug line: "See page 1 for the headline. See page 4 for what it means when the yardstick is broken."

Style: classic broadsheet, ink-on-newsprint, yellowed paper, column rules, halftone textures. Physical size escalation IS the message."""


# ═══════════════════════════════════════════════════════════════
# HOTTEST MARCH — CEMETERY FORMAT
# What dies at each order of consequence.
# ═══════════════════════════════════════════════════════════════
ELNINO_CEMETERY = """An editorial cartoon of a hillside cemetery in forced perspective, bottom of hill looking up. Four rows of graves ascending, each larger.

ROW 1 (foreground, small headstones): "Comfortable Summers," "Predictable Harvests," "Spring Frost Dates," "Ski Season." Small stones with wilted flowers. A few farmers placing bouquets.

ROW 2 (larger stones): "Crop Insurance Pricing Models," "Midwest Corn Belt Yields," "Indian Monsoon Reliability," "Australian Wheat Forecasts." Weathered obelisks. Agricultural executives in khaki looking uncomfortable.

ROW 3 (grand monuments): "Munich Re's Risk Models," "Sovereign Credit Ratings of Climate-Exposed Nations," "Coastal Property Values," "The Reinsurance Safety Net." Marble monuments with carved angels. Insurance executives and government officials in dark coats.

ROW 4 (top of hill, ENORMOUS mausoleum): A single massive neoclassical mausoleum. Carved above its entrance: "THE CONCEPT OF NORMAL." No mourners — nobody has walked up this far. The path is empty. Storm clouds gather behind it. Because once the baseline shifts, there is no "normal" to return to. The thing that died isn't a crop or a company — it's the assumption that there exists a stable reference point.

Groundskeeper with a shovel in foreground, checking names off a clipboard, hasn't looked up the hill.

Style: pen-and-ink editorial cartoon with watercolor wash, muted grey-green, atmospheric perspective toward the top. Dark humor from specificity of inscriptions."""


# ═══════════════════════════════════════════════════════════════
# EMPEROR PENGUIN — ICEBERG FORMAT
# Literally Antarctic. The format IS the subject.
# ═══════════════════════════════════════════════════════════════
PENGUIN_ICEBERG = """An editorial illustration of an Antarctic iceberg cross-section. The waterline divides at the upper quarter.

ABOVE THE WATERLINE (small, emotionally charged):
A single emperor penguin stands alone on the tip of the iceberg, looking small and dignified against a pale sky. Nearby, a small sign reads "ENDANGERED" in official-looking type. A camera crew films the penguin. Headlines float: "Emperor Penguin Now Endangered!" and "The Face of Climate Change." Emotional, shareable, the part of the story that gets likes and retweets.

BELOW THE WATERLINE (enormous, structural):

Layer 1 (just below surface): Text: "WHAT KILLED THE PENGUIN: SEA ICE FAILURE." Illustrations frozen in ice: crumbling ice shelves, open water where solid ice should be, breeding colonies collapsing as ice breaks apart months too early. The penguin isn't dying from temperature — it's dying because the platform it breeds on is disappearing.

Layer 2 (deeper, wider): Text: "WHAT ELSE LIVES ON THAT ICE: KRILL." The ice layer is filled with dense swarms of krill — billions of tiny shrimp-like creatures, the foundation of the Southern Ocean food web. Frozen into this layer: fish, whales, seals, albatrosses — all connected to the krill by lines showing the food chain. The krill depend on the same ice the penguin depends on.

Layer 3 (deepest, widest): Text: "WHO EATS THE KRILL: ONE BILLION HUMANS." At the base of the iceberg, an entire world is frozen: fishing fleets, fish markets, dinner tables across Japan, Southeast Asia, Africa, South America. Protein supply chains radiating outward from the Southern Ocean to a billion plates. And below even that, carved into the very base: "THERMOHALINE CIRCULATION" — the global ocean conveyor belt, disrupted by the same ice melt, changing rainfall patterns across the entire Southern Hemisphere for generations.

A lone research submarine at the very bottom, its spotlight illuminating the text: "The penguin is the canary. The coal mine is the Southern Hemisphere's food system."

Style: beautiful Antarctic palette — crystalline blues, whites, deep navy below. The penguin on top should be emotionally evocative (the shareable image). The layers below should be clinically precise (the information nobody shares). The contrast between emotional surface and structural depth IS the editorial."""


# ═══════════════════════════════════════════════════════════════
# EMPEROR PENGUIN — WEATHER MAP FORMAT
# The Antarctic Ecosystem Forecast
# ═══════════════════════════════════════════════════════════════
PENGUIN_WEATHER = """A mock television weather forecast screen. Chyron: "ECOSYSTEM FORECAST — SOUTHERN OCEAN ADVISORY"

The display shows a stylized map of Antarctica and the Southern Ocean, with four systems:

SYSTEM 1 (over Antarctic Peninsula, small sad-face cloud): "SPECIES LOSS — Light. Emperor penguin declared endangered. Conservation concern. Documentary crews dispatched. Emotional but contained."

SYSTEM 2 (spreading across Antarctic coast, moderate orange): "SEA ICE COLLAPSE — Moderate. Breeding platforms failing. Same ice loss affects krill habitat. Krill biomass declining. Southern Ocean food web under stress."

SYSTEM 3 (expanding into Southern Ocean, large red): "FISHERY DISRUPTION — Severe. Krill decline cascades into commercial fisheries. Protein supply for 1 billion people at risk. Fish markets from Tokyo to Lagos affected. Food security alert for Southern Hemisphere nations."

SYSTEM 4 (massive system covering entire Southern Hemisphere, deep purple): "THERMOHALINE DISRUPTION — CATASTROPHIC. Antarctic melt disrupts global ocean circulation. Rainfall patterns across Africa, South America, and Australasia shift permanently. Agricultural systems built for the old patterns fail. Generational impact. No forecast model accounts for this."

Weather presenter at left, pointing at the penguin icon in System 1, with a sympathetic expression. The massive purple System 4 behind them covers half the planet.

Bottom ticker: "ADVISORY: Public attention focused on System 1. Systems 2-4 not in any policy framework."

Style: broadcast weather aesthetic, radar gradients, Antarctic map projection centered on South Pole. The deadpan broadcast format makes the escalation hit harder."""


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

    # Strait of Hormuz
    results["strait_weather_nb2"] = gen_nb2(STRAIT_WEATHER, "strait_weather_nb2.png", "16:9")
    results["strait_iceberg_nb2"] = gen_nb2(STRAIT_ICEBERG, "strait_iceberg_nb2.png", "9:16")

    # Hottest March + El Nino
    results["elnino_newspaper_nb2"] = gen_nb2(ELNINO_NEWSPAPER, "elnino_newspaper_nb2.png", "4:5")
    results["elnino_cemetery_nb2"] = gen_nb2(ELNINO_CEMETERY, "elnino_cemetery_nb2.png", "4:5")

    # Emperor Penguin
    results["penguin_iceberg_nb2"] = gen_nb2(PENGUIN_ICEBERG, "penguin_iceberg_nb2.png", "9:16")
    results["penguin_weather_nb2"] = gen_nb2(PENGUIN_WEATHER, "penguin_weather_nb2.png", "16:9")

    # Recraft versions of strongest concepts
    results["strait_weather_recraft"] = gen_recraft(STRAIT_WEATHER, "strait_weather_recraft.png", "1344x768")
    results["penguin_iceberg_recraft"] = gen_recraft(PENGUIN_ICEBERG, "penguin_iceberg_recraft.png", "768x1344")

    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        status = "OK" if v else "FAIL"
        print(f"  {status}: {k}")
