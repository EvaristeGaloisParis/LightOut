from typing import Optional, Final
import json
from dataclasses import dataclass
import pygame
import sys

st__MAPS_FILE__: Final[str] = r'maps/maps.json'
i__GRID__MAX_ROW__: Final[int] = 5
i__GRID__MAX_COL__: Final[int] = 5
i__GRID__MAX_ID__: Final[int] = i__GRID__MAX_ROW__ * i__GRID__MAX_COL__

# ─── Couleurs ─────────────────────────────────────────────────────────────────

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
JAUNE = (255, 240, 50)
BLEU_ELECTRIQUE = (30, 80, 255)
GRIS_TEXTE = (180, 180, 180)

# ─── Dimensions ───────────────────────────────────────────────────────────────

FENETRE_L = 520
FENETRE_H = 620
ZONE_TEXTE_H = 80  # hauteur de la zone d'info en haut
MARGE = 20  # marge autour de la grille
EPAISSEUR_MUR = 4  # épaisseur des traits de grille
EPAISSEUR_ACTIF = 14  # épaisseur du contour jaune de la case active

# Taille d'une case calculée dynamiquement
GRILLE_L = FENETRE_L - 2 * MARGE
GRILLE_H = FENETRE_H - ZONE_TEXTE_H - 2 * MARGE
CASE_L = GRILLE_L // i__GRID__MAX_COL__
CASE_H = GRILLE_H // i__GRID__MAX_ROW__


@dataclass
class Position:
    row: int
    col: int

class Map:

    def __init__(self, idx: int, initial_value: int):
        self.__idx: int = idx
        self.__initial_value: int = initial_value
        self.__current_value: int = initial_value

    @property
    def id(self) -> int:
        return self.__idx


    def __mask_to_position(self, mask: int, pow: int) -> Optional[Position]:

        if mask & (mask-1) > 0: return None

        row = pow // i__GRID__MAX_ROW__
        col = pow - row * i__GRID__MAX_ROW__

        return Position(row + 1, col + 1)

    def is_on(self, row: int, col: int) -> bool:
        """Renvoie True si la case (row, col) est allumée (0-indexé)."""
        position = row * i__GRID__MAX_COL__ + col
        mask = 1 << (i__GRID__MAX_ID__ - 1 - position)
        return bool(self.__current_value & mask)

    def change(self, x: int, y: int):

        position = x * i__GRID__MAX_COL__ + y
        mask = 1 << (i__GRID__MAX_ID__ - 1 - position)


        self.__current_value ^= mask

    def blit(self) -> None:

        mask: int = 1
        for i in range(i__GRID__MAX_ID__):
            if (i % i__GRID__MAX_ROW__) == 0:
                print("\n")
                print("----------\n")

            if self.__current_value & mask:
                pos = self.__mask_to_position(mask=mask, pow=i)
                print("x|", end="")
            else:
                print(" |", end="")

            mask += mask


class Board:
    @staticmethod
    def __loads_maps() -> dict[int, int]:
        values: dict[int, int] = json.load(open(st__MAPS_FILE__, mode="r"))
        return {int(x): y for x, y in values.items()}

    def __init__(self):

        self.__maps: dict[int, int] = Board.__loads_maps()
        self.__active: Optional[Map] = None
        self.__coups: int = 0
        self.__coups_level: int = 0

    @property
    def level(self) -> int:
        return self.__active.id

    @property
    def coups(self) -> int:
        return self.__coups

    @property
    def coups_level(self) -> int:
        return self.__coups_level

    def push_map(self, idx: int) -> bool:

        if not idx in self.__maps: return False

        self.__active = Map(idx, self.__maps[idx])
        return True

    def start(self) -> bool:
        self.push_map(1)
        return True

    def reset_level(self) -> bool:
        idx = self.__active.id
        self.push_map(idx=idx)
        return True

    def draw(self) -> bool:
        self.__active.blit()
        return True

    def is_on(self, row: int, col: int) -> bool:
        if self.__active is None:
            return False
        return self.__active.is_on(row, col)

    def high_light(self, row: int, col: int) -> None:

        for x in range(max(1, row-1), 1 + min(i__GRID__MAX_ROW__, row + 1)):
            for y in range(max(1, col - 1), 1 + min(i__GRID__MAX_COL__, col + 1)):
                self.__active.change(x-1, y-1)

class GameRenderer:

    def __init__(self, board: Board):
        pygame.init()
        self.board = board
        self.fenetre = pygame.display.set_mode((FENETRE_L, FENETRE_H))
        pygame.display.set_caption('Grid Game')
        self.horloge = pygame.time.Clock()
        self.fonte_titre = pygame.font.SysFont('monospace', 22, bold=True)
        self.fonte_info = pygame.font.SysFont('monospace', 16)

        # Case active (0-indexé)
        self.active_row: int = 0
        self.active_col: int = 0

    def _case_rect(self, row: int, col: int) -> pygame.Rect:
        """Renvoie le Rect pygame de la case (row, col)."""
        x = MARGE + col * CASE_L
        y = ZONE_TEXTE_H + MARGE + row * CASE_H
        return pygame.Rect(x, y, CASE_L, CASE_H)

    def _draw_zone_texte(self) -> None:
        # Fond de la zone texte
        pygame.draw.rect(self.fenetre, (15, 15, 15), (0, 0, FENETRE_L, ZONE_TEXTE_H))
        pygame.draw.line(self.fenetre, BLANC, (0, ZONE_TEXTE_H), (FENETRE_L, ZONE_TEXTE_H), 2)

        # Textes
        txt_level = self.fonte_titre.render(f'LEVEL  {self.board.level}', True, BLANC)
        txt_coups = self.fonte_info.render(f'Coups total : {self.board.coups}', True, GRIS_TEXTE)
        txt_clevel = self.fonte_info.render(f'Coups level : {self.board.coups_level}', True, GRIS_TEXTE)

        self.fenetre.blit(txt_level, (MARGE, 12))
        self.fenetre.blit(txt_coups, (MARGE, 42))
        self.fenetre.blit(txt_clevel, (MARGE + 220, 42))

    def _draw_grille(self) -> None:
        for row in range(i__GRID__MAX_ROW__):
            for col in range(i__GRID__MAX_COL__):
                rect = self._case_rect(row, col)

                # Fond de la case
                if self.board.is_on(row, col):
                    pygame.draw.rect(self.fenetre, BLEU_ELECTRIQUE, rect)
                else:
                    pygame.draw.rect(self.fenetre, NOIR, rect)

                # Contour jaune si case active
                if row == self.active_row and col == self.active_col:
                    inner = rect.inflate(-EPAISSEUR_ACTIF * 2, -EPAISSEUR_ACTIF * 2)
                    pygame.draw.rect(self.fenetre, JAUNE, rect, EPAISSEUR_ACTIF)

        # Traits de grille blancs et épais par-dessus
        for row in range(i__GRID__MAX_ROW__ + 1):
            y = ZONE_TEXTE_H + MARGE + row * CASE_H
            pygame.draw.line(self.fenetre, BLANC, (MARGE, y), (MARGE + GRILLE_L, y), EPAISSEUR_MUR)

        for col in range(i__GRID__MAX_COL__ + 1):
            x = MARGE + col * CASE_L
            pygame.draw.line(self.fenetre, BLANC, (x, ZONE_TEXTE_H + MARGE), (x, ZONE_TEXTE_H + MARGE + GRILLE_H),
                             EPAISSEUR_MUR)

    def _handle_keys(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_LEFT:
            self.active_col = max(0, self.active_col - 1)
        elif event.key == pygame.K_RIGHT:
            self.active_col = min(i__GRID__MAX_COL__ - 1, self.active_col + 1)
        elif event.key == pygame.K_UP:
            self.active_row = max(0, self.active_row - 1)
        elif event.key == pygame.K_DOWN:
            self.active_row = min(i__GRID__MAX_ROW__ - 1, self.active_row + 1)
        elif event.key == pygame.K_SPACE:
            self.board.high_light(self.active_row + 1, self.active_col + 1)


    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._handle_keys(event)

            self.fenetre.fill(NOIR)
            self._draw_zone_texte()
            self._draw_grille()
            pygame.display.flip()
            self.horloge.tick(60)


if __name__ == '__main__':
    all_map: Board = Board()
    all_map.start()
    render = GameRenderer(all_map)
    render.run()


