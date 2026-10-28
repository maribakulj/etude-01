"""
mesure_cloche.py — constante de décroissance d'une cloche enregistrée
(PHASE2-PROTOCOLE.md §2) : intégration inverse de Schroeder de l'énergie
large bande, ajustement linéaire entre −5 et −25 dB, T60 extrapolé,
τ (constante de temps de l'amplitude) = T60 / ln(1000).

Le bruit de fond est estimé sur les 2 dernières secondes et soustrait ;
l'intégration s'arrête quand l'enveloppe lissée (50 ms) redescend à deux fois
ce bruit. Ces trois choix (2 s, 50 ms, facteur 2) sont techniques et déclarés
au registre ; leur sensibilité est rapportée dans le fichier de sortie.

Usage : python3 boucle/mesure_cloche.py chemin/vers/12-c1.wav
Sortie : boucle/mesures/cloche_12c1_decroissance.json (l'audio n'est pas commité).
"""

import hashlib
import json
import os
import sys

import numpy as np
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or '.') != ICI]
sys.path.insert(0, os.path.dirname(ICI))

from boucle.registre import val   # noqa: E402


def t60_schroeder(x, sr, bruit_s, lissage_s, facteur_bruit, haut_db=-5.0, bas_db=-25.0):
    e = x ** 2
    debut = int(np.argmax(e))
    bruit = float(np.mean(e[-int(bruit_s * sr):]))
    n_l = int(lissage_s * sr)
    env = np.convolve(e, np.ones(n_l) / n_l, mode='same')
    fin_candidats = np.where(env[debut:] <= facteur_bruit * bruit)[0]
    fin = debut + (int(fin_candidats[0]) if len(fin_candidats) else len(e) - debut)
    utile = np.clip(e[debut:fin] - bruit, 0, None)
    E = np.cumsum(utile[::-1])[::-1]
    db = 10 * np.log10(E / E[0] + 1e-300)
    t = np.arange(len(db)) / sr
    m = (db <= haut_db) & (db >= bas_db)
    pente, _ = np.polyfit(t[m], db[m], 1)
    return -60.0 / pente, fin / sr - debut / sr


def main(chemin):
    x, sr = sf.read(chemin, always_2d=True)
    x = x.mean(axis=1)
    sha = hashlib.sha256(open(chemin, 'rb').read()).hexdigest()[:16]
    b, l, f = val('MESURE_BRUIT_S'), val('MESURE_LISSAGE_S'), val('MESURE_FACTEUR_BRUIT')
    t60, duree = t60_schroeder(x, sr, b, l, f)
    sens = {f'bruit {bb} s, lissage {ll} s, facteur {ff}': round(t60_schroeder(x, sr, bb, ll, ff)[0], 3)
            for bb in (1.0, 2.0, 3.0) for ll in (0.02, 0.05) for ff in (2.0, 4.0)}
    out = dict(source='12-c1.wav, github.com/pmcharrison/CarillonConsonancePaper '
                      '(Harrison & MacConnachie 2024), input/bell-samples',
               sha256_16=sha, sr=sr, duree_s=round(len(x) / sr, 3),
               duree_integree_s=round(duree, 3),
               methode='Schroeder, ajustement −5 à −25 dB, T60 extrapolé',
               T60_s=round(t60, 3), tau_s=round(t60 / np.log(1000.0), 3),
               sensibilite_T60_s=sens)
    os.makedirs(os.path.join(ICI, 'mesures'), exist_ok=True)
    chemin_out = os.path.join(ICI, 'mesures', 'cloche_12c1_decroissance.json')
    with open(chemin_out, 'w') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1])
