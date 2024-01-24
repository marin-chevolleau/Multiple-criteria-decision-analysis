# Multiple-criteria-decision-analysis

The aim of this project is to propose a turnkey implementation of the main multi-criteria decision-support tools.

## Requirements

### Python dependencies
- pandas
- typing
- networkx
- matplotlib

### Structure

## Files

├─ 🐍 dominance.py → find the dominant pareto solutions \
├─ 🐍 electre_1.py → plot ranking graph using [Electre 1](https://en.wikipedia.org/wiki/%C3%89LECTRE) method  \
├─ 📒 initial_solutions.csv → dummy dataset of cities to rank \
├─ 📜 README.md → This file \
├─ 🐍 satisfaction.py → find satisfying solutions according to the decision-maker needs \
├─ 🐍 topsis.py → rank solutions using [TOPSIS](https://en.wikipedia.org/wiki/TOPSIS) method  \
└─ 🐍 weighting.py → rank solutions using [weighted sum](https://en.wikipedia.org/wiki/Weighted_sum_model) method \