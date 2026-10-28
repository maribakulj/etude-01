"""Tests de la boucle v2 (PHASE2-PROTOCOLE.md)."""

import numpy as np

from boucle.phase2 import lignes, non_resolue, grille_registre
from boucle.oreille.erb import erb
from metriques_fusion import harmonic


def test_lignes_van_noorden():
    """Lignes : un écart de 50 c à 100 ms forme une ligne ; un écart de
    2000 c à 100 ms (au-delà de 9 demi-tons, frontière à T_eff = 160 ms)
    sépare ; une ligne se ferme au-delà de 200 ms."""
    assert [len(l) for l in lignes([0.0, 50.0, 100.0, 150.0], 100.0, 'A')] == [4]
    assert len(lignes([0.0, 2000.0, 0.0, 2000.0], 100.0, 'A')) == 2
    # avec la variante B (fission, 1 demi-ton), 150 c sépare
    assert len(lignes([0.0, 150.0], 100.0, 'B')) == 2
    # fermeture : à T = 300 ms, chaque événement ouvre une ligne
    assert len(lignes([0.0, 10.0, 20.0], 300.0, 'A')) == 3


def test_exclusion_erb():
    """Une candidate à moins d'1 ERB du partiel dominant d'une copie active
    est exclue ; au-delà, non."""
    son = harmonic()
    f = 220.0
    e = erb(f)
    t_proche = 1200 * np.log2((f + 0.5 * e) / f)
    t_loin = 1200 * np.log2((f + 2.0 * e) / f)
    assert non_resolue(t_proche, [0.0], son, f, 1.0)
    assert not non_resolue(t_loin, [0.0], son, f, 1.0)


def test_grille_registre():
    g = grille_registre(harmonic(), 220.0)
    f_dom = 220.0 * 2 ** (g / 1200.0)
    assert f_dom.min() >= 30.0 - 1e-6 and f_dom.max() <= 4700.0 * 2 ** (2 / 1200)
