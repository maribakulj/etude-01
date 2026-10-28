"""
phase2.py — boucle simulée v2, sans consigne. Protocole : PHASE2-PROTOCOLE.md,
commité avant ce fichier.

Changements par rapport à l'étape 1 (etape1.py) : registre de transposition
fixé par les limites de la hauteur mélodique appliquées au partiel dominant ;
exclusion d'une candidate non résolue (moins d'1 ERB) ; temps réel (période T,
persistance τ en secondes, τ mesuré pour la cloche) ; et formation des lignes
par l'oreille modélisée (van Noorden 1975), qui ne sert pas au choix.

Rejouer : `python3 boucle/phase2.py` (long : plusieurs dizaines de minutes).
Sorties : boucle/phase2_resultats.json, boucle/phase2_trajectoires.png.
"""

import itertools
import json
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or '.') != ICI]
sys.path.insert(0, os.path.dirname(ICI))

from boucle.registre import val                       # noqa: E402
from boucle.etape1 import sons, maxima                 # noqa: E402
from boucle.oreille import courbe_coincidence          # noqa: E402
from boucle.oreille.erb import erb                     # noqa: E402
from boucle.oreille import sequentiel                  # noqa: E402

SIGMA = val('SIGMA_MILNE')
SONS_MESURES = {'cloche': 'F_REF_CLOCHE_HZ', 'cloche12c1': 'F_REF_CLOCHE_HZ',
                'dent994': 'F_REF_DENT994_HZ'}
TAU_MESURE = {'cloche': 'TAU_CLOCHE_S', 'cloche12c1': 'TAU_CLOCHE_S'}


def f_ref(code):
    return val(SONS_MESURES.get(code, 'F_REF_SYNTH_HZ'))


def taus(code):
    return [val(TAU_MESURE[code])] if code in TAU_MESURE else list(val('TAUS_SYNTH_S'))


# ---------------------------------------------------------------------------
# Registre et exclusion, à partir de l'oreille
# ---------------------------------------------------------------------------
def partiel_dominant(son):
    ratios, amps = son
    return float(ratios[int(np.argmax(amps))])


def grille_registre(son, fref):
    """Transpositions (cents) où le partiel dominant reste dans les limites
    de la hauteur mélodique (C6, appliquées au partiel dominant)."""
    f_dom = fref * partiel_dominant(son)
    lo = 1200.0 * np.log2(val('LIMITE_BASSE_HZ') / f_dom)
    hi = 1200.0 * np.log2(val('LIMITE_HAUTE_HZ') / f_dom)
    pas = val('PAS_GRILLE')
    return np.arange(np.ceil(lo / pas) * pas, hi + pas / 2, pas)


def non_resolue(t, actives, son, fref, n_erb):
    """La candidate t (scalaire ou tableau) est-elle à moins de n_erb ERB
    d'une copie active (partiel dominant) ? ERB prise à la fréquence moyenne
    des deux."""
    f_dom = fref * partiel_dominant(son)
    f1 = f_dom * 2 ** (np.atleast_1d(np.asarray(t, float))[:, None] / 1200.0)
    f2 = f_dom * 2 ** (np.asarray(actives, float)[None, :] / 1200.0)
    masque = np.any(np.abs(f1 - f2) < n_erb * erb(0.5 * (f1 + f2)), axis=1)
    return bool(masque[0]) if np.ndim(t) == 0 else masque


# ---------------------------------------------------------------------------
# La boucle v2
# ---------------------------------------------------------------------------
def trajectoire(son, fref, regle, graine, T_ms, tau_s, n_erb=None, w_min=None):
    n_erb = val('EXCLUSION_ERB') if n_erb is None else n_erb
    w_min = val('W_MIN') if w_min is None else w_min
    grille = grille_registre(son, fref)
    rng = np.random.default_rng(graine) if graine is not None else None
    copies = [(0.0, 1.0)]
    ts, n_act, secours, silences = [0.0], [1], 0, 0
    decroit = np.exp(-(T_ms / 1000.0) / tau_s)
    for _ in range(val('N_PAS')):
        actives = [t for t, w in copies]
        exclu = non_resolue(grille, actives, son, fref, n_erb)
        if exclu.all():
            # Cas non prévu au protocole (consigné dans les résultats) : aucune
            # nouvelle copie ne serait résolue par l'oreille, donc pas
            # d'événement à ce pas. Les copies continuent de s'éteindre.
            silences += 1
            copies = [(t, w * decroit) for t, w in copies if w * decroit >= w_min]
            if not copies:
                copies = [(ts_non_nuls(ts)[-1], 0.0)]
            ts.append(None)
            n_act.append(len([c for c in copies if c[1] > 0]))
            continue
        y = courbe_coincidence(son, copies, SIGMA, grille)
        cand = [i for i in maxima(y) if not exclu[i]]
        if not cand:
            secours += 1
            libres = np.where(~exclu)[0]
            cand = [int(libres[np.argmax(y[libres])])]
        dernier = ts_non_nuls(ts)[-1]
        if regle == 'argmax':
            haut = max(y[i] for i in cand)
            ex = [i for i in cand if y[i] >= haut - val('EGALITE')]
            choix = min(ex, key=lambda i: (abs(grille[i] - dernier), grille[i]))
        else:
            h = np.array([y[i] for i in cand]) ** val('EXPOSANT_TIRAGE')
            p = h / h.sum() if h.sum() > 0 else np.full(len(cand), 1.0 / len(cand))
            choix = cand[rng.choice(len(cand), p=p)]
        t_new = float(_affine(y, choix, grille))
        copies = [(t, w * decroit) for t, w in copies if w * decroit >= w_min]
        copies.append((t_new, 1.0))
        copies = [c for c in copies if c[1] > 0]
        ts.append(t_new)
        n_act.append(len(copies))
    return dict(t=ts, n_actives=n_act, secours=secours, silences=silences)


def ts_non_nuls(ts):
    return [t for t in ts if t is not None]


def _affine(y, i, grille):
    if 0 < i < len(y) - 1:
        a, b, c = y[i - 1], y[i], y[i + 1]
        den = a - 2 * b + c
        if den < 0:
            return grille[i] + 0.5 * (grille[1] - grille[0]) * (a - c) / den
    return grille[i]


# ---------------------------------------------------------------------------
# L'oreille écoute : lignes (PHASE2-PROTOCOLE.md §3)
# ---------------------------------------------------------------------------
def lignes(ts, T_ms, variante):
    """Répartit les événements (un toutes les T_ms) en lignes. Renvoie la
    liste des lignes, chacune une liste d'indices d'événements."""
    ouvertes = []        # [indices]
    toutes = []
    for k, t in enumerate(ts):
        temps = k * T_ms
        if t is None:            # silence : le temps avance, pas d'événement
            ouvertes = [l for l in ouvertes
                        if temps - l[-1] * T_ms <= val('LIGNE_FERMETURE_MS')]
            continue
        eligibles = []
        for ligne in ouvertes:
            j = ligne[-1]
            ecart_t = temps - j * T_ms
            if ecart_t > val('LIGNE_FERMETURE_MS'):
                continue
            borne = (sequentiel.frontiere_coherence(ecart_t, complexe=True)
                     if variante == 'A' else sequentiel.frontiere_fission())
            dt = abs(t - ts[j])
            if dt / 100.0 < borne:
                eligibles.append((dt, id(ligne), ligne))
        if eligibles:
            min(eligibles, key=lambda e: (e[0], e[1]))[2].append(k)
        else:
            nouvelle = [k]
            ouvertes.append(nouvelle)
            toutes.append(nouvelle)
        ouvertes = [l for l in ouvertes
                    if temps - l[-1] * T_ms <= val('LIGNE_FERMETURE_MS')]
    return toutes


def mesures_lignes(ls):
    longueurs = [len(l) for l in ls]
    n_ev = sum(longueurs)
    return dict(n_lignes=len(ls), longueur_moyenne=float(np.mean(longueurs)),
                part_lignes_4=float(sum(n for n in longueurs if n >= 4) / n_ev))


# ---------------------------------------------------------------------------
# Mesures son contre réglages
# ---------------------------------------------------------------------------
def histos(ts):
    e, bi, bp = val('BIN_INTERVALLES_ETENDUS'), val('BIN_INTERVALLES'), val('BIN_POSITIONS')
    ts = np.array(ts_non_nuls(ts))
    iv = np.diff(ts)
    hi, _ = np.histogram(iv, bins=np.arange(-e, e + bi, bi))
    hp, _ = np.histogram(np.mod(ts, 1200.0), bins=np.arange(0.0, 1200.0 + bp, bp))
    return hi / hi.sum(), hp / hp.sum()


def d_traj(a, b):
    return 0.5 * (0.5 * np.abs(a[0] - b[0]).sum() + 0.5 * np.abs(a[1] - b[1]).sum())


def d_lignes(a, b):
    cles = ('n_lignes', 'longueur_moyenne', 'part_lignes_4')
    return float(np.mean([abs(a[c] - b[c]) / max(abs(a[c]), abs(b[c]), 1e-12) for c in cles]))


def meme_reglage(r1, r2):
    """Même règle, même période ; même τ sauf si l'un des deux a un τ mesuré
    (le τ mesuré fait alors partie du son, pas des réglages)."""
    if (r1['regle'], r1['graine'], r1['T_ms']) != (r2['regle'], r2['graine'], r2['T_ms']):
        return False
    return r1['tau_mesure'] or r2['tau_mesure'] or r1['tau_s'] == r2['tau_s']


def rapport(runs, dist, cle):
    n = len(runs)
    D = {(i, j): dist(runs[i][cle], runs[j][cle]) for i, j in itertools.combinations(range(n), 2)}

    def R(lab):
        entre, intra = [], []
        for (i, j), d in D.items():
            mr = meme_reglage(runs[i], runs[j])
            if mr and lab[i] != lab[j]:
                entre.append(d)
            elif lab[i] == lab[j] and not mr:
                intra.append(d)
        return np.mean(entre) / np.mean(intra)

    lab = [r['son'] for r in runs]
    r_obs = R(lab)
    rng = np.random.default_rng(val('GRAINE_ALEATOIRE'))
    groupes = {}
    for i, r in enumerate(runs):
        groupes.setdefault((r['regle'], r['graine'], r['T_ms']), []).append(i)
    nuls = []
    for _ in range(val('N_PERMUTATIONS')):
        perm = list(lab)
        for idx in groupes.values():
            l = [lab[i] for i in idx]
            rng.shuffle(l)
            for i, x in zip(idx, l):
                perm[i] = x
        nuls.append(R(perm))
    return float(r_obs), float(np.mean(np.array(nuls) >= r_obs))


# ---------------------------------------------------------------------------
def analyser(code, son, regle, graine, T_ms, tau_s, **kw):
    tr = trajectoire(son, f_ref(code), regle, graine, T_ms, tau_s, **kw)
    ls = {v: lignes(tr['t'], T_ms, v) for v in ('A', 'B')}
    return dict(son=code, regle=regle, graine=graine, T_ms=T_ms, tau_s=tau_s,
                tau_mesure=code in TAU_MESURE, **tr,
                lignes={v: [list(map(int, l)) for l in ls[v]] for v in ls},
                mesures={v: mesures_lignes(ls[v]) for v in ls})


def main():
    S = sons()
    regles = [('argmax', None)] + [('tirage', g) for g in val('GRAINES_TIRAGE')]
    runs = []
    for code, son in S.items():
        for (regle, graine), T_ms, tau_s in itertools.product(regles, val('PERIODES_MS'), taus(code)):
            runs.append(analyser(code, son, regle, graine, T_ms, tau_s))
        print(f'  {code} : fait', flush=True)

    sens = []
    T_sens = val('PERIODES_MS')[1]
    for code, son in S.items():
        tau_s = taus(code)[0]
        for n_erb in (0.5, 1.5):
            sens.append(dict(variation=f'exclusion {n_erb} ERB',
                             **analyser(code, son, 'argmax', None, T_sens, tau_s, n_erb=n_erb)))
        for w in val('W_MIN_SENS'):
            sens.append(dict(variation=f'W_MIN {w}',
                             **analyser(code, son, 'argmax', None, T_sens, tau_s, w_min=w)))
    print('  sensibilité : fait', flush=True)

    for r in runs:
        r['histos'] = histos(r['t'])
    R_traj, p_traj = rapport(runs, d_traj, 'histos')
    for r in runs:
        r['mA'] = r['mesures']['A']
    R_lig, p_lig = rapport(runs, d_lignes, 'mA')

    iv_max = max(np.max(np.abs(np.diff(ts_non_nuls(r['t'])))) for r in runs + sens)
    out = dict(R_traj=R_traj, p_traj=p_traj, R_lignes=R_lig, p_lignes=p_lig,
               intervalle_max=float(iv_max),
               runs=[{k: v for k, v in r.items() if k not in ('histos', 'mA')} for r in runs],
               sensibilite=sens)
    with open(os.path.join(ICI, 'phase2_resultats.json'), 'w') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False,
                  default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))
    print(f'R_traj = {R_traj:.2f} (p = {p_traj:.3f}) ; R_lignes = {R_lig:.2f} (p = {p_lig:.3f})')


if __name__ == '__main__':
    main()
