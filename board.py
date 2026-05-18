from typing import Optional
import json

from constantes import (
    MAPS_FILE,
    MAPS_FILE_DBG,
    GRID_MAX_ROW,
    GRID_MAX_COL,
    DBG_IS_ON,
)
from map import Map


def fmt_time(ms: int) -> str:
    """Formate des millisecondes en mm:ss."""
    s = ms // 1000
    return f'{s // 60:02d}:{s % 60:02d}'


class Board:

    def __init__(self, maps: dict[int, int]):
        self.__maps:        dict[int, int] = maps
        self.__active:      Optional[Map]  = None
        self.__total_moves: int            = 0
        self.__total_light: int            = 0
        self.__total_ms:    int            = 0   # cumul temps des levels terminés
        self.__won:         bool           = False

    @classmethod
    def from_file(cls) -> 'Board':
        """Charge les maps depuis le fichier par défaut (debug ou prod selon DBG_IS_ON)."""
        path = [MAPS_FILE, MAPS_FILE_DBG][DBG_IS_ON]
        with open(path, mode="r") as f:
            raw: dict[str, int] = json.load(f)
        return cls({int(k): v for k, v in raw.items()})

    @property
    def is_won(self) -> bool:
        return self.__won

    @property
    def total_moves(self) -> int:
        return self.__total_moves

    @property
    def total_lights(self) -> int:
        return self.__total_light

    @property
    def total_ms(self) -> int:
        return self.__total_ms

    @property
    def level(self) -> int:
        if self.__active is None:
            return 0
        return self.__active.level_id

    @property
    def coups(self) -> str:
        m  = self.__total_moves + (self.__active.moves      if self.__active else 0)
        l  = self.__total_light + (self.__active.lighting   if self.__active else 0)
        ms = self.__total_ms    + (self.__active.elapsed_ms if self.__active else 0)
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
        if self.__active is None:
            return False
        return self.push_map(self.__active.level_id)

    def reset_all(self) -> None:
        """Repart à zéro : totaux remis et niveau 1 chargé."""
        self.__total_moves = 0
        self.__total_light = 0
        self.__total_ms    = 0
        self.__won         = False
        self.push_map(1)

    def add_move(self) -> None:
        if self.__active is None:
            return
        self.__active.add_coup(move=True, light=False)

    def is_on(self, row: int, col: int) -> bool:
        if self.__active is None:
            return False
        return self.__active.is_on(row, col)

    def high_light(self, row: int, col: int) -> None:
        if self.__active is None:
            return

        self.__active.add_coup(move=False, light=True)
        for r in range(max(0, row - 1), min(GRID_MAX_ROW, row + 2)):
            for c in range(max(0, col - 1), min(GRID_MAX_COL, col + 2)):
                self.__active.change(r, c)

        if self.__active.is_finish() or DBG_IS_ON:
            self.__active.stop_timer()                      # fige le chrono avant tout
            self.__total_moves += self.__active.moves
            self.__total_light += self.__active.lighting
            self.__total_ms    += self.__active.elapsed_ms  # cumule le temps figé
            if not self.push_map(self.__active.level_id + 1):
                self.__active = None
                self.__won    = True
