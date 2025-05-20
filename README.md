# game_of_life_sim

A Python-based simulator for Conway’s Game of Life.  
Features both an animated, interactive single-board run and a high-throughput batch mode that logs results to CSV.

## Features

- **Interactive mode**  
  Animate one board in real time inside Jupyter/Colab.
- **Batch mode**  
  Run many simulations in parallel (via multiprocessing) and record  
  `size`, `prob`, `cycles`, and `init_board` to `data/results.csv`.
- **Portable CLI**  
  All logic lives in `src/life_core.py`; entry point is `run_sim.py`.
- **Demo notebook**  
  `game_of_life_demo.ipynb` shows how to clone, install, animate, and batch-run in Colab.

## Requirements

- Python 3.8+  
- NumPy ≥1.25  
- Matplotlib ≥3.8  

Install with:

```bash
pip install -r requirements.txt
```

## Installation

```bash
git clone https://github.com/<your-user>/game_of_life_sim.git
cd game_of_life_sim
pip install -r requirements.txt
```

## Usage

### Animated single run

In a terminal or Jupyter environment:

```bash
python run_sim.py --size 60 --prob 0.25
```

- `--size`   Board width/height (square).  
- `--prob`   Initial probability of a live cell (0–1).  

In Jupyter/Colab, for inline rendering use:

```python
%run -i run_sim.py --size 60 --prob 0.25
```

### Batch headless run

Run 10 000 boards in parallel and append results to `data/results.csv`:

```bash
python run_sim.py --runs 10000 --size 60 --prob 0.25 --workers 8
```

- `--runs`    Number of boards to simulate.  
- `--workers` Number of parallel processes (defaults to CPU core count).  

### Demo in Colab

Open [game_of_life_demo.ipynb](game_of_life_demo.ipynb) in Colab for a step-by-step guide.

## Project Structure

```
game_of_life_sim/
├── src/
│   ├── __init__.py
│   └── life_core.py       # Core simulation logic
├── run_sim.py             # CLI entry point
├── requirements.txt       # Project dependencies
├── game_of_life_demo.ipynb# Jupyter demo (public)
├── data/                  # results.csv is appended here
└── README.md
```

## License

This project is released under the MIT License.
