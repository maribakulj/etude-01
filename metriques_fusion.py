"""
metriques_fusion.py — Étape 1 du projet : solidifier la pièce centrale (la métrique Φ).

Ce module implémente plusieurs métriques de fusion / harmonicité tirées de la
littérature, plus la proxy actuelle, derrière UNE interface commune, pour les
comparer sur le cas de contrôle (timbre harmonique + récepteur humain).

Contrat (cf. SPEC-v1 §1, CADRAGE-v2 §5, PASSATION) :
  - Φ(i) = tendance à la fusion = harmonicité du spectre combiné (union des
    partiels de la voix A et de la voix B transposée de l'intervalle i).
  - Le SUBSTRAT (localisation des pics de coïncidence) est arithmétique,
    indépendant du récepteur ; seule la FENÊTRE de tolérance qui décide quelles
    coïncidences "comptent" dépend du récepteur.
  - La rugosité C n'entre JAMAIS dans Φ (hygiène absolue, SPEC §1). Aucune
    métrique ici ne touche à l'interférence/rugosité.
  - Récepteur = paramètre explicite (le "port"), jamais présupposé enfoui.

Périmètre : simultanéité, première espèce. Aucun contact avec graphe / rendu /
instrument. Volontairement autonome (ne déclenche pas l'exécution de
test_noyau.py, qui est le noyau jetable).

Critère de contrôle (SPEC §6.1, éliminatoire) : sur harmonique + humain, Φ doit
piquer à l'octave (1200c) PUIS à la quinte (702c). Toute métrique qui échoue est
fausse et éliminée.

Métriques implémentées
----------------------
  proxy_coincidence  — la proxy actuelle (coïncidence A↔B, noyau gaussien).
                       Paramétrable : w=25c (proxy d'origine, choisie à la main)
                       ou w=6.83c (recalibrage Milne 2013, valeur publiée).
  sieve_darwin       — crible harmonique : gabarit 1/k évalué à la FONDAMENTALE
                       COMMUNE f0/m, fenêtre large dérivée des seuils de
                       mistuning de Moore et al. (3%→8%).
  virtual_pitch      — pitch virtuel Terhardt/Parncutt : gabarit aux poids
                       root-support {10,5,3,2,1}, fondamentale commune, fenêtre
                       fine. (Décision de conception famille A : évaluation à la
                       fondamentale commune, PAS max sur F0 libre — voir
                       diag_famille_A.py pour la démonstration du verrouillage.)
  periodicity        — périodicité de Stolzenburg (2015) : harmonicité = 1 /
                       (dénominateur du rapport rationalisé). ÉTALON DE CONTRÔLE
                       seulement : n'utilise que le rapport, AVEUGLE au spectre,
                       donc structurellement incapable de porter P5.

Toutes les constantes numériques portent leur provenance en commentaire.
"""

import numpy as np

CENTS = lambda r: 1200.0 * np.log2(r)
RATIO = lambda c: 2.0 ** (c / 1200.0)


# ===========================================================================
# Timbres (identiques à test_noyau.py, redéfinis ici pour l'autonomie du module)
# ===========================================================================
def harmonic(n=10):
    """Timbre quasi harmonique : partiels 1..n, roll-off d'amplitude 1/k."""
    k = np.arange(1, n + 1)
    return k.astype(float), 1.0 / k


def music_box(n=5):
    """Lame encastrée-libre (cantilever) : modes 1 : 6.267 : 17.55 : 34.39 : 56.84.
    Spectre ANALYTIQUE (Euler-Bernoulli), amplitudes posées — à remplacer par un
    enregistrement réel à l'étape 2. Utilisé ici UNIQUEMENT pour le test binaire
    'la métrique réagit-elle au spectre ?', jamais pour la sélection."""
    modes = np.array([1.0, 6.267, 17.55, 34.39, 56.84])[:n]
    amps = 1.0 / np.sqrt(np.arange(1, len(modes) + 1))
    return modes, amps


# ===========================================================================
# Outils communs : union des deux voix, détection de pics, repères d'intervalles
# ===========================================================================
def union_spectrum(spec, r, f0=261.6):
    """Union des partiels : voix A à f0, voix B = A transposée de r.
    Renvoie (freqs, amps) concaténés. C'est le 'spectre combiné' de la SPEC §1
    dont les métriques famille A mesurent l'harmonicité."""
    f, a = spec
    F = np.concatenate([f * f0, f * f0 * r])
    A = np.concatenate([a, a])
    return F, A


JUST = {  # repères d'intervalles justes (cents)
    'm2': 111.7, 'M2': 203.9, 'm3': 315.6, 'M3': 386.3, 'P4': 498.0, 'TT': 590.2,
    'P5': 702.0, 'm6': 813.7, 'M6': 884.4, 'm7': 1017.6, 'M7': 1088.3, 'P8': 1200.0}


def nearest_interval(c):
    name = min(JUST, key=lambda k: abs(JUST[k] - c))
    return name, JUST[name], c - JUST[name]


def peaks(curve, x, n=6, min_sep=40.0, x_floor=100.0):
    """Pics d'une courbe, zone de quasi-unisson (< seconde mineure ~100c) exclue.

    x_floor : justifié SPEC/noyau — l'unisson et les micro-intervalles sont hors
    domaine de R2 (écart minimal entre voix, pas de croisement). Pour les
    métriques famille A (harmonicité de l'union), la zone <100c est en plus
    trivialement maximale : deux voix quasi confondues SONT presque une seule
    note, leur union est presque un seul spectre harmonique. On l'exclut donc,
    exactement comme le noyau. Décision de modélisation déclarée, pas oubliée."""
    idx = np.argsort(curve)[::-1]
    chosen = []
    for i in idx:
        if x[i] < x_floor:
            continue
        if all(abs(x[i] - x[j]) > min_sep for j in chosen):
            chosen.append(i)
        if len(chosen) >= n:
            break
    return sorted(chosen, key=lambda i: -curve[i])


# ===========================================================================
# MÉTRIQUE 0 — proxy actuelle : coïncidence spectrale A↔B sous transposition
#   (famille B : similarité spectrale ; = spectral pitch similarity de Milne 2013
#    à la normalisation près). w = fenêtre de tolérance = paramètre récepteur.
# ===========================================================================
def proxy_coincidence(spec, r, w_cents=25.0):
    """Proxy d'origine du noyau. Recouvrement de la voix A {f_i} avec la voix
    B = {r f_j}, noyau gaussien en cents. La self-coïncidence i=j à r=1 (un
    partiel alignant sa propre copie) est exclue : deux voix à l'unisson ne
    fusionnent pas, elles SONT la même note.

    w_cents : fenêtre de tolérance (récepteur). 25c = valeur d'origine choisie à
    la main. 6.83c = recalibrage sur la 'spectral pitch similarity' de Milne
    (2013), constante publiée (package hrep de Harrison, sigma=6.83c)."""
    f, a = spec
    fa = f[:, None]
    fb = r * f[None, :]
    ab = a[:, None] * a[None, :]
    d = 1200.0 * np.log2(fa / fb)               # écart en cents A_i vs B_j
    K = np.exp(-(d / w_cents) ** 2)
    same = (np.abs(d) < 1e-6) & (np.arange(len(f))[:, None] == np.arange(len(f))[None, :])
    K = np.where(same, 0.0, K)                  # retire la self-coïncidence i=j
    return float(np.sum(ab * K))


# ===========================================================================
# Famille A — harmonicité du spectre combiné par appariement de GABARIT,
# normalisé en COSINUS (Milne 2013 ; Harrison & Pearce 2018).
#
# Forme commune : on cherche la fondamentale F0 dont le gabarit harmonique
# ressemble le plus à l'union des partiels, au sens du cosinus entre spectres
# lissés. Le cosinus est essentiel : il pénalise les fondamentales graves dont
# la série est incomplète (sinon une F0 très grave 'capture' tout par alignement
# fortuit). Les deux métriques famille A ci-dessous ne diffèrent QUE par les
# poids du gabarit et la largeur de fenêtre (le récepteur) ; elles partagent ce
# moteur. Calcul analytique : le produit scalaire de deux spectres faits de
# gaussiennes (SD sigma en cents) est une somme de noyaux exp(-d²/(4σ²)) sur les
# paires de raies — pas de rastérisation.
# ===========================================================================
_HMAX = 16  # rang harmonique max des gabarits


def _self_overlap(cents, weights, sigma):
    """Norme² d'un spectre de raies gaussiennes : <s,s>."""
    d = cents[:, None] - cents[None, :]
    K = np.exp(-(d ** 2) / (4.0 * sigma ** 2))
    return float((weights[:, None] * weights[None, :] * K).sum())


def _template_cosine(spec, r, template_weights, sigma, f0=261.6):
    """Cosinus entre l'union (voix A + voix B transposée de r) et le gabarit
    harmonique de la FONDAMENTALE COMMUNE f0/m, où m est le dénominateur du
    rapport rationalisé. C'est la lecture littérale de la SPEC §1 : « à quel
    point l'union se laisse décrire par UNE fondamentale commune ».

    Note de méthode (cf. diag_famille_A.py) : on évalue à la fondamentale
    commune, PAS au maximum sur une fondamentale libre. Un maximum libre se
    verrouille sur f0 (la fondamentale de la voix A seule, toujours parfaitement
    harmonique) et mesure l'auto-harmonicité d'une voix — constante en r — au
    lieu de la fusion des DEUX voix. La fondamentale commune de deux voix au
    rapport n/m (réduit) est f0/m — le pgcd des deux fondamentales.

    `template_weights` : poids des harmoniques 1.._HMAX. `sigma` : fenêtre en
    cents (= récepteur ; règle la finesse, pas la position des pics)."""
    _n, m = _rationalize(float(r))
    F, A = union_spectrum(spec, r, f0)
    cU = 1200.0 * np.log2(F / f0)                # union en cents (réf f0)
    nU = _self_overlap(cU, A, sigma)
    if nU <= 0:
        return 0.0
    ks = np.arange(1, _HMAX + 1).astype(float)
    wk = template_weights[:_HMAX]
    cT = -1200.0 * np.log2(m) + 1200.0 * np.log2(ks)   # harmoniques de f0/m, en cents
    nT = _self_overlap(cT, wk, sigma)
    d = cU[:, None] - cT[None, :]
    K = np.exp(-(d ** 2) / (4.0 * sigma ** 2))
    overlap = float((A[:, None] * wk[None, :] * K).sum())
    return overlap / np.sqrt(nU * max(nT, 1e-12))


# --- MÉTRIQUE 1 : crible harmonique à tolérance Darwin/Moore -----------------
#   Gabarit harmonique à roll-off doux (source quasi harmonique typique) ;
#   fenêtre LARGE fixée par la tolérance de mistuning de Moore, Glasberg &
#   Peters (1985) : pleine contribution au pitch < 3%, ~nulle vers 8%. Le crible
#   (Duifhuis, Willems & Sluyter 1982) demande 'ces partiels forment-ils UNE
#   série harmonique ?'. Le récepteur = la largeur de fenêtre.
_DARWIN_TOL_FULL = 0.03   # Moore, Glasberg & Peters (1985) : pleine contribution
_DARWIN_TOL_ZERO = 0.08   # ... contribution ~nulle au-delà de 8% de mistuning
# Largeur de fenêtre en cents : ~milieu de la rampe 3%→8% (≈5.5% ≈ 93c d'écart
# relatif pleine-largeur) -> sigma gaussien ≈ 35c. Provenance : conversion en
# cents des seuils de Moore et al. (3% ≈ 51c, 8% ≈ 133c).
_DARWIN_SIGMA = 35.0
_DARWIN_ROLLOFF = 1.0     # poids harmonique 1/k^rolloff du gabarit (source 1/k)


def sieve_darwin(spec, r, f0=261.6, sigma_cents=_DARWIN_SIGMA):
    """Φ = harmonicité de l'union = cosinus au meilleur gabarit harmonique, dans
    la fenêtre large de Darwin/Moore. sigma_cents = fenêtre récepteur ; la
    resserrer affine les pics sans les déplacer (substrat arithmétique)."""
    wk = 1.0 / np.arange(1, _HMAX + 1) ** _DARWIN_ROLLOFF
    return _template_cosine(spec, r, wk, sigma_cents, f0)


# --- MÉTRIQUE 2 : pitch virtuel Terhardt / Parncutt -------------------------
#   Même moteur, mais le gabarit porte les poids root-support de Parncutt (1988)
#   — c'est l'appariement sous-harmonique du modèle de pitch virtuel — et une
#   fenêtre plus fine (le pitch virtuel est assez précis).
# Poids root-support de Parncutt (1988), confirmés Parncutt (2006) :
#   unisson (P1)=10 ; quinte (P5)=5 ; tierce maj (M3)=3 ; septième min (m7)=2 ;
#   seconde maj (M2)=1. Mappés sur le rang harmonique n (intervalle octave-réduit
#   de l'harmonique n) -> n=1..10 : [10,10,5,10,3,5,2,10,1,3], n>10 : 0.
_PARNCUTT_W = np.array([0, 10, 10, 5, 10, 3, 5, 2, 10, 1, 3], dtype=float)  # index = n
_VP_SIGMA = 12.0          # fenêtre de coïncidence (récepteur), pitch virtuel précis


def _parncutt_template():
    w = np.zeros(_HMAX)
    m = min(_HMAX, len(_PARNCUTT_W) - 1)
    w[:m] = _PARNCUTT_W[1:m + 1]
    return w


def virtual_pitch(spec, r, f0=261.6, tol_cents=_VP_SIGMA):
    """Φ = cosinus au meilleur gabarit de pitch virtuel (poids root-support de
    Parncutt). tol_cents = fenêtre récepteur (finesse des pics, pas position)."""
    return _template_cosine(spec, r, _parncutt_template(), tol_cents, f0)


# ===========================================================================
# MÉTRIQUE 3 — périodicité de Stolzenburg (2015)  [ÉTALON DE CONTRÔLE]
#   harmonicité = 1 / periodicity ; periodicity = dénominateur du rapport
#   rationalisé (= longueur de la période commune des deux fondamentales, en
#   périodes du grave). Tolérance de rationalisation d = 1% (JND de hauteur,
#   Stolzenburg 2015, Table 1 #1).
#   AVEUGLE AU SPECTRE : n'utilise que r. Reproduit l'ordre de fusion sur
#   l'harmonique (P2) mais ne peut PAS porter P5 -> gardé comme sanity check,
#   éliminé comme candidat final.
# ===========================================================================
_STOLZ_TOL = 0.01   # d = 1.0% (Stolzenburg 2015, Table 1, tuning #1 ; JND ~1%)


def _rationalize(x, tol=_STOLZ_TOL, mmax=1000):
    """Plus simple fraction n/m (plus petit dénominateur) avec |x - n/m|/x <= tol.
    Renvoie (n, m) réduits."""
    for m in range(1, mmax + 1):
        n = round(x * m)
        if n == 0:
            continue
        if abs(x - n / m) / x <= tol:
            g = np.gcd(int(n), int(m))
            return n // g, m // g
    n = round(x * mmax)
    g = np.gcd(int(n), int(mmax))
    return n // g, mmax // g


def periodicity(spec, r, tol=_STOLZ_TOL):
    """Φ = 1 / periodicity, periodicity = dénominateur de r rationalisé.
    Le paramètre `spec` est ignoré (métrique purement intervallique) — présent
    pour respecter l'interface commune et rendre explicite qu'elle n'en dépend
    PAS (c'est précisément ce qui l'élimine pour P5)."""
    _n, m = _rationalize(float(r), tol)
    return 1.0 / m


# ===========================================================================
# Registre des métriques : interface commune phi(spec, r, **recepteur)
# ===========================================================================
METRIQUES = {
    'proxy_w25':      lambda spec, r: proxy_coincidence(spec, r, w_cents=25.0),
    'proxy_milne':    lambda spec, r: proxy_coincidence(spec, r, w_cents=6.83),
    'sieve_darwin':   lambda spec, r: sieve_darwin(spec, r),
    'virtual_pitch':  lambda spec, r: virtual_pitch(spec, r),
    'periodicity':    lambda spec, r: periodicity(spec, r),
}

LABELS = {
    'proxy_w25':     'Proxy coïncidence (w=25c, d\'origine)',
    'proxy_milne':   'Proxy = Milne spectral pitch sim. (σ=6.83c)',
    'sieve_darwin':  'Crible harmonique Darwin/Moore (3→8%)',
    'virtual_pitch': 'Pitch virtuel Terhardt/Parncutt (root-support)',
    'periodicity':   'Périodicité Stolzenburg (étalon, aveugle au spectre)',
}


def courbe(metrique, spec, cents_axis):
    """Évalue une métrique sur tout le balayage d'intervalles. Renvoie un vecteur."""
    fn = METRIQUES[metrique]
    rs = RATIO(cents_axis)
    return np.array([fn(spec, r) for r in rs])


if __name__ == '__main__':
    # Auto-test minimal des invariants arithmétiques (pas la comparaison complète,
    # qui est dans comparaison_phi.py).
    print("Validation analytique des constantes/définitions :")
    # Stolzenburg : périodicités attendues (dénominateurs réduits).
    attendu = {'P8': (1200.0, 1), 'P5': (702.0, 2), 'P4': (498.0, 3),
               'M3': (386.3, 4), 'm3': (315.6, 5), 'M6': (884.4, 3)}
    print("  Stolzenburg periodicity (dénominateur réduit) :")
    ok = True
    for nm, (c, exp) in attendu.items():
        _n, m = _rationalize(RATIO(c))
        flag = '' if m == exp else '  <-- INATTENDU'
        ok &= (m == exp)
        if flag:
            ok = False
        print(f"    {nm:3s} ({c:6.1f}c) -> {_n}/{m}  (periodicity={m}, attendu {exp}){flag}")
    print(f"  => {'OK' if ok else 'ÉCART'}")
    # Poids root-support de Parncutt
    print(f"  Parncutt root-support w[n=1..10] = {_PARNCUTT_W[1:11].astype(int).tolist()}")
    print(f"    (attendu [10,10,5,10,3,5,2,10,1,3])")
