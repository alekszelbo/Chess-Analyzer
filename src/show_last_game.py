import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def show_last_game():
    metadata = pd.read_csv(os.path.join(DATA_DIR, "metadata.csv"))
    moves = pd.read_csv(os.path.join(DATA_DIR, "moves.csv"))

    # Assume last row = most recent game
    last_game = metadata.iloc[-1]
    game_id = last_game["GameID"]

    print("♟ Last Played Game Metadata")
    print("=" * 40)
    for col, val in last_game.items():
        print(f"{col}: {val}")
    print("=" * 40)

    # Show moves for this game
    game_moves = moves[moves["GameID"] == game_id]
    print("Moves:")
    for _, row in game_moves.iterrows():
        print(f"{row['MoveNumber']}. {row['Move']}")

if __name__ == "__main__":
    show_last_game()
