# Chess Analyzer

A Python-based toolkit for analyzing and visualizing chess games.  
The project supports importing games from Chess.com, parsing PGN files, extracting metadata, and generating visual reports.  
It also includes a Streamlit web application for interactive exploration of games.

---

## Features

- Import games from Chess.com or local PGN files  
- Extract and store metadata (players, event, opening, result, etc.)  
- Process move sequences and generate structured datasets  
- Create visual reports (win rate by color, performance by time control, etc.)  
- Streamlit web app for uploading and replaying PGN games with board visualization  

---

## Installation

Clone the repository and install dependencies:

```bash
git clone git@github.com:alekszelbo/chess-analyzer.git
cd chess-analyzer
pip install -r requirements.txt


chess-analyzer/
│
├── app.py                # Streamlit web app
├── config.yaml           # Configuration settings
├── requirements.txt      # Python dependencies
│
├── src/                  # Source code
│   ├── import_games.py
│   ├── parse_pgns.py
│   ├── combine_classifications.py
│   ├── run_all.py
│   ├── show_last_game.py
│   └── utils.py
│
├── data/                 # Data (raw PGNs, processed CSVs, reports)
│   ├── raw_pgns/
│   ├── processed/
│   └── metadata.csv
│
└── README.md             # Project documentation
