#!/usr/bin/env python3
"""
Unified CLI for Conway's Game of Life.

• If --runs 1  → animated single board and a single output line.
• If --runs >1 → parallel batch, one output line per board.
• Results are appended to data/results.csv.
"""

import argparse
import csv
import multiprocessing as mp
import pathlib

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output, display

from src.life_core import run_until_collapse, life_step

OUT_PATH = pathlib.Path("data/results.csv")


def board_to_string(board: np.ndarray) -> str:
    return "".join("1" if x else "0" for x in board.flat)


def append_rows(rows: list[tuple[int, float, int, str]]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    new = not OUT_PATH.exists()
    with OUT_PATH.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["size", "prob", "cycles", "init_board"])
        w.writerows(rows)


def run_with_animation(size: int, prob: float) -> tuple[int, np.ndarray]:
    """
    Animate one board smoothly, stopping on extinction,
    still life (period-1) or 2-cycle (period-2).

    Returns
    -------
    cycles : int
    init_board : np.ndarray
    """
    board = np.random.rand(size, size) < prob
    init_board = board.copy()
    prev, prev2 = None, None
    cycles = 0

    fig, ax = plt.subplots(figsize=(4, 4))
    img = ax.imshow(board, cmap="binary")
    ax.axis("off")
    title = ax.set_title("Gen 0")
    display(fig)

    while True:
        next_board = life_step(board)
        cycles += 1

        img.set_data(next_board)
        title.set_text(f"Gen {cycles}")
        clear_output(wait=True)
        display(fig)

        if not next_board.any():
            return cycles, init_board
        if prev is not None and np.array_equal(next_board, prev):
            return cycles, init_board
        if prev2 is not None and np.array_equal(next_board, prev2):
            return cycles, init_board

        prev2, prev = prev, board
        board = next_board


def _one_run(args: tuple[int, float]) -> tuple[int, float, int, str]:
    size, prob = args
    cycles, init_board = run_until_collapse(size, prob)
    return size, prob, cycles, board_to_string(init_board)


def main() -> None:
    parser = argparse.ArgumentParser(description="Game-of-Life simulator")
    parser.add_argument("--size",    type=int,   default=50,
                        help="board side length")
    parser.add_argument("--prob",    type=float, default=0.2,
                        help="initial alive probability")
    parser.add_argument("--runs",    type=int,   default=1,
                        help="number of boards to run")
    parser.add_argument("--workers", type=int,   default=mp.cpu_count(),
                        help="parallel processes (runs > 1)")
    args = parser.parse_args()

    if args.runs == 1:
        cycles, init_board = run_with_animation(args.size, args.prob)
        print(f"prob={args.prob}  cycles={cycles}")
        append_rows([(args.size, args.prob, cycles, board_to_string(init_board))])
    else:
        with mp.Pool(args.workers) as pool:
            rows = pool.map(_one_run, [(args.size, args.prob)] * args.runs)
        for _, pr, cy, _ in rows:
            print(f"prob={pr}  cycles={cy}")
        append_rows(rows)


if __name__ == "__main__":
    main()
