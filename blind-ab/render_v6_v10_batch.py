#!/usr/bin/env python3
"""Blind A/B v6-v10 batch — 5 photoreal sub-registers.

RANDOMIZED ASSIGNMENT per-test (see labels files):
  v6: A=TERSE,   B=CRAFTED
  v7: A=TERSE,   B=CRAFTED
  v8: A=CRAFTED, B=TERSE
  v9: A=CRAFTED, B=TERSE
  v10: A=CRAFTED, B=TERSE

No overlays (testing pure photoreal, not brand-hold).
"""

import requests, json, time, os

API_KEY = os.environ.get("VEO_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
if not API_KEY:
    raise SystemExit("VEO_API_KEY or GOOGLE_AI_API_KEY env var required")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-fast-generate-preview"
OUT_DIR = "/root/blind-ab"

SHARED_NEGATIVE = (
    "faces, hands, arms, people, human figures, text, readable characters, "
    "logos, watermarks, motion blur, warping, bright backgrounds, overexposure, "
    "jitter, filmstrip edges, sprocket holes, film burns"
)

# Prompt library
TERSE = {
    "v6": "8-second cinematic photoreal exterior. Weathered stone building facade at golden hour, single arched window with aged wooden frame, ivy climbing one side, cobblestone in foreground. Slow static pull-back. Warm low-angle sunlight. No people.",
    "v7": "8-second cinematic photoreal landscape. Foggy mountain valley at dawn, pine forest on slopes, distant snow-capped peaks, mist rising from valley floor. Slow camera pan across valley. Cold dawn palette. No people.",
    "v8": "8-second cinematic photoreal close-up. Honey dripping from honeycomb onto thick sourdough toast slice on wooden board. Slow-motion amber drip. Morning sidelight. Shallow depth of field. Warm palette. No hands.",
    "v9": "8-second cinematic photoreal close-up. Linen curtain billowing in open window, morning light streaming through, wooden sill visible. Slow natural breeze motion. Soft warm palette. No people.",
    "v10": "8-second cinematic photoreal close-up. Water droplets on single tulip petal, morning light, slow focus pull from droplet to full flower. Shallow depth of field. Soft palette. No people.",
}

CRAFTED = {
    "v6": "Cinematography: wide lens, slow pull-back from building facade, eye-level framing, shallow foreground compression. Subject: weathered stone building facade, single arched window with aged wooden frame, ivy climbing left side of facade, cobblestone ground in foreground. Action: camera slowly pulls back revealing more of the facade, ivy leaves shift slightly in breeze, warm light shifts across stone texture. Context: golden hour, low-angle sunlight from frame-left casting long shadows across cobblestones, irregular stone weathering with moss patches, no people in frame, European alley atmosphere. Style & Ambiance: intimate architectural study, warm amber + grey stone + green ivy palette, natural light falloff, contemplative mood, authentic wear. Audio: distant church bell, soft wind, occasional bird call, ambient alley tone.",
    "v7": "Cinematography: wide-angle lens, slow horizontal pan from left to right across mountain valley, establishing shot framing, deep focus. Subject: mountain valley at dawn, dense pine forest covering slopes, distant snow-capped peaks on horizon, mist rising from valley floor in slow convection. Action: camera pans slowly across the valley revealing depth layers, fog drifts and lifts from valley floor, pine tops sway slightly, light shifts subtly on distant peaks. Context: first light before sunrise, cold blue-grey palette with first warm tones on highest peaks, irregular forest density with varied tree heights, exposed rock patches among trees, no people in frame. Style & Ambiance: pristine wilderness quiet, cold blue + dark pine + warm peak-tip palette, soft atmospheric perspective, meditative mood, natural chaos in mist patterns. Audio: distant birdcall, faint wind through pines, soft ambient tone.",
    "v8": "Cinematography: 100mm macro lens, shallow depth of field f/2.8, locked static shot at board height, tight close-up framing. Subject: honeycomb piece suspended above thick sourdough toast slice, amber honey dripping in slow stream, wooden cutting board with visible grain. Action: honey drips from honeycomb edge in smooth viscous stream, pools on toast surface before slowly spreading, tiny bubbles visible in honey flow. Context: warm morning sidelight from frame-right at 30 degrees, soft bokeh wooden background, irregular wax texture on honeycomb, rough crumb texture on toast, no hands visible just comb and toast. Style & Ambiance: artisan food ritual, warm amber + honey gold + dark bread crust palette, subtle halation on honey highlights, abundance mood. Audio: soft honey drip, faint kitchen ambience.",
    "v9": "Cinematography: 50mm lens, shallow depth of field, locked static shot at window level, medium-close framing. Subject: sheer linen curtain, open wooden window with weathered sill, backlit by morning light. Action: curtain billows slowly and irregularly in breeze, fabric folds shift organically, light filters through fabric weave creating shifting patterns on wall. Context: warm morning sunlight streaming through from behind curtain, wooden sill with paint wear and subtle dust, stone wall beyond window suggested out of focus, no people visible. Style & Ambiance: quiet domestic morning, cream + honey-wood + soft warm-white palette, translucent fabric glow, serene mood, natural fabric irregularity. Audio: soft fabric rustle, distant outdoor birds, faint wind, quiet room tone.",
    "v10": "Cinematography: 100mm macro lens, very shallow depth of field f/2.8, slow rack focus from extreme close-up droplet to wider flower view, locked camera position. Subject: single tulip flower in soft focus, isolated water droplets clinging to outer petal surface, green stem just visible below. Action: focus slowly pulls back from one specific droplet to reveal full flower and second tulip behind, droplets reflect light as focus shifts, petal edges tremble barely. Context: early morning diffused light, soft overcast sky or window light, blurred green foliage background, irregular petal texture with subtle veining, no people or hands. Style & Ambiance: meditative botanical study, cream + soft pink + green foliage palette, dewy freshness, stillness mood, natural droplet variance. Audio: very faint garden ambience, distant birds, soft wind, near-silence.",
}

# Per-test A/B mapping (randomized)
MAPPING = {
    "v6":  {"a": "terse",   "b": "crafted"},
    "v7":  {"a": "terse",   "b": "crafted"},
    "v8":  {"a": "crafted", "b": "terse"},
    "v9":  {"a": "crafted", "b": "terse"},
    "v10": {"a": "crafted", "b": "terse"},
}


def build_outputs():
    out = {}
    for v, m in MAPPING.items():
        for slot in ("a", "b"):
            approach = m[slot]
            prompt = TERSE[v] if approach == "terse" else CRAFTED[v]
            out[f"{v}-output-{slot}-raw"] = {"prompt": prompt, "negative": SHARED_NEGATIVE}
    return out


OUTPUTS = build_outputs()


def submit(key):
    p = OUTPUTS[key]
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": p["prompt"]}],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "sampleCount": 1,
            "negativePrompt": p["negative"],
        },
    }
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[{key}] SUBMIT ERROR {r.status_code}: {r.text[:300]}")
        return None
    op = r.json().get("name")
    print(f"[{key}] submitted: {op}")
    return op


def check_download(key, op):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d.get("done"):
        return None
    samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
    if not samples:
        print(f"[{key}] no samples: {json.dumps(d)[:300]}")
        return False
    uri = samples[0].get("video", {}).get("uri", "")
    if not uri:
        return False
    dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
    v = requests.get(dl, timeout=120, allow_redirects=True)
    if v.status_code != 200:
        return False
    out_path = os.path.join(OUT_DIR, f"{key}.mp4")
    with open(out_path, "wb") as f:
        f.write(v.content)
    print(f"[{key}] saved ({len(v.content)/1e6:.1f} MB)")
    return True


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    keys = list(OUTPUTS.keys())

    # Parallel submit — all 10 operations submitted upfront
    print(f"=== Submitting {len(keys)} operations ===")
    ops = {}
    for k in keys:
        op = submit(k)
        if op:
            ops[k] = op

    print(f"\n=== Polling {len(ops)} operations ===")
    results = {}
    start = time.time()
    pending = dict(ops)
    while pending and time.time() - start < 900:
        for k in list(pending):
            r = check_download(k, pending[k])
            if r is True:
                results[k] = "OK"
                del pending[k]
            elif r is False:
                results[k] = "FAIL"
                del pending[k]
        if pending:
            elapsed = int(time.time() - start)
            print(f"  {len(pending)} pending ({elapsed}s)...")
            time.sleep(15)

    for k in keys:
        if k not in results:
            results[k] = "TIMEOUT"

    print("\n=== RESULTS ===")
    for k in keys:
        print(f"  {k}: {results.get(k, '?')}")
