from typing import Final

st__MAPS_FILE__: Final[str] = r'referential/maps.json'
st__MAPS_FILE_DBG__: Final[str] = r'referential/maps_debug.json'
st__SCORES_FILE__: Final[str] = r'referential/scores.json'

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

FENETRE_L: Final[int]       = 520
FENETRE_H: Final[int]       = 650
ZONE_TEXTE_H: Final[int]    = 110   # agrandie pour accueillir la 3ème ligne chrono
MARGE: Final[int]           = 20
EPAISSEUR_MUR: Final[int]   = 4
EPAISSEUR_ACTIF: Final[int] = 14

GRILLE_L: Final[int]  = FENETRE_L - 2 * MARGE
GRILLE_H: Final[int]  = FENETRE_H - ZONE_TEXTE_H - 2 * MARGE
CASE_L: Final[int]    = GRILLE_L // i__GRID__MAX_COL__
CASE_H: Final[int]    = GRILLE_H // i__GRID__MAX_ROW__

DBG_IS_ON: Final[bool] = False
