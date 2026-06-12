"""
etape4_stimuli.py — Étape 4 : rendu pour l'écoute de falsification.

Synthèse additive avec EXACTEMENT les partiels des modèles (harmonique 1..10
roll-off 1/k ; cloche Westerkerk : les 11 partiels publiés, amplitudes
comprises). Tenue stationnaire : ce que le modèle v1 modélise est la
simultanéité de spectres tenus — on écoute donc le modèle, pas un instrument
imité. Mono (la spatialisation séparerait les voix par un indice hors modèle).

Plan de stimuli (noms NEUTRES A..F pour l'écoute ; correspondance dans
ETAPE4-ECOUTE.md, à lire APRÈS avoir noté) :

  Croisement décisif (mêmes notes, timbre échangé) :
    - quintes parallèles : interdites par la grammaire harmonique,
      ~légales sur la cloche (Φ_cloche(702)=0.287 < tau_F=0.291) ;
    - « tierces de cloche » (307 c) parallèles : interdites sur la cloche,
      légales sur l'harmonique (Φ_harm(307)≈0.02 — creux de fusion).
  Plus les deux chemins LÉGAUX dérivés à l'étape 3 (un par grammaire).

Les voix sont à RMS égal ; jugement demandé : SÉPARABILITÉ (une couche ou
deux voix ?), pas l'agrément — l'hygiène C≠Φ vaut aussi à l'écoute.
"""

import json

import numpy as np
import soundfile as sf

from metriques_fusion import harmonic
from etape3_fux import cloche_westerkerk, CANTUS_FUX
from graphe_grammaire import construire_automate, chemin_legal, grille_etats

SR = 44100
DUREE_NOTE = 1.15      # s
FONDU = 0.02           # crossfade entre notes (s)
ATT, REL = 0.03, 0.12  # attaque/relâchement global (s)
F_BASE = 220.0         # cantus : note de référence (cents=0)


def voix(spec, cents_seq, f_base=F_BASE):
    """Une voix : séquence de notes tenues (synthèse additive du spectre)."""
    ratios, amps = spec
    n_note = int(DUREE_NOTE * SR)
    n_x = int(FONDU * SR)
    total = n_note * len(cents_seq)
    y = np.zeros(total)
    for k, c in enumerate(cents_seq):
        f = f_base * 2 ** (c / 1200.0)
        t = np.arange(n_note) / SR
        note = np.zeros(n_note)
        for r, a in zip(ratios, amps):
            fp = f * r
            if fp < SR / 2 * 0.95:
                note += a * np.sin(2 * np.pi * fp * t + 2 * np.pi * np.random.rand())
        env = np.ones(n_note)
        env[:n_x] = np.linspace(0, 1, n_x)
        env[-n_x:] = np.linspace(1, 0, n_x)
        a0 = k * n_note
        y[a0:a0 + n_note] += note * env
    return y


def stimulus(spec, cantus, contrepoint, fichier):
    """Deux voix (cantus + contrepoint en cents au-dessus), RMS égal, mono."""
    vA = voix(spec, cantus)
    vB = voix(spec, [c + i for c, i in zip(cantus, contrepoint)])
    vA /= np.sqrt(np.mean(vA ** 2)) + 1e-12
    vB /= np.sqrt(np.mean(vB ** 2)) + 1e-12
    y = vA + vB
    n_att, n_rel = int(ATT * SR), int(REL * SR)
    y[:n_att] *= np.linspace(0, 1, n_att)
    y[-n_rel:] *= np.linspace(1, 0, n_rel)
    y = 0.7 * y / np.max(np.abs(y))
    sf.write(fichier, y, SR, subtype='PCM_16')
    print(f"  {fichier}  ({len(y)/SR:.1f} s)")


def main():
    rng = np.random.default_rng(42)
    np.random.seed(7)  # phases de synthèse reproductibles

    spec_h = harmonic()
    spec_b = cloche_westerkerk()

    # Chemins légaux recalculés (provenance : harnais étape 3, mêmes seuils)
    g_h, _ = grille_etats(spec_h)
    g_b, _ = grille_etats(spec_b)
    phimax_h = max(e['Phi'] for e in g_h if np.isfinite(e['Phi']))
    phimax_b = max(e['Phi'] for e in g_b if np.isfinite(e['Phi']))
    TAUF_REL = 0.226
    auto_h = construire_automate(spec_h, CANTUS_FUX, 0.279, TAUF_REL * phimax_h)
    ch_h = chemin_legal(auto_h)
    MIROIR = [-c for c in CANTUS_FUX]
    auto_b = construire_automate(spec_b, MIROIR, 0.226, TAUF_REL * phimax_b)
    ch_b = chemin_legal(auto_b)
    assert ch_h and ch_b

    PAR_P5 = [702.0] * len(CANTUS_FUX)    # quintes parallèles strictes
    PAR_M3C = [307.0] * len(CANTUS_FUX)   # tierces-de-cloche parallèles

    print("Génération des stimuli (noms neutres) :")
    plan = {
        'stim_A.wav': dict(timbre='cloche', notes='tierces 307c parallèles (cantus Fux)',
                           statut='INTERDIT par R2-cloche',
                           spec=spec_b, cantus=CANTUS_FUX, ctp=PAR_M3C),
        'stim_B.wav': dict(timbre='harmonique', notes='chemin légal étape 3 (cantus Fux)',
                           statut='LÉGAL (grammaire harmonique)',
                           spec=spec_h, cantus=CANTUS_FUX, ctp=ch_h),
        'stim_C.wav': dict(timbre='cloche', notes='quintes 702c parallèles (cantus Fux)',
                           statut='~légal sur cloche (Φ=0.287 < tau_F=0.291)',
                           spec=spec_b, cantus=CANTUS_FUX, ctp=PAR_P5),
        'stim_D.wav': dict(timbre='harmonique', notes='quintes 702c parallèles (cantus Fux)',
                           statut='INTERDIT par R2-harmonique',
                           spec=spec_h, cantus=CANTUS_FUX, ctp=PAR_P5),
        'stim_E.wav': dict(timbre='cloche', notes='chemin légal étape 3 (cantus miroir)',
                           statut='LÉGAL (grammaire cloche)',
                           spec=spec_b, cantus=MIROIR, ctp=ch_b),
        'stim_F.wav': dict(timbre='harmonique', notes='tierces 307c parallèles (cantus Fux)',
                           statut='légal sur harmonique (Φ≈0.02, creux)',
                           spec=spec_h, cantus=CANTUS_FUX, ctp=PAR_M3C),
    }
    mapping = {}
    for nom, d in plan.items():
        stimulus(d['spec'], d['cantus'], d['ctp'], nom)
        mapping[nom] = {k: v for k, v in d.items() if k in ('timbre', 'notes', 'statut')}
        if d['ctp'] in (ch_h, ch_b):
            mapping[nom]['contrepoint_cents'] = [round(c) for c in d['ctp']]
    with open('etape4_mapping.json', 'w') as fh:
        json.dump(mapping, fh, indent=1, ensure_ascii=False)
    print("écrit : etape4_mapping.json")


if __name__ == '__main__':
    main()
