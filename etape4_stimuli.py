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
DUREE_NOTE = 0.62      # s — v3 : tempo musical (la ségrégation vit dans le mouvement)
RING = 2.0             # chaque note résonne au-delà de son pas (×DUREE_NOTE),
                       # comme un vrai carillon ; identique partout
ATT_NOTE = 0.008       # attaque par note (s)
TAU_DECAY = 0.55       # décroissance exponentielle GLOBALE par note (s).
                       # Globale = tous les partiels décroissent ensemble :
                       # les rapports d'amplitudes (donc Φ) restent EXACTEMENT
                       # ceux du modèle à chaque instant de la note. On
                       # restaure l'événement (l'articulation, sans laquelle
                       # AUCUNE voix n'est audible — constat de la 1re écoute,
                       # v. ETAPE4-ECOUTE.md §7) sans toucher au spectre.
ATT, REL = 0.03, 0.25  # attaque/relâchement global (s)
F_BASE = 220.0         # cantus : note de référence (cents=0)
PAUSE_PAIRE = 0.9      # silence entre les deux moitiés d'une paire (s)


def voix(spec, cents_seq, f_base=F_BASE):
    """Une voix : notes articulées (attaque brève + décroissance exponentielle
    globale) dont la résonance DÉBORDE sur la note suivante (RING), comme un
    carillon réel. Synthèse additive du spectre du modèle. Enveloppe IDENTIQUE
    pour toutes les voix et tous les timbres (aucun indice de ségrégation
    asymétrique ajouté)."""
    ratios, amps = spec
    n_pas = int(DUREE_NOTE * SR)
    n_note = int(RING * DUREE_NOTE * SR)
    total = n_pas * len(cents_seq) + (n_note - n_pas)
    y = np.zeros(total)
    t = np.arange(n_note) / SR
    n_att = int(ATT_NOTE * SR)
    env = np.exp(-t / TAU_DECAY)
    env[:n_att] *= np.linspace(0, 1, n_att)
    env[-int(0.005 * SR):] *= np.linspace(1, 0, int(0.005 * SR))
    for k, c in enumerate(cents_seq):
        f = f_base * 2 ** (c / 1200.0)
        note = np.zeros(n_note)
        for r, a in zip(ratios, amps):
            fp = f * r
            if fp < SR / 2 * 0.95:
                note += a * np.sin(2 * np.pi * fp * t + 2 * np.pi * np.random.rand())
        a0 = k * n_pas
        y[a0:a0 + n_note] += note * env
    return y


def sans_unisson_median(automate):
    """Copie de l'automate où l'unisson est retiré des colonnes MÉDIANES, pour
    la sélection du chemin-STIMULUS uniquement (pas un changement de
    grammaire) : la fusion de l'unisson est triviale par construction et
    masquerait la comparaison demandée à l'auditeur — et c'est par ailleurs la
    règle de Fux (unisson réservé aux extrémités), résidu déjà documenté à
    l'étape 3."""
    a = dict(automate)
    cols = [list(c) for c in automate['colonnes']]
    for t in range(1, len(cols) - 1):
        cols[t] = [e for e in cols[t] if e['intervalle'] > 1e-9]
    ok = {(t, e['intervalle']) for t, col in enumerate(cols) for e in col}
    a['colonnes'] = cols
    a['aretes'] = [ar for ar in automate['aretes']
                   if (ar['t'], ar['de']) in ok and (ar['t'] + 1, ar['vers']) in ok]
    return a


def extrait(spec, cantus, contrepoint):
    """Deux voix (cantus + contrepoint en cents au-dessus), RMS égal, mono."""
    vA = voix(spec, cantus)
    vB = voix(spec, [c + i for c, i in zip(cantus, contrepoint)])
    vA /= np.sqrt(np.mean(vA ** 2)) + 1e-12
    vB /= np.sqrt(np.mean(vB ** 2)) + 1e-12
    y = vA + vB
    n_att, n_rel = int(ATT * SR), int(REL * SR)
    y[:n_att] *= np.linspace(0, 1, n_att)
    y[-n_rel:] *= np.linspace(1, 0, n_rel)
    return 0.7 * y / np.max(np.abs(y))


def paire(ex1, ex2, fichier):
    """Un fichier = extrait 1, silence, extrait 2 (choix forcé)."""
    y = np.concatenate([ex1, np.zeros(int(PAUSE_PAIRE * SR)), ex2])
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
    ch_h = chemin_legal(sans_unisson_median(auto_h))
    MIROIR = [-c for c in CANTUS_FUX]
    auto_b = construire_automate(spec_b, MIROIR, 0.226, TAUF_REL * phimax_b)
    ch_b = chemin_legal(sans_unisson_median(auto_b))
    assert ch_h and ch_b, "pas de chemin légal sans unisson médian"
    print(f"chemin harmonique (sans unisson médian) : {[round(c) for c in ch_h]}")
    print(f"chemin cloche     (sans unisson médian) : {[round(c) for c in ch_b]}")

    PAR_P5 = [702.0] * len(CANTUS_FUX)    # quintes parallèles strictes
    PAR_M3C = [307.0] * len(CANTUS_FUX)   # tierces-de-cloche parallèles

    # Extraits (conditions nommées)
    ex = {
        'harm_legal':    extrait(spec_h, CANTUS_FUX, ch_h),
        'harm_par_P5':   extrait(spec_h, CANTUS_FUX, PAR_P5),
        'harm_par_307':  extrait(spec_h, CANTUS_FUX, PAR_M3C),
        'cloche_legal':  extrait(spec_b, MIROIR, ch_b),
        'cloche_par_P5': extrait(spec_b, CANTUS_FUX, PAR_P5),
        'cloche_par_307': extrait(spec_b, CANTUS_FUX, PAR_M3C),
    }

    # v3 (2026-06-12, après 2e écoute) : CHOIX FORCÉ PAR PAIRES — chaque
    # fichier = deux extraits dos à dos ; question : quelle moitié se fond le
    # plus en une seule coulée ? L'ordre des moitiés est tiré et consigné dans
    # le mapping (à ne lire qu'après réponse).
    paires = {
        'paire_P1.wav': ('harm_par_P5', 'harm_legal'),       # E1, ordre: parallèles d'abord
        'paire_P2.wav': ('cloche_legal', 'cloche_par_307'),  # E2, ordre: légal d'abord
        'paire_P3.wav': ('cloche_par_P5', 'harm_par_P5'),    # E3, ordre: cloche d'abord
        'paire_P4.wav': ('harm_par_307', 'cloche_par_307'),  # E4, ordre: harmonique d'abord
    }
    print("Génération des paires v3 :")
    mapping = {}
    for nom, (m1, m2) in paires.items():
        paire(ex[m1], ex[m2], nom)
        mapping[nom] = dict(moitie_1=m1, moitie_2=m2)
    mapping['chemins'] = dict(harm=[round(c) for c in ch_h],
                              cloche=[round(c) for c in ch_b])
    with open('etape4_mapping.json', 'w') as fh:
        json.dump(mapping, fh, indent=1, ensure_ascii=False)
    print("écrit : etape4_mapping.json")


if __name__ == '__main__':
    main()
