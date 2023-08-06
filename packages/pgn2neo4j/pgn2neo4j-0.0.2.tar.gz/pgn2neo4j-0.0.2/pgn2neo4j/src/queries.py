from .enums import ChessResult

def update_fen_node(neo4j_driver, fen, result):
    with neo4j_driver.session() as session:
        # Check if the node already exists based on the FEN
        query = """
        MERGE (n:Position {fen: $fen})
        ON CREATE SET n.blackWins = 0,
                        n.whiteWins = 0,
                        n.gamesPlayed = 0
        """
        session.run(query, fen=fen)

        # Update the node's properties based on the result
        update_query = """
        MATCH (n:Position {fen: $fen})
        SET n.blackWins = n.blackWins + $blackWins,
            n.whiteWins = n.whiteWins + $whiteWins,
            n.gamesPlayed = n.gamesPlayed + $gamesPlayed
        """
        black_wins = 0
        white_wins = 0
        games_played = 0
        
        if result == ChessResult.WHITE_WON:
            white_wins = 1
            games_played = 1
        elif result == ChessResult.BLACK_WON:
            black_wins = 1
            games_played = 1
        elif result == ChessResult.DRAWN_GAME:
            games_played = 1
        
        session.run(update_query, fen=fen, blackWins=black_wins, whiteWins=white_wins, gamesPlayed=games_played)

def add_move_between_nodes(neo4j_driver, prev_fen, fen, move):
    with neo4j_driver.session() as session:
        query = """
        MATCH (a:Position {fen: $prevFen}), (b:Position {fen: $fen})
        WHERE NOT EXISTS((a)-[:TO {move: $move}]->(b))
        CREATE (a)-[:TO {move: $move}]->(b)
        """
        session.run(query, prevFen=prev_fen, fen=fen, move=move)

