import os
import pandas as pd
import chess.pgn

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def material_signature(board: chess.Board) -> str:
    """Return a simple material signature like 'KQ vs KR'."""
    white_pieces = []
    black_pieces = []
    piece_symbols = {
        chess.PAWN: "P",
        chess.KNIGHT: "N",
        chess.BISHOP: "B",
        chess.ROOK: "R",
        chess.QUEEN: "Q",
        chess.KING: "K",
    }
    for square, piece in board.piece_map().items():
        symbol = piece_symbols[piece.piece_type]
        if piece.color == chess.WHITE:
            white_pieces.append(symbol)
        else:
            black_pieces.append(symbol)
    return "K" + "".join(sorted([p for p in white_pieces if p != "K"])) + \
           " vs " + \
           "K" + "".join(sorted([p for p in black_pieces if p != "K"]))

def parse_pgns():
    metadata_rows = []
    moves_rows = []

    raw_dir = os.path.join(DATA_DIR, "raw_pgns")

    for fname in os.listdir(raw_dir):
        if not fname.endswith(".pgn"):
            continue
        with open(os.path.join(raw_dir, fname), "r", encoding="utf-8") as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break

                board = game.board()
                headers = game.headers
                moves = list(game.mainline_moves())

                game_id = len(metadata_rows) + 1

                # --- Track metadata from moves ---
                captures = 0
                checks = 0
                promotions = 0
                white_castled = False
                black_castled = False

                for move in moves:
                    if board.is_capture(move):
                        captures += 1
                    if board.gives_check(move):
                        checks += 1
                    if move.promotion:
                        promotions += 1
                    if move == chess.Move.from_uci("e1g1") or move == chess.Move.from_uci("e1c1"):
                        white_castled = True
                    if move == chess.Move.from_uci("e8g8") or move == chess.Move.from_uci("e8c8"):
                        black_castled = True
                    board.push(move)

                final_material = material_signature(board)

                # --- Metadata row ---
                metadata_rows.append({
                    "GameID": game_id,
                    "Event": headers.get("Event"),
                    "Site": headers.get("Site"),
                    "Date": headers.get("UTCDate"),
                    "UTC_Time": headers.get("UTCTime"),
                    "TimeControl": headers.get("TimeControl"),
                    "Result": headers.get("Result"),
                    "Termination": headers.get("Termination"),
                    "Variant": headers.get("Variant"),
                    "White": headers.get("White"),
                    "Black": headers.get("Black"),
                    "WhiteElo": headers.get("WhiteElo"),
                    "BlackElo": headers.get("BlackElo"),
                    "ECO": headers.get("ECO"),
                    "Opening": headers.get("Opening"),
                    "TotalMoves": len(moves),
                    "NumCaptures": captures,
                    "NumChecks": checks,
                    "Promotions": promotions,
                    "WhiteCastled": white_castled,
                    "BlackCastled": black_castled,
                    "FinalMaterial": final_material,
                })

                # --- Reset board to record moves with SAN + FEN ---
                board = game.board()
                for i, move in enumerate(moves, 1):
                    san = board.san(move)
                    board.push(move)
                    moves_rows.append({
                        "GameID": game_id,
                        "MoveNumber": i,
                        "Move": san,
                        "FEN": board.fen(),
                    })

    # Save clean CSVs
    pd.DataFrame(metadata_rows).to_csv(os.path.join(DATA_DIR, "metadata.csv"), index=False)
    pd.DataFrame(moves_rows).to_csv(os.path.join(DATA_DIR, "moves.csv"), index=False)

    print("✅ Exported metadata.csv and moves.csv with extra metadata")

if __name__ == "__main__":
    parse_pgns()
