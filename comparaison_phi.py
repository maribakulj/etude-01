"""
comparaison_phi.py — Étape 1 : comparer les métriques de fusion sur le cas de
contrôle, appliquer le critère éliminatoire P2, et préparer la décision.

Protocole (validé avant codage) :
  1. Toutes les métriques sont évaluées sur le timbre HARMONIQUE + récepteur
     humain — le seul cas où P2 a un sens (SPEC §6.1).
  2. Critère P2 (ÉLIMINATOIRE) : Φ doit piquer à l'octave (1200c) PUIS à la
     quinte (702c), avec Φ(octave) > Φ(quinte). Échec => métrique fausse, éliminée.
  3. Contrôle du port (mini-P6, sur l'harmonique seulement) : resserrer la
     fenêtre récepteur ne doit PAS déplacer les pics (substrat arithmétique).
  4. Réactivité spectrale (test BINAIRE, anti-triche) : la métrique réagit-elle
     au spectre ? On regarde seulement OUI/NON sur la boîte à musique, jamais OÙ
     tombent les pics — sinon on sélectionnerait la métrique qui 'confirme' P5.
     Une métrique aveugle au spectre ne peut pas porter P5 (testabilité).

Produit : une table de verdicts en console + la figure comparaison_phi.png.
La décision finale (quelle métrique figer) est consignée dans DECISION-PHI.md.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from metriques_fusion import (
    harmonic, music_box, courbe, peaks, nearest_interval,
    METRIQUES, LABELS, JUST, RATIO,
    proxy_coincidence, sieve_darwin, virtual_pitch,
)

CENTS_AXIS = np.linspace(1.0, 1200.0, 1200)

# Cible P2 et tolérance de localisation. ±20c : un peu plus large que les ±15c
# nominaux pour absorber la discrétisation (pas de 1c) et, pour l'étalon
# Stolzenburg, l'effet d'escalier (plateaux de périodicité). Les vraies
# candidates ont des pics pointus et tombent bien dans ±15c (voir sortie).
P2_OCT, P2_FIFTH = 1200.0, 702.0
P2_TOL = 20.0


def localise_pics(curve, k=4):
    """Renvoie [(cents, valeur), ...] des k premiers pics (zone <100c exclue),
    triés par valeur décroissante. Même détecteur que le noyau (comparabilité)."""
    idx = peaks(curve, CENTS_AXIS, n=k)
    return [(float(CENTS_AXIS[i]), float(curve[i])) for i in idx]


def verdict_P2(curve):
    """Applique le critère P2. Renvoie (passe: bool, detail: str, pics)."""
    pics = localise_pics(curve, k=4)
    if len(pics) < 2:
        return False, "moins de 2 pics détectés", pics
    (c1, v1), (c2, v2) = pics[0], pics[1]
    oct_ok = abs(c1 - P2_OCT) <= P2_TOL
    fifth_ok = abs(c2 - P2_FIFTH) <= P2_TOL
    order_ok = v1 > v2
    passe = oct_ok and fifth_ok and order_ok
    bits = []
    bits.append(f"pic1={c1:6.1f}c {'~P8 OK' if oct_ok else 'PAS P8'}")
    bits.append(f"pic2={c2:6.1f}c {'~P5 OK' if fifth_ok else 'PAS P5'}")
    bits.append(f"Φ(P8)>Φ(P5) {'OK' if order_ok else 'NON'}")
    return passe, " | ".join(bits), pics


# --- Contrôle du port : pics stables quand on resserre la fenêtre récepteur ----
# Pour chaque métrique à fenêtre, une variante 'récepteur résolvant' (fenêtre
# étroite). periodicity n'a pas de fenêtre-récepteur (sa tolérance est le JND),
# d'où N/A.
def courbe_fenetre_etroite(nom, spec):
    rs = RATIO(CENTS_AXIS)
    if nom == 'proxy_w25':
        return np.array([proxy_coincidence(spec, r, w_cents=8.0) for r in rs])
    if nom == 'proxy_milne':
        return np.array([proxy_coincidence(spec, r, w_cents=3.0) for r in rs])
    if nom == 'sieve_darwin':
        return np.array([sieve_darwin(spec, r, sigma_cents=18.0) for r in rs])
    if nom == 'virtual_pitch':
        return np.array([virtual_pitch(spec, r, tol_cents=5.0) for r in rs])
    return None  # periodicity : pas de port récepteur


def controle_port(nom, spec):
    """Renvoie (deplacement_max_cents | None). None => N/A (pas de fenêtre)."""
    etroite = courbe_fenetre_etroite(nom, spec)
    if etroite is None:
        return None
    large = courbe(nom, spec, CENTS_AXIS)
    pl = sorted(c for c, _ in localise_pics(large, k=3))
    pe = sorted(c for c, _ in localise_pics(etroite, k=3))
    # appariement par proximité
    dmax = 0.0
    for c in pl:
        d = min(abs(c - x) for x in pe) if pe else 999
        dmax = max(dmax, d)
    return dmax


# --- Réactivité spectrale : binaire, sans regarder OÙ -------------------------
def reactif_au_spectre(nom):
    """Les positions des pics changent-elles entre harmonique et boîte ? OUI/NON.
    On ne lit PAS où vont les pics de la boîte (verrou anti-triche). C'est le
    test de TESTABILITÉ de P5 : une métrique dont les pics ne bougent pas avec
    le timbre ne peut pas déplacer l'interdit de parallèles."""
    ph = sorted(c for c, _ in localise_pics(courbe(nom, harmonic(), CENTS_AXIS), k=4))
    pb = sorted(c for c, _ in localise_pics(courbe(nom, music_box(), CENTS_AXIS), k=4))
    if len(ph) != len(pb):
        return True
    return any(abs(a - b) > 40.0 for a, b in zip(ph, pb))


# Pourquoi les pics d'une métrique ne bougent pas : raisons structurelles
# distinctes (l'une n'utilise pas le spectre, les autres l'utilisent mais
# restent ancrées aux rapports rationnels des fondamentales).
RAISON_RIGIDE = {
    'periodicity':   "aveugle au spectre par construction (n'utilise que r)",
    'sieve_darwin':  "lit le spectre mais pics ancrés aux rationnels des fondamentales",
    'virtual_pitch': "lit le spectre mais pics ancrés aux rationnels des fondamentales",
}


# ===========================================================================
# Exécution : table de verdicts + figure
# ===========================================================================
def main():
    spec = harmonic()
    ordre = ['proxy_w25', 'proxy_milne', 'sieve_darwin', 'virtual_pitch', 'periodicity']

    print("=" * 78)
    print("ÉTAPE 1 — COMPARAISON DES MÉTRIQUES DE FUSION Φ")
    print("Cas de contrôle : timbre HARMONIQUE + récepteur humain")
    print("=" * 78)

    courbes = {}
    resultats = {}
    for nom in ordre:
        c = courbe(nom, spec, CENTS_AXIS)
        courbes[nom] = c
        passe, detail, pics = verdict_P2(c)
        port = controle_port(nom, spec)
        reactif = reactif_au_spectre(nom)
        resultats[nom] = dict(passe=passe, detail=detail, pics=pics,
                              port=port, reactif=reactif)

        print(f"\n● {LABELS[nom]}")
        print(f"    P2 : {'✓ PASSE' if passe else '✗ ÉCHEC'}  [{detail}]")
        tete = "  ".join(f"{nearest_interval(c0)[0]}@{c0:.0f}c(Φ={v:.3f})"
                         for c0, v in pics[:3])
        print(f"    pics : {tete}")
        if port is None:
            print(f"    contrôle port : N/A (pas de fenêtre récepteur)")
        else:
            verdict_port = "stable" if port <= 20 else f"DÉPLACÉ {port:.0f}c"
            print(f"    contrôle port (fenêtre resserrée) : déplacement max {port:.1f}c -> {verdict_port}")
        if reactif:
            print("    pics mobiles avec le timbre (P5 testable) : OUI")
        else:
            raison = RAISON_RIGIDE.get(nom, 'raison à diagnostiquer')
            print(f"    pics mobiles avec le timbre (P5 testable) : NON — {raison}")

    # --- synthèse ---
    print("\n" + "=" * 78)
    print("SYNTHÈSE")
    print("=" * 78)
    survivantes = [n for n in ordre if resultats[n]['passe']]
    eliminees = [n for n in ordre if not resultats[n]['passe']]
    print(f"  Passent P2 (candidates) : {', '.join(survivantes) if survivantes else '—'}")
    print(f"  Échouent P2 (éliminées) : {', '.join(eliminees) if eliminees else '—'}")
    # parmi les survivantes, lesquelles peuvent porter P5 (réactives) ?
    portent_P5 = [n for n in survivantes if resultats[n]['reactif']]
    print(f"  Survivantes à pics MOBILES avec le timbre (P5 testable) : "
          f"{', '.join(portent_P5) if portent_P5 else '—'}")
    rigides = [n for n in survivantes if not resultats[n]['reactif']]
    if rigides:
        print(f"  Survivantes à pics RIGIDES (contrôles, hors P5) : {', '.join(rigides)}")

    # --- figure ---
    fig, axes = plt.subplots(len(ordre), 1, figsize=(11, 2.1 * len(ordre)), sharex=True)
    for ax, nom in zip(axes, ordre):
        c = courbes[nom]
        cn = c / c.max() if c.max() > 0 else c
        passe = resultats[nom]['passe']
        col = '#1b7837' if passe else '#b2182b'
        ax.plot(CENTS_AXIS, cn, color=col, lw=1.5)
        for nm, cc in JUST.items():
            ax.axvline(cc, color='0.88', lw=0.8, zorder=0)
            ax.text(cc, 1.04, nm, ha='center', va='bottom', fontsize=6.5, color='0.55')
        for c0, v in resultats[nom]['pics'][:3]:
            ax.plot(c0, v / c.max(), 'o', color=col, ms=5)
        tag = 'PASSE P2' if passe else 'ÉCHEC P2'
        ax.set_title(f"{LABELS[nom]}   —   [{tag}]", fontsize=9.5, loc='left', color=col)
        ax.set_ylim(0, 1.12)
        ax.set_ylabel('Φ norm.', fontsize=8)
    axes[-1].set_xlabel('intervalle (cents) — unisson → octave  (timbre harmonique, récepteur humain)')
    plt.tight_layout()
    out = '/home/user/etude-01/comparaison_phi.png'
    plt.savefig(out, dpi=130)
    print(f"\nFigure écrite : {out}")
    return resultats


if __name__ == '__main__':
    main()
