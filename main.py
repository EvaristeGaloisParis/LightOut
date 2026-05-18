from board import Board
from game_renderer import GameRenderer
from scores import Scores


if __name__ == '__main__':
    all_map: Board = Board()
    all_map.start()
    scores = Scores()
    render = GameRenderer(all_map, scores)
    render.run()
