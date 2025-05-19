"""
Pure NumPy implementation of Conway's Game of Life (toroidal board).
No I/O, no plotting.
"""

from __future__ import annotations
import numpy as np
import zlib

__all__ = ["life_step", "run_until_collapse"]

def life_step(board: np.ndarray) -> np.ndarray:
    """Return the next generation of the board."""
    neighbours = sum(
        np.roll(np.roll(board, dy, 0), dx, 1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if (dy, dx) != (0, 0)
    )
    return (neighbours == 3) | (board & (neighbours == 2))


def _hash(board: np.ndarray) -> int:
    """CRC32 hash used for cycle detection."""
    return zlib.crc32(board.tobytes())


def run_until_collapse(size: int = 50,
                       prob: float = 0.2) -> tuple[int, np.ndarray]:
    """
    Simulate a random board until it collapses
    (extinction or any repeating state).

    Returns
    -------
    cycles : int
        Number of generations lived.
    init_board : np.ndarray
        The initial configuration.
    """
    board = np.random.rand(size, size) < prob
    init_board = board.copy()
    seen = {_hash(board)}
    cycles = 0

    while True:
        board = life_step(board)
        cycles += 1
        if not board.any():                # extinction
            return cycles, init_board
        h = _hash(board)
        if h in seen:                      # any cycle length
            return cycles, init_board
        seen.add(h)
