import streamlit as st
import chess.pgn
import chess.svg

st.set_page_config(page_title="Chess Analyzer", layout="wide")

st.title("♟️ Chess Analyzer")
st.write("Upload a PGN file and visualize the game with metadata.")

uploaded_file = st.file_uploader("Upload PGN file", type=["pgn"])

if uploaded_file:
    game = chess.pgn.read_game(uploaded_file)

    if game:
        st.subheader("Game Metadata")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Event:**", game.headers.get("Event", "Unknown"))
            st.write("**Site:**", game.headers.get("Site", "Unknown"))
            st.write("**Date:**", game.headers.get("Date", "Unknown"))
            st.write("**Round:**", game.headers.get("Round", "Unknown"))

        with col2:
            st.write("**White:**", game.headers.get("White", "Unknown"))
            st.write("**Black:**", game.headers.get("Black", "Unknown"))
            st.write("**Result:**", game.headers.get("Result", "Unknown"))
            st.write("**ECO Opening:**", game.headers.get("ECO", "Unknown"))

        # Replay moves with a slider
        board = game.board()
        moves = list(game.mainline_moves())
        move_number = st.slider("Move number", 0, len(moves), 0)

        for i in range(move_number):
            board.push(moves[i])

        st.subheader("Board Position")
        st.image(chess.svg.board(board=board, size=400))

