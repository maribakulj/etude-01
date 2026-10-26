"""
etape2_p5.py — Étape 2 : rejouer P5 sur un spectre MESURÉ, avec la métrique Φ
figée (DECISION-PHI.md : coïncidence spectrale sous transposition, σ=6,83 c).

Usage :
  python3 etape2_p5.py extraction.json      # spectre mesuré (extraction_spectre.py)
  python3 etape2_p5.py --analytique         # démo : spectre Euler-Bernoulli (pas une mesure)

Verdict P5 (opérationnalisation de SPEC §6.2, déclarée AVANT toute mesure,
cf. ETAPE2-PROTOCOLE.md) :
  - pics PRINCIPAUX = pics hors zone quasi-unisson (<100 c) dont la hauteur
    vaut au moins PIC_MIN_FRAC du pic maximal de la courbe ;
  - un pic mesuré « coïncide » avec un pic harmonique (1200/702/498 c) si leur
    écart est ≤ SEUIL_DEPLACEMENT ;
  - P5 TIENT si la structure des pics diffère : au moins un pic principal
    mesuré ne coïncide avec aucun pic harmonique, OU un pic harmonique majeur
    (octave, quinte) n'a aucun correspondant mesuré.
  - P5 ÉCHOUE (critère d'abandon SPEC §6.2) si tous les pics principaux
    mesurés coïncident avec les pics harmoniques ET réciproquement.

SEUIL_DEPLACEMENT = 25 c : largement au-dessus de la tolérance de la chaîne de
mesure (±15 c, validée par test_extraction.py) et de la JND d'accordage (~10 c),
et en dessous du déplacement prédit par le modèle analytique (35 c pour
l'octave comprimée). PIC_MIN_FRAC = 0,05.
"""

import json
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from metriques_fusion import harmonic, music_box, proxy_coincidence, peaks, JUST
from extraction_spectre import spectre_pour_phi

SIGMA_FIGEE = 6.83          # DECISION-PHI.md — ne pas modifier ici
SEUIL_DEPLACEMENT = 25.0    # cents — déclaré avant mesure
PIC_MIN_FRAC = 0.05
PICS_HARMONIQUES = [1200.0, 702.0, 498.0]   # P2, validés étape 1
# Garde de dégénérescence (ajout daté du 2026-06-11, ETAPE2-PROTOCOLE.md §7,
# déclarée avant tout calcul de Φ sur le matériau mesuré) : si la courbe
# mesurée culmine sous 5 % du pic d'octave harmonique, elle est PLATE -> cas
# dégénéré du CADRAGE §9, verdict P5 SANS OBJET. La garde ne peut qu'empêcher
# un verdict (le harnais détecterait sinon des « pics » de bruit numérique sur
# une courbe nulle), jamais en fabriquer un.
GARDE_DEGENERESCENCE = 0.05

CENTS = np.linspace(1.0, 1200.0, 1200)


def courbe_phi(spec):
    return np.array([proxy_coincidence(spec, 2 ** (c / 1200.0), w_cents=SIGMA_FIGEE)
                     for c in CENTS])


def pics_principaux(P):
    out = []
    idx = peaks(P, CENTS, n=6)
    if not idx:
        return out
    top = max(P[i] for i in idx)
    for i in idx:
        if P[i] >= PIC_MIN_FRAC * top:
            out.append((float(CENTS[i]), float(P[i])))
    return out


def verdict_p5(pics_mes):
    """Applique le verdict déclaré. Renvoie (tient: bool, lignes de détail)."""
    detail = []
    deplaces = []
    for c, v in pics_mes:
        d = min(abs(c - h) for h in PICS_HARMONIQUES)
        h = min(PICS_HARMONIQUES, key=lambda x: abs(c - x))
        coincide = d <= SEUIL_DEPLACEMENT
        detail.append(f"pic {c:6.1f} c (Φ={v:.3f}) : à {d:5.1f} c de {h:.0f} c -> "
                      f"{'COÏNCIDE' if coincide else 'DÉPLACÉ'}")
        if not coincide:
            deplaces.append(c)
    orphelins = []
    for h in PICS_HARMONIQUES[:2]:  # octave et quinte = pics majeurs
        if not any(abs(c - h) <= SEUIL_DEPLACEMENT for c, _ in pics_mes):
            orphelins.append(h)
            detail.append(f"pic harmonique {h:.0f} c : AUCUN correspondant mesuré")
    tient = bool(deplaces or orphelins)
    return tient, detail


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    if sys.argv[1] == '--analytique':
        spec, label = music_box(), "boîte ANALYTIQUE (Euler-Bernoulli) — démo, pas une mesure"
        src = "modèle analytique"
    else:
        with open(sys.argv[1]) as fh:
            ext = json.load(fh)
        spec = (np.array([p['ratio'] for p in ext['partiels']]),
                np.array([p['amp'] for p in ext['partiels']]))
        label = f"spectre MESURÉ ({ext['source']}, sha256:{ext['sha256_16']})"
        src = ext['source']
        print(f"Spectre mesuré : f0={ext['f0_hz']:.1f} Hz, "
              f"{len(ext['partiels'])} partiels, ratios "
              f"{[round(p['ratio'], 3) for p in ext['partiels']]}")

    print(f"\nΦ figée : coïncidence sous transposition, σ={SIGMA_FIGEE} c (DECISION-PHI.md)")
    P_mes = courbe_phi(spec)
    P_har = courbe_phi(harmonic())
    P_ana = courbe_phi(music_box())

    pics_mes = pics_principaux(P_mes)
    print(f"\nPics principaux ({label}) :")
    for c, v in pics_mes:
        print(f"  {c:7.1f} c   Φ={v:.4f}")

    masque = CENTS >= 100.0
    ref_octave = float(P_har[masque].max())
    cmax = float(P_mes[masque].max())
    if cmax < GARDE_DEGENERESCENCE * ref_octave:
        print(f"\nGarde de dégénérescence : max Φ(mesuré) = {cmax:.4f} "
              f"< {GARDE_DEGENERESCENCE:.0%} du pic harmonique ({ref_octave:.4f}).")
        print("  Courbe PLATE -> cas dégénéré (CADRAGE §9) : ce timbre, tel que mesuré")
        print("  en régime tenu, ne porte pas de structure de fusion.")
        print("\n  => P5 SANS OBJET sur cet exemplaire (ni confirmé ni infirmé).")
    else:
        tient, detail = verdict_p5(pics_mes)
        print(f"\nVerdict P5 (seuil {SEUIL_DEPLACEMENT:.0f} c, déclaré avant mesure) :")
        for ln in detail:
            print("  " + ln)
        msg = ('TIENT : la structure des pics de fusion diffère du cas harmonique' if tient
               else 'ÉCHOUE : les pics coïncident avec le cas harmonique (critère d’abandon SPEC §6.2)')
        print(f"\n  => P5 {msg}")

    print("\nComparaison à la prédiction analytique (information, pas critère) :")
    for c, v in pics_principaux(P_ana):
        print(f"  analytique : {c:7.1f} c   Φ={v:.4f}")

    # figure
    fig, ax = plt.subplots(figsize=(11, 4.2))
    for nm, cc in JUST.items():
        ax.axvline(cc, color='0.9', lw=0.8, zorder=0)
        ax.text(cc, 1.03, nm, ha='center', va='bottom', fontsize=7, color='0.6')
    ax.plot(CENTS, P_har / P_har.max(), color='0.65', lw=1.2, label='harmonique (référence P2)')
    ax.plot(CENTS, P_ana / P_ana.max(), color='#2a6f97', lw=1.4, ls='--',
            label='boîte analytique (prédiction)')
    ax.plot(CENTS, P_mes / P_mes.max(), color='#c1121f', lw=1.8, label=label)
    for c, v in pics_mes:
        ax.plot(c, v / P_mes.max(), 'o', color='#c1121f', ms=6)
    ax.set_xlabel('intervalle (cents)')
    ax.set_ylabel('Φ normalisé')
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_title(f"P5 — Φ figée (σ={SIGMA_FIGEE} c) : {label}", fontsize=10, loc='left')
    plt.tight_layout()
    out = 'etape2_p5.png'
    plt.savefig(out, dpi=130)
    print(f"\nFigure : {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
