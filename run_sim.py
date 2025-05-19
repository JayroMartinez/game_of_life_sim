#!/usr/bin/env python3
"""
Unified CLI for Conway's Game of Life.

• If --runs 1  → animated single board and a single output line.
• If --runs >1 → parallel batch, one output line per board.
• Results are appended to data/results.csv.
"""

from __future__ import annotations
import argparse, csv, multiprocessing as mp, pathlib, time
import numpy as np, matplotlib.pyplot as plt, IPython.display as dsp
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


# ----- animation helpers (runs == 1) -----
def _animate(board: np.ndarray, pause: float) -> None:
    dsp.clear_output(wait=True)
    plt.imshow(board, cmap="binary")
    plt.axis("off")
    plt.show()
    time.sleep(pause)


def run_with_animation(size: int, prob: float, pause: float) -> int:
    board = np.random.rand(size, size) < prob
    cycles = 0
    while True:
        _animate(board, pause)
        nxt = life_step(board)
        cycles += 1
        if not nxt.any() or np.array_equal(nxt, board):
            return cycles
        board = nxt


# ----- worker for multiprocessing (runs > 1) -----
def _one_run(args: tuple[int, float]) -> tuple[int, float, int, str]:
    size, prob = args
    cycles, init_board = run_until_collapse(size, prob)
    return size, prob, cycles, board_to_string(init_board)


def main() -> None:
    p = argparse.ArgumentParser(description="Game-of-Life simulator")
    p.add_argument("--size",     type=int,   default=50,  help="board side length")
    p.add_argument("--prob",     type=float, default=0.2, help="initial alive probability")
    p.add_argument("--runs",     type=int,   default=1,   help="number of boards to run")
    p.add_argument("--workers",  type=int,   default=mp.cpu_count(),
                   help="parallel processes (runs > 1)")
    p.add_argument("--pause",    type=float, default=0.1,
                   help="seconds between frames when runs == 1")
    args = p.parse_args()

    if args.runs == 1:                                 # animated single run
        cycles = run_with_animation(args.size, args.prob, args.pause)
        print(f"prob={args.prob}  cycles={cycles}")
        append_rows([(args.size, args.prob, cycles, "N/A")])
    else:                                              # parallel batch
        with mp.Pool(args.workers) as pool:
            rows = pool.map(_one_run, [(args.size, args.prob)] * args.runs)
        for _, pr, cy, _ in rows:
            print(f"prob={pr}  cycles={cy}")
        append_rows(rows)


if __name__ == "__main__":
    main()
