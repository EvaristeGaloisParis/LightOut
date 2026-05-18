from board import Board
from game_renderer import GameRenderer


if __name__ == '__main__':
    all_map: Board = Board()
    all_map.start()
    render = GameRenderer(all_map)
    render.run()
