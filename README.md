# Multiple-criteria-decision-analysis

The aim of this project is to propose a turnkey implementation of the main multi-criteria decision-support tools.

This project was created by Marin CHEVOLLEAU helped by Tristan MANIER.

## Requirements

### Python dependencies

- pandas
- typing
- networkx
- matplotlib

## Structure

### Files

├─ 📒 data → input datasets (example of cities to rank) \
├─ 📒 output → csv result files \
├─ 📜 README.md → This file \
├─ 🐍 criterion.py → criterion class \
├─ 🐍 normalize.py → normalize function \
├─ 🐍 dominance.py → find the dominant pareto solutions \
├─ 🐍 satisfaction.py → find satisfying solutions according to the decision-maker needs \
├─ 🐍 electre_1.py → plot ranking graph using [Electre 1](https://en.wikipedia.org/wiki/%C3%89LECTRE) method  \
├─ 🐍 topsis.py → rank solutions using [TOPSIS](https://en.wikipedia.org/wiki/TOPSIS) method  \
└─ 🐍 weighting.py → rank solutions using [weighted sum](https://en.wikipedia.org/wiki/Weighted_sum_model) method

## Execution

### Global

Run the main script `main.py`.
Uncomment lines to select the satisfaction or dominance method to use.

### Individual

First you need to run `python3 dominance.py` **OR** `python3 satisfaction.py`

Then you can use the following (independant) scripts:

- `python3 weighting.py`
- `python3 electre_1.py`
- `python3 electre_2.py`
- `python3 topsis.py`
