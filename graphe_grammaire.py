"""
graphe_grammaire.py — Étape 3 : le graphe-grammaire (SPEC v1 §2-§4).

Un automate par (timbre × récepteur). Périmètre v1 : simultanéité, première
espèce, deux voix, compas d'une octave (0-1200 c). Le séquentiel est une
extension (R6 différée).

Invariants d'architecture honorés ici :
  - RÈGLES = DONNÉES : les gabarits R1/R2/R3/R5 sont le dict GABARITS,
    interprété par le constructeur — pas du code épars (CADRAGE §10.2).
  - RÉCEPTEUR = PORT : paramètre explicite (bw_scale pour C, sigma pour Φ),
    jamais soudé (CADRAGE §10.1).
  - TRAÇABILITÉ DU SEUILLAGE : chaque état retient (C, tau_C) ; chaque arête
    supprimée retient (mouvement, Φ à l'arrivée, tau_F, paire de partiels
    dominante qui porte la coïncidence) — c'est ce qui distingue règle robuste
    et règle fragile (CADRAGE §10.4).
  - C et Φ jamais mélangés : C vient de rugosite.py, Φ de metriques_fusion.

Décisions de modélisation v1 (déclarées) :
  - Grille d'états par colonne = PICS LOCAUX de C(i) pour ce (timbre ×
    récepteur) — la « gamme de l'objet » (acquis Sethares, CADRAGE §3) — puis
    gate R1 : C(pic) >= tau_C. L'unisson (0 c) est un état si c'est un pic.
  - Cantus donné en cents (ici 12-TET pour comparabilité inter-timbres) ; le
    même cantus sert à tous les automates comparés. Le contrepoint choisit ses
    intervalles dans la grille du timbre.
  - Φ(unisson) : la proxy exclut la self-coïncidence (zone <100 c hors domaine,
    décision documentée au noyau). Convention déclarée : l'unisson est fusion
    MAXIMALE par identité (deux voix confondues SONT une) -> Φ(0) := +inf pour
    R2/R3. R2 interdit donc toujours le mouvement parallèle vers l'unisson dès
    qu'il est actif, et l'unisson est toujours dans les états de frontière R3.
"""

import numpy as np

from metriques_fusion import proxy_coincidence
from rugosite import consonance_curve

SIGMA_FIGEE = 6.83   # DECISION-PHI.md
X_FLOOR = 100.0      # zone quasi-unisson hors domaine de Φ (cf. noyau)

# ---------------------------------------------------------------------------
# RÈGLES = DONNÉES. Les gabarits de la SPEC §3, comme structure déclarative.
# ---------------------------------------------------------------------------
GABARITS = {
    'R1': dict(type='gate_etat', metrique='C', seuil='tau_C',
               commentaire="un intervalle n'est un état que si C(i) >= tau_C"),
    'R2': dict(type='suppression_arete', metrique='Phi', seuil='tau_F',
               mouvements=('parallele', 'direct'), cible='intervalle_arrivee',
               commentaire="anti-fusion : pas de mouvement parallèle/direct "
                           "vers un intervalle de forte coïncidence"),
    'R3': dict(type='frontiere', positions=('debut', 'fin'), etat='argmax_Phi',
               commentaire="commencer/finir sur l'intervalle le plus fusionnel"),
    'R5': dict(type='poids_arete',
               poids={'contraire': 0.0, 'oblique': 0.15,
                      'direct': 0.6, 'parallele': 1.0},
               commentaire="préférence graduée : contraire/oblique > direct > parallèle"),
}


# ---------------------------------------------------------------------------
# Courbes et grille d'états
# ---------------------------------------------------------------------------
def courbes(spec, bw_scale=1.0, sigma=SIGMA_FIGEE, n=1201, cmax=1200.0):
    """C(i) et Φ(i) sur 0..cmax cents. Φ sous X_FLOOR : NaN (hors domaine).

    `cmax` : compas d'analyse. Défaut 1200 c = le compas d'une octave déclaré
    en v1 (résultats des étapes 3 et 4 inchangés au bit près). Le diagramme de
    phase l'étend (DIAGRAMME-PHASE.md §2.0) : sur un timbre dont l'octave se
    déplace, un compas fixé à 1200 c découperait justement le phénomène qu'on
    mesure. Le compas d'une octave est une convention du monde harmonique."""
    cents = np.linspace(0.0, cmax, n)
    C = consonance_curve(spec, cents, bw_scale=bw_scale)
    P = np.array([proxy_coincidence(spec, 2 ** (c / 1200.0), w_cents=sigma)
                  if c >= X_FLOOR else np.nan for c in cents])
    return cents, C, P


def pics_locaux(y, x, min_sep=40.0):
    """Indices des maxima locaux, dédoublonnés à min_sep cents."""
    idx = [i for i in range(1, len(y) - 1)
           if y[i] >= y[i - 1] and y[i] >= y[i + 1]]
    if y[0] >= y[1]:
        idx = [0] + idx
    if y[-1] >= y[-2]:
        idx = idx + [len(y) - 1]
    idx.sort(key=lambda i: -y[i])
    keep = []
    for i in idx:
        if all(abs(x[i] - x[j]) > min_sep for j in keep):
            keep.append(i)
    return sorted(keep)


def phi_de(P, cents, c):
    """Φ(c) avec la convention unisson (cf. en-tête)."""
    if c < X_FLOOR:
        return np.inf if c < 1e-9 else np.nan
    return float(P[int(np.argmin(np.abs(cents - c)))])


def grille_etats(spec, bw_scale=1.0, sigma=SIGMA_FIGEE, cmax=1200.0):
    """Grille candidate = pics locaux de C ; chaque candidat porte C et Φ.
    Le gate R1 (tau_C) s'applique ensuite, balayable."""
    cents, C, P = courbes(spec, bw_scale, sigma, cmax=cmax)
    out = []
    for i in pics_locaux(C, cents):
        c = float(cents[i])
        out.append(dict(intervalle=c, C=float(C[i]), Phi=phi_de(P, cents, c)))
    return out, (cents, C, P)


def paire_dominante(spec, c, sigma=SIGMA_FIGEE):
    """Trace : quelle paire de partiels (p de A, q de B) porte la coïncidence
    à l'intervalle c. Renvoie (p, q, écart_cents)."""
    f, a = spec
    r = 2 ** (c / 1200.0)
    d = 1200.0 * np.log2(f[:, None] / (r * f[None, :]))
    K = (a[:, None] * a[None, :]) * np.exp(-(d / sigma) ** 2)
    same = (np.abs(d) < 1e-6) & (np.arange(len(f))[:, None] == np.arange(len(f))[None, :])
    K = np.where(same, 0.0, K)
    p, q = np.unravel_index(int(np.argmax(K)), K.shape)
    return int(p + 1), int(q + 1), float(d[p, q])


# ---------------------------------------------------------------------------
# Mouvements et construction de l'automate
# ---------------------------------------------------------------------------
def type_mouvement(pas_cantus, pas_ctp, tol=1e-6):
    """parallèle / direct (similaire) / contraire / oblique, depuis les pas
    des deux voix en cents. Parallèle = même direction et intervalle conservé
    (pas identiques à tol près)."""
    if abs(pas_cantus) < tol or abs(pas_ctp) < tol:
        return 'oblique'
    if np.sign(pas_cantus) != np.sign(pas_ctp):
        return 'contraire'
    if abs(pas_cantus - pas_ctp) < tol:
        return 'parallele'
    return 'direct'


def construire_automate(spec, cantus_cents, tau_C, tau_F,
                        bw_scale=1.0, sigma=SIGMA_FIGEE, label=''):
    """Construit l'automate (timbre × récepteur) sur un cantus donné.

    Renvoie dict : colonnes d'états, arêtes (avec poids R5), arêtes supprimées
    par R2 (avec trace), états de frontière R3, et les courbes pour figures."""
    grille, (cents, C, P) = grille_etats(spec, bw_scale, sigma)
    etats = [e for e in grille if e['C'] >= tau_C]          # R1
    if not etats:
        return dict(label=label, etats=[], colonnes=[], aretes=[],
                    supprimees=[], degenere=True)

    # R3 : état(s) de frontière = argmax Φ parmi les états admis.
    # Convention unisson : Φ=+inf -> l'unisson admis est toujours frontière ;
    # on retient aussi l'argmax parmi les Φ finis (information + frontière).
    phi_finis = [e for e in etats if np.isfinite(e['Phi'])]
    argmax_fini = max(phi_finis, key=lambda e: e['Phi']) if phi_finis else None
    frontieres = [e['intervalle'] for e in etats if np.isinf(e['Phi'])]
    if argmax_fini:
        frontieres.append(argmax_fini['intervalle'])

    N = len(cantus_cents)
    colonnes = [[dict(e) for e in etats] for _ in range(N)]
    colonnes[0] = [e for e in colonnes[0] if e['intervalle'] in frontieres]
    colonnes[-1] = [e for e in colonnes[-1] if e['intervalle'] in frontieres]

    aretes, supprimees = [], []
    for t in range(N - 1):
        pas_cantus = cantus_cents[t + 1] - cantus_cents[t]
        for ea in colonnes[t]:
            for eb in colonnes[t + 1]:
                pas_ctp = (cantus_cents[t + 1] + eb['intervalle']) - \
                          (cantus_cents[t] + ea['intervalle'])
                mvt = type_mouvement(pas_cantus, pas_ctp)
                phi_arr = eb['Phi']
                if mvt in GABARITS['R2']['mouvements'] and \
                        (np.isinf(phi_arr) or (np.isfinite(phi_arr) and phi_arr >= tau_F)):
                    p, q, dev = (0, 0, 0.0) if np.isinf(phi_arr) else \
                        paire_dominante(spec, eb['intervalle'], sigma)
                    supprimees.append(dict(
                        t=t, de=ea['intervalle'], vers=eb['intervalle'],
                        mouvement=mvt,
                        Phi_arrivee=None if np.isinf(phi_arr) else phi_arr,
                        tau_F=tau_F, paire=(p, q), ecart_paire_cents=dev,
                        regle='R2'))
                    continue
                aretes.append(dict(t=t, de=ea['intervalle'],
                                   vers=eb['intervalle'], mouvement=mvt,
                                   poids=GABARITS['R5']['poids'][mvt]))
    return dict(label=label, etats=etats, frontieres=sorted(set(frontieres)),
                argmax_phi_fini=(argmax_fini['intervalle'] if argmax_fini else None),
                colonnes=colonnes, aretes=aretes, supprimees=supprimees,
                courbes=(cents, C, P), tau_C=tau_C, tau_F=tau_F,
                cantus=list(cantus_cents), degenere=False)


def chemin_legal(automate):
    """Une composition légale = un chemin de poids minimal (programmation
    dynamique sur le treillis, poids R5)."""
    if automate['degenere']:
        return None
    cols, aretes = automate['colonnes'], automate['aretes']
    N = len(cols)
    adj = {}
    for a in aretes:
        adj.setdefault((a['t'], a['de']), []).append(a)
    INF = float('inf')
    cout = [{e['intervalle']: (INF, None) for e in col} for col in cols]
    for e in cols[0]:
        cout[0][e['intervalle']] = (0.0, None)
    for t in range(N - 1):
        for iv, (c0, _) in cout[t].items():
            if c0 == INF:
                continue
            for a in adj.get((t, iv), []):
                nv = c0 + a['poids']
                if a['vers'] in cout[t + 1] and nv < cout[t + 1][a['vers']][0]:
                    cout[t + 1][a['vers']] = (nv, iv)
    fin = min(cout[-1].items(), key=lambda kv: kv[1][0])
    if fin[1][0] == INF:
        return None
    chemin = [fin[0]]
    for t in range(N - 1, 0, -1):
        chemin.append(cout[t][chemin[-1]][1])
    return list(reversed(chemin))
