from typing import Final

# ─── Fichiers de référence ────────────────────────────────────────────────────

MAPS_FILE:     Final[str] = r'referential/maps.json'
MAPS_FILE_DBG: Final[str] = r'referential/maps_debug.json'
SCORES_FILE:   Final[str] = r'referential/scores.json'

# ─── Grille ───────────────────────────────────────────────────────────────────

GRID_MAX_ROW: Final[int] = 5
GRID_MAX_COL: Final[int] = 5
GRID_MAX_ID:  Final[int] = GRID_MAX_ROW * GRID_MAX_COL
READER:       Final[int] = 2**GRID_MAX_ID - 1

# ─── Couleurs ─────────────────────────────────────────────────────────────────

NOIR:            Final[tuple[int, int, int]] = (0,   0,   0  )
BLANC:           Final[tuple[int, int, int]] = (255, 255, 255)
JAUNE:           Final[tuple[int, int, int]] = (255, 240, 50 )
BLEU_ELECTRIQUE: Final[tuple[int, int, int]] = (30,  80,  255)
GRIS_TEXTE:      Final[tuple[int, int, int]] = (180, 180, 180)
GRIS_FOND:       Final[tuple[int, int, int]] = (15,  15,  15 )

# ─── Dimensions fenêtre ───────────────────────────────────────────────────────

FENETRE_L:            Final[int] = 520
FENETRE_H:            Final[int] = 650
ZONE_TEXTE_H:         Final[int] = 110   # agrandie pour accueillir la 3ème ligne chrono
MARGE:                Final[int] = 20
EPAISSEUR_MUR:        Final[int] = 4
EPAISSEUR_ACTIF:      Final[int] = 14
EPAISSEUR_SEPARATEUR: Final[int] = 2

GRILLE_L: Final[int] = FENETRE_L - 2 * MARGE
GRILLE_H: Final[int] = FENETRE_H - ZONE_TEXTE_H - 2 * MARGE
CASE_L:   Final[int] = GRILLE_L // GRID_MAX_COL
CASE_H:   Final[int] = GRILLE_H // GRID_MAX_ROW

# ─── Tailles de fontes ────────────────────────────────────────────────────────

FONTE_TITRE_TAILLE:  Final[int] = 22
FONTE_INFO_TAILLE:   Final[int] = 16
FONTE_PETITE_TAILLE: Final[int] = 14
FONTE_BRAVO_TAILLE:  Final[int] = 48

# ─── Zone texte (mode jeu) ────────────────────────────────────────────────────

TITRE_Y:  Final[int] = 10
COUPS_Y:  Final[int] = 40
CLEVEL_Y: Final[int] = 66

# ─── Écran victoire ───────────────────────────────────────────────────────────

BRAVO_Y:        Final[int] = 30
STATS_Y:        Final[int] = 100
LIGNE_INFO_H:   Final[int] = 22
LIGNE_PETITE_H: Final[int] = 20
APRES_INVITE_H: Final[int] = 26
GAP_PETIT:      Final[int] = 8
GAP_MOYEN:      Final[int] = 10

# ─── Saisie nom ───────────────────────────────────────────────────────────────

LONGUEUR_NOM_MAX: Final[int] = 16

# ─── Debug ────────────────────────────────────────────────────────────────────

DBG_IS_ON: Final[bool] = False
