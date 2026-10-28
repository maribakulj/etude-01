"""Tests du modèle de l'oreille : chaque composant reproduit une donnée."""

import json
import os

import numpy as np

from boucle.oreille import courbe_coincidence
from boucle.registre import val
from metriques_fusion import harmonic, proxy_coincidence

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _cloche():
    with open(os.path.join(RACINE, 'materiau', 'cloche_westerkerk_publie.json')) as fh:
        d = json.load(fh)
    return (np.array([p['ratio'] for p in d['partiels']]),
            np.array([p['amp'] for p in d['partiels']]))


def test_coincidence_egale_phi_publiee():
    """Avec une seule copie à t = 0, la courbe est exactement Φ (forme de
    Milne, σ publié), et elle reproduit sur le son harmonique le classement de
    fusion octave > quinte > quarte (Stumpf ; DeWitt & Crowder 1987)."""
    sigma = val('SIGMA_MILNE')
    grille = np.array([498.0, 702.0, 1200.0, 307.0, 886.0])
    for son in (harmonic(), _cloche()):
        y = courbe_coincidence(son, [(0.0, 1.0)], sigma, grille)
        attendu = [proxy_coincidence(son, 2 ** (t / 1200.0), w_cents=sigma) for t in grille]
        assert np.allclose(y, attendu, rtol=1e-12, atol=0)
    y = courbe_coincidence(harmonic(), [(0.0, 1.0)], sigma, grille)
    assert y[2] > y[1] > y[0]
