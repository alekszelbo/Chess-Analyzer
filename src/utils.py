import pandas as pd
import chess

def classify_time_of_day(utc_time: str) -> str:
    try:
        hour = int(utc_time.split(":")[0])
    except Exception:
        return "Unknown"
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def classify_game_length(total_moves: int) -> str:
    if total_moves < 30:
        return "Short"
    elif total_moves < 60:
        return "Medium"
    return "Long"

def classify_result(result: str, color: str) -> str:
    if result == "1-0":
        return "Win" if color == "white" else "Loss"
    elif result == "0-1":
        return "Loss" if color == "white" else "Win"
    elif result == "1/2-1/2":
        return "Draw"
    else:
        return "Unknown"

def rating_difference(my_rating: int, opp_rating: int) -> int:
    return my_rating - opp_rating

def get_phase_score(board: chess.Board) -> int:
    material = sum(piece.piece_type for piece in board.piece_map().values())
    return material

def classify_phase(board: chess.Board) -> str:
    material = get_phase_score(board)
    if material > 60:
        return "Opening"
    elif material > 30:
        return "Middlegame"
    return "Endgame"

def evaluate_position_stockfish(board: chess.Board) -> dict:
    return {"cpl": None, "wpl": None}

def evaluate_position_lc0(board: chess.Board) -> dict:
    return {"wpl": None, "policy": None}
