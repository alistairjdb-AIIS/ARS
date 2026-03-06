#!/usr/bin/env python3
"""
Nonogram solver/validator.

Provides:
1. Clue computation from a binary grid.
2. Line-solvability check via alternating H/V sweeps (SIMPLE-SOLVER).
3. Uniqueness check via constraint propagation + backtracking.
4. Sweep count (difficulty metric).

Based on Batenburg & Kosters (2012) difficulty classification.
"""

from itertools import product
from typing import Optional


def compute_clues(grid: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """Derive row and column clues from a binary solution grid."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    row_clues = []
    for r in range(rows):
        clue = []
        run = 0
        for c in range(cols):
            if grid[r][c] == 1:
                run += 1
            else:
                if run > 0:
                    clue.append(run)
                run = 0
        if run > 0:
            clue.append(run)
        row_clues.append(clue if clue else [0])

    col_clues = []
    for c in range(cols):
        clue = []
        run = 0
        for r in range(rows):
            if grid[r][c] == 1:
                run += 1
            else:
                if run > 0:
                    clue.append(run)
                run = 0
        if run > 0:
            clue.append(run)
        col_clues.append(clue if clue else [0])

    return row_clues, col_clues


# ---------- Line solver core ----------

def _generate_line_placements(clue: list[int], length: int) -> list[list[int]]:
    """Generate all valid placements for a clue within a line of given length.

    Returns list of lines where each line is a list of 0/1 values.
    """
    if clue == [0]:
        return [[0] * length]

    num_blocks = len(clue)
    # Minimum space needed: sum of blocks + gaps between them
    min_space = sum(clue) + (num_blocks - 1)
    if min_space > length:
        return []

    slack = length - min_space
    # Each placement is defined by the starting gap sizes
    # gap[0] + block[0] + gap[1](>=1) + block[1] + ... + gap[n]
    # We need num_blocks + 1 gaps, where internal gaps >= 1

    placements = []
    _place_recursive(clue, length, 0, 0, [0] * length, placements)
    return placements


def _place_recursive(
    clue: list[int],
    length: int,
    block_idx: int,
    pos: int,
    line: list[int],
    results: list[list[int]],
):
    """Recursively place blocks to generate all valid line arrangements."""
    if block_idx == len(clue):
        results.append(line[:])
        return

    block_size = clue[block_idx]
    remaining_blocks = clue[block_idx + 1:]
    remaining_space = sum(remaining_blocks) + len(remaining_blocks)

    max_start = length - block_size - remaining_space
    for start in range(pos, max_start + 1):
        new_line = line[:]
        for i in range(start, start + block_size):
            new_line[i] = 1
        next_pos = start + block_size + 1  # +1 for mandatory gap
        _place_recursive(clue, length, block_idx + 1, next_pos, new_line, results)


def _solve_line(clue: list[int], known: list[Optional[int]]) -> list[Optional[int]]:
    """Given a clue and partially known line, return the intersection of all
    valid placements consistent with the known cells.

    known[i] = 0 (empty), 1 (filled), or None (unknown).
    Returns updated known line. If no valid placement exists, returns None.
    """
    length = len(known)
    placements = _generate_line_placements(clue, length)

    # Filter placements consistent with known cells
    valid = []
    for p in placements:
        consistent = True
        for i in range(length):
            if known[i] is not None and known[i] != p[i]:
                consistent = False
                break
        if consistent:
            valid.append(p)

    if not valid:
        return None  # Contradiction

    # Intersect: cell is determined if all valid placements agree
    result = list(known)
    for i in range(length):
        if result[i] is not None:
            continue
        values = {p[i] for p in valid}
        if len(values) == 1:
            result[i] = values.pop()

    return result


def line_solve(
    row_clues: list[list[int]],
    col_clues: list[list[int]],
) -> tuple[list[list[Optional[int]]], int]:
    """Attempt to solve a nonogram using only line-solving (alternating sweeps).

    Returns (grid, sweep_count) where grid cells are 0, 1, or None (unsolved).
    sweep_count = number of complete H+V sweep passes.
    """
    rows = len(row_clues)
    cols = len(col_clues)

    # Initialize unknown grid
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    sweep_count = 0
    max_sweeps = rows + cols  # Safety limit

    while sweep_count < max_sweeps:
        changed = False
        sweep_count += 1

        # Horizontal sweep (rows)
        for r in range(rows):
            known = grid[r]
            result = _solve_line(row_clues[r], known)
            if result is None:
                return grid, sweep_count  # Contradiction
            if result != known:
                grid[r] = result
                changed = True

        # Vertical sweep (columns)
        for c in range(cols):
            known = [grid[r][c] for r in range(rows)]
            result = _solve_line(col_clues[c], known)
            if result is None:
                return grid, sweep_count
            if result != known:
                for r in range(rows):
                    grid[r][c] = result[r]
                changed = True

        if not changed:
            break

    return grid, sweep_count


def is_line_solvable(
    row_clues: list[list[int]],
    col_clues: list[list[int]],
) -> tuple[bool, int]:
    """Check if a puzzle is fully solvable by line-solving alone.

    Returns (solvable, sweep_count).
    """
    grid, sweeps = line_solve(row_clues, col_clues)
    solved = all(
        grid[r][c] is not None
        for r in range(len(row_clues))
        for c in range(len(col_clues))
    )
    return solved, sweeps


def has_unique_solution(
    row_clues: list[list[int]],
    col_clues: list[list[int]],
) -> tuple[bool, Optional[list[list[int]]]]:
    """Check if the clue set has exactly one solution.

    Uses constraint propagation + backtracking.
    Returns (is_unique, solution_or_None).
    """
    rows = len(row_clues)
    cols = len(col_clues)

    solutions = []

    def solve_with_backtracking(grid: list[list[Optional[int]]]):
        if len(solutions) > 1:
            return  # Already found non-unique

        # Apply line solving first
        g = [row[:] for row in grid]
        changed = True
        while changed:
            changed = False
            for r in range(rows):
                result = _solve_line(row_clues[r], g[r])
                if result is None:
                    return  # Dead end
                if result != g[r]:
                    g[r] = result
                    changed = True
            for c in range(cols):
                known = [g[r][c] for r in range(rows)]
                result = _solve_line(col_clues[c], known)
                if result is None:
                    return
                if result != known:
                    for r in range(rows):
                        g[r][c] = result[r]
                    changed = True

        # Find first unknown cell
        unknown = None
        for r in range(rows):
            for c in range(cols):
                if g[r][c] is None:
                    unknown = (r, c)
                    break
            if unknown:
                break

        if unknown is None:
            # Fully solved
            solutions.append([row[:] for row in g])
            return

        r, c = unknown
        for val in (0, 1):
            g2 = [row[:] for row in g]
            g2[r][c] = val
            solve_with_backtracking(g2)
            if len(solutions) > 1:
                return

    initial = [[None] * cols for _ in range(rows)]
    solve_with_backtracking(initial)

    if len(solutions) == 1:
        return True, solutions[0]
    return False, None


def validate_puzzle(grid: list[list[int]]) -> dict:
    """Full validation of a puzzle grid.

    Returns dict with:
        - row_clues, col_clues
        - is_unique: bool
        - is_line_solvable: bool
        - sweep_count: int
        - difficulty: 'easy' | 'medium' | 'hard' | None
        - fill_ratio: float
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    row_clues, col_clues = compute_clues(grid)

    unique, _ = has_unique_solution(row_clues, col_clues)

    solvable = False
    sweeps = 0
    if unique:
        solvable, sweeps = is_line_solvable(row_clues, col_clues)

    filled = sum(cell for row in grid for cell in row)
    total = rows * cols
    fill_ratio = filled / total if total > 0 else 0

    difficulty = None
    if solvable and rows == 10 and cols == 10:
        if sweeps <= 4:
            difficulty = "easy"
        elif sweeps <= 7:
            difficulty = "medium"
        else:
            difficulty = "hard"

    return {
        "row_clues": row_clues,
        "col_clues": col_clues,
        "is_unique": unique,
        "is_line_solvable": solvable,
        "sweep_count": sweeps,
        "difficulty": difficulty,
        "fill_ratio": round(fill_ratio, 2),
        "grid_size": [rows, cols],
    }


# ---------- CLI ----------

if __name__ == "__main__":
    import json
    import sys

    # Test with a simple 5x5 heart
    heart = [
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]

    print("Testing solver with 5x5 heart pattern...")
    result = validate_puzzle(heart)
    print(json.dumps(result, indent=2))

    # Test with the 10x10 apple from the pipeline spec
    apple = [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]

    print("\nTesting solver with 10x10 apple pattern...")
    result = validate_puzzle(apple)
    print(json.dumps(result, indent=2))
