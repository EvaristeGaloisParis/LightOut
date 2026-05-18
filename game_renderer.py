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
from board import Board, fmt_time
from scores import Score, Scores


LONGUEUR_NOM_MAX = 16


class GameRenderer:

    def __init__(self, board: Board, scores: Scores):
        pygame.init()
        self.board       = board
        self.scores      = scores
        self.fenetre     = pygame.display.set_mode((FENETRE_L, FENETRE_H))
        pygame.display.set_caption('Lights ! brain-teaser')
        self.horloge      = pygame.time.Clock()
        self.fonte_titre  = pygame.font.SysFont('monospace', 22, bold=True)
        self.fonte_info   = pygame.font.SysFont('monospace', 16)
        self.fonte_bravo  = pygame.font.SysFont('monospace', 48, bold=True)
        self.fonte_petite = pygame.font.SysFont('monospace', 14)

        self.active_row: int = 0
        self.active_col: int = 0

        # État écran victoire
        self.__nom_saisi:    str  = ''
        self.__score_sauve:  bool = False
        self.__rang:         int  = 0

    # ─── Géométrie ────────────────────────────────────────────────────────────

    def _case_rect(self, row: int, col: int) -> pygame.Rect:
        x = MARGE + col * CASE_L
        y = ZONE_TEXTE_H + MARGE + row * CASE_H
        return pygame.Rect(x, y, CASE_L, CASE_H)

    # ─── Rendu : zone texte + grille (mode jeu) ───────────────────────────────

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

    # ─── Rendu : écran victoire ───────────────────────────────────────────────

    def _draw_victoire(self) -> None:
        bravo = self.fonte_bravo.render('BRAVO !', True, JAUNE)
        self.fenetre.blit(bravo, (FENETRE_L // 2 - bravo.get_width() // 2, 30))

        y = 100
        for ligne in (
            f'coups   : {self.board.total_moves}',
            f'lumieres: {self.board.total_lights}',
            f'temps   : {fmt_time(self.board.total_ms)}',
        ):
            surf = self.fonte_info.render(ligne, True, BLANC)
            self.fenetre.blit(surf, (MARGE, y))
            y += 22

        # Saisie du nom ou rang confirmé
        y += 8
        if not self.__score_sauve:
            invite = self.fonte_info.render('ton nom : ' + self.__nom_saisi + '_', True, BLANC)
            self.fenetre.blit(invite, (MARGE, y))
            y += 26
            aide = self.fonte_petite.render('[Entree] valider   [Q]/[Echap] quitter', True, GRIS_TEXTE)
            self.fenetre.blit(aide, (MARGE, y))
            y += 22
        else:
            rang = self.fonte_info.render(f'ton rang : #{self.__rang}', True, JAUNE)
            self.fenetre.blit(rang, (MARGE, y))
            y += 26
            aide = self.fonte_petite.render('[R] rejouer (peux-tu faire mieux ?)   [Q]/[Echap] quitter', True, GRIS_TEXTE)
            self.fenetre.blit(aide, (MARGE, y))
            y += 22

        # Top 5
        y += 10
        titre = self.fonte_info.render('TOP 5', True, BLANC)
        self.fenetre.blit(titre, (MARGE, y))
        y += 22
        top = self.scores.top(5)
        if not top:
            vide = self.fonte_petite.render('(aucun score enregistre)', True, GRIS_TEXTE)
            self.fenetre.blit(vide, (MARGE, y))
        else:
            for i, s in enumerate(top, start=1):
                ligne = f'{i}. {s.nom:<{LONGUEUR_NOM_MAX}}  coups:{s.moves:>4}  temps:{fmt_time(s.time_ms)}  {s.date[:10]}'
                surf  = self.fonte_petite.render(ligne, True, GRIS_TEXTE)
                self.fenetre.blit(surf, (MARGE, y))
                y += 20

    # ─── Input ────────────────────────────────────────────────────────────────

    def _handle_keys(self, event: pygame.event.Event) -> None:
        if self.board.is_won:
            self._handle_keys_victoire(event)
            return

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

    def _handle_keys_victoire(self, event: pygame.event.Event) -> None:
        if event.key in (pygame.K_q, pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        if not self.__score_sauve:
            if event.key == pygame.K_BACKSPACE:
                self.__nom_saisi = self.__nom_saisi[:-1]
            elif event.key == pygame.K_RETURN:
                nom = self.__nom_saisi.strip()
                if nom:
                    self.__rang = self.scores.add(Score(
                        nom     = nom,
                        moves   = self.board.total_moves,
                        lights  = self.board.total_lights,
                        time_ms = self.board.total_ms,
                    ))
                    self.__score_sauve = True
            elif event.unicode and event.unicode.isprintable() and len(self.__nom_saisi) < LONGUEUR_NOM_MAX:
                self.__nom_saisi += event.unicode
        else:
            if event.key == pygame.K_r:
                self.board.reset_all()
                self.__nom_saisi   = ''
                self.__score_sauve = False
                self.__rang        = 0
                self.active_row    = 0
                self.active_col    = 0

    # ─── Boucle ───────────────────────────────────────────────────────────────

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._handle_keys(event)

            self.fenetre.fill(NOIR)
            if self.board.is_won:
                self._draw_victoire()
            else:
                self._draw_zone_texte()
                self._draw_grille()
            pygame.display.flip()
            self.horloge.tick(60)
