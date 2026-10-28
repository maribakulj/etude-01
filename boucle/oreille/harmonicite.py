"""
harmonicite.py — regroupement par fondamentale commune (C4) et hauteur
virtuelle (C5). PHASE1-PROTOCOLE.md §4.

Forme simplifiée du modèle de hauteur virtuelle de Terhardt, déclarée comme
telle : on cherche la fondamentale f0 dont les harmoniques (rang ≤ K)
rendent compte de la plus grande part de l'amplitude des partiels. Un
partiel est « expliqué » s'il est à moins de δ (relatif) d'un harmonique de
f0. Parmi les candidats qui expliquent la même part (à la tolérance
d'égalité près), on retient la fondamentale la plus haute : sans cette règle,
une fondamentale assez grave explique toujours tout. Les candidats sont les
sous-harmoniques f_i / n (n ≤ K) des partiels, au-dessus de la limite basse
de la hauteur mélodique (C6). Paramètres : boucle/registre.py.
"""

import numpy as np

from boucle.registre import val


def _rangs(freqs, f0):
    k = np.maximum(np.rint(freqs / f0), 1.0)
    ecart = np.abs(freqs / (k * f0) - 1.0)
    return k, ecart


def partiels_expliques(freqs, f0, delta=None, kmax=None):
    """Masque des partiels expliqués par f0 (rang ≤ kmax, écart ≤ delta)."""
    delta = val('DELTA_HARMONICITE') if delta is None else delta
    kmax = val('K_HARMONIQUES') if kmax is None else kmax
    k, ecart = _rangs(np.asarray(freqs, float), f0)
    return (ecart <= delta) & (k <= kmax)


def hauteur_virtuelle(freqs, amps, delta=None, kmax=None):
    """Hauteur virtuelle (Hz) et part d'amplitude expliquée.
    freqs en Hz (absolues), amps linéaires."""
    freqs, amps = np.asarray(freqs, float), np.asarray(amps, float)
    kmax = val('K_HARMONIQUES') if kmax is None else kmax
    f_bas = val('LIMITE_BASSE_HZ')
    cands = sorted({f / n for f in freqs for n in range(1, int(kmax) + 1) if f / n >= f_bas},
                   reverse=True)
    total = amps.sum()
    meilleur, part_max = None, -1.0
    for f0 in cands:                       # du plus aigu au plus grave
        part = amps[partiels_expliques(freqs, f0, delta, kmax)].sum() / total
        if part > part_max + val('EGALITE_PART'):
            meilleur, part_max = f0, part
    m = partiels_expliques(freqs, meilleur, delta, kmax)
    k, _ = _rangs(freqs[m], meilleur)
    f0 = float(np.sum(amps[m] * freqs[m] / k) / np.sum(amps[m]))   # affinage
    return f0, float(part_max)


def partiel_regroupe(freqs, amps, i, delta=None, kmax=None):
    """Le partiel i est-il regroupé avec les autres (expliqué par la
    hauteur virtuelle de l'ensemble) ? C4."""
    f0, _ = hauteur_virtuelle(freqs, amps, delta, kmax)
    return bool(partiels_expliques(np.asarray(freqs, float), f0, delta, kmax)[i])
