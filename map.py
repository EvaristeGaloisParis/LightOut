import pygame

from constantes import i__GRID__MAX_COL__, i__GRID__MAX_ID__, i__READER__


class Map:

    def __init__(self, idx: int, initial_value: int):
        self.__idx: int           = idx
        self.__initial_value: int = initial_value & i__READER__
        self.__current_value: int = initial_value & i__READER__
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
    def id(self) -> int:
        return self.__idx

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
        position = row * i__GRID__MAX_COL__ + col
        mask     = 1 << (i__GRID__MAX_ID__ - 1 - position)
        return bool(self.__current_value & mask)

    def change(self, x: int, y: int) -> None:
        position = x * i__GRID__MAX_COL__ + y
        mask     = 1 << (i__GRID__MAX_ID__ - 1 - position)
        self.__current_value ^= mask

    def is_finish(self) -> bool:
        return self.__current_value == 0
