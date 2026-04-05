#!/usr/bin/env python3
"""Retry remaining v7-v10 renders with chunked submissions (quota ~3 concurrent)."""

import requests, json, time, os, sys

# Reuse the main batch script's prompt data
sys.path.insert(0, "/root/blind-ab")
from render_v6_v10_batch import OUTPUTS, BASE_URL, MODEL, OUT_DIR, API_KEY

PAIR_GROUPS = [
    ["v7-output-b-raw"],                           # completes v7 (a already done)
    ["v8-output-a-raw", "v8-output-b-raw"],        # v8 pair
    ["v9-output-a-raw", "v9-output-b-raw"],        # v9 pair
    ["v10-output-a-raw", "v10-output-b-raw"],      # v10 pair
]


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
    if r.status_code == 429:
        return "RATE_LIMIT"
    if r.status_code != 200:
        print(f"[{key}] SUBMIT ERROR {r.status_code}: {r.text[:200]}")
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
        print(f"[{key}] no samples")
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


def process_chunk(chunk_keys, results):
    """Submit a chunk, poll until all done."""
    ops = {}
    for k in chunk_keys:
        # Retry submit up to 3 times if rate-limited
        for attempt in range(3):
            op = submit(k)
            if op == "RATE_LIMIT":
                print(f"[{k}] rate-limited, waiting 30s (attempt {attempt+1})")
                time.sleep(30)
                continue
            if op:
                ops[k] = op
            break
        else:
            results[k] = "SUBMIT_FAIL"
            continue

    # Poll until all done
    pending = dict(ops)
    start = time.time()
    while pending and time.time() - start < 600:
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
            print(f"  chunk: {len(pending)} pending ({elapsed}s)...")
            time.sleep(15)
    for k in pending:
        results[k] = "TIMEOUT"


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = {}

    for i, group in enumerate(PAIR_GROUPS, 1):
        print(f"\n=== Batch {i}/{len(PAIR_GROUPS)}: {group} ===")
        process_chunk(group, results)
        # Stop-on-failure: abort if any failed to preserve credits
        batch_statuses = [results.get(k) for k in group]
        if any(s != "OK" for s in batch_statuses):
            print(f"\n!! Batch {i} had failures — aborting to preserve credits")
            print(f"   Batch results: {dict(zip(group, batch_statuses))}")
            break

    print("\n=== RESULTS ===")
    for group in PAIR_GROUPS:
        for k in group:
            print(f"  {k}: {results.get(k, 'NOT_RUN')}")
