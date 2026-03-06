#!/usr/bin/env python3
"""
Prepare puzzles for the game by selecting a balanced set and creating
a daily puzzle index.
"""

import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def load_puzzles(puzzle_dir: str) -> list[dict]:
    """Load all puzzle JSON files from a directory."""
    puzzles = []
    for f in sorted(Path(puzzle_dir).glob("*.json")):
        if f.name.startswith("_"):
            continue
        with open(f) as fh:
            puzzle = json.load(fh)
            puzzle["_filename"] = f.name
            puzzles.append(puzzle)
    return puzzles


def select_balanced_set(
    puzzles: list[dict],
    total: int = 180,
    difficulty_mix: dict = None,
) -> list[dict]:
    """Select a balanced set of puzzles across difficulties and categories."""
    if difficulty_mix is None:
        # Target: 40% easy, 45% medium, 15% hard
        difficulty_mix = {"easy": 0.40, "medium": 0.45, "hard": 0.15}

    by_diff = {"easy": [], "medium": [], "hard": []}
    for p in puzzles:
        d = p.get("difficulty", "easy")
        if d in by_diff:
            by_diff[d].append(p)

    selected = []
    for diff, ratio in difficulty_mix.items():
        count = int(total * ratio)
        pool = by_diff[diff]
        # Prioritize category diversity
        by_cat = {}
        for p in pool:
            cat = p.get("category", "misc")
            by_cat.setdefault(cat, []).append(p)

        picked = []
        cats = list(by_cat.keys())
        idx = 0
        while len(picked) < count and any(by_cat.values()):
            cat = cats[idx % len(cats)]
            if by_cat.get(cat):
                picked.append(by_cat[cat].pop(0))
            idx += 1
            # Remove empty categories
            cats = [c for c in cats if by_cat.get(c)]

        selected.extend(picked)

    return selected[:total]


def assign_dates(puzzles: list[dict], start_date: str = None) -> list[dict]:
    """Assign daily dates to puzzles following the difficulty curve."""
    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")

    start = datetime.strptime(start_date, "%Y-%m-%d")

    # Sort by difficulty for the curve:
    # Days 1-7: easy only
    # Days 8-30: easy + medium
    # Days 31+: rotate easy/medium/hard
    easy = [p for p in puzzles if p["difficulty"] == "easy"]
    medium = [p for p in puzzles if p["difficulty"] == "medium"]
    hard = [p for p in puzzles if p["difficulty"] == "hard"]

    scheduled = []

    for day in range(len(puzzles)):
        date = (start + timedelta(days=day)).strftime("%Y-%m-%d")

        if day < 7:
            # Easy only
            if easy:
                p = easy.pop(0)
            elif medium:
                p = medium.pop(0)
            else:
                break
        elif day < 30:
            # Alternate easy/medium
            if day % 2 == 0 and easy:
                p = easy.pop(0)
            elif medium:
                p = medium.pop(0)
            elif easy:
                p = easy.pop(0)
            else:
                break
        else:
            # Rotate: easy Mon, medium Wed, hard Fri, mix others
            weekday = (start + timedelta(days=day)).weekday()
            if weekday == 4 and hard:  # Friday
                p = hard.pop(0)
            elif weekday == 2 and medium:  # Wednesday
                p = medium.pop(0)
            elif easy:
                p = easy.pop(0)
            elif medium:
                p = medium.pop(0)
            elif hard:
                p = hard.pop(0)
            else:
                break

        p["id"] = date
        scheduled.append(p)

    return scheduled


def export_for_game(puzzles: list[dict], output_dir: str):
    """Export puzzles to the game's puzzle directory."""
    os.makedirs(output_dir, exist_ok=True)

    index = []
    for p in puzzles:
        # Remove internal fields
        export = {k: v for k, v in p.items() if not k.startswith("_")}

        filename = f"{p['id']}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(export, f)  # Compact for production

        index.append(filename)

    # Write index file
    with open(os.path.join(output_dir, "index.json"), "w") as f:
        json.dump(index, f)

    print(f"Exported {len(puzzles)} puzzles to {output_dir}")
    print(f"Date range: {puzzles[0]['id']} to {puzzles[-1]['id']}")

    # Difficulty breakdown
    diffs = {}
    for p in puzzles:
        d = p.get("difficulty", "unknown")
        diffs[d] = diffs.get(d, 0) + 1
    print(f"Difficulty: {diffs}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Directory of validated puzzle JSONs")
    parser.add_argument("output_dir", help="Game puzzle directory")
    parser.add_argument("--count", type=int, default=180)
    parser.add_argument("--start-date", default=None)
    args = parser.parse_args()

    puzzles = load_puzzles(args.input_dir)
    print(f"Loaded {len(puzzles)} puzzles")

    selected = select_balanced_set(puzzles, total=args.count)
    print(f"Selected {len(selected)} balanced puzzles")

    scheduled = assign_dates(selected, start_date=args.start_date)
    print(f"Scheduled {len(scheduled)} puzzles")

    export_for_game(scheduled, args.output_dir)
