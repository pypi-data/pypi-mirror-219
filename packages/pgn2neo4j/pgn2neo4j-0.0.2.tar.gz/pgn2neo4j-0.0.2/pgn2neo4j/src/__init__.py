from .gameparser import read_games
from .gamehandler import handle_game

__version__ = "0.0.2"

def pgn2neo4j(path, driver, show_progress=False, max_depth=10, max_games=1000):
    """
    path: path to the pgn file
    driver: neo4j driver
    show_progress: show progress bar for uploading games
    max_depth: maximum depth of the game tree to be uploaded
    max_games: maximum number of games to be uploaded
    """
    with driver.session() as session:
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Position) REQUIRE p.fen IS UNIQUE")

    games = list(read_games(path))[:max_games]

    if show_progress:
        from tqdm import tqdm
        games = tqdm(games)

    for game in games:
        handle_game(driver, game, max_depth=max_depth)