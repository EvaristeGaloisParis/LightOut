import sys
import pygame

from constantes import (
    GRID_MAX_ROW,
    GRID_MAX_COL,
    FENETRE_L,
    FENETRE_H,
    ZONE_TEXTE_H,
    ZONE_BOUTONS_H,
    MARGE,
    EPAISSEUR_MUR,
    EPAISSEUR_ACTIF,
    EPAISSEUR_SEPARATEUR,
    GRILLE_L,
    GRILLE_H,
    CASE_L,
    CASE_H,
    NOIR,
    BLANC,
    JAUNE,
    BLEU_ELECTRIQUE,
    GRIS_TEXTE,
    GRIS_FOND,
    COUL_BOUTON_RESET,
    COUL_BOUTON_RESET_HOVER,
    COUL_BOUTON_QUIT,
    COUL_BOUTON_QUIT_HOVER,
    BOUTON_L,
    BOUTON_H,
    BOUTON_ESPACE,
    FONTE_TITRE_TAILLE,
    FONTE_INFO_TAILLE,
    FONTE_PETITE_TAILLE,
    FONTE_BRAVO_TAILLE,
    FONTE_BOUTON_TAILLE,
    TITRE_Y,
    COUPS_Y,
    CLEVEL_Y,
    BRAVO_Y,
    STATS_Y,
    LIGNE_INFO_H,
    LIGNE_PETITE_H,
    APRES_INVITE_H,
    GAP_PETIT,
    GAP_MOYEN,
    LONGUEUR_NOM_MAX,
)
from board import Board, fmt_time
from scores import Score, Scores


class GameRenderer:

    def __init__(self, board: Board, scores: Scores):
        pygame.init()
        self.board       = board
        self.scores      = scores
        self.fenetre     = pygame.display.set_mode((FENETRE_L, FENETRE_H))
        pygame.display.set_caption('Lights ! brain-teaser')
        self.horloge      = pygame.time.Clock()
        self.fonte_titre  = pygame.font.SysFont('monospace', FONTE_TITRE_TAILLE, bold=True)
        self.fonte_info   = pygame.font.SysFont('monospace', FONTE_INFO_TAILLE)
        self.fonte_bravo  = pygame.font.SysFont('monospace', FONTE_BRAVO_TAILLE, bold=True)
        self.fonte_petite = pygame.font.SysFont('monospace', FONTE_PETITE_TAILLE)
        self.fonte_bouton = pygame.font.SysFont('monospace', FONTE_BOUTON_TAILLE, bold=True)

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

    def _rect_bouton_reset(self) -> pygame.Rect:
        zone_top = ZONE_TEXTE_H + MARGE + GRILLE_H + MARGE
        y        = zone_top + (ZONE_BOUTONS_H - BOUTON_H) // 2
        x        = (FENETRE_L - (2 * BOUTON_L + BOUTON_ESPACE)) // 2
        return pygame.Rect(x, y, BOUTON_L, BOUTON_H)

    def _rect_bouton_quit(self) -> pygame.Rect:
        reset = self._rect_bouton_reset()
        return pygame.Rect(reset.right + BOUTON_ESPACE, reset.y, BOUTON_L, BOUTON_H)

    # ─── Rendu : zone texte + grille (mode jeu) ───────────────────────────────

    def _draw_zone_texte(self) -> None:
        pygame.draw.rect(self.fenetre, GRIS_FOND, (0, 0, FENETRE_L, ZONE_TEXTE_H))
        pygame.draw.line(self.fenetre, BLANC, (0, ZONE_TEXTE_H), (FENETRE_L, ZONE_TEXTE_H), EPAISSEUR_SEPARATEUR)

        txt_level  = self.fonte_titre.render(f'LEVEL  {self.board.level}', True, BLANC)
        txt_coups  = self.fonte_info.render(f'total: {self.board.coups}', True, GRIS_TEXTE)
        txt_clevel = self.fonte_info.render(f'level: {self.board.coups_level}', True, GRIS_TEXTE)

        self.fenetre.blit(txt_level,  (MARGE, TITRE_Y))
        self.fenetre.blit(txt_coups,  (MARGE, COUPS_Y))
        self.fenetre.blit(txt_clevel, (MARGE, CLEVEL_Y))

    def _draw_grille(self) -> None:
        for row in range(GRID_MAX_ROW):
            for col in range(GRID_MAX_COL):
                rect = self._case_rect(row, col)

                if self.board.is_on(row, col):
                    pygame.draw.rect(self.fenetre, BLEU_ELECTRIQUE, rect)
                else:
                    pygame.draw.rect(self.fenetre, NOIR, rect)

                if row == self.active_row and col == self.active_col:
                    pygame.draw.rect(self.fenetre, JAUNE, rect, EPAISSEUR_ACTIF)

        for row in range(GRID_MAX_ROW + 1):
            y = ZONE_TEXTE_H + MARGE + row * CASE_H
            pygame.draw.line(self.fenetre, BLANC, (MARGE, y), (MARGE + GRILLE_L, y), EPAISSEUR_MUR)

        for col in range(GRID_MAX_COL + 1):
            x = MARGE + col * CASE_L
            pygame.draw.line(self.fenetre, BLANC, (x, ZONE_TEXTE_H + MARGE), (x, ZONE_TEXTE_H + MARGE + GRILLE_H), EPAISSEUR_MUR)

    # ─── Rendu : boutons ──────────────────────────────────────────────────────

    def _draw_bouton(self, rect: pygame.Rect, label: str,
                     fond: tuple[int, int, int],
                     fond_hover: tuple[int, int, int],
                     mouse_pos: tuple[int, int]) -> None:
        couleur = fond_hover if rect.collidepoint(mouse_pos) else fond
        pygame.draw.rect(self.fenetre, couleur, rect)
        pygame.draw.rect(self.fenetre, BLANC, rect, EPAISSEUR_SEPARATEUR)
        txt = self.fonte_bouton.render(label, True, BLANC)
        self.fenetre.blit(
            txt,
            (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2),
        )

    def _draw_zone_boutons(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self._draw_bouton(self._rect_bouton_reset(), 'RESET',
                          COUL_BOUTON_RESET, COUL_BOUTON_RESET_HOVER, mouse_pos)
        self._draw_bouton(self._rect_bouton_quit(), 'QUITTER',
                          COUL_BOUTON_QUIT, COUL_BOUTON_QUIT_HOVER, mouse_pos)

    # ─── Rendu : écran victoire ───────────────────────────────────────────────

    def _draw_victoire(self) -> None:
        bravo = self.fonte_bravo.render('BRAVO !', True, JAUNE)
        self.fenetre.blit(bravo, (FENETRE_L // 2 - bravo.get_width() // 2, BRAVO_Y))

        y = STATS_Y
        for ligne in (
            f'coups   : {self.board.total_moves}',
            f'lumieres: {self.board.total_lights}',
            f'temps   : {fmt_time(self.board.total_ms)}',
        ):
            surf = self.fonte_info.render(ligne, True, BLANC)
            self.fenetre.blit(surf, (MARGE, y))
            y += LIGNE_INFO_H

        # Saisie du nom ou rang confirmé
        y += GAP_PETIT
        if not self.__score_sauve:
            invite = self.fonte_info.render('ton nom : ' + self.__nom_saisi + '_', True, BLANC)
            self.fenetre.blit(invite, (MARGE, y))
            y += APRES_INVITE_H
            aide = self.fonte_petite.render('[Entree] valider   [Q]/[Echap] quitter', True, GRIS_TEXTE)
            self.fenetre.blit(aide, (MARGE, y))
            y += LIGNE_INFO_H
        else:
            rang = self.fonte_info.render(f'ton rang : #{self.__rang}', True, JAUNE)
            self.fenetre.blit(rang, (MARGE, y))
            y += APRES_INVITE_H
            aide = self.fonte_petite.render('[R] rejouer (peux-tu faire mieux ?)   [Q]/[Echap] quitter', True, GRIS_TEXTE)
            self.fenetre.blit(aide, (MARGE, y))
            y += LIGNE_INFO_H

        # Top 5
        y += GAP_MOYEN
        titre = self.fonte_info.render('TOP 5', True, BLANC)
        self.fenetre.blit(titre, (MARGE, y))
        y += LIGNE_INFO_H
        top = self.scores.top(5)
        if not top:
            vide = self.fonte_petite.render('(aucun score enregistre)', True, GRIS_TEXTE)
            self.fenetre.blit(vide, (MARGE, y))
        else:
            for i, s in enumerate(top, start=1):
                ligne = f'{i}. {s.nom:<{LONGUEUR_NOM_MAX}}  coups:{s.moves:>4}  temps:{fmt_time(s.time_ms)}  {s.date[:10]}'
                surf  = self.fonte_petite.render(ligne, True, GRIS_TEXTE)
                self.fenetre.blit(surf, (MARGE, y))
                y += LIGNE_PETITE_H

    # ─── Input ────────────────────────────────────────────────────────────────

    def _handle_mouse(self, event: pygame.event.Event) -> None:
        if self.board.is_won:
            return
        if event.button != 1:
            return
        if self._rect_bouton_reset().collidepoint(event.pos):
            self.board.reset_level()
        elif self._rect_bouton_quit().collidepoint(event.pos):
            pygame.quit()
            sys.exit()

    def _handle_keys(self, event: pygame.event.Event) -> None:
        if self.board.is_won:
            self._handle_keys_victoire(event)
            return

        move: int = 0
        if event.key == pygame.K_LEFT:
            self.active_col = max(0, self.active_col - 1)
            move = 1
        elif event.key == pygame.K_RIGHT:
            self.active_col = min(GRID_MAX_COL - 1, self.active_col + 1)
            move = 1
        elif event.key == pygame.K_UP:
            self.active_row = max(0, self.active_row - 1)
            move = 1
        elif event.key == pygame.K_DOWN:
            self.active_row = min(GRID_MAX_ROW - 1, self.active_row + 1)
            move = 1
        elif event.key == pygame.K_SPACE:
            self.board.high_light(self.active_row, self.active_col)

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse(event)

            self.fenetre.fill(NOIR)
            if self.board.is_won:
                self._draw_victoire()
            else:
                self._draw_zone_texte()
                self._draw_grille()
                self._draw_zone_boutons()
            pygame.display.flip()
            self.horloge.tick(60)
