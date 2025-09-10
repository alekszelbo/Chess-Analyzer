# ♟ Chess Analyzer

A modular pipeline to parse, classify, and visualize Chess.com PGN games.

## 📂 Project Structure
chess-analyzer/
│── data/
│ ├── raw_pgns/ # downloaded PGN files
│ └── processed/ # output CSVs + plots
│── src/
│ ├── parse_pgns.py
│ ├── utils.py
│ ├── combine_classifications.py
│ ├── quick_visuals.py
│ └── run_all.py
│── requirements.txt
└── README.md

## 🚀 Usage
1. Place PGN files in `data/raw_pgns/`.
2. Run the pipeline:
```bash
cd ~/Desktop/chess-analyzer
source venv/bin/activate
python src/run_all.py
📊 Outputs
data/processed/games_summary.csv → enriched dataset (1 row per game).
data/processed/games_moves.csv → enriched dataset (1 row per move).
PNG plots in data/processed/.
🔧 Future Work
Engine evals (Stockfish/LC0): centipawn loss, win probability loss, move richness.
Phase-based accuracy analysis.
Interactive Streamlit dashboard.
