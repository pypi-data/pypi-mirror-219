# pgn2neo4j
Convert a series of chess games in a PGN file to a Neo4j database.

The database contains Position nodes representing a board position, and Move relationships representing a move from one position to another.

Each Position node has a fen property containing the FEN representation of the position. Additionally, each node contains the following properties:
* whiteWins: the number of games won by white from this position
* blackWins: the number of games won by black from this position
* gamesPlayed: the total number of games played from this position