import pygame

from constantes import GRID_MAX_COL, GRID_MAX_ID, READER


class Map:

    def __init__(self, idx: int, initial_value: int):
        self.__level_id: int      = idx
        self.__initial_value: int = initial_value & READER
        self.__current_value: int = initial_value & READER
        self.__lighting: int      = 0
        self.__moves: int         = 0
        self.__start_ticks: int   = pygame.time.get_ticks()  # démarrage chrono level
        self.__elapsed_ms: int    = 0                         # temps figé à la fin
        self.__finished: bool     = False

    def add_coup(self, move: bool, light: bool) -> None:
        if move:
            self.__moves += 1
        if light:
            self.__lighting += 1

    def stop_timer(self) -> None:
        """Fige le chrono au moment de la résolution."""
        if not self.__finished:
            self.__elapsed_ms = pygame.time.get_ticks() - self.__start_ticks
            self.__finished   = True

    @property
    def level_id(self) -> int:
        return self.__level_id

    @property
    def moves(self) -> int:
        return self.__moves

    @property
    def lighting(self) -> int:
        return self.__lighting

    @property
    def elapsed_ms(self) -> int:
        """Temps écoulé : figé si terminé, courant sinon."""
        if self.__finished:
            return self.__elapsed_ms
        return pygame.time.get_ticks() - self.__start_ticks

    def is_on(self, row: int, col: int) -> bool:
        position = row * GRID_MAX_COL + col
        mask     = 1 << (GRID_MAX_ID - 1 - position)
        return bool(self.__current_value & mask)

    def change(self, row: int, col: int) -> None:
        position = row * GRID_MAX_COL + col
        mask     = 1 << (GRID_MAX_ID - 1 - position)
        self.__current_value ^= mask

    def is_finish(self) -> bool:
        return self.__current_value == 0
