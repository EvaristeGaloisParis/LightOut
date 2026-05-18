from dataclasses import dataclass, asdict, field
from datetime import datetime
import json
import os

from constantes import SCORES_FILE


def _maintenant() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M')


@dataclass
class Score:
    nom:     str
    moves:   int
    lights:  int
    time_ms: int
    date:    str = field(default_factory=_maintenant)

    @property
    def key(self) -> tuple[int, int]:
        """Critère de tri : moins de coups d'abord, puis moins de temps."""
        return (self.moves, self.time_ms)


class Scores:

    def __init__(self):
        self.__scores: list[Score] = self.__load()

    @staticmethod
    def __load() -> list[Score]:
        if not os.path.exists(SCORES_FILE):
            return []
        with open(SCORES_FILE, mode="r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Score(**entry) for entry in raw]

    def __save(self) -> None:
        with open(SCORES_FILE, mode="w", encoding="utf-8") as f:
            json.dump([asdict(s) for s in self.__scores], f, indent=2, ensure_ascii=False)

    def add(self, score: Score) -> int:
        """Ajoute un score, persiste, retourne le rang 1-based."""
        self.__scores.append(score)
        self.__scores.sort(key=lambda s: s.key)
        self.__save()
        return self.__scores.index(score) + 1

    def top(self, n: int) -> list[Score]:
        return self.__scores[:n]
