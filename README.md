# game_of_life_sim

A Python simulator for Conway’s Game of Life.

## Description

This project offers two modes of use:

- **Local Execution:**  
  Run the simulation directly via the command-line interface (CLI) using the Python scripts in `src/` and `run_sim.py`.

- **Notebook Demo:**  
  Use the Jupyter notebook (`game_of_life_demo.ipynb`) in Colab or locally to see interactive animations. Note that Colab sessions are ephemeral; you must save or export your `data/results.csv` manually if you want to preserve results beyond the session.

## Features

**Inline GIF animation**  
  Run the simulation until collapse and export it as a self-contained GIF for smooth playback on any device.

- **Batch mode**  
  Run many simulations in parallel (via multiprocessing) and record  
  `size`, `prob`, `cycles`, and `init_board` to `data/results.csv`.

- **Command-line interface**  
  Run simulations locally with `run_sim.py` for flexible scripting and batch jobs.

## Requirements

- Python 3.8+  
- NumPy ≥1.25  
- Matplotlib ≥3.8  
- Imageio ≥ 2.9

Install with:

```bash
pip install -r requirements.txt
```

## Installation

```bash
git clone https://github.com/JayroMartinez/game_of_life_sim.git
cd game_of_life_sim
pip install -r requirements.txt
```

## Usage

### Local CLI

Run a single animated simulation in your terminal:

```bash
python run_sim.py --size 60 --prob 0.25
```

Run a headless batch of 10 000 boards:

```bash
python run_sim.py --runs 10000 --size 60 --prob 0.25 --workers 8
```

### Notebook Demo

Open `game_of_life_demo.ipynb` in Jupyter or Colab:

```bash
# In Colab:
https://colab.research.google.com/github/JayroMartinez/game_of_life_sim/blob/main/game_of_life_sim.ipynb
```

Then:
1. Run the setup cell to clone and install dependencies.  
2. Execute the animated and batch example cells.  
3. **Important:** Colab sessions are temporary. Download or push `data/results.csv` if you want to keep results beyond the session.

## Project Structure

```
game_of_life_sim/
├── data/                   # results.csv is saved here at runtime
├── src/
│   ├── __init__.py
│   └── life_core.py        # Core simulation logic
├── run_sim.py              # CLI entry point
├── requirements.txt        # Project dependencies
├── game_of_life_demo.ipynb # Jupyter demo (public)
└── README.md
```
