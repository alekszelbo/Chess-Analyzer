import os
import yaml
import pandas as pd

from src import import_games, parse_pgns, combine_classifications, quick_visuals

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def generate_report(username: str):
    games_path = os.path.join(DATA_DIR, "games.csv")
    if not os.path.exists(games_path):
        print("⚠️ No games.csv found. Skipping report.")
        return

    games = pd.read_csv(games_path)

    with open(os.path.join(DATA_DIR, "summary_report.txt"), "w") as f:
        f.write(f"♟ Chess Analyzer Report for {username}\n")
        f.write("=" * 50 + "\n\n")

        total_games = len(games)
        f.write(f"Total games: {total_games}\n\n")

        results = games["ResultClass"].value_counts()
        for res, count in results.items():
            f.write(f"{res}: {count}\n")
        if "Win" in results:
            winrate = results["Win"] / total_games * 100
            f.write(f"Overall winrate: {winrate:.1f}%\n\n")

        if "Opening" in games.columns:
            f.write("Top 5 Openings:\n")
            top_openings = games["Opening"].value_counts().head(5)
            for opening, count in top_openings.items():
                f.write(f"  {opening}: {count} games\n")

    print("📝 Summary report saved to data/summary_report.txt")

def main():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    username = config["username"]

    print(f"♟ Running Chess Analyzer for user: {username}")

    print("🌐 Importing games from Chess.com...")
    import_games.download_all_games()

    print("🔎 Parsing PGNs...")
    parse_pgns.parse_pgns()

    print("🧹 Combining classifications...")
    combine_classifications.enrich_data()

    print("📊 Generating visuals...")
    quick_visuals.make_visuals()

    print("📝 Generating summary report...")
    generate_report(username)

    print("✅ Pipeline complete! Check data/ for results.")

if __name__ == "__main__":
    main()
