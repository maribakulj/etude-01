"""
etape1.py — boucle simulée sans consigne (étape 1). Ancien nom : boucle.py
(conservé comme lanceur, pour que les commandes du protocole restent valides). Protocole et prédictions :
boucle/PROTOCOLE.md, commité avant ce fichier.

À chaque pas, une nouvelle copie du son de départ entre à la transposition où
elle coïncide le plus (règle `argmax`) ou par tirage parmi les maxima de
coïncidence (règle `tirage`) avec ce qui sonne déjà. Aucune gamme, aucune
règle musicale : les coups possibles sont les maxima de la courbe de
coïncidence calculée sur le son lui-même.

Rejouer (depuis la racine du dépôt) : `python3 boucle/boucle.py`
Paramètres : tous dans boucle/registre.py (provenance de chaque nombre).
Sorties : boucle/resultats.json, boucle/trajectoires.png
"""

import itertools
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

from metriques_fusion import harmonic          # noqa: E402
from famille_raide import corde_raide          # noqa: E402
from boucle.registre import val                # noqa: E402
from boucle.oreille import courbe_coincidence as _courbe   # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))

# --- Choix fixés (PROTOCOLE.md §2) : voir registre.py ----------------------
T_MIN, T_MAX, PAS_GRILLE = val('T_MIN'), val('T_MAX'), val('PAS_GRILLE')
N_PAS = val('N_PAS')
EXCLUSION = val('EXCLUSION')
W_MIN = val('W_MIN')
EGALITE = val('EGALITE')
SIGMA_FIGEE = val('SIGMA_MILNE')

# --- Réglages variés (PROTOCOLE.md §3) ------------------------------------
REGLES = [('argmax', None)] + [('tirage', g) for g in val('GRAINES_TIRAGE')]
TAUS = list(val('TAUS'))
SIGMAS = [SIGMA_FIGEE, val('SIGMA_LARGE')]
REGLAGE_CANONIQUE = ('argmax', None, TAUS[1], SIGMA_FIGEE)


# ---------------------------------------------------------------------------
# Sons de départ (PROTOCOLE.md §4)
# ---------------------------------------------------------------------------
def _depuis_json(nom):
    with open(os.path.join(RACINE, 'materiau', nom)) as fh:
        d = json.load(fh)
    return (np.array([p['ratio'] for p in d['partiels']], dtype=float),
            np.array([p['amp'] for p in d['partiels']], dtype=float))


def _aleatoire():
    n = val('ALEATOIRE_N')
    rng = np.random.default_rng(val('GRAINE_ALEATOIRE'))
    r = np.sort(np.exp(rng.uniform(0.0, np.log(val('ALEATOIRE_RAPPORT_MAX')), n)))
    return r, 1.0 / np.arange(1, n + 1)


def sons():
    return {
        'harm': harmonic(),
        'cloche': _depuis_json('cloche_westerkerk_publie.json'),
        'cloche12c1': _depuis_json('cloche_westerkerk_12c1_extraction.json'),
        'corde1e-3': corde_raide(1e-3),
        'corde1e-2': corde_raide(1e-2),
        'corde1e-1': corde_raide(1e-1),
        'dent994': _depuis_json('dent994.json'),
        'aleatoire': _aleatoire(),
    }


# ---------------------------------------------------------------------------
# La boucle
# ---------------------------------------------------------------------------
GRILLE = np.arange(T_MIN, T_MAX + PAS_GRILLE / 2, PAS_GRILLE)


def courbe_coincidence(son, copies, sigma):
    """Coïncidence entre le son transposé de t (pour t sur GRILLE) et le
    mélange des copies actives (boucle/oreille/coincidence.py)."""
    return _courbe(son, copies, sigma, GRILLE)


def maxima(courbe):
    """Indices des maxima locaux (bords compris), comme pics_locaux."""
    y = courbe
    idx = [i for i in range(1, len(y) - 1) if y[i] >= y[i - 1] and y[i] >= y[i + 1]]
    if y[0] >= y[1]:
        idx.insert(0, 0)
    if y[-1] >= y[-2]:
        idx.append(len(y) - 1)
    return idx


def affine(courbe, i):
    """Position du maximum affinée par interpolation parabolique."""
    if 0 < i < len(courbe) - 1:
        a, b, c = courbe[i - 1], courbe[i], courbe[i + 1]
        den = a - 2 * b + c
        if den < 0:
            return GRILLE[i] + 0.5 * PAS_GRILLE * (a - c) / den
    return GRILLE[i]


def trajectoire(son, regle, graine, tau, sigma):
    rng = np.random.default_rng(graine) if graine is not None else None
    copies = [(0.0, 1.0)]
    ts, n_actives, centroides = [0.0], [1], [centroide(son, copies)]
    secours = 0
    for _ in range(N_PAS):
        y = courbe_coincidence(son, copies, sigma)
        actives = np.array([t for t, w in copies])
        cand = [i for i in maxima(y)
                if np.min(np.abs(GRILLE[i] - actives)) >= EXCLUSION]
        if not cand:   # cas non prévu au protocole : consigné dans les résultats
            secours += 1
            libres = [i for i in range(len(GRILLE))
                      if np.min(np.abs(GRILLE[i] - actives)) >= EXCLUSION]
            cand = [max(libres, key=lambda i: y[i])]
        dernier = ts[-1]
        if regle == 'argmax':
            haut = max(y[i] for i in cand)
            ex = [i for i in cand if y[i] >= haut - EGALITE]
            choix = min(ex, key=lambda i: (abs(GRILLE[i] - dernier), GRILLE[i]))
        else:
            h = np.array([y[i] for i in cand]) ** val('EXPOSANT_TIRAGE')
            p = h / h.sum() if h.sum() > 0 else np.full(len(cand), 1.0 / len(cand))
            choix = cand[rng.choice(len(cand), p=p)]
        t_new = float(affine(y, choix))
        decroit = np.exp(-1.0 / tau)
        copies = [(t, w * decroit) for t, w in copies if w * decroit >= W_MIN]
        copies.append((t_new, 1.0))
        ts.append(t_new)
        n_actives.append(len(copies))
        centroides.append(centroide(son, copies))
    return dict(t=ts, n_actives=n_actives, centroide_hz=centroides, secours=secours)


def centroide(son, copies, f0=val('F0_RENDU')):
    ratios, amps = son
    f = np.concatenate([f0 * 2 ** (t / 1200.0) * ratios for t, w in copies])
    a = np.concatenate([amps * w for t, w in copies])
    return float(np.sum(f * a) / np.sum(a))


# ---------------------------------------------------------------------------
# Mesures (PROTOCOLE.md §5)
# ---------------------------------------------------------------------------
_BI, _BP = val('BIN_INTERVALLES'), val('BIN_POSITIONS')
BINS_IV = np.arange(-3600.0, 3600.0 + _BI, _BI)
BINS_POS = np.arange(0.0, 1200.0 + _BP, _BP)


def intervalles(ts):
    return np.diff(np.asarray(ts))


def histos(ts):
    iv = intervalles(ts)
    hi, _ = np.histogram(iv, bins=BINS_IV)
    hp, _ = np.histogram(np.mod(ts, 1200.0), bins=BINS_POS)
    return hi / hi.sum(), hp / hp.sum()


def distance(h1, h2):
    return 0.5 * (0.5 * np.abs(h1[0] - h2[0]).sum() + 0.5 * np.abs(h1[1] - h2[1]).sum())


def triviale(ts):
    iv = intervalles(ts)
    fin = iv[-val('TRIVIAL_FENETRE'):]
    for p in range(1, val('TRIVIAL_PERIODE_MAX') + 1):
        if np.all(np.abs(fin[p:] - fin[:-p]) <= val('TRIVIAL_TOL_PERIODE')):
            return True, f'périodique (période {p})'
    part = max(np.mean(np.abs(iv - v) <= val('TRIVIAL_TOL_DOMINANT')) for v in iv)
    if part >= val('TRIVIAL_PART'):
        return True, f'un intervalle domine ({100 * part:.0f} %)'
    return False, f'non triviale (intervalle dominant {100 * part:.0f} %)'


def intervalle_dominant(ts, tol=val('DOMINANT_TOL')):
    a = np.abs(intervalles(ts))
    comptes = [np.sum(np.abs(a - v) <= tol) for v in a]
    k = int(np.argmax(comptes))
    return float(a[k]), int(comptes[k])


def rapport_R(H, etiq_son, etiq_reglage):
    n = len(H)
    D = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        D[i, j] = D[j, i] = distance(H[i], H[j])

    def R(son_lab):
        entre, intra = [], []
        for i, j in itertools.combinations(range(n), 2):
            if etiq_reglage[i] == etiq_reglage[j] and son_lab[i] != son_lab[j]:
                entre.append(D[i, j])
            elif son_lab[i] == son_lab[j] and etiq_reglage[i] != etiq_reglage[j]:
                intra.append(D[i, j])
        return np.mean(entre) / np.mean(intra)

    r_obs = R(etiq_son)
    rng = np.random.default_rng(val('GRAINE_ALEATOIRE'))
    reglages = sorted(set(etiq_reglage))
    nuls = []
    for _ in range(val('N_PERMUTATIONS')):
        perm = list(etiq_son)
        for g in reglages:
            idx = [i for i in range(n) if etiq_reglage[i] == g]
            lab = [etiq_son[i] for i in idx]
            rng.shuffle(lab)
            for i, l in zip(idx, lab):
                perm[i] = l
        nuls.append(R(perm))
    p = float(np.mean(np.array(nuls) >= r_obs))
    return float(r_obs), p, D


# ---------------------------------------------------------------------------
def nom_reglage(regle, graine, tau, sigma):
    g = '' if graine is None else str(graine)
    return f'{regle}{g}_tau{tau:g}_sig{sigma:g}'


def main():
    S = sons()
    runs = []
    for code, son in S.items():
        for (regle, graine), tau, sigma in itertools.product(REGLES, TAUS, SIGMAS):
            tr = trajectoire(son, regle, graine, tau, sigma)
            runs.append(dict(son=code, regle=regle, graine=graine, tau=tau,
                             sigma=sigma, reglage=nom_reglage(regle, graine, tau, sigma),
                             **tr))
        print(f'  {code} : 16 trajectoires')

    H = [histos(r['t']) for r in runs]
    R, p, D = rapport_R(H, [r['son'] for r in runs], [r['reglage'] for r in runs])

    print('\n### Trivialité (règle argmax)')
    b1 = {}
    for r in runs:
        tv, why = triviale(r['t'])
        r['triviale'], r['triviale_motif'] = tv, why
        if r['regle'] == 'argmax':
            print(f"  {r['son']:11s} τ={r['tau']:<3g} σ={r['sigma']:<5g} : {why}")
            b1.setdefault(r['son'], []).append(tv)
    ok_b1 = sum(b1['harm']) >= 3 and sum(b1['cloche']) >= 3
    print(f"  => B1 : harm {sum(b1['harm'])}/4, cloche {sum(b1['cloche'])}/4 triviales "
          f"-> {'VÉRIFIÉE' if ok_b1 else 'NON VÉRIFIÉE'}")

    print('\n### Intervalle dominant (argmax, σ = 6,83)')
    dom = {}
    for r in runs:
        if r['regle'] == 'argmax' and r['sigma'] == SIGMA_FIGEE:
            v, n = intervalle_dominant(r['t'])
            dom.setdefault(r['son'], []).append(v)
            print(f"  {r['son']:11s} τ={r['tau']:<3g} : ±{v:.0f} c ({n}/{N_PAS})")
    ok_b2 = (all(abs(v - 307) <= 15 for v in dom['cloche'])
             and all(min(abs(v - 1200), abs(v - 702)) <= 15 for v in dom['harm']))
    print(f"  => B2 {'VÉRIFIÉE' if ok_b2 else 'NON VÉRIFIÉE'}")

    print('\n### Variabilité intra-son (distance moyenne entre réglages)')
    intra = {}
    codes = list(S)
    for c in codes:
        idx = [i for i, r in enumerate(runs) if r['son'] == c]
        intra[c] = float(np.mean([D[i, j] for i, j in itertools.combinations(idx, 2)]))
    for c in sorted(codes, key=lambda c: -intra[c]):
        print(f'  {c:11s} {intra[c]:.3f}')
    ok_b3 = max(intra, key=intra.get) == 'dent994'
    print(f"  => B3 {'VÉRIFIÉE' if ok_b3 else 'NON VÉRIFIÉE'}")

    print(f'\n### Le son contre les réglages')
    print(f'  R = {R:.2f}, p = {p:.3f} (1000 permutations)')
    ok_b4 = R >= 2 and p < 0.01
    print(f"  => B4 {'VÉRIFIÉE' if ok_b4 else 'NON VÉRIFIÉE'}")

    secours = sum(r['secours'] for r in runs)
    print(f'\nPas sans candidat (secours, non prévu au protocole) : {secours}')

    out = dict(R=R, p=p, intra_son=intra, B1=ok_b1, B2=ok_b2, B3=ok_b3, B4=ok_b4,
               pas_secours=secours,
               runs=[{k: (np.round(v, 2).tolist() if isinstance(v, list) else v)
                      for k, v in r.items()} for r in runs])
    with open(os.path.join(ICI, 'resultats.json'), 'w') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    figure(runs, codes)
    print('Écrit : boucle/resultats.json, boucle/trajectoires.png')


def figure(runs, codes):
    fig, axes = plt.subplots(len(codes), 2, figsize=(13, 2.1 * len(codes)), sharex=True)
    for k, c in enumerate(codes):
        for col, (regle, graine) in enumerate([('argmax', None), ('tirage', 1)]):
            ax = axes[k, col]
            r = next(r for r in runs if r['son'] == c and r['regle'] == regle
                     and r['graine'] == graine and r['tau'] == TAUS[1]
                     and r['sigma'] == SIGMA_FIGEE)
            ax.plot(range(len(r['t'])), r['t'], '-o', ms=3, lw=0.8, color='#2a6f97')
            for y in (0, 1200, 2400):
                ax.axhline(y, color='0.85', lw=0.6, zorder=0)
            ax.set_ylim(T_MIN - 100, T_MAX + 100)
            ax.set_title(f'{c} — {regle}{"" if graine is None else graine}, τ=4, σ=6,83'
                         f' ({r["triviale_motif"]})', fontsize=8, loc='left')
            ax.set_ylabel('t (c)', fontsize=7)
            ax.tick_params(labelsize=7)
    for ax in axes[-1]:
        ax.set_xlabel('pas', fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(ICI, 'trajectoires.png'), dpi=110)


if __name__ == '__main__':
    main()
