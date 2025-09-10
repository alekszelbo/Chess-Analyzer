import os
import pandas as pd
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def export_weekly_json():
    metadata_path = os.path.join(DATA_DIR, "metadata.csv")
    moves_path = os.path.join(DATA_DIR, "moves.csv")

    if not os.path.exists(metadata_path) or not os.path.exists(moves_path):
        print("⚠️ Missing metadata.csv or moves.csv. Run parse_pgns.py first.")
        return

    metadata = pd.read_csv(metadata_path)
    moves = pd.read_csv(moves_path)

    # Parse dates
    metadata["Date"] = pd.to_datetime(metadata["Date"], errors="coerce")
    metadata["Week"] = metadata["Date"].dt.strftime("%Y-W%U")  # Year-Week bins

    weekly_data = {}

    for week, week_games in metadata.groupby("Week"):
        weekly_data[week] = []
        for _, game in week_games.iterrows():
            gid = game["GameID"]

            # Reconstruct PGN-like moves from moves.csv
            game_moves = moves[moves["GameID"] == gid]
            moves_list = [f"{row['MoveNumber']}. {row['Move']}" for _, row in game_moves.iterrows()]

            weekly_data[week].append({
                "GameID": int(gid),
                "Date": game["Date"].strftime("%Y-%m-%d") if pd.notnull(game["Date"]) else None,
                "White": game["White"],
                "Black": game["Black"],
                "Result": game["Result"],
                "Opening": game.get("Opening", None),
                "Site": game.get("Site", None),
                "Moves": moves_list,
            })

    out_path = os.path.join(DATA_DIR, "weekly_games.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(weekly_data, f, indent=2)

    print(f"✅ Exported weekly_games.json with {len(metadata)} games binned by week")

if __name__ == "__main__":
    export_weekly_json()
