"""
famille_raide.py — l'axe physique continu du diagramme de phase : la corde raide.

    f_n = n · f0 · sqrt(1 + B · n²)      n = 1..N,  amplitudes 1/n

`B` est le coefficient d'inharmonicité d'une corde raide (rigidité en flexion).
Valeurs réelles : ~1e-4 pour les cordes médium d'un piano, ~1e-3 et au-delà
pour les basses d'un petit droit.

Deux propriétés qui font de `B` le bon axe (cf. DIAGRAMME-PHASE.md §1.1) :
  - à B = 0, la famille est EXACTEMENT le timbre harmonique de contrôle des
    étapes 1 et 3 (partiels n, roll-off 1/n) — celui qui reproduit Fux ;
  - quand B croît, f_n → f0·sqrt(B)·n² : un régime purement inharmonique de
    type barre, dont les coïncidences sous transposition tombent aux CARRÉS de
    rationnels et non aux rationnels.

Aucune constante de la chaîne (Φ, C, seuils) n'est touchée ici.
"""

import numpy as np


def corde_raide(B, n=10):
    """Spectre (fréquences relatives, amplitudes) d'une corde raide de
    coefficient d'inharmonicité B. B=0 -> timbre harmonique de contrôle."""
    k = np.arange(1, n + 1).astype(float)
    f = k * np.sqrt(1.0 + B * k ** 2)
    a = 1.0 / k
    return f, a


if __name__ == '__main__':
    from metriques_fusion import harmonic
    f0, a0 = corde_raide(0.0)
    fh, ah = harmonic(10)
    print("Ancrage B=0 vs timbre harmonique de contrôle :")
    print(f"  écart max fréquences : {np.max(np.abs(f0 - fh)):.2e}")
    print(f"  écart max amplitudes : {np.max(np.abs(a0 - ah)):.2e}")
    print("\nRatios des 5 premiers partiels selon B :")
    print(f"  {'B':>8s}  " + "  ".join(f"f{k}/f1" for k in range(1, 6)))
    for B in [0.0, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]:
        f, _ = corde_raide(B, 5)
        print(f"  {B:8.0e}  " + "  ".join(f"{x:5.3f}" for x in f / f[0]))
    print("  limite n² :  " + "  ".join(f"{k**2:5.3f}" for k in range(1, 6)))
