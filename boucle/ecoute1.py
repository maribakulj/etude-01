"""
ecoute1.py — contrôle d'écoute : trajectoire de la boucle contre les mêmes
notes dans un ordre mélangé (ECOUTE1-PROTOCOLE.md).

Pour la cloche et le son harmonique (règle argmax, T = 200 ms, τ le plus
court), on rend deux fichiers au même tempo : l'original, et une permutation
aléatoire des mêmes notes. L'ordre des deux fichiers de chaque paire est tiré
au hasard ; la correspondance est écrite dans le fichier passé en argument,
à garder hors de vue de l'auditeur jusqu'à sa réponse.

Usage : python3 boucle/ecoute1.py chemin/correspondance.json
Sorties : boucle/sons/ecoute1_{A,B}{1,2}.wav ; mesures des lignes du modèle
pour chaque version, imprimées (elles ne disent pas quel fichier est lequel).
"""

import json
import os
import sys

import numpy as np
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or '.') != ICI]
sys.path.insert(0, os.path.dirname(ICI))

from boucle.registre import val                       # noqa: E402
from boucle.etape1 import sons                         # noqa: E402
from boucle.phase2 import f_ref, lignes, mesures_lignes  # noqa: E402
from boucle.rendu_phase2 import rendre                 # noqa: E402


def main(chemin_correspondance):
    with open(os.path.join(ICI, 'phase2_resultats.json')) as fh:
        runs = json.load(fh)['runs']
    S = sons()
    rng = np.random.default_rng(val('GRAINE_ECOUTE1'))
    correspondance = {}
    for paire, code in zip('AB', val('SONS_ECOUTE1')):
        T = val('PERIODE_ECOUTE1_MS')
        r = next(x for x in runs if x['son'] == code and x['regle'] == 'argmax'
                 and x['T_ms'] == T and x['tau_s'] == min(y['tau_s'] for y in runs if y['son'] == code))
        original = list(r['t'])
        melange = list(rng.permutation(np.array(original, dtype=float)))
        versions = {'original': original, 'melange': melange}
        for nom, ts in versions.items():
            m = mesures_lignes(lignes(ts, T, 'A'))
            print(f"  {code:7s} {nom:9s} lignes (modèle, variante A) : {m['n_lignes']}, "
                  f"{100 * m['part_lignes_4']:.0f} % des notes dans une ligne d'au moins 4")
        ordre = ['original', 'melange'] if rng.random() < 0.5 else ['melange', 'original']
        for i, nom in enumerate(ordre, start=1):
            y = rendre(S[code], f_ref(code), versions[nom], T, r['tau_s'])
            fichier = f'ecoute1_{paire}{i}.wav'
            sf.write(os.path.join(ICI, 'sons', fichier), y, val('SR_RENDU'), subtype='PCM_16')
            correspondance[fichier] = dict(son=code, version=nom)
    with open(chemin_correspondance, 'w') as fh:
        json.dump(correspondance, fh, indent=1, ensure_ascii=False)
    print('  fichiers : boucle/sons/ecoute1_A1.wav, A2, B1, B2')


if __name__ == '__main__':
    main(sys.argv[1])
