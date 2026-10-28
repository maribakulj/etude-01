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


# --- Phase 1 (PHASE1-PROTOCOLE.md) -------------------------------------------
from boucle.oreille.erb import erb                                        # noqa: E402
from boucle.oreille.rugosite import maximum_en_bandes_critiques           # noqa: E402
from boucle.oreille.harmonicite import hauteur_virtuelle, partiel_regroupe  # noqa: E402
from boucle.oreille.limites import plage_transposition                     # noqa: E402
from boucle.oreille import sequentiel                                      # noqa: E402
import pytest                                                              # noqa: E402

_ECHEC_C5 = pytest.mark.xfail(strict=True, reason="échec consigné : PHASE1-RESULTATS.md §1 et §3")

PRIME_WESTERKERK_HZ = 544.8   # notre extraction du bourdon 12-c1 (materiau/)


def test_erb():
    """C1 (cohérence)."""
    for f, attendu in ((100, 35.49), (1000, 132.64), (4000, 456.46)):
        assert abs(erb(f) - attendu) < 0.1


def test_rugosite_maximum_quart_de_bande():
    """C2 (validation partielle) : maximum entre 0,15 et 0,45 bande critique."""
    for f in (250, 500, 1000, 2000):
        assert 0.15 <= maximum_en_bandes_critiques(f) <= 0.45, f


def test_harmonique_desaccorde():
    """C4 (cohérence) : 0,5 % de désaccord reste regroupé, 4 % non."""
    k = np.arange(1, 11)
    for desaccord, attendu in ((0.005, True), (0.04, False)):
        f = 200.0 * k
        f[2] *= 1 + desaccord
        assert partiel_regroupe(f, 1.0 / k, 2) is attendu, desaccord


def test_fondamentale_absente():
    """C5 (a) : harmoniques 3 à 10 de 200 Hz -> 200 Hz à 1 % près."""
    f = 200.0 * np.arange(3, 11)
    h, _ = hauteur_virtuelle(f, np.ones_like(f))
    assert abs(h / 200.0 - 1) < 0.01


@_ECHEC_C5
def test_decalage_de_hauteur():
    """C5 (b) : 1840, 2040, 2240 Hz -> entre 202 et 206 Hz [SRC62, à vérifier]."""
    h, _ = hauteur_virtuelle([1840.0, 2040.0, 2240.0], [1.0, 1.0, 1.0])
    assert 202.0 <= h <= 206.0


@_ECHEC_C5
def test_note_de_frappe_cloche():
    """C5 (c) : cloche Westerkerk, hauteur à ±100 c de la prime."""
    r, a = _cloche()
    h, _ = hauteur_virtuelle(r * PRIME_WESTERKERK_HZ, a)
    assert abs(1200 * np.log2(h / PRIME_WESTERKERK_HZ)) <= 100.0


def test_plage_transposition():
    """C6 (cohérence) : son harmonique à 220 Hz."""
    k = np.arange(1, 11)
    t0, t1 = plage_transposition(k.astype(float), 1.0 / k, 220.0)
    assert abs(t0 - 1200 * np.log2(30 / 220)) < 1 and abs(t1 - 1200 * np.log2(4700 / 220)) < 1


def test_frontieres_van_noorden():
    """C7 (cohérence) : valeurs de van Noorden (1975) aux périodes 100, 150, 200 ms."""
    assert sequentiel.frontiere_fission() == 1.0
    assert sequentiel.frontiere_coherence(100, complexe=False) == 1.0
    assert abs(sequentiel.frontiere_coherence(150, complexe=False) - 7.5) < 1e-9
    assert abs(sequentiel.frontiere_coherence(200, complexe=False) - 15.0) < 1e-9
    assert abs(sequentiel.frontiere_coherence(150, complexe=True) - 16.5) < 1e-9
    assert sequentiel.relation(50, 150) == 'meme_ligne'
    assert sequentiel.relation(500, 150) == 'possible'
    assert sequentiel.relation(2000, 150) == 'separees'
