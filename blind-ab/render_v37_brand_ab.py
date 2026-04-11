#!/usr/bin/env python3
"""v37 — Brand film A/B test, 3 briefs × 2 process variants (first-instinct vs post-dialogue).

Goal: N=3 evidence for the internal-dialogue rule, across 3 distinct brand domains
(Liquid Death, Patagonia, Apple). All on veo-3.1-fast direct (latest, native audio).

AUDIO PATH: Veo 3.1 native audio (per standing decision Apr 10).

Labels randomized per brief so A/B ordering does not leak the process.
Sealed mapping written to v37-labels.md after render completes.
"""

import os, json, time, random, requests
from datetime import datetime

API_KEY = os.environ.get("VEO_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY env var required")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"
DURATION = 8
ASPECT = "16:9"

SHARED_NEGATIVE = (
    "text, watermarks, logos, deformed, extra limbs, extra fingers, "
    "blurry, jittery, camera shake, morphing, warping, flickering, "
    "overexposure, static noise"
)

# --- Briefs ---
# Each brief has: name, first_instinct prompt, post_dialogue prompt

BRIEFS = {
    "liquid_death": {
        "display_name": "Liquid Death — Ice Throne",
        "first_instinct": (
            "A heavy metal king in black leather sits on a throne of ice in a dark "
            "cave. He cracks open a Liquid Death tallboy can. Metallic choir sting "
            "plays. He takes a long swig, then tilts his head back with eyes closed "
            "in satisfaction. Cinematic, dramatic lighting, black and silver color "
            "palette, moody heavy metal atmosphere. Audio: silence, can crack, "
            "choir sting, swallow, exhale."
        ),
        "post_dialogue": (
            "Bearded heavy-metal figure in black studded leather jacket, tattooed "
            "forearms, crown of obsidian shards, sits in total ritual stillness on "
            "a throne carved from rough blue-white ice. Shadowy cave, single cold "
            "blue light from above, steam rising from the ice. He holds a black "
            "metal tallboy can in both hands like a chalice. With complete ritual "
            "gravity -- no irony, no smile -- he cracks the tab. The crack echoes "
            "through the cave. He raises the can, takes one long deliberate swig, "
            "tilts his head back, closes his eyes, holds. Audio: silence, then the "
            "metallic CRACK of the tab reverberating, a single sustained low gothic "
            "choral note, the liquid swallow, a low exhale. No dialogue, no tagline."
        ),
    },
    "patagonia": {
        "display_name": "Patagonia -- Pre-Wave Surfer",
        "first_instinct": (
            "A surfer in a black wetsuit stands waist-deep in cold Pacific water at "
            "dawn, looking out at a rising wave. Breath visible in the cold air. "
            "They exhale, then duck under the water as the wave curls. Documentary "
            "style, natural light, muted color grading, grounded humanism. Audio: "
            "wave wash, breath, wind, distant gull."
        ),
        "post_dialogue": (
            "A figure in a weathered black wetsuit seen from three-quarters behind, "
            "holding a surfboard tucked under one arm, other hand trailing in the "
            "water, standing waist-deep in cold steel-grey Pacific water at "
            "pre-dawn. The water is still except for distant swell building on the "
            "horizon. Warm first-light just catching the eastern edge of low "
            "clouds. The figure holds completely still, watching the horizon, "
            "breath fogging visibly in the cold air. Then takes one long slow "
            "exhale -- a visible plume of breath in the air. Muted warm-cool color "
            "grading, natural light only, weathered texture on the wetsuit. Audio: "
            "slow wave wash, low wind, one distant gull call, the soft exhale. No "
            "dialogue, no music, no wave breaking."
        ),
    },
    "apple": {
        "display_name": "Apple -- AirPods Sculpture",
        "first_instinct": (
            "Extreme close-up of hands holding a matte white AirPods case on a warm "
            "sunlit marble surface. The case clicks open, one earbud lifts out, "
            "chrome catches the light, then the case clicks shut. Minimal, clean, "
            "Apple aesthetic, shallow depth of field, warm color grading. Audio: "
            "magnetic click, soft ambient hum, single chime."
        ),
        "post_dialogue": (
            "Extreme macro shot, shallow focus. A matte white wireless earbud case "
            "sits alone on a pale linen cloth. Warm morning light from one "
            "direction catches a soft rim along the hinge edge. Only the hinge is "
            "in perfect focus; the rest of the case softens into bokeh. A hand "
            "enters from frame edge -- just fingertips, no palm, no wrist -- and "
            "gently presses the case seam. The lid clicks open with a precise "
            "magnetic sound. The lid lifts in one smooth unhurried arc. Inside, "
            "the chrome stem of an earbud reveals itself, catching the warm "
            "light. Hold on the open case. Soft dust particles drift in the "
            "morning beam. Audio: silence, then the exact magnetic CLICK, the "
            "soft hiss of the hinge opening, a single low warm sustained tone. "
            "No music, no voice. Linen texture visible in the foreground."
        ),
    },
}


def submit(brief_key, label, prompt):
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": ASPECT,
            "durationSeconds": DURATION,
            "sampleCount": 1,
            "negativePrompt": SHARED_NEGATIVE,
        },
    }
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[{brief_key}/{label}] SUBMIT ERROR {r.status_code}: {r.text[:400]}")
        return None
    op = r.json().get("name")
    print(f"[{brief_key}/{label}] submitted: {op}")
    return op


def check_download(brief_key, label, op):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d.get("done"):
        return None
    err = d.get("error")
    if err:
        print(f"[{brief_key}/{label}] ERROR: {json.dumps(err)[:300]}")
        return False
    samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
    if not samples:
        print(f"[{brief_key}/{label}] no samples: {json.dumps(d)[:300]}")
        return False
    uri = samples[0].get("video", {}).get("uri", "")
    if not uri:
        return False
    dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
    v = requests.get(dl, timeout=120, allow_redirects=True)
    if v.status_code != 200:
        return False
    out_path = os.path.join(OUT_DIR, f"v37-{brief_key}-{label}.mp4")
    with open(out_path, "wb") as f:
        f.write(v.content)
    print(f"[{brief_key}/{label}] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
    return True


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Randomize label assignment per brief
    rng = random.SystemRandom()
    mappings = {}
    for brief_key, brief in BRIEFS.items():
        if rng.random() < 0.5:
            mappings[brief_key] = {
                "a": ("first_instinct", brief["first_instinct"]),
                "b": ("post_dialogue", brief["post_dialogue"]),
            }
        else:
            mappings[brief_key] = {
                "a": ("post_dialogue", brief["post_dialogue"]),
                "b": ("first_instinct", brief["first_instinct"]),
            }

    print("=== Submitting v37 brand A/B (6 renders) ===")
    ops = {}
    for brief_key, mapping in mappings.items():
        for label, (process, prompt) in mapping.items():
            key = f"{brief_key}-{label}"
            op = submit(brief_key, label, prompt)
            if op:
                ops[key] = (brief_key, label, op)
    if len(ops) != 6:
        print(f"WARNING: only {len(ops)}/6 submissions succeeded")
        if len(ops) == 0:
            raise SystemExit("No submissions accepted")

    print(f"\n=== Polling {len(ops)} operations ===")
    results = {}
    pending = dict(ops)
    start = time.time()
    while pending and time.time() - start < 1200:
        for key in list(pending):
            brief_key, label, op = pending[key]
            r = check_download(brief_key, label, op)
            if r is True:
                results[key] = "OK"
                del pending[key]
            elif r is False:
                results[key] = "FAIL"
                del pending[key]
        if pending:
            elapsed = int(time.time() - start)
            print(f"  {len(pending)} pending ({elapsed}s)...")
            time.sleep(15)
    for key in pending:
        results[key] = "TIMEOUT"

    print("\n=== RESULTS ===")
    for brief_key, mapping in mappings.items():
        for label in sorted(mapping):
            key = f"{brief_key}-{label}"
            process = mapping[label][0]
            print(f"  v37-{brief_key}-{label}.mp4: {results.get(key, '?')} ({process})")

    # Write sealed mapping
    labels_path = os.path.join(OUT_DIR, "v37-labels.md")
    with open(labels_path, "w") as f:
        f.write("# v37 Brand A/B -- Sealed Mapping\n\n")
        f.write(f"Session 36 elective A/B (not counter-triggered).\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write(f"**Model:** {MODEL}\n")
        f.write(f"**Duration:** {DURATION}s / Aspect: {ASPECT}\n")
        f.write("**AUDIO PATH:** Veo 3.1 native audio (per standing decision Apr 10)\n\n")
        f.write("**Goal:** N=3 evidence for internal-dialogue rule across 3 brand domains.\n")
        f.write("**Variable:** prompt-writing process only (first-instinct vs post-dialogue).\n\n")
        for brief_key, brief in BRIEFS.items():
            f.write(f"## {brief['display_name']}\n\n")
            for label in sorted(mappings[brief_key]):
                process, prompt = mappings[brief_key][label]
                key = f"{brief_key}-{label}"
                f.write(f"### v37-{brief_key}-{label}.mp4 -- **{process}**\n\n")
                f.write(f"Render status: {results.get(key, '?')}\n\n")
                f.write(f"Prompt:\n> {prompt}\n\n")
            f.write("\n")
        f.write("## Operation IDs\n\n")
        for key, (brief_key, label, op) in ops.items():
            f.write(f"- {key}: {op}\n")
    print(f"\nSealed mapping written: {labels_path}")


if __name__ == "__main__":
    main()
