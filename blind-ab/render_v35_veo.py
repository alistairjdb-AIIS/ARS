#!/usr/bin/env python3
"""Blind A/B v35 — Pulse quiet-realization beat, Veo 3.1 Fast direct.

Supersedes v34 after tool-selection failure (Kling v1-6 defaulted to still+camera pan).
Same held-constant brief and same two prompts as v34 (preserves A/B validity).
Tool changed: Veo 3.1 Fast direct via Google generativelanguage API.

Duration: 8s (Veo minimum is effectively 8s — no 5s option here).
Aspect: 16:9.
Native audio: enabled (Veo 3.1 default).
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

# --- Brief (constant) ---
BRIEF = (
    "Pulse, the round fluffy yellow angel, alone at a window at sunset, "
    "looking at a small paper drawing, having a quiet realization."
)

# --- Output 1: first instinct, no dialogue (IDENTICAL to v34) ---
PROMPT_FIRST_INSTINCT = (
    "Pulse the round yellow fluffy angel sits on a wooden windowsill at dusk. "
    "Warm evening light. Holding a small paper drawing. Looks down at it, then "
    "lifts head slowly, eyes lighting up with realization. Small happy smile "
    "forms. Anime style, Studio Ghibli mood, soft lighting."
)

# --- Output 2: post-dialogue (IDENTICAL to v34) ---
PROMPT_POST_DIALOGUE = (
    "Pulse — round fluffy yellow body, no external ears, big brown eyes, small "
    "halo floating above head, small feathered wings, small paw-hands. Standing "
    "on wooden floorboards beside a window at sunset, holding a small crumpled "
    "paper drawing in both paws. Holding completely still, staring at the "
    "drawing. Then: eyes widen slowly, mouth parts just slightly, a small smile "
    "begins. Warm golden window light across the fur. Hand-drawn anime, soft "
    "line-weight, gentle atmospheric haze. Body remains still — motion confined "
    "to the face."
)

SHARED_NEGATIVE = (
    "live-action, photorealistic, text, watermarks, logos, deformed, "
    "extra limbs, blurry, jittery, camera shake, camera zoom, camera pan, "
    "static image"
)


def submit(label, prompt):
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
        print(f"[{label}] SUBMIT ERROR {r.status_code}: {r.text[:400]}")
        return None
    op = r.json().get("name")
    print(f"[{label}] submitted: {op}")
    return op


def check_download(label, op):
    url = f"{BASE_URL}/{op}?key={API_KEY}"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d.get("done"):
        return None
    err = d.get("error")
    if err:
        print(f"[{label}] ERROR: {json.dumps(err)[:300]}")
        return False
    samples = d.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
    if not samples:
        print(f"[{label}] no samples: {json.dumps(d)[:300]}")
        return False
    uri = samples[0].get("video", {}).get("uri", "")
    if not uri:
        return False
    dl = f"{uri}&key={API_KEY}" if "?" in uri else f"{uri}?key={API_KEY}"
    v = requests.get(dl, timeout=120, allow_redirects=True)
    if v.status_code != 200:
        return False
    out_path = os.path.join(OUT_DIR, f"v35-output-{label}.mp4")
    with open(out_path, "wb") as f:
        f.write(v.content)
    print(f"[{label}] saved: {out_path} ({len(v.content)/1e6:.1f} MB)")
    return True


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Randomize label assignment
    rng = random.SystemRandom()
    if rng.random() < 0.5:
        mapping = {"a": ("first_instinct", PROMPT_FIRST_INSTINCT),
                   "b": ("post_dialogue", PROMPT_POST_DIALOGUE)}
    else:
        mapping = {"a": ("post_dialogue", PROMPT_POST_DIALOGUE),
                   "b": ("first_instinct", PROMPT_FIRST_INSTINCT)}

    print(f"=== Submitting v35 blind A/B ({MODEL}) ===")
    ops = {}
    for label, (process, prompt) in mapping.items():
        op = submit(label, prompt)
        if op:
            ops[label] = op
    if len(ops) != 2:
        raise SystemExit(f"Only {len(ops)}/2 submissions succeeded — aborting")

    print(f"\n=== Polling {len(ops)} operations ===")
    results = {}
    pending = dict(ops)
    start = time.time()
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
    for k in pending:
        results[k] = "TIMEOUT"

    print("\n=== RESULTS ===")
    for k in sorted(mapping):
        print(f"  v35-output-{k}.mp4: {results.get(k, '?')} ({mapping[k][0]})")

    # Write sealed mapping AFTER render
    labels_path = os.path.join(OUT_DIR, "v35-labels.md")
    with open(labels_path, "w") as f:
        f.write("# v35 Blind A/B — Sealed Mapping\n\n")
        f.write(f"Session 36 blind test, supersedes v34.\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write(f"**Model:** {MODEL} / duration={DURATION}s / aspect={ASPECT}\n\n")
        f.write(f"**Brief:** {BRIEF}\n\n")
        f.write("**Variable:** prompt-writing process only. Prompts IDENTICAL to v34.\n\n")
        f.write("## Label → Process\n\n")
        for k in sorted(mapping):
            process, prompt = mapping[k]
            f.write(f"### v35-output-{k}.mp4 — **{process}**\n\n")
            f.write(f"Render status: {results.get(k, '?')}\n\n")
            f.write(f"Prompt:\n> {prompt}\n\n")
        f.write("## Operation IDs\n\n")
        for k, op in ops.items():
            f.write(f"- {k}: {op}\n")
    print(f"\nSealed mapping written: {labels_path}")


if __name__ == "__main__":
    main()
