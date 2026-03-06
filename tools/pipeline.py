#!/usr/bin/env python3
"""
Image-to-puzzle converter pipeline.

Converts SVG/PNG images to validated 10x10 nonogram puzzles.
Pipeline: render → grayscale → threshold → downsample → cleanup → validate → classify.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageFilter

from solver import compute_clues, validate_puzzle

# Categories inferred from Twemoji Unicode codepoint ranges
EMOJI_CATEGORIES = {
    "face": (0x1F600, 0x1F64F),
    "hand": (0x1F440, 0x1F4A0),
    "animal": (0x1F400, 0x1F43F),
    "food": (0x1F345, 0x1F37F),
    "travel": (0x1F680, 0x1F6FF),
    "nature": (0x1F300, 0x1F33F),
    "sport": (0x1F3C0, 0x1F3CF),
    "object": (0x1F4A0, 0x1F4FF),
    "symbol": (0x2600, 0x26FF),
    "weather": (0x1F324, 0x1F32D),
    "vehicle": (0x1F680, 0x1F6C5),
    "music": (0x1F3A0, 0x1F3BF),
    "clothing": (0x1F451, 0x1F462),
}


def categorize_emoji(filename: str) -> str:
    """Guess category from Unicode codepoint in filename."""
    name = filename.replace(".svg", "").replace(".png", "")
    # Handle compound codepoints (e.g., 1f1e6-1f1e8)
    parts = name.split("-")
    try:
        cp = int(parts[0], 16)
    except ValueError:
        return "misc"

    for cat, (lo, hi) in EMOJI_CATEGORIES.items():
        if lo <= cp <= hi:
            return cat
    return "misc"


def svg_to_png(svg_path: str, size: int = 64) -> Image.Image:
    """Render SVG to PNG at given size using rsvg-convert or cairosvg fallback."""
    # Try rsvg-convert first (fast)
    try:
        result = subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size), svg_path],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            import io
            return Image.open(io.BytesIO(result.stdout)).convert("RGBA")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: use cairosvg
    try:
        import cairosvg
        import io
        png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
        return Image.open(io.BytesIO(png_data)).convert("RGBA")
    except ImportError:
        pass

    # Last resort: Pillow direct (limited SVG support)
    raise RuntimeError(
        f"Cannot render SVG. Install rsvg-convert (apt install librsvg2-bin) "
        f"or cairosvg (pip install cairosvg)."
    )


def image_to_binary_grid(
    img: Image.Image,
    grid_size: int = 10,
    threshold: float = 0.5,
) -> list[list[int]]:
    """Convert image to binary grid at target resolution.

    Steps: composite on white → grayscale → downsample → threshold → cleanup.
    """
    # Composite RGBA onto white background
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img)
        img = bg.convert("L")
    else:
        img = img.convert("L")

    # Downsample to grid_size using area averaging (LANCZOS for quality)
    img = img.resize((grid_size, grid_size), Image.LANCZOS)

    # Apply threshold: dark pixels → filled (1), light → empty (0)
    grid = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            pixel = img.getpixel((x, y))
            # Invert: low pixel value = dark = filled
            row.append(1 if pixel < (threshold * 255) else 0)
        grid.append(row)

    return grid


def cleanup_grid(grid: list[list[int]]) -> list[list[int]]:
    """Remove isolated single pixels (noise from downsampling)."""
    rows = len(grid)
    cols = len(grid[0])
    result = [row[:] for row in grid]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                # Check if isolated (no filled neighbors)
                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbors.append(grid[nr][nc])
                if sum(neighbors) == 0:
                    result[r][c] = 0

    return result


def get_dominant_color(img: Image.Image) -> str:
    """Extract the dominant non-white, non-transparent color as hex."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = list(img.convert("RGBA").getdata())
    color_counts = {}

    for r, g, b, a in pixels:
        if a < 128:  # Skip transparent
            continue
        if r > 240 and g > 240 and b > 240:  # Skip near-white
            continue
        # Quantize to reduce color space
        qr, qg, qb = (r // 32) * 32, (g // 32) * 32, (b // 32) * 32
        key = (qr, qg, qb)
        color_counts[key] = color_counts.get(key, 0) + 1

    if not color_counts:
        return "#000000"

    dominant = max(color_counts, key=color_counts.get)
    return f"#{dominant[0]:02X}{dominant[1]:02X}{dominant[2]:02X}"


def process_image(
    image_path: str,
    grid_size: int = 10,
    threshold: float = 0.5,
    title: str = None,
    source: str = "twemoji",
    source_license: str = "CC-BY-4.0",
) -> dict | None:
    """Process a single image through the full pipeline.

    Returns puzzle dict if valid, None if rejected.
    """
    path = Path(image_path)

    # Load image
    if path.suffix.lower() == ".svg":
        try:
            img = svg_to_png(str(path), size=64)
        except RuntimeError:
            return None
    else:
        try:
            img = Image.open(str(path)).convert("RGBA")
        except Exception:
            return None

    # Get dominant color before grayscale conversion
    filled_color = get_dominant_color(img)

    # Convert to binary grid
    grid = image_to_binary_grid(img, grid_size, threshold)

    # Cleanup isolated pixels
    grid = cleanup_grid(grid)

    # Check fill ratio bounds
    filled = sum(cell for row in grid for cell in row)
    total = grid_size * grid_size
    fill_ratio = filled / total

    if fill_ratio < 0.15 or fill_ratio > 0.85:
        return None  # Too sparse or too dense

    # Validate
    validation = validate_puzzle(grid)

    if not validation["is_unique"]:
        return None

    if not validation["is_line_solvable"]:
        return None

    # Build puzzle dict
    if title is None:
        title = path.stem

    category = categorize_emoji(path.name)

    puzzle = {
        "id": None,  # Assigned during scheduling
        "title": title,
        "category": category,
        "difficulty": validation["difficulty"],
        "grid_size": [grid_size, grid_size],
        "fill_ratio": validation["fill_ratio"],
        "sweep_count": validation["sweep_count"],
        "solution": grid,
        "row_clues": validation["row_clues"],
        "col_clues": validation["col_clues"],
        "source": source,
        "source_license": source_license,
        "image_colors": {
            "filled": filled_color,
            "background": "#FFFFFF",
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return puzzle


def batch_process(
    input_dir: str,
    output_dir: str,
    grid_size: int = 10,
    thresholds: list[float] = None,
    limit: int = 0,
) -> dict:
    """Process a directory of images through the pipeline.

    Tries multiple thresholds per image and picks the best valid result.
    Returns stats dict.
    """
    if thresholds is None:
        thresholds = [0.4, 0.5, 0.6]

    os.makedirs(output_dir, exist_ok=True)

    input_path = Path(input_dir)
    extensions = {".svg", ".png", ".jpg", ".jpeg"}
    files = sorted([
        f for f in input_path.iterdir()
        if f.suffix.lower() in extensions
    ])

    if limit > 0:
        files = files[:limit]

    stats = {
        "total_input": len(files),
        "valid": 0,
        "rejected_fill_ratio": 0,
        "rejected_not_unique": 0,
        "rejected_not_line_solvable": 0,
        "rejected_error": 0,
        "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
        "by_category": {},
    }

    puzzles = []

    for i, filepath in enumerate(files):
        if (i + 1) % 100 == 0:
            print(f"Processing {i + 1}/{len(files)}...", file=sys.stderr)

        best_puzzle = None

        for threshold in thresholds:
            puzzle = process_image(
                str(filepath),
                grid_size=grid_size,
                threshold=threshold,
            )
            if puzzle is not None:
                # Prefer medium difficulty, then easy, then hard
                if best_puzzle is None:
                    best_puzzle = puzzle
                elif puzzle["difficulty"] == "medium" and best_puzzle["difficulty"] != "medium":
                    best_puzzle = puzzle
                elif puzzle["difficulty"] == "easy" and best_puzzle["difficulty"] == "hard":
                    best_puzzle = puzzle
                break  # Use first valid threshold

        if best_puzzle is not None:
            stats["valid"] += 1
            diff = best_puzzle["difficulty"] or "unknown"
            if diff in stats["by_difficulty"]:
                stats["by_difficulty"][diff] += 1
            cat = best_puzzle["category"]
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1

            # Save individual puzzle JSON
            out_file = Path(output_dir) / f"{filepath.stem}.json"
            with open(out_file, "w") as f:
                json.dump(best_puzzle, f, indent=2)

            puzzles.append(best_puzzle)

    stats["yield_rate"] = round(stats["valid"] / stats["total_input"], 3) if stats["total_input"] > 0 else 0

    # Save stats
    with open(Path(output_dir) / "_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nPipeline complete:", file=sys.stderr)
    print(f"  Input: {stats['total_input']}", file=sys.stderr)
    print(f"  Valid: {stats['valid']}", file=sys.stderr)
    print(f"  Yield: {stats['yield_rate']:.1%}", file=sys.stderr)
    print(f"  Difficulty: {stats['by_difficulty']}", file=sys.stderr)
    print(f"  Categories: {stats['by_category']}", file=sys.stderr)

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Nonogram puzzle pipeline")
    parser.add_argument("input_dir", help="Directory of source images")
    parser.add_argument("output_dir", help="Directory for puzzle JSON output")
    parser.add_argument("--grid-size", type=int, default=10)
    parser.add_argument("--limit", type=int, default=0, help="Limit number of images to process")
    parser.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        default=[0.4, 0.5, 0.6],
    )

    args = parser.parse_args()
    batch_process(
        args.input_dir,
        args.output_dir,
        grid_size=args.grid_size,
        thresholds=args.thresholds,
        limit=args.limit,
    )
