import sys
import pygame

from constantes import (
    i__GRID__MAX_ROW__,
    i__GRID__MAX_COL__,
    FENETRE_L,
    FENETRE_H,
    ZONE_TEXTE_H,
    MARGE,
    EPAISSEUR_MUR,
    EPAISSEUR_ACTIF,
    GRILLE_L,
    GRILLE_H,
    CASE_L,
    CASE_H,
    NOIR,
    BLANC,
    JAUNE,
    BLEU_ELECTRIQUE,
    GRIS_TEXTE,
)
from board import Board


class GameRenderer:

    def __init__(self, board: Board):
        pygame.init()
        self.board       = board
        self.fenetre     = pygame.display.set_mode((FENETRE_L, FENETRE_H))
        pygame.display.set_caption('Lights ! brain-teaser')
        self.horloge     = pygame.time.Clock()
        self.fonte_titre = pygame.font.SysFont('monospace', 22, bold=True)
        self.fonte_info  = pygame.font.SysFont('monospace', 16)

        self.active_row: int = 0
        self.active_col: int = 0

    def _case_rect(self, row: int, col: int) -> pygame.Rect:
        x = MARGE + col * CASE_L
        y = ZONE_TEXTE_H + MARGE + row * CASE_H
        return pygame.Rect(x, y, CASE_L, CASE_H)

    def _draw_zone_texte(self) -> None:
        pygame.draw.rect(self.fenetre, (15, 15, 15), (0, 0, FENETRE_L, ZONE_TEXTE_H))
        pygame.draw.line(self.fenetre, BLANC, (0, ZONE_TEXTE_H), (FENETRE_L, ZONE_TEXTE_H), 2)

        txt_level  = self.fonte_titre.render(f'LEVEL  {self.board.level}', True, BLANC)
        txt_coups  = self.fonte_info.render(f'total: {self.board.coups}', True, GRIS_TEXTE)
        txt_clevel = self.fonte_info.render(f'level: {self.board.coups_level}', True, GRIS_TEXTE)

        self.fenetre.blit(txt_level,  (MARGE, 10))
        self.fenetre.blit(txt_coups,  (MARGE, 40))
        self.fenetre.blit(txt_clevel, (MARGE, 66))

    def _draw_grille(self) -> None:
        for row in range(i__GRID__MAX_ROW__):
            for col in range(i__GRID__MAX_COL__):
                rect = self._case_rect(row, col)

                if self.board.is_on(row, col):
                    pygame.draw.rect(self.fenetre, BLEU_ELECTRIQUE, rect)
                else:
                    pygame.draw.rect(self.fenetre, NOIR, rect)

                if row == self.active_row and col == self.active_col:
                    pygame.draw.rect(self.fenetre, JAUNE, rect, EPAISSEUR_ACTIF)

        for row in range(i__GRID__MAX_ROW__ + 1):
            y = ZONE_TEXTE_H + MARGE + row * CASE_H
            pygame.draw.line(self.fenetre, BLANC, (MARGE, y), (MARGE + GRILLE_L, y), EPAISSEUR_MUR)

        for col in range(i__GRID__MAX_COL__ + 1):
            x = MARGE + col * CASE_L
            pygame.draw.line(self.fenetre, BLANC, (x, ZONE_TEXTE_H + MARGE), (x, ZONE_TEXTE_H + MARGE + GRILLE_H), EPAISSEUR_MUR)

    def _handle_keys(self, event: pygame.event.Event) -> None:
        move: int = 0
        if event.key == pygame.K_LEFT:
            self.active_col = max(0, self.active_col - 1)
            move = 1
        elif event.key == pygame.K_RIGHT:
            self.active_col = min(i__GRID__MAX_COL__ - 1, self.active_col + 1)
            move = 1
        elif event.key == pygame.K_UP:
            self.active_row = max(0, self.active_row - 1)
            move = 1
        elif event.key == pygame.K_DOWN:
            self.active_row = min(i__GRID__MAX_ROW__ - 1, self.active_row + 1)
            move = 1
        elif event.key == pygame.K_SPACE:
            self.board.high_light(self.active_row + 1, self.active_col + 1)

        if move:
            self.board.add_move()

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
