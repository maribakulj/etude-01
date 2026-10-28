"""Critère de sortie de la phase 0 : l'étape 1 est reproduite à l'identique
(ici sur les deux trajectoires canoniques ; reproduire.sh rejoue le tout)."""

import json
import os

import numpy as np

from boucle.etape1 import sons, trajectoire, REGLAGE_CANONIQUE

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_trajectoires_canoniques_identiques():
    with open(os.path.join(ICI, 'resultats.json')) as fh:
        res = json.load(fh)
    regle, graine, tau, sigma = REGLAGE_CANONIQUE
    S = sons()
    for code in ('harm', 'cloche'):
        ref = next(r for r in res['runs'] if r['son'] == code and r['regle'] == regle
                   and r['graine'] == graine and r['tau'] == tau and r['sigma'] == sigma)
        tr = trajectoire(S[code], regle, graine, tau, sigma)
        assert np.round(tr['t'], 2).tolist() == ref['t'], code
