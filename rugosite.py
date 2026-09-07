"""
rugosite.py — le scalaire C (consonance verticale) : inverse de la rugosité.

Modèle de Sethares (constantes d'origine, ajustées sur Plomp-Levelt 1965) —
accepté comme socle par la PASSATION (fragilité n°3 : empirique de seconde
main, daté, mais standard). Le récepteur entre par bw_scale (échelle de bande
critique) : c'est le port du CADRAGE §5.

HYGIÈNE ABSOLUE (SPEC §1) : C ne contient pas Φ, Φ ne contient pas C. Ce
module n'importe rien de metriques_fusion.
"""

import numpy as np


def sethares_pair(f1, f2, a1, a2, bw_scale=1.0):
    """Rugosité d'une paire de partiels (Sethares 1993, constantes d'origine)."""
    b1, b2 = 3.5, 5.75
    s1, s2, xstar = 0.0207, 18.96, 0.24
    fmin = np.minimum(f1, f2)
    s = xstar / ((s1 * fmin + s2) * bw_scale)
    df = np.abs(f2 - f1)
    return a1 * a2 * (np.exp(-b1 * s * df) - np.exp(-b2 * s * df))


def rugosite(spec, r, f0=261.6, bw_scale=1.0):
    """Rugosité totale de deux voix de même timbre à l'intervalle r."""
    fA, aA = spec
    F = np.concatenate([fA * f0, fA * f0 * r])
    A = np.concatenate([aA, aA])
    d = sethares_pair(F[:, None], F[None, :], A[:, None], A[None, :], bw_scale)
    return float(np.triu(d, k=1).sum())


def consonance_curve(spec, cents, f0=261.6, bw_scale=1.0):
    """C(i) = consonance verticale normalisée [0,1] sur la grille `cents`.
    C = -rugosité, remis à l'échelle min-max sur la grille (la valeur absolue
    de la rugosité n'a pas d'unité perceptive ; seuls comptent les contrastes,
    et le seuil tau_C est balayé, jamais figé — SPEC §7)."""
    C = np.array([-rugosite(spec, 2 ** (c / 1200.0), f0, bw_scale) for c in cents])
    return (C - C.min()) / (C.max() - C.min() + 1e-12)
