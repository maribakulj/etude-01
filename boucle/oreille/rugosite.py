"""
rugosite.py — rugosité de deux sons purs (C2), modèle de Sethares.

Le modèle et ses constantes sont ceux de `rugosite.py` à la racine (ajustés
par Sethares sur la courbe de Plomp & Levelt 1965). Ce module ajoute
seulement la mesure de la position du maximum, pour le test de C2.
"""

import numpy as np

from rugosite import sethares_pair
from boucle.oreille.erb import bande_critique


def ecart_maximum(f, pas_hz=0.01):
    """Écart (Hz) entre deux sons purs, le plus grave à f, qui maximise la
    dissonance de Sethares. Recherche sur une grille fine (choix technique :
    pas de 0,01 Hz, bien en dessous de la tolérance du test)."""
    df = np.arange(pas_hz, 2.0 * bande_critique(f), pas_hz)
    d = sethares_pair(f, f + df, 1.0, 1.0)
    return float(df[int(np.argmax(d))])


def maximum_en_bandes_critiques(f):
    """Position du maximum de dissonance, en fraction de la bande critique."""
    return ecart_maximum(f) / bande_critique(f)
