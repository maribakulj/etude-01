"""
coincidence.py — coïncidence de partiels entre un son transposé et un mélange.

Noyau de Φ (DECISION-PHI.md) : Σ_{i,j} a_i b_j exp(−(d_ij/σ)²), d_ij étant
l'écart en cents entre le partiel i du son transposé et le partiel j du
mélange. Pour un mélange réduit à une copie du son à t = 0, la courbe est
exactement Φ (`metriques_fusion.proxy_coincidence`), ce que vérifie
`tests/test_oreille.py`.

Statut : mesure de coïncidence, non validée comme mesure perceptive de fusion
(README.md, limite 5). Une variante « harmonicité » sera ajoutée en phase 1.
"""

import numpy as np


def courbe_coincidence(son, copies, sigma, grille):
    """Coïncidence entre `son` transposé de t (t parcourant `grille`, en cents)
    et le mélange des `copies` actives [(t_k, w_k)] de ce même son."""
    ratios, amps = son
    c_son = 1200.0 * np.log2(ratios)
    m_c = np.concatenate([c_son + t for t, w in copies])
    m_a = np.concatenate([amps * w for t, w in copies])
    o = (c_son[:, None] - m_c[None, :]).ravel()
    poids = (amps[:, None] * m_a[None, :]).ravel()
    # Optimisation : on ignore les paires dont la contribution est inférieure
    # à exp(-64) sur toute la grille. Une paire compte en t si |t + o| est
    # petit, donc seules les paires avec |o| <= max|t| + 8σ peuvent compter.
    # La borne retenue contient aussi l'étendue de la grille, pour que le
    # calcul de l'étape 1 reste identique au bit près.
    portee = max(np.max(grille) - np.min(grille), np.max(np.abs(grille)))
    garde = np.abs(o) < portee + 8 * sigma
    o, poids = o[garde], poids[garde]
    return np.exp(-((grille[:, None] + o[None, :]) / sigma) ** 2) @ poids
