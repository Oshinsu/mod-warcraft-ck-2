#!/usr/bin/env python3
"""
GoA Heroes of Azeroth — Asset Generation Pipeline
Reads SOTA JSON prompts, calls Replicate API, downloads directly to repo.
"""

import json
import os
import sys
import time
import glob
import requests

API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
API_URL = "https://api.replicate.com/v1/models/google/nano-banana-pro/predictions"
REPO_DIR = "/home/user/mod-warcraft-ck-2"
PROMPTS_DIR = os.path.join(REPO_DIR, "tools/prompts")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "wait",
}


def generate_one(json_path):
    """Generate a single asset from a JSON prompt file."""
    with open(json_path) as f:
        data = json.load(f)

    asset_id = data["meta"]["asset_id"]
    target_path = os.path.join(REPO_DIR, data["meta"]["target_path"])
    aspect_ratio = data["parameters"]["aspect_ratio"]
    positive = data["prompt_construction"]["positive"]

    # Skip if already exists
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        size_mb = os.path.getsize(target_path) / 1024 / 1024
        print(f"  [SKIP] {asset_id} — already exists ({size_mb:.1f}MB)")
        return "skip"

    # Ensure output directory
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    print(f"  [GEN]  {asset_id} ({aspect_ratio})...", end="", flush=True)

    payload = {
        "input": {
            "prompt": positive,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
        }
    }

    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=300)
        result = resp.json()

        if result.get("status") == "failed":
            print(f" FAIL: {result.get('error', 'unknown')}")
            return "fail"

        output = result.get("output", "")
        if isinstance(output, list):
            output = output[0] if output else ""

        if not output:
            print(f" FAIL: no output URL (status={result.get('status')})")
            # Debug: show what went wrong
            if result.get("error"):
                print(f"         Error: {result['error']}")
            return "fail"

        # Download image
        img_resp = requests.get(output, timeout=60)
        with open(target_path, "wb") as f:
            f.write(img_resp.content)

        size_mb = os.path.getsize(target_path) / 1024 / 1024
        print(f" OK ({size_mb:.1f}MB)")
        return "ok"

    except requests.exceptions.Timeout:
        print(" FAIL: timeout")
        return "fail"
    except Exception as e:
        print(f" FAIL: {e}")
        return "fail"


def main():
    print("=" * 60)
    print("  GoA Heroes of Azeroth — SOTA Asset Generation")
    print("=" * 60)

    # Collect all JSON prompt files
    categories = sorted(glob.glob(os.path.join(PROMPTS_DIR, "*")))
    all_prompts = []

    for cat_dir in categories:
        if not os.path.isdir(cat_dir):
            continue
        cat_name = os.path.basename(cat_dir)
        jsons = sorted(glob.glob(os.path.join(cat_dir, "*.json")))
        if jsons:
            all_prompts.append((cat_name, jsons))

    total = sum(len(js) for _, js in all_prompts)
    print(f"\n  Found {total} prompts across {len(all_prompts)} categories\n")

    stats = {"ok": 0, "fail": 0, "skip": 0}
    count = 0

    for cat_name, jsons in all_prompts:
        print(f"\n{'━' * 60}")
        print(f"  {cat_name} ({len(jsons)} prompts)")
        print(f"{'━' * 60}\n")

        for json_path in jsons:
            count += 1
            result = generate_one(json_path)
            stats[result] = stats.get(result, 0) + 1

            # Small delay between API calls to be polite
            if result == "ok":
                time.sleep(1)

    print(f"\n{'=' * 60}")
    print(f"  COMPLETE: {stats['ok']} ok / {stats['fail']} fail / {stats['skip']} skip / {total} total")
    print(f"{'=' * 60}\n")

    # List generated files
    print("Generated files:")
    for root, dirs, files in os.walk(os.path.join(REPO_DIR, "GoA_Heroes_of_Azeroth/gfx")):
        for f in sorted(files):
            if f.endswith(".png"):
                path = os.path.join(root, f)
                size = os.path.getsize(path) / 1024 / 1024
                print(f"  {size:.1f}MB  {os.path.relpath(path, REPO_DIR)}")


if __name__ == "__main__":
    main()
