"""
rendu_phase2.py — rendu audio de quelques trajectoires de la phase 2, pour
l'écoute (qui ne fait pas partie des verdicts).

Chaque événement est une copie du son, transposée de t, à la fréquence de
référence du son (mesurée pour la cloche et la dent), avec la décroissance
exp(−temps/τ) du modèle, arrêtée quand le poids passe sous W_MIN. Les
silences de la boucle sont des pas sans événement.

Rejouer (après phase2.py) : `python3 boucle/rendu_phase2.py`
Sorties : boucle/sons/phase2_<son>_T<période>.wav, boucle/phase2_lignes.png
"""

import json
import os
import sys

import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or '.') != ICI]
sys.path.insert(0, os.path.dirname(ICI))

from boucle.registre import val                 # noqa: E402
from boucle.etape1 import sons                   # noqa: E402
from boucle.phase2 import f_ref                  # noqa: E402

CHOIX = val('EXEMPLES_ECOUTE_PHASE2')


def rendre(son, fref, ts, T_ms, tau_s, graine=0):
    sr = val('SR_RENDU')
    ratios, amps = son
    rng = np.random.default_rng(graine)
    n_copie = int(tau_s * np.log(1.0 / val('W_MIN')) * sr)
    temps = np.arange(n_copie) / sr
    env = np.exp(-temps / tau_s)
    n_att, n_fondu = int(val('ATTAQUE_RENDU') * sr), int(val('FONDU_RENDU') * sr)
    env[:n_att] *= np.linspace(0, 1, n_att)
    env[-n_fondu:] *= np.linspace(1, 0, n_fondu)
    n_pas = int(T_ms / 1000.0 * sr)
    y = np.zeros(n_pas * len(ts) + n_copie)
    for k, t in enumerate(ts):
        if t is None:
            continue
        f = fref * 2 ** (t / 1200.0)
        note = np.zeros(n_copie)
        for r, a in zip(ratios, amps):
            if f * r < 0.45 * sr:
                note += a * np.sin(2 * np.pi * f * r * temps + 2 * np.pi * rng.random())
        y[k * n_pas:k * n_pas + n_copie] += note * env
    return 0.8 * y / np.max(np.abs(y))


def main():
    with open(os.path.join(ICI, 'phase2_resultats.json')) as fh:
        runs = json.load(fh)['runs']
    S = sons()
    os.makedirs(os.path.join(ICI, 'sons'), exist_ok=True)
    fig, axes = plt.subplots(len(CHOIX), 1, figsize=(12, 2.2 * len(CHOIX)))
    for ax, (code, T) in zip(axes, CHOIX):
        r = next(r for r in runs if r['son'] == code and r['regle'] == 'argmax'
                 and r['T_ms'] == T and r['tau_s'] == min(x['tau_s'] for x in runs if x['son'] == code))
        y = rendre(S[code], f_ref(code), r['t'], T, r['tau_s'])
        nom = f'phase2_{code}_T{int(T)}.wav'
        sf.write(os.path.join(ICI, 'sons', nom), y, val('SR_RENDU'), subtype='PCM_16')
        print(f'  boucle/sons/{nom} ({len(y) / val("SR_RENDU"):.1f} s)')
        for li, ligne in enumerate(r['lignes']['A']):
            xs = [k * T / 1000 for k in ligne]
            ax.plot(xs, [r['t'][k] for k in ligne], '-o', ms=3, lw=0.9)
        m = r['mesures']['A']
        ax.set_title(f'{code}, T = {T:g} ms, τ = {r["tau_s"]} s — lignes (variante A) : '
                     f'{m["n_lignes"]}, {100 * m["part_lignes_4"]:.0f} % des événements '
                     f'dans une ligne d\'au moins 4', fontsize=8, loc='left')
        ax.set_ylabel('t (c)', fontsize=7)
        ax.tick_params(labelsize=7)
    axes[-1].set_xlabel('temps (s)', fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(ICI, 'phase2_lignes.png'), dpi=110)


if __name__ == '__main__':
    main()
