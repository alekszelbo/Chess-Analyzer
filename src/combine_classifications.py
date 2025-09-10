import os
import pandas as pd
import yaml
from src.utils import (
    classify_time_of_day,
    classify_game_length,
    classify_result,
    rating_difference,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def enrich_data():
    metadata = pd.read_csv(os.path.join(DATA_DIR, "metadata.csv"))

    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    MY_USERNAME = config["username"]

    # Apply helper classifications
    metadata["TimeOfDay"] = metadata["UTC_Time"].apply(classify_time_of_day)
    metadata["GameLength"] = metadata["TotalMoves"].apply(classify_game_length)

    def classify_row(row):
        if row["White"] == MY_USERNAME:
            return classify_result(row["Result"], "white")
        elif row["Black"] == MY_USERNAME:
            return classify_result(row["Result"], "black")
        else:
            return None

    metadata["ResultClass"] = metadata.apply(classify_row, axis=1)

    def rating_diff_row(row):
        if row["White"] == MY_USERNAME:
            return rating_difference(int(row["WhiteElo"]), int(row["BlackElo"])) \
                if pd.notnull(row["WhiteElo"]) and pd.notnull(row["BlackElo"]) else None
        elif row["Black"] == MY_USERNAME:
            return rating_difference(int(row["BlackElo"]), int(row["WhiteElo"])) \
                if pd.notnull(row["WhiteElo"]) and pd.notnull(row["BlackElo"]) else None
        else:
            return None

    metadata["RatingDiff"] = metadata.apply(rating_diff_row, axis=1)

    # Save enriched dataset
    metadata.to_csv(os.path.join(DATA_DIR, "games.csv"), index=False)
    print("✅ Exported games.csv (enriched)")

if __name__ == "__main__":
    enrich_data()
