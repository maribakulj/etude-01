"""
diag_famille_A.py — pièce d'archive : pourquoi les métriques famille A
(harmonicité par gabarit) s'évaluent à la FONDAMENTALE COMMUNE f0/m et non au
maximum sur une fondamentale libre.

Constat (premier essai, conservé ici comme démonstration) : avec un max sur F0
candidate libre, l'appariement se VERROUILLE sur f0 — la fondamentale de la
voix A seule. L'union contient toujours la série harmonique complète de A,
parfaitement harmonique ; le max mesure donc l'auto-harmonicité d'UNE voix
(quasi constante en r) au lieu de la fusion des DEUX. Symptômes observés :
hiérarchie écrasée (tous les intervalles ~0.71-0.76), quarte devant quinte pour
le gabarit Parncutt, pics parasites en épaule d'octave.

Évaluée à la fondamentale commune f0/m (pgcd des deux fondamentales, m =
dénominateur du rapport réduit — la lecture littérale de SPEC §1 : « l'union se
laisse décrire par UNE fondamentale commune »), la hiérarchie de fusion
empirique (Stumpf ; DeWitt & Crowder 1987) sort entière :
P8 > P5 > P4 > {M3, M6} > m3, pour les deux gabarits.

Exécuter : python3 diag_famille_A.py
"""

import numpy as np
from metriques_fusion import (harmonic, union_spectrum, _self_overlap, _HMAX,
                              _rationalize, _parncutt_template, RATIO)

f0 = 261.6
spec = harmonic()
INTERVALLES = {'P8': 1200.0, 'P5': 702.0, 'P4': 498.0, 'M3': 386.3,
               'M6': 884.4, 'm3': 315.6}
SIGMA = 12.0


def cosine_at_F0(spec_, r, template_w, sigma, F0_ratio):
    """Cosinus union <-> gabarit harmonique d'une fondamentale f0*F0_ratio."""
    F, A = union_spectrum(spec_, r, f0)
    cU = 1200.0 * np.log2(F / f0)
    nU = _self_overlap(cU, A, sigma)
    ks = np.arange(1, _HMAX + 1).astype(float)
    wk = template_w[:_HMAX]
    cT = 1200.0 * np.log2(F0_ratio) + 1200.0 * np.log2(ks)
    nT = _self_overlap(cT, wk, sigma)
    d = cU[:, None] - cT[None, :]
    K = np.exp(-(d ** 2) / (4.0 * sigma ** 2))
    overlap = float((A[:, None] * wk[None, :] * K).sum())
    return overlap / np.sqrt(nU * max(nT, 1e-12))


def argmax_F0(spec_, r, template_w, sigma):
    """La variante REJETÉE : max sur une grille de fondamentales libres."""
    F0s = np.geomspace(1.0 / 8.0, 1.0, 700)
    vals = [cosine_at_F0(spec_, r, template_w, sigma, x) for x in F0s]
    i = int(np.argmax(vals))
    return F0s[i], vals[i]


def table(template_w, titre):
    print(f"\n{titre}")
    print(f"{'iv':4s} {'r':>7s} {'m':>3s} {'cos@argmaxF0':>13s} {'F0*/f0':>7s} {'cos@(f0/m)':>11s}")
    for nm, c in INTERVALLES.items():
        r = RATIO(c)
        _n, m = _rationalize(r)
        F0star, cmax = argmax_F0(spec, r, template_w, SIGMA)
        ccomm = cosine_at_F0(spec, r, template_w, SIGMA, 1.0 / m)
        print(f"{nm:4s} {r:7.4f} {m:3d} {cmax:13.4f} {F0star:7.4f} {ccomm:11.4f}")


if __name__ == '__main__':
    print("Diagnostic famille A : max-sur-F0 (rejeté) vs fondamentale commune (retenu)")
    print("Lire : F0*/f0=1.0 partout sauf P8/P5 => le max se verrouille sur la voix A.")
    table(1.0 / np.arange(1, _HMAX + 1), "Gabarit roll-off 1/k (crible) :")
    table(_parncutt_template(), "Gabarit root-support Parncutt :")
