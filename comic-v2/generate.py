"""
Comic v2 — Editorial caricature on Anthropic mythos
"THE ORACLE OF SAN FRANCISCO"
Same scene, 3 visual registers: Manga (seinen), Pixar 3D, Victorian Punch etching.
Tools: NB2 for manga + Victorian, Recraft V4 for Pixar 3D.
"""
import os, json, base64, requests

OUT = "/root/comic-v2"
os.makedirs(OUT, exist_ok=True)

NB2_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GEMINI_API_KEY")
RECRAFT_KEY = os.environ.get("RECRAFT_API_KEY")

# ── Scene (shared across all 3 styles) ──
SCENE = """A single editorial cartoon. On top of a high mountain temple above San Francisco, a robed AI researcher (the Oracle) stands with arms raised, beard flowing, eyes closed in solemn concentration. Behind the Oracle, a tall obsidian obelisk with the word "CLAUDE" carved vertically into it glows with soft blue light.

Gathered on stone steps below the Oracle: a US senator in a dark suit clutching a notepad with wide worried eyes; a Silicon Valley venture capitalist in a Patagonia vest clutching an oversized checkbook with greedy bright eyes; a journalist with a recorder and glasses leaning forward eagerly; a hooded developer at a laptop typing furiously. Each supplicant has exaggerated caricature features — big head, expressive facial expression, recognizable archetype.

The Oracle's mouth is shaped to utter a single word: "SAFETY". Speech ribbon rising from his mouth in calligraphic script reads "SAFETY".

Above the VC's head, a thought bubble shows dollar signs and rocket ships. Above the senator's head, a thought bubble shows a gavel and a ballot. Above the journalist's head, a thought bubble shows a viral headline. Above the developer's head, a thought bubble shows a GitHub commit graph going vertical.

At the bottom of the image, a bold caption bar reads: "THE ORACLE SPEAKS OF SAFETY. THE PILGRIMS HEAR OPPORTUNITY." At the very top, a smaller title reads: "THE ORACLE OF SAN FRANCISCO".
"""

# ── Style 1: MANGA (seinen sub-register — adult, muted, realistic) ──
MANGA_PROMPT = f"""A seinen manga editorial illustration, high-contrast black and white with heavy screentone shading, sharp inking, realistic proportions, muted grayscale palette, kinetic speed lines around the Oracle, dramatic low-angle composition, hand-drawn look, clean thick-thin linework, classic seinen manga editorial page aesthetic reminiscent of Naoki Urasawa. Flat 2D, no 3D rendering.

{SCENE}

Rendered in seinen manga style: dramatic half-face shadow on the Oracle, screentone dot patterns for shading, bold black ink outlines, kinetic action-movement lines radiating from the obelisk, classic manga paneled single-page composition. Text rendered in bold sans-serif manga lettering."""

# ── Style 2: PIXAR 3D (Feature-film Pixar, heroic proportions, warm lighting) ──
PIXAR_PROMPT = f"""A Pixar-like 3D animation still, feature-film-quality CG rendering, heroic proportions for the Oracle (8 heads tall, elongated stately figure), exaggerated caricature shape language for each supplicant — round plump VC, square broad-shouldered senator, angular sharp-featured journalist, slouched hooded developer. 60-30-10 color palette: warm gold sunset (60) + cobalt temple shadows (30) + glowing teal obelisk accent (10). Soft volumetric god-ray lighting from behind the Oracle. Smooth subsurface skin shading, rich material rendering, polished and expressive faces.

{SCENE}

Rendered in feature-film Pixar 3D style: physics-plausible squash-and-stretch on the supplicants, controlled exaggeration, warm inviting lighting, everyone's face readable as a distinct character archetype, cinematic composition, children's-movie polish that makes the adult satire land harder."""

# ── Style 3: VICTORIAN PUNCH MAGAZINE ETCHING (1890s political cartoon) ──
VICTORIAN_PROMPT = f"""A Victorian-era political cartoon in the style of Punch magazine circa 1895, pen-and-ink crosshatch etching on aged cream paper, sepia brown ink tones, meticulous hand-drawn hatching and stippling, classical editorial cartoon composition, ornate decorative frame around the scene, archaic typography with serif fonts and drop caps, tonal depth built entirely through crosshatch density.

{SCENE}

Rendered in 19th-century Punch magazine editorial cartoon style: every character drawn with meticulous crosshatched engraving lines, exaggerated caricature features in the tradition of Sir John Tenniel and Sir Bernard Partridge, decorative art-nouveau border frame, title in ornate Victorian display serif at top, caption at bottom in italic engraved script. Aged parchment background texture. No color — monochrome brown-sepia etching only. The satire is delivered with Victorian formal gravity which amplifies the comedy."""


def gen_nb2(prompt: str, filename: str):
    print(f"\n{'='*60}\nNB2 → {filename}\n{'='*60}")
    if not NB2_KEY:
        print("  SKIP — no key"); return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={NB2_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "1:1"},
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


def gen_recraft(prompt: str, filename: str):
    print(f"\n{'='*60}\nRECRAFT V4 → {filename}\n{'='*60}")
    if not RECRAFT_KEY:
        print("  SKIP — no key"); return None
    url = "https://external.api.recraft.ai/v1/images/generations"
    headers = {"Authorization": f"Bearer {RECRAFT_KEY}", "Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "model": "recraftv4",
        "size": "1024x1024",
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
    results["manga_nb2"] = gen_nb2(MANGA_PROMPT, "oracle_manga_nb2.png")
    results["pixar_recraft"] = gen_recraft(PIXAR_PROMPT, "oracle_pixar_recraft.png")
    results["victorian_nb2"] = gen_nb2(VICTORIAN_PROMPT, "oracle_victorian_nb2.png")
    print("\n" + "="*60 + "\nSUMMARY\n" + "="*60)
    for k, v in results.items():
        print(f"  {k}: {v}")
