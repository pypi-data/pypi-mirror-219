import chess.pgn

from .enums import ChessResult

def parse_game_result(result_string):
    if result_string == "1-0":
        return ChessResult.WHITE_WON
    elif result_string == "0-1":
        return ChessResult.BLACK_WON
    elif result_string == "1/2-1/2":
        return ChessResult.DRAWN_GAME
    else:
        return None

def read_games(path):
    pgn_file = open(path, "r")
    game = chess.pgn.read_game(pgn_file)
    while game is not None:
        yield game
        game = chess.pgn.read_game(pgn_file)