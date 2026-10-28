"""
rendu.py — rendu audio des trajectoires de la boucle (PROTOCOLE.md §8).

Une trajectoire par son, réglage canonique (argmax, τ = 4, σ = 6,83), lue
dans boucle/resultats.json. Chaque copie est le son de départ transposé de t
(t = 0 ↔ 220 Hz), synthétisé à partir de ses partiels, avec une décroissance
exp(−temps / (τ × durée d'un pas)) : c'est la version continue des poids du
modèle, et la copie s'arrête quand son poids passe sous 0,05, comme dans la
boucle. L'écoute ne fait pas partie du verdict.

Rejouer (après boucle.py) : `python3 boucle/rendu.py`
Sorties : boucle/sons/boucle_<son>.wav
"""

import json
import os
import sys

import numpy as np
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from boucle import sons, W_MIN, REGLAGE_CANONIQUE   # noqa: E402

SR = 22050
DUREE_PAS = 0.45     # s
F0 = 220.0           # Hz pour t = 0
ATTAQUE = 0.005      # s
FONDU = 0.03         # s, pour éviter un clic à l'arrêt de la copie


def rendre(son, ts, tau, graine=0):
    ratios, amps = son
    rng = np.random.default_rng(graine)
    duree_copie = tau * np.log(1.0 / W_MIN) * DUREE_PAS
    n_copie = int(duree_copie * SR)
    temps = np.arange(n_copie) / SR
    env = np.exp(-temps / (tau * DUREE_PAS))
    n_att, n_fondu = int(ATTAQUE * SR), int(FONDU * SR)
    env[:n_att] *= np.linspace(0, 1, n_att)
    env[-n_fondu:] *= np.linspace(1, 0, n_fondu)
    n_pas = int(DUREE_PAS * SR)
    y = np.zeros(n_pas * len(ts) + n_copie)
    for k, t in enumerate(ts):
        f = F0 * 2 ** (t / 1200.0)
        note = np.zeros(n_copie)
        for r, a in zip(ratios, amps):
            if f * r < 0.45 * SR:
                note += a * np.sin(2 * np.pi * f * r * temps + 2 * np.pi * rng.random())
        y[k * n_pas:k * n_pas + n_copie] += note * env
    return 0.8 * y / np.max(np.abs(y))


def main():
    with open(os.path.join(ICI, 'resultats.json')) as fh:
        res = json.load(fh)
    regle, graine, tau, sigma = REGLAGE_CANONIQUE
    os.makedirs(os.path.join(ICI, 'sons'), exist_ok=True)
    for code, son in sons().items():
        r = next(r for r in res['runs'] if r['son'] == code and r['regle'] == regle
                 and r['graine'] == graine and r['tau'] == tau and r['sigma'] == sigma)
        y = rendre(son, r['t'], tau)
        chemin = os.path.join(ICI, 'sons', f'boucle_{code}.wav')
        sf.write(chemin, y, SR, subtype='PCM_16')
        print(f'  {os.path.relpath(chemin, os.path.dirname(ICI))} ({len(y) / SR:.1f} s)')


if __name__ == '__main__':
    main()
