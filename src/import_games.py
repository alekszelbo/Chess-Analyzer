import os
import requests
import yaml
from tqdm import tqdm

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw_pgns")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

with open(CONFIG_FILE, "r") as f:
    config = yaml.safe_load(f)
USERNAME = config["username"].lower()

HEADERS = {"User-Agent": "ChessAnalyzer/1.0 (https://github.com/alekscottz)"}

def download_all_games():
    os.makedirs(RAW_DIR, exist_ok=True)
    base_url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"

    print(f"♟ Downloading games for {USERNAME}...")

    r = requests.get(base_url, headers=HEADERS)
    r.raise_for_status()
    archives = r.json()["archives"]

    for url in tqdm(archives, desc="Downloading archives"):
        year, month = url.split("/")[-2:]
        out_path = os.path.join(RAW_DIR, f"{USERNAME}_{year}_{month}.pgn")

        if os.path.exists(out_path):
            continue  # skip already downloaded

        resp = requests.get(url + "/pgn", headers=HEADERS)
        resp.raise_for_status()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(resp.text)

    print(f"✅ Finished downloading games into {RAW_DIR}")

if __name__ == "__main__":
    download_all_games()
