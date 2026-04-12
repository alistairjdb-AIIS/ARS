"""
Comic v7 — LLM NEWS carousel: progressive disclosure weather map.
4 slides, each adding one system. Swipe right = deeper consequence.
Branded "LLM NEWS" top-left (not a real network).

Subject: Strait of Hormuz ceasefire — "The Trap"
Format: 4-image Twitter carousel, each slide adds one system layer.
Tool: NB2 (operator preference) + Recraft backup.
"""
import os, json, base64, requests

OUT = "/root/comic-v7"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")

# Shared visual context that each slide builds on
BASE_CONTEXT = """A television news broadcast screen with a consistent visual identity across all slides:
- Top-left corner: "LLM NEWS" logo in bold modern sans-serif white text on a dark navy rounded rectangle badge
- Top banner: "STRAIT FORECAST — GEOPOLITICAL ADVISORY" in clean white text on a dark navy bar spanning the full width
- The main display area shows a stylized map of the Persian Gulf region with the Strait of Hormuz as a narrow chokepoint between Iran (north) and Oman/UAE (south)
- Bottom ticker bar: dark navy bar with scrolling advisory text in white
- Overall broadcast aesthetic: clean, professional, dark navy and teal color scheme with white text, modern news graphics"""


SLIDE_1 = f"""{BASE_CONTEXT}

This is SLIDE 1 of 4. The map shows ONLY ONE weather system:

SYSTEM 1 — centered over the Strait of Hormuz: A bright golden sun icon breaking through light clouds. The area around the Strait glows warm yellow-green, indicating calm conditions.

Label in clean bold white text: "SYSTEM 1: CEASEFIRE"
Sub-label: "Temporary clearing. Strait reopens. Oil prices ease."
Status indicator: Green circle with "ALL CLEAR"

The rest of the map is empty and calm — soft blue ocean, no other weather systems visible. The Persian Gulf looks peaceful.

Bottom ticker reads: "BREAKING: Iran reopens Strait of Hormuz under 2-week ceasefire agreement. Oil futures drop 4%. Shipping companies begin re-routing."

The mood is optimistic. This is the headline everyone sees. One system, one story, good news.

Style: broadcast-quality news graphic, clean modern design, dark navy/teal palette with warm golden accent for the sun. Professional and calm."""


SLIDE_2 = f"""{BASE_CONTEXT}

This is SLIDE 2 of 4. The map now shows TWO weather systems. System 1 from the previous slide is still visible but slightly smaller:

SYSTEM 1 (still over the Strait, golden sun, slightly faded): Same as before but now occupying less visual attention.

SYSTEM 2 — NEW, appearing across the shipping lanes approaching the Strait: Moderate orange wind arrows and directional flow lines showing ship traffic converging on the Strait from both the Indian Ocean side and the Persian Gulf side. Multiple small ship icons are visible, all moving TOWARD the narrow chokepoint.

Label: "SYSTEM 2: RE-ROUTING"
Sub-label: "Vessels returning from Cape of Good Hope routes. Cost savings drive traffic back through bottleneck."
Status indicator: Orange triangle with "WATCH"

The visual emphasis is on the CONVERGENCE — arrows and ship icons all funneling into the narrow Strait passage. The traffic pattern shows a clear bottleneck forming.

Bottom ticker reads: "UPDATE: Major shipping lines redirecting vessels through Strait of Hormuz. Maersk, MSC, CMA CGM resume direct Gulf routing. Estimated savings: $800K per voyage vs Cape route."

The mood has shifted slightly — still broadly positive, but the convergence pattern is visible. The funnel shape should make the viewer uneasy even though the text is still optimistic.

Style: same broadcast aesthetic, orange added to the palette for System 2. Ship icons as simple white silhouettes."""


SLIDE_3 = f"""{BASE_CONTEXT}

This is SLIDE 3 of 4. The map now shows THREE weather systems. Systems 1 and 2 are still visible:

SYSTEM 1 (golden sun, now small and pushed to the corner, fading)
SYSTEM 2 (orange arrows, ships still converging on Strait)

SYSTEM 3 — NEW, a dark red storm cell forming directly OVER the Strait chokepoint, engulfing the ships from System 2: A rotating storm system with lightning bolt icons, rendered in deep red and dark crimson. The ships from System 2 are now INSIDE the red zone — trapped in the bottleneck with a storm closing over them.

Label: "SYSTEM 3: TRAP FORMATION"
Sub-label: "Ceasefire expires. Every vessel inside the Strait is exposed. Those who re-routed back are caught."
Status indicator: Red octagon with "SEVERE"

A thin dotted line shows an alternative route around the Cape of Good Hope labeled "SAFE ROUTE" in small green text — the route the trapped ships abandoned to save costs.

A countdown overlay in the corner reads: "CEASEFIRE WINDOW: 14 DAYS" with an hourglass icon, the sand nearly run out.

Bottom ticker reads: "ANALYSIS: Companies that maintained Cape of Good Hope routes now positioned advantageously. Re-routed vessels face 72-hour exit window if ceasefire collapses."

The mood is now alarming. The ships that went back in are visually trapped — red over the chokepoint, no easy exit. The green Cape route is a quiet indictment of the cost-saving decision.

Style: same broadcast aesthetic, deep red/crimson added. The red storm should dominate the visual center. Tension is high."""


SLIDE_4 = f"""{BASE_CONTEXT}

This is SLIDE 4 of 4 — the FINAL REVEAL. The map now shows ALL FOUR systems, with System 4 dominating:

SYSTEM 1 (tiny golden sun, barely visible, pushed to far corner)
SYSTEM 2 (orange arrows, still showing ship convergence)
SYSTEM 3 (red storm over the Strait)

SYSTEM 4 — NEW, ENORMOUS: A massive deep purple and black weather system that covers the ENTIRE Persian Gulf, Indian Ocean approach, and extends far beyond the map boundaries. This is not a storm — it is a permanent atmospheric condition. It has no clear edges. It extends beyond the frame. It covers not just the Strait but every shipping lane, every port, every coastline in the region.

Label: "SYSTEM 4: PERMANENT WEAPONIZATION"
Sub-label: "The Strait is now a weapon even when open. Maritime insurance permanently reprices. Every Strait-dependent economy operates under perpetual closure risk. The option to close has been demonstrated."
Status indicator: Black pentagon with "UNPRECEDENTED — NO HISTORICAL MODEL"

The deep purple system should look QUALITATIVELY DIFFERENT from systems 1-3. Not just bigger — different in kind. Systems 1-3 are weather events (temporary). System 4 is a climate shift (permanent). It will never leave the map.

Bottom ticker reads: "ADVISORY: Markets pricing System 1. Shipping companies responding to System 2. Analysts debating System 3. Nobody has a model for System 4. Geography is now geopolitics."

The mood is ominous and permanent. The purple doesn't look like it will clear. This is the new normal.

Style: same broadcast aesthetic but the purple overwhelms the clean design. The professional news format is barely containing what it's showing — the purple bleeds to the edges. The framework is straining."""


def gen_nb2(prompt, filename, aspect):
    print(f"\n{'='*60}\nNB2 -> {filename}\n{'='*60}")
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
    print(f"\n{'='*60}\nRECRAFT -> {filename}\n{'='*60}")
    if not RECRAFT_KEY:
        print("  SKIP -- no key"); return None
    url = "https://external.api.recraft.ai/v1/images/generations"
    headers = {"Authorization": f"Bearer {RECRAFT_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "model": "recraftv4", "size": size, "n": 1, "response_format": "url"}
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

    # NB2 carousel (primary)
    results["s1_nb2"] = gen_nb2(SLIDE_1, "strait_slide1_nb2.png", "16:9")
    results["s2_nb2"] = gen_nb2(SLIDE_2, "strait_slide2_nb2.png", "16:9")
    results["s3_nb2"] = gen_nb2(SLIDE_3, "strait_slide3_nb2.png", "16:9")
    results["s4_nb2"] = gen_nb2(SLIDE_4, "strait_slide4_nb2.png", "16:9")

    # Recraft carousel (comparison)
    results["s1_rc"] = gen_recraft(SLIDE_1, "strait_slide1_recraft.png", "1344x768")
    results["s2_rc"] = gen_recraft(SLIDE_2, "strait_slide2_recraft.png", "1344x768")
    results["s3_rc"] = gen_recraft(SLIDE_3, "strait_slide3_recraft.png", "1344x768")
    results["s4_rc"] = gen_recraft(SLIDE_4, "strait_slide4_recraft.png", "1344x768")

    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        status = "OK" if v else "FAIL"
        print(f"  {status}: {k}")
