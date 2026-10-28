"""
sensibilite_seuil.py — audit : que deviennent les résultats publiés quand on
bouge le seuil relatif τ_F autour de la valeur déclarée 0,226 ?

Aucune modification du modèle : on relit la grille d'états (Φ figée) des
timbres de l'étape 3 et les grammaires sauvées par diagramme_phase.py, et on
balaie τ_F. Trois questions (STATUT.md §2) :

  A. Sur le contrôle harmonique, sur quelle fenêtre de τ_F retrouve-t-on Fux
     (parallèles interdites = {unisson, P5, P8}) ? — c'est la fenêtre dont le
     milieu a FIXÉ τ_F : ce résultat est une calibration, pas une prédiction.
  B. Sur la cloche (seul test hors calibration), à quelle distance de la
     valeur déclarée l'ensemble des interdits change-t-il ?
  C. Dans le diagramme de phase, la 1re bifurcation (B ≈ 7,7e-3) et le
     nombre de bifurcations dépendent-ils de τ_F ?

Rejouer : `python3 sensibilite_seuil.py` (après diagramme_phase.py).
"""

import json

import numpy as np

from graphe_grammaire import grille_etats
from metriques_fusion import harmonic
from etape3_fux import cloche_westerkerk

TAUF_DECLARE = 0.226
TAUS = np.round(np.arange(0.005, 1.0, 0.001), 3)


def interdits(phis, tau_rel):
    """Interdits de parallèles pour des {intervalle: Φ} (None = +inf)."""
    finis = [v for v in phis.values() if v is not None]
    seuil = tau_rel * max(finis)
    return tuple(sorted(c for c, v in phis.items() if v is None or v >= seuil))


def plateaux(phis):
    """Liste de (tau_min, tau_max, ensemble interdit) le long de TAUS."""
    out = []
    for t in TAUS:
        s = interdits(phis, t)
        if out and out[-1][2] == s:
            out[-1][1] = t
        else:
            out.append([t, t, s])
    return out


def phis_timbre(spec):
    grille, _ = grille_etats(spec)
    return {round(e['intervalle']): (None if np.isinf(e['Phi']) else e['Phi'])
            for e in grille}


def affiche(titre, phis):
    print(f"\n### {titre}")
    print("  Φ par état (classement, indépendant de tout seuil) : "
          + ", ".join(f"{c}c={'inf' if v is None else f'{v:.3f}'}"
                      for c, v in sorted(phis.items(),
                                         key=lambda kv: -np.inf if kv[1] is None
                                         else -kv[1])))
    for a, b, s in plateaux(phis):
        mark = '  <== τ_F déclaré' if a <= TAUF_DECLARE <= b else ''
        print(f"  τ_F ∈ [{a:.3f}, {b:.3f}] : {list(s)}{mark}")
    for a, b, s in plateaux(phis):
        if a <= TAUF_DECLARE <= b:
            print(f"  marge sous / au-dessus du τ_F déclaré : "
                  f"{TAUF_DECLARE - a:.3f} / {b - TAUF_DECLARE:.3f}")


def main():
    print("=" * 78)
    print("SENSIBILITÉ AU SEUIL τ_F (relatif au max de Φ fini du timbre)")
    print("=" * 78)

    affiche("A. Contrôle harmonique (calibration : τ_F = milieu de la fenêtre Fux)",
            phis_timbre(harmonic()))
    affiche("B. Cloche Westerkerk (spectre publié) — hors calibration",
            phis_timbre(cloche_westerkerk()))

    print("\n### C. Diagramme de phase : bifurcations selon τ_F")
    with open('diagramme_phase_resultats.json') as fh:
        G = json.load(fh)['grammaires']
    print(f"  {'τ_F':>6s}  {'interdits à B=0':<22s} {'1re bifurcation B':>18s}  {'n':>3s}")
    for t in [0.10, 0.15, 0.20, TAUF_DECLARE, 0.25, 0.30, 0.35, 0.40]:
        card = []
        for g in G:
            phis = {int(k): v for k, v in g['etats_phi'].items()}
            card.append(len(interdits(phis, t)))
        bifs = [G[i]['B'] for i in range(1, len(G)) if card[i] != card[i - 1]]
        s0 = list(interdits({int(k): v for k, v in G[0]['etats_phi'].items()}, t))
        b1 = f"{bifs[0]:.1e}" if bifs else "aucune"
        print(f"  {t:6.3f}  {str(s0):<22s} {b1:>18s}  {len(bifs):3d}")


if __name__ == '__main__':
    main()
