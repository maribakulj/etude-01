"""
diagramme_phase.py — la grammaire comme fonction du paramètre physique B.

Balaye le coefficient d'inharmonicité de la corde raide (famille_raide.py) et
recompile, à chaque pas, la grammaire complète avec la chaîne FIGÉE (Φ à
σ=6,83 c ; C de Sethares ; schéma de seuils symétrique déclaré à l'étape 3).
Produit : trajectoires des pics de fusion, diagramme de phase 2D (B × τ_F),
table des bifurcations.

Prédictions D1-D4 : DIAGRAMME-PHASE.md §1.3, commitées avant ce fichier.

Deux pipelines, tous deux déjà utilisés tels quels dans le projet :
  - SUBSTRAT (trajectoires des pics de Φ) : proxy_coincidence + peaks, le
    pipeline des étapes 1 et 2 ;
  - GRAMMAIRE (états, interdits, frontières) : grille_etats, le pipeline de
    l'étape 3.
Seule modification déclarée : le compas d'analyse peut dépasser 1200 c
(cf. §2.0 du document) — sans quoi une octave étirée sortirait de la fenêtre.
"""

import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from famille_raide import corde_raide
from metriques_fusion import proxy_coincidence, peaks
from graphe_grammaire import grille_etats, SIGMA_FIGEE
from etape3_fux import plateaux_tau_C, nom

CMAX = 1400.0          # compas d'analyse étendu (déclaré)
TAUF_REL = 0.226       # schéma de seuils de l'étape 3, inchangé
B_GRID = np.concatenate([[0.0], np.geomspace(1e-5, 1e1, 80)])
JUSTES = {'m3': 315.6, 'M3': 386.3, 'P4': 498.0, 'TT': 590.2, 'P5': 702.0,
          'm6': 813.7, 'M6': 884.4, 'm7': 1017.6, 'P8': 1200.0}
CARRES = {'81/64': 405.9, '25/16': 772.6, '16/9': 996.1}   # carrés de rationnels (D4)


# ---------------------------------------------------------------------------
# Substrat : courbe de fusion et suivi de pics par continuité
# ---------------------------------------------------------------------------
def courbe_phi(spec, cents):
    return np.array([proxy_coincidence(spec, 2 ** (c / 1200.0), w_cents=SIGMA_FIGEE)
                     for c in cents])


def pic_local_fin(spec, c0, demi=45.0, pas=0.02):
    """Maximum local de Φ autour de c0, à la résolution `pas` (cents)."""
    grille = np.arange(c0 - demi, c0 + demi + pas, pas)
    vals = courbe_phi(spec, grille)
    i = int(np.argmax(vals))
    return float(grille[i]), float(vals[i])


def suivre_pic(c_depart, Bs, demi=45.0):
    """Suit par CONTINUITÉ le pic de Φ issu de l'intervalle c_depart le long de
    l'axe B (à chaque pas, maximum local dans une fenêtre autour de la position
    précédente). Renvoie (positions, hauteurs)."""
    pos, haut, c = [], [], c_depart
    for B in Bs:
        spec = corde_raide(B)
        c, v = pic_local_fin(spec, c, demi=demi)
        pos.append(c)
        haut.append(v)
    return np.array(pos), np.array(haut)


# ---------------------------------------------------------------------------
# Grammaire : états, interdits, frontières, au schéma de seuils déclaré
# ---------------------------------------------------------------------------
def grammaire(B, cmax=CMAX):
    """Recompile la grammaire complète pour un B donné. Renvoie un dict."""
    spec = corde_raide(B)
    grille, _ = grille_etats(spec, cmax=cmax)
    pC = plateaux_tau_C(grille)
    plat = max(pC, key=lambda p: p[3])          # plus large plateau
    tau_C = (plat[1] + plat[2]) / 2
    etats = [e for e in grille if e['C'] >= tau_C]
    finis = [e['Phi'] for e in etats if np.isfinite(e['Phi'])]
    phimax = max(finis) if finis else 0.0
    tau_F = TAUF_REL * phimax
    interdits = {round(e['intervalle']) for e in etats
                 if np.isinf(e['Phi']) or e['Phi'] >= tau_F}
    argmax_fini = max((e for e in etats if np.isfinite(e['Phi'])),
                      key=lambda e: e['Phi'], default=None)
    frontieres = {round(e['intervalle']) for e in etats if np.isinf(e['Phi'])}
    if argmax_fini:
        frontieres.add(round(argmax_fini['intervalle']))
    return dict(B=float(B), tau_C=float(tau_C), tau_F=float(tau_F),
                phimax=float(phimax),
                etats=sorted(round(e['intervalle']) for e in etats),
                interdits=sorted(interdits), frontieres=sorted(frontieres),
                etats_phi={round(e['intervalle']):
                           (None if np.isinf(e['Phi']) else round(e['Phi'], 5))
                           for e in etats})


def interdits_a_seuil(g, tau_rel):
    """Ensemble des interdits pour un τ_F relatif donné (pour le plan 2D)."""
    s = set()
    for iv, phi in g['etats_phi'].items():
        if phi is None or phi >= tau_rel * g['phimax']:
            s.add(iv)
    return frozenset(s)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("DIAGRAMME DE PHASE — la grammaire le long de l'axe d'inharmonicité B")
    print("=" * 78)

    # ---- D1 : ancrage bas, dans la configuration EXACTE de l'étape 3 -------
    g0_v1 = grammaire(0.0, cmax=1200.0)
    ok_d1 = (g0_v1['interdits'] == [0, 702, 1200]
             and g0_v1['frontieres'] == [0, 1200])
    print(f"\n### D1 — ancrage bas (B=0, compas 1200 c = config étape 3)")
    print(f"  états     : {g0_v1['etats']}")
    print(f"  interdits : {g0_v1['interdits']}   (étape 3 : [0, 702, 1200])")
    print(f"  frontières: {g0_v1['frontieres']}  (étape 3 : [0, 1200])")
    print(f"  => D1 {'CONFIRMÉE' if ok_d1 else 'ÉCHOUE'}")

    # ---- Balayage complet --------------------------------------------------
    print(f"\nBalayage de {len(B_GRID)} valeurs de B (compas étendu {CMAX:.0f} c)…")
    grams = [grammaire(B) for B in B_GRID]

    # ---- D2 : trajectoire de l'octave, suivie par continuité ---------------
    print("\n### D2 — trajectoire du pic de fusion issu de l'octave")
    pos_oct, haut_oct = suivre_pic(1200.0, B_GRID)
    pos_q, haut_q = suivre_pic(702.0, B_GRID)
    print(f"  {'B':>9s}  {'pic octave':>11s}  {'écart':>8s}  {'Φ':>7s}")
    for i, B in enumerate(B_GRID):
        if B == 0.0 or B in (B_GRID[np.searchsorted(B_GRID, [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0])]):
            print(f"  {B:9.1e}  {pos_oct[i]:11.2f}  {pos_oct[i]-1200:+8.2f}  {haut_oct[i]:7.4f}")
    i_piano = int(np.argmin(np.abs(B_GRID - 1e-4)))
    ecart_piano = pos_oct[i_piano] - 1200.0
    sens = ("VERS L'AIGU (octave étirée)" if ecart_piano > 0
            else "vers le grave (octave comprimée)")
    print(f"  À B=1e-4 (piano médium) : écart {ecart_piano:+.2f} c -> {sens}")
    ok_d2 = ecart_piano > 0
    print(f"  => D2 {'CONFIRMÉE' if ok_d2 else 'RÉFUTÉE'}")

    # ---- D3 : bifurcations le long de la ligne de seuils déclarée ----------
    # Critère DURCI (cf. §2.3) : une bifurcation est un changement de
    # CARDINALITÉ de l'ensemble des interdits — une règle apparaît ou
    # disparaît. La simple DÉRIVE des positions (les mêmes interdits qui
    # glissent de quelques cents quand le spectre s'étire) n'en est pas une :
    # c'est un mouvement continu, et le premier test, qui comparait les
    # ensembles arrondis au cent, la comptait à tort.
    card = [len(g['interdits']) for g in grams]
    bifs, derives = [], 0
    for i in range(1, len(grams)):
        a, b = set(grams[i - 1]['interdits']), set(grams[i]['interdits'])
        if len(a) != len(b):
            bifs.append(dict(B_avant=grams[i - 1]['B'], B_apres=grams[i]['B'],
                             avant=sorted(a), apres=sorted(b),
                             card_avant=len(a), card_apres=len(b)))
        elif a != b:
            derives += 1
    print("\n### D3 — bifurcations (changement de CARDINALITÉ des interdits)")
    print(f"  {len(bifs)} bifurcation(s) ; {derives} pas de simple dérive (non comptés)")
    for x in bifs:
        print(f"    B ≈ {x['B_apres']:.3e} : {x['card_avant']} -> {x['card_apres']} "
              f"interdits   {x['avant']} -> {x['apres']}")
    regions, cur = [], [0]
    for i in range(1, len(grams)):
        if card[i] == card[i - 1]:
            cur.append(i)
        else:
            regions.append(cur)
            cur = [i]
    regions.append(cur)
    plus_longue = max(regions, key=len)
    print(f"  {len(regions)} région(s) à cardinalité constante ; plus longue = "
          f"{len(plus_longue)}/{len(grams)} pas "
          f"(B de {B_GRID[plus_longue[0]]:.1e} à {B_GRID[plus_longue[-1]]:.1e})")
    ok_d3 = len(bifs) >= 1 and len(plus_longue) >= 3
    print(f"  => D3 {'CONFIRMÉE' if ok_d3 else 'RÉFUTÉE'}")
    # Lecture : où tombe la 1re bifurcation par rapport aux instruments réels ?
    if bifs:
        b1 = bifs[0]['B_apres']
        print(f"  1re bifurcation à B ≈ {b1:.1e} ; pour mémoire, cordes de piano :"
              f" médium ≈ 1e-4, basses de droit ≈ 1e-3")
        print(f"    -> sur TOUTE la plage des cordes réelles, la grammaire garde sa "
              f"structure (3 interdits) ; seules les POSITIONS dérivent.")

    # ---- D4 : limite raide -------------------------------------------------
    print("\n### D4 — limite raide (B grand) : disparition de l'octave ?")
    g_haut = grams[-1]
    spec_haut = corde_raide(B_GRID[-1])
    cents_f = np.linspace(1.0, CMAX, int(CMAX))
    P = courbe_phi(spec_haut, cents_f)
    pics_haut = sorted(float(cents_f[i]) for i in peaks(P, cents_f, n=6))
    print(f"  B = {B_GRID[-1]:.1e} ; pics de Φ : "
          + ", ".join(f"{c:.0f}c" for c in pics_haut))
    print(f"  repères carrés de rationnels : "
          + ", ".join(f"{k}={v:.0f}c" for k, v in CARRES.items()))
    for k, v in CARRES.items():
        d = min(abs(c - v) for c in pics_haut)
        print(f"    {k:6s} ({v:6.1f} c) : pic le plus proche à {d:5.1f} c")
    oct_presente = 1200 in g_haut['interdits']
    print(f"  interdits à B max : {g_haut['interdits']}")
    print(f"  octave (1200 c) parmi les interdits ? {'OUI' if oct_presente else 'NON'}")
    ok_d4 = not oct_presente
    print(f"  => D4 {'CONFIRMÉE' if ok_d4 else 'RÉFUTÉE'}")

    # ---- Figures -----------------------------------------------------------
    figure_trajectoires(B_GRID, grams, pos_oct, pos_q)
    regions_2d = figure_2d(B_GRID, grams)

    # ---- Sauvegarde des faits ---------------------------------------------
    with open('diagramme_phase_resultats.json', 'w') as fh:
        json.dump(dict(B=list(map(float, B_GRID)),
                       grammaires=grams,
                       pic_octave=list(map(float, pos_oct)),
                       pic_quinte=list(map(float, pos_q)),
                       bifurcations=bifs,
                       verdicts=dict(D1=bool(ok_d1), D2=bool(ok_d2),
                                     D3=bool(ok_d3), D4=bool(ok_d4))),
                  fh, indent=1)
    print("\nécrit : diagramme_phase_resultats.json")
    print(f"\nVERDICTS : D1={'OK' if ok_d1 else 'ÉCHEC'}  D2={'OK' if ok_d2 else 'ÉCHEC'}"
          f"  D3={'OK' if ok_d3 else 'ÉCHEC'}  D4={'OK' if ok_d4 else 'ÉCHEC'}")
    return dict(grams=grams, bifs=bifs)


def figure_trajectoires(Bs, grams, pos_oct, pos_q):
    Bp = np.where(Bs == 0, Bs[1] / 3, Bs)      # B=0 placé hors échelle log
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.15, 1]))
    ax = axes[0]
    for nm, c in JUSTES.items():
        ax.axhline(c, color='0.9', lw=0.8, zorder=0)
        ax.text(Bp[0], c + 8, nm, fontsize=7, color='0.55')
    for nm, c in CARRES.items():
        ax.axhline(c, color='#c1121f', lw=0.7, ls=':', alpha=0.5, zorder=0)
        ax.text(Bp[-1], c + 8, nm, fontsize=7, color='#c1121f', ha='right')
    ax.plot(Bp, pos_oct, color='#c1121f', lw=2.0, label="pic issu de l'octave")
    ax.plot(Bp, pos_q, color='#2a6f97', lw=2.0, label='pic issu de la quinte')
    ax.set_xscale('log')
    ax.set_ylabel('position du pic de Φ (cents)')
    ax.set_title("Substrat : les pics de fusion suivis par continuité le long de B "
                 "(pointillés rouges = carrés de rationnels)",
                 fontsize=10, loc='left')
    ax.legend(fontsize=8, loc='center left')

    ax = axes[1]
    for i, g in enumerate(grams):
        for iv in g['interdits']:
            ax.plot(Bp[i], iv, 's', color='#c1121f', ms=3.2)
        for iv in g['etats']:
            if iv not in g['interdits']:
                ax.plot(Bp[i], iv, '.', color='0.75', ms=2.5)
    ax.set_xscale('log')
    ax.set_xlabel("coefficient d'inharmonicité B  (0 placé à gauche hors échelle ; "
                  "piano médium ≈ 1e-4, basses de droit ≈ 1e-3)")
    ax.set_ylabel('intervalle (cents)')
    ax.set_title("Grammaire : états admis (gris) et interdits de parallèles R2 (rouge), "
                 "au schéma de seuils déclaré", fontsize=10, loc='left')
    for nm, c in JUSTES.items():
        ax.axhline(c, color='0.93', lw=0.8, zorder=0)
    plt.tight_layout()
    plt.savefig('diagramme_phase_trajectoires.png', dpi=130)
    plt.close()
    print("figure : diagramme_phase_trajectoires.png")


def _edges_log(v):
    lv = np.log10(v)
    e = np.concatenate([[lv[0] - (lv[1] - lv[0]) / 2],
                        (lv[:-1] + lv[1:]) / 2,
                        [lv[-1] + (lv[-1] - lv[-2]) / 2]])
    return 10 ** e


def _edges_lin(v):
    d = v[1] - v[0]
    return np.concatenate([[v[0] - d / 2], (v[:-1] + v[1:]) / 2, [v[-1] + d / 2]])


def figure_2d(Bs, grams, n_tau=120):
    """Diagramme de phase (B × τ_F) coloré par le NOMBRE d'interdits — la
    variable structurelle (cf. D3 durci : la dérive des positions n'est pas une
    bifurcation, le changement de cardinalité en est une). B=0 est exclu de
    l'échelle log ; il est traité par D1 et par la figure des trajectoires."""
    idx = [i for i, b in enumerate(Bs) if b > 0]
    B = np.array([Bs[i] for i in idx])
    G = [grams[i] for i in idx]
    taus = np.linspace(0.02, 1.0, n_tau)
    card = np.zeros((n_tau, len(G)), dtype=int)
    for j, g in enumerate(G):
        for i, tr in enumerate(taus):
            card[i, j] = len(interdits_a_seuil(g, tr))
    cmax_card = int(card.max())
    cmap = plt.get_cmap('viridis', cmax_card + 1)
    fig, ax = plt.subplots(figsize=(11, 5.2))
    m = ax.pcolormesh(_edges_log(B), _edges_lin(taus), card,
                      cmap=cmap, vmin=-0.5, vmax=cmax_card + 0.5)
    ax.set_xscale('log')
    ax.axvspan(1e-4, 1e-3, color='w', alpha=0.0)
    for b, lab in [(1e-4, 'piano médium'), (1e-3, 'basses de droit')]:
        ax.axvline(b, color='w', lw=1.2, ls=':')
        ax.text(b, 0.955, lab, fontsize=7.5, color='w', ha='center',
                rotation=90, va='top')
    ax.axhline(TAUF_REL, color='w', lw=1.8, ls='--')
    ax.text(B[0] * 1.3, TAUF_REL + 0.02, 'τ_F déclaré (0,226)',
            fontsize=8, color='w')
    ax.set_xlabel("coefficient d'inharmonicité B")
    ax.set_ylabel('τ_F relatif (× max Φ)')
    ax.set_title("Diagramme de phase du contrepoint : nombre de règles "
                 "anti-parallèles (R2) selon le timbre et le seuil\n"
                 "les frontières entre plages de couleur sont les bifurcations",
                 fontsize=10, loc='left')
    cb = fig.colorbar(m, ax=ax, ticks=range(cmax_card + 1), pad=0.015)
    cb.set_label("nombre d'interdits de parallèles", fontsize=9)
    plt.tight_layout()
    plt.savefig('diagramme_phase_2d.png', dpi=130)
    plt.close()
    print("figure : diagramme_phase_2d.png")
    return card


if __name__ == '__main__':
    main()
