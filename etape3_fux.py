"""
etape3_fux.py — Étape 3 : automates (timbre × récepteur), fraction de Fux
récupérée (mesure SPEC §6.3), analyse de sensibilité tau_C / tau_F, et
comparaison harmonique vs cloche Westerkerk sur le même cantus.

Méthode (SPEC §7) : les seuils ne sont PAS figés. On les balaye ; une règle est
ROBUSTE si elle tient sur un large plateau de seuils, FRAGILE si elle bascule
avec le curseur. Les automates illustratifs sont construits aux seuils de
milieu de plateau, déclarés dans la sortie.

Cantus : le cantus firmus dorien de Fux (Gradus ad Parnassum, 1re espèce) :
D F E D G F A G F E D, en cents relatifs (12-TET), identique pour tous les
timbres comparés (décision déclarée dans graphe_grammaire.py).
"""

import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from metriques_fusion import harmonic
from graphe_grammaire import (grille_etats, construire_automate, chemin_legal,
                              SIGMA_FIGEE)

CANTUS_FUX = [0, 300, 200, 0, 500, 300, 700, 500, 300, 200, 0]  # cents, D dorien

NOMS = {0: 'unisson', 111.7: 'm2', 203.9: 'M2', 315.6: 'm3', 386.3: 'M3',
        498.0: 'P4', 590.2: 'TT', 702.0: 'P5', 813.7: 'm6', 884.4: 'M6',
        1017.6: 'm7', 1088.3: 'M7', 1200.0: 'P8'}


def nom(c):
    k = min(NOMS, key=lambda x: abs(x - c))
    d = c - k
    return NOMS[k] if abs(d) <= 20 else f"{NOMS[k]}{d:+.0f}c"


def cloche_westerkerk():
    with open('materiau/cloche_westerkerk_publie.json') as fh:
        d = json.load(fh)
    r = np.array([p['ratio'] for p in d['partiels']])
    a = np.array([p['amp'] for p in d['partiels']])
    return r, a


# ---------------------------------------------------------------------------
# Balayages : plateaux de seuils
# ---------------------------------------------------------------------------
def plateaux_tau_F(grille):
    """Ensemble d'intervalles interdits de parallèles (R2, parmi les états à
    Φ fini ; l'unisson est TOUJOURS interdit par convention) en fonction de
    tau_F. Renvoie [(set_intervalles, tau_min, tau_max, largeur_relative)]."""
    finis = sorted([e for e in grille if np.isfinite(e['Phi'])],
                   key=lambda e: -e['Phi'])
    phimax = finis[0]['Phi']
    bornes = [0.0] + sorted({e['Phi'] for e in finis}) + [phimax * 1.05]
    out = []
    for lo, hi in zip(bornes[:-1], bornes[1:]):
        tau = (lo + hi) / 2
        interdits = frozenset(round(e['intervalle']) for e in finis if e['Phi'] >= tau)
        if out and out[-1][0] == interdits:
            out[-1] = (interdits, out[-1][1], hi)
        else:
            out.append((interdits, lo, hi))
    return [(set(s), lo, hi, (hi - lo) / (phimax * 1.05)) for s, lo, hi in out]


def plateaux_tau_C(grille):
    """Ensemble d'états admis (R1) en fonction de tau_C."""
    cs = sorted({e['C'] for e in grille})
    bornes = [0.0] + cs + [1.0001]
    out = []
    for lo, hi in zip(bornes[:-1], bornes[1:]):
        tau = (lo + hi) / 2
        admis = frozenset(round(e['intervalle']) for e in grille if e['C'] >= tau)
        if out and out[-1][0] == admis:
            out[-1] = (admis, out[-1][1], hi)
        else:
            out.append((admis, lo, hi))
    return [(set(s), lo, hi, hi - lo) for s, lo, hi in out]


def affiche_plateaux(plats, titre, fmt_set):
    print(f"\n  {titre}")
    for s, lo, hi, w in plats:
        print(f"    tau ∈ [{lo:5.3f}, {hi:5.3f}] (largeur {w:4.2f}) : {fmt_set(s)}")


# ---------------------------------------------------------------------------
# Fraction de Fux (harmonique + humain)
# ---------------------------------------------------------------------------
FUX_CONSONANCES = {0, 316, 386, 702, 814, 884, 1200}   # P4 (498) EXCLUE par Fux
FUX_PARALLELES_INTERDITS = {0, 702, 1200}


def table_fux(grille):
    pC = plateaux_tau_C(grille)
    pF = plateaux_tau_F(grille)

    def proche(s, cible, tol=20):
        return {x for x in s if any(abs(x - c) <= tol for c in cible)} == s and \
               all(any(abs(x - c) <= tol for x in s) for c in cible)

    # F1 : existe-t-il un plateau tau_C donnant exactement l'ensemble de Fux ?
    f1 = [(s, w) for s, lo, hi, w in pC if proche(s, FUX_CONSONANCES)]
    # même chose en tolérant la quarte (ensemble Fux + P4)
    f1_p4 = [(s, w) for s, lo, hi, w in pC if proche(s, FUX_CONSONANCES | {498})]
    # F2/F3 : plateau tau_F donnant exactement {unisson, quinte, octave} ?
    # (l'unisson est interdit par convention -> on cherche {702, 1200} parmi les finis)
    f23 = [(s | {0}, w) for s, lo, hi, w in pF if proche(s, {702, 1200})]

    return dict(pC=pC, pF=pF, f1=f1, f1_p4=f1_p4, f23=f23)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def figure_automate(auto, fichier, chemin=None):
    cents, C, P = auto['courbes']
    fig, axes = plt.subplots(2, 1, figsize=(12, 7),
                             gridspec_kw=dict(height_ratios=[1, 1.3]))
    ax = axes[0]
    ax.plot(cents, C, color='#2a6f97', lw=1.4, label='C (consonance)')
    Pn = P / np.nanmax(P)
    ax.plot(cents, Pn, color='#c1121f', lw=1.4, label='Φ (fusion, norm.)')
    for e in auto['etats']:
        ax.axvline(e['intervalle'], color='0.8', lw=0.7, zorder=0)
        ax.plot(e['intervalle'], e['C'], 'o', color='#2a6f97', ms=5)
    interdits = sorted({a['vers'] for a in auto['supprimees']})
    for iv in interdits:
        ax.axvline(iv, color='#c1121f', lw=1.6, alpha=0.35)
    ax.set_title(f"{auto['label']} — états (pics de C, gate tau_C={auto['tau_C']}) ; "
                 f"interdits de parallèles R2 en rouge (tau_F={auto['tau_F']})",
                 fontsize=10, loc='left')
    ax.set_ylabel('normalisé')
    ax.legend(fontsize=8, loc='upper left')
    ax.set_xlim(0, 1200)

    ax = axes[1]
    N = len(auto['cantus'])
    for t, col in enumerate(auto['colonnes']):
        for e in col:
            ax.plot(t, e['intervalle'], 'o', color='0.6', ms=4, zorder=2)
    for a in auto['aretes']:
        ax.plot([a['t'], a['t'] + 1], [a['de'], a['vers']],
                color='0.85', lw=0.6, zorder=1)
    if chemin:
        ax.plot(range(N), chemin, '-o', color='#1b7837', lw=2.2, ms=6, zorder=3,
                label='chemin légal de poids minimal (R5)')
        ax.legend(fontsize=8, loc='upper right')
    ax.set_xticks(range(N))
    ax.set_xticklabels([f"{c / 100:.0f}" for c in auto['cantus']], fontsize=8)
    ax.set_xlabel('colonnes du cantus (pas en demi-tons, cantus de Fux en ré dorien)')
    ax.set_ylabel('intervalle du contrepoint (cents)')
    ax.set_title(f"treillis : {sum(len(c) for c in auto['colonnes'])} états, "
                 f"{len(auto['aretes'])} arêtes, {len(auto['supprimees'])} supprimées par R2",
                 fontsize=10, loc='left')
    plt.tight_layout()
    plt.savefig(fichier, dpi=130)
    plt.close()


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("ÉTAPE 3 — GRAPHE-GRAMMAIRE : automates, fraction de Fux, sensibilité")
    print("=" * 78)

    # ---------- Timbre harmonique + récepteur humain (contrôle) -------------
    spec_h = harmonic()
    grille_h, _ = grille_etats(spec_h)
    print("\n### HARMONIQUE + humain — grille candidate (pics de C) :")
    for e in grille_h:
        phi = '+inf (convention unisson)' if np.isinf(e['Phi']) else f"{e['Phi']:.3f}"
        print(f"  {e['intervalle']:7.1f} c ({nom(e['intervalle']):9s})  C={e['C']:.3f}  Φ={phi}")

    t = table_fux(grille_h)
    affiche_plateaux(t['pC'], "Plateaux tau_C (états admis par R1) :",
                     lambda s: sorted(s))
    affiche_plateaux(t['pF'], "Plateaux tau_F (interdits de parallèles R2, Φ finis) :",
                     lambda s: sorted(s))

    print("\n### FRACTION DE FUX RÉCUPÉRÉE (SPEC §6.3), harmonique + humain :")
    print(f"  F1 (verticales = consonances de Fux, SANS la quarte) : "
          f"{'OUI' if t['f1'] else 'NON'}"
          + (f" (plateau {t['f1'][0][1]:.2f})" if t['f1'] else ""))
    print(f"  F1' (consonances de Fux + quarte admise)             : "
          f"{'OUI' if t['f1_p4'] else 'NON'}"
          + (f" (plateau {t['f1_p4'][0][1]:.2f})" if t['f1_p4'] else ""))
    print(f"  F2+F3 (parallèles ET directes interdites vers unisson/quinte/octave) : "
          f"{'OUI' if t['f23'] else 'NON'}"
          + (f" (plateau relatif {t['f23'][0][1]:.2f})" if t['f23'] else ""))
    # F1 : à défaut d'un plateau exact, on mesure le recouvrement maximal
    def jaccard(s, cible, tol=20):
        inter = sum(1 for c in cible if any(abs(x - c) <= tol for x in s))
        union = len(s) + len(cible) - inter
        return inter / union
    jmax = max((jaccard(s, FUX_CONSONANCES), sorted(s)) for s, lo, hi, w in t['pC'] if s)
    print(f"  F1 (mesure du résidu) : meilleur recouvrement Jaccard = {jmax[0]:.2f}, "
          f"atteint par {jmax[1]}")
    print("  F4 (commencer/finir sur unisson/octave) : voir frontières R3 ci-dessous")
    print("  F5 (préférence mouvement contraire) : GABARIT R5 (forme imposée v1,")
    print("      pas une découverte — CADRAGE §9 ; seuls ses POIDS seraient ajustables)")

    # Automate illustratif : seuils choisis par un schéma DÉCLARÉ et symétrique
    # entre timbres (pas de cherry-picking) :
    #   tau_C = milieu du PLUS LARGE plateau de tau_C du timbre ;
    #   tau_F = même niveau RELATIF pour tous les timbres, défini une fois sur
    #           le cas de contrôle = milieu (relatif) du plateau de tau_F qui
    #           reproduit Fux ({P5, P8}) sur l'harmonique.
    pC_h = max(t['pC'], key=lambda p: p[3])
    tauC_h = (pC_h[1] + pC_h[2]) / 2
    phimax_h = max(e['Phi'] for e in grille_h if np.isfinite(e['Phi']))
    plateau_fux = next(p for p in t['pF'] if p[0] == {702, 1200})
    TAUF_REL = ((plateau_fux[1] + plateau_fux[2]) / 2) / phimax_h
    tauF_h = TAUF_REL * phimax_h
    print(f"\n  Schéma de seuils déclaré : tau_C = milieu du plus large plateau ;"
          f"\n  tau_F = {TAUF_REL:.3f} x max(Φ fini) du timbre (fixé par le plateau Fux du contrôle).")
    auto_h = construire_automate(spec_h, CANTUS_FUX, tauC_h, tauF_h,
                                 label='Timbre harmonique (récepteur humain)')
    ch_h = chemin_legal(auto_h)
    print(f"\n  Automate illustratif (tau_C={tauC_h}, tau_F={tauF_h:.3f}) :")
    print(f"    états admis : {[round(e['intervalle']) for e in auto_h['etats']]}")
    print(f"    frontières R3 : {auto_h['frontieres']} (argmax Φ fini : {auto_h['argmax_phi_fini']})")
    print(f"    arêtes : {len(auto_h['aretes'])} ; supprimées par R2 : {len(auto_h['supprimees'])}")
    if ch_h:
        print(f"    chemin légal : {[f'{c:.0f}' for c in ch_h]}")
        print(f"                   ({' '.join(nom(c) for c in ch_h)})")
    ex = [s for s in auto_h['supprimees'] if s['Phi_arrivee']][:3]
    for s in ex:
        print(f"    trace R2 ex. : t={s['t']} {s['de']:.0f}->{s['vers']:.0f}c "
              f"({s['mouvement']}), Φ={s['Phi_arrivee']:.3f}>=tau_F, "
              f"paire de partiels {s['paire']} (écart {s['ecart_paire_cents']:.1f}c)")
    figure_automate(auto_h, 'etape3_automate_harmonique.png', ch_h)

    # ---------- Cloche Westerkerk + récepteur humain -------------------------
    spec_b = cloche_westerkerk()
    grille_b, _ = grille_etats(spec_b)
    print("\n### CLOCHE WESTERKERK (spectre publié) + humain — grille candidate :")
    for e in grille_b:
        phi = '+inf' if np.isinf(e['Phi']) else f"{e['Phi']:.3f}"
        print(f"  {e['intervalle']:7.1f} c ({nom(e['intervalle']):9s})  C={e['C']:.3f}  Φ={phi}")
    tb = dict(pC=plateaux_tau_C(grille_b), pF=plateaux_tau_F(grille_b))
    affiche_plateaux(tb['pC'], "Plateaux tau_C :", lambda s: sorted(s))
    affiche_plateaux(tb['pF'], "Plateaux tau_F (interdits R2) :", lambda s: sorted(s))

    # Mêmes règles de seuils déclarées que pour le contrôle :
    pC_b = max(tb['pC'], key=lambda p: p[3])
    tauC_b = (pC_b[1] + pC_b[2]) / 2
    phimax_b = max(e['Phi'] for e in grille_b if np.isfinite(e['Phi']))
    tauF_b = TAUF_REL * phimax_b
    auto_b = construire_automate(spec_b, CANTUS_FUX, tauC_b, tauF_b,
                                 label='Cloche Westerkerk (récepteur humain)')
    ch_b = chemin_legal(auto_b)
    print(f"\n  Automate illustratif (tau_C={tauC_b}, tau_F={tauF_b:.3f}) :")
    print(f"    états admis : {[round(e['intervalle']) for e in auto_b['etats']]}")
    print(f"    frontières R3 : {auto_b['frontieres']} (argmax Φ fini : {auto_b['argmax_phi_fini']})")
    print(f"    interdits R2 (parmi états) : {sorted({round(a['vers']) for a in auto_b['supprimees']})}")
    print(f"    arêtes : {len(auto_b['aretes'])} ; supprimées : {len(auto_b['supprimees'])}")
    if ch_b:
        print(f"    chemin légal : {[f'{c:.0f}' for c in ch_b]}")
        print(f"                   ({' '.join(nom(c) for c in ch_b)})")
    else:
        print("    AUCUN CHEMIN LÉGAL pour ce cantus dans la grammaire de la cloche :")
        print("      R3 exige de finir sur {unisson, 307c} ; la descente finale du")
        print("      cantus ne permet d'atteindre ni l'un (toute arrivée serait")
        print("      parallèle/directe vers Φ=+inf) ni l'autre (approche contraire")
        print("      exigée depuis un état < 107c, lui-même inaccessible).")
        print("      -> Le cantus, écrit pour la grammaire harmonique, est REJETÉ.")
        # Contre-épreuve : le cantus MIROIR (inversion stricte, geste classique)
        cantus_miroir = [-c for c in CANTUS_FUX]
        auto_b2 = construire_automate(spec_b, cantus_miroir, tauC_b, tauF_b,
                                      label='Cloche Westerkerk — cantus miroir')
        ch_b2 = chemin_legal(auto_b2)
        if ch_b2:
            print(f"    Contre-épreuve (cantus MIROIR) : chemin légal trouvé :")
            print(f"      {[f'{c:.0f}' for c in ch_b2]}")
            print(f"      ({' '.join(nom(c) for c in ch_b2)})")
            figure_automate(auto_b2, 'etape3_automate_cloche_miroir.png', ch_b2)
        else:
            print("    Contre-épreuve (cantus miroir) : pas de chemin non plus.")
    figure_automate(auto_b, 'etape3_automate_cloche.png', ch_b)

    # ---------- Comparaison (LE résultat : un automate par timbre) ----------
    print("\n### COMPARAISON DES AUTOMATES (le produit du système) :")
    et_h = {round(e['intervalle']) for e in auto_h['etats']}
    et_b = {round(e['intervalle']) for e in auto_b['etats']}
    in_h = {round(a['vers']) for a in auto_h['supprimees']}
    in_b = {round(a['vers']) for a in auto_b['supprimees']}
    print(f"  états harmonique : {sorted(et_h)}")
    print(f"  états cloche     : {sorted(et_b)}")
    print(f"  interdits de parallèles harmonique : {sorted(in_h)}")
    print(f"  interdits de parallèles cloche     : {sorted(in_b)}")
    print(f"  frontières R3 harmonique : {auto_h['frontieres']}")
    print(f"  frontières R3 cloche     : {auto_b['frontieres']}")

    return dict(auto_h=auto_h, auto_b=auto_b, fux=t)


if __name__ == '__main__':
    main()
