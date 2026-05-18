from typing import Final

st__MAPS_FILE__: Final[str] = r'maps/maps.json'

i__GRID__MAX_ROW__: Final[int] = 5
i__GRID__MAX_COL__: Final[int] = 5
i__GRID__MAX_ID__: Final[int] = i__GRID__MAX_ROW__ * i__GRID__MAX_COL__
i__READER__: Final[int] = 2**i__GRID__MAX_ID__ - 1

# ─── Couleurs ─────────────────────────────────────────────────────────────────

NOIR            = (0,   0,   0  )
BLANC           = (255, 255, 255)
JAUNE           = (255, 240, 50 )
BLEU_ELECTRIQUE = (30,  80,  255)
GRIS_TEXTE      = (180, 180, 180)

# ─── Dimensions ───────────────────────────────────────────────────────────────

FENETRE_L       = 520
FENETRE_H       = 650
ZONE_TEXTE_H    = 110   # agrandie pour accueillir la 3ème ligne chrono
MARGE           = 20
EPAISSEUR_MUR   = 4
EPAISSEUR_ACTIF = 14

GRILLE_L = FENETRE_L - 2 * MARGE
GRILLE_H = FENETRE_H - ZONE_TEXTE_H - 2 * MARGE
CASE_L   = GRILLE_L // i__GRID__MAX_COL__
CASE_H   = GRILLE_H // i__GRID__MAX_ROW__

DBG_IS_ON: Final[bool] = False
