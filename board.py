from typing import Optional
import json

from constantes import (
    st__MAPS_FILE__,
    i__GRID__MAX_ROW__,
    i__GRID__MAX_COL__,
    DBG_IS_ON,
)
from map import Map


def fmt_time(ms: int) -> str:
    """Formate des millisecondes en mm:ss."""
    s = ms // 1000
    return f'{s // 60:02d}:{s % 60:02d}'


class Board:

    @staticmethod
    def __loads_maps() -> dict[int, int]:
        with open(st__MAPS_FILE__, mode="r") as f:
            values: dict[int, int] = json.load(f)
        return {int(x): y for x, y in values.items()}

    def __init__(self):
        self.__maps:        dict[int, int] = Board.__loads_maps()
        self.__active:      Optional[Map]  = None
        self.__total_moves: int            = 0
        self.__total_light: int            = 0
        self.__total_ms:    int            = 0   # cumul temps des levels terminés

    @property
    def level(self) -> int:
        return self.__active.id

    @property
    def coups(self) -> str:
        m   = self.__total_moves + self.__active.moves
        l   = self.__total_light + self.__active.lighting
        ms  = self.__total_ms + (self.__active.elapsed_ms if self.__active else 0)
        return f'move: {m} - light: {l} - time: {fmt_time(ms)}'

    @property
    def coups_level(self) -> str:
        if self.__active is None:
            return 'move: 0 - light: 0 - time: 00:00'
        return f'move: {self.__active.moves} - light: {self.__active.lighting} - time: {fmt_time(self.__active.elapsed_ms)}'

    def push_map(self, idx: int) -> bool:
        if idx not in self.__maps:
            return False
        self.__active = Map(idx, self.__maps[idx])
        return True

    def start(self) -> bool:
        return self.push_map(1)

    def reset_level(self) -> bool:
        """Remet uniquement la disposition — coups et temps ne sont pas effacés."""
        return self.push_map(self.__active.id)

    def add_move(self) -> None:
        self.__active.add_coup(move=True, light=False)

    def is_on(self, row: int, col: int) -> bool:
        if self.__active is None:
            return False
        return self.__active.is_on(row, col)

    def high_light(self, row: int, col: int) -> None:
        self.__active.add_coup(move=False, light=True)
        for x in range(max(1, row - 1), 1 + min(i__GRID__MAX_ROW__, row + 1)):
            for y in range(max(1, col - 1), 1 + min(i__GRID__MAX_COL__, col + 1)):
                self.__active.change(x - 1, y - 1)

        if self.__active.is_finish() or DBG_IS_ON:
            self.__active.stop_timer()                      # fige le chrono avant tout
            self.__total_moves += self.__active.moves
            self.__total_light += self.__active.lighting
            self.__total_ms    += self.__active.elapsed_ms  # cumule le temps figé
            self.push_map(self.__active.id + 1)
