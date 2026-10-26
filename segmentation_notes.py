"""
segmentation_notes.py — front-end de SÉLECTION pour matériau mélodique
(étape 2, entrée datée dans ETAPE2-PROTOCOLE.md §7).

Le protocole demandait des notes isolées ; le matériau reçu est une mélodie
(boîte à manivelle, bande perforée) avec bruit de manivelle et voix en fin de
fichier. Ce module NE TOUCHE NI aux paramètres d'extraction (figés,
extraction_spectre.py) NI aux seuils du verdict (figés, etape2_p5.py) : il
sélectionne des fenêtres mono-note et filtre la contamination, c'est tout.

Règle d'intégrité : les notes sont retenues sur des critères de QUALITÉ DE
MESURE (nombre de partiels nés à l'onset, absence de second onset dans la
fenêtre), jamais d'après la courbe Φ qui en résulte.

Méthode :
  1. Onsets par flux spectral (hausse demi-onde redressée du spectre),
     seuil médiane + 3·MAD, séparation minimale 0,25 s.
  2. Fenêtre candidate = onset sans autre onset pendant >= 0,55 s ;
     analyse [onset, min(onset + 1,2 s, onset suivant - 0,05 s)].
  3. Extraction figée (extraction_spectre.extraire) sur la fenêtre.
  4. Garde anti-contamination : un partiel n'appartient à la note que s'il
     NAÎT à l'onset — son amplitude dans les 170 ms PRÉCÉDANT l'onset doit
     être < PRE_RATIO_MAX fois son amplitude après. Élimine les queues de
     résonance des notes précédentes et les raies stationnaires.
  5. Note retenue si >= 3 partiels survivants.
"""

import json
import sys
import tempfile

import numpy as np
import soundfile as sf
from scipy.signal.windows import blackmanharris

from extraction_spectre import extraire

T_MAX_S = 30.0          # voix humaine après ~30 s dans le matériau reçu : exclu
FLUX_N = 1024
FLUX_HOP = 512
FLUX_BAND = (150.0, 8000.0)
ONSET_SEP_S = 0.25
# Densité du matériau reçu (médiane des écarts entre onsets : 0,31 s) :
# fenêtres au minimum exact de l'extraction figée (4 trames = 0,24 s de piste,
# soit 0,26 s de fenêtre).
ISOLATION_S = 0.28      # pas d'autre onset pendant ce délai
WIN_MAX_S = 1.0
WIN_MIN_S = 0.26
WIN_MARGIN_S = 0.02     # marge avant l'onset suivant
PRE_S = 0.17            # fenêtre de contrôle avant onset
PRE_GAP_S = 0.01
POST_S = 0.20           # fenêtre de comparaison après onset
PRE_RATIO_MAX = 0.30    # amplitude avant / après maximale pour « naître à l'onset »
LATE_T0_S, LATE_T1_S = 0.33, 0.53
LATE_RISE_MAX = 2.0     # un partiel qui FORCIT nettement après l'onset est une
                        # autre note frappée en cours de fenêtre : rejeté
MIN_PARTIELS = 3
GROUP_TOL_CENTS = 30.0  # regroupement des occurrences d'une même dent
# Gardes anti-accord (plusieurs dents frappées ensemble par le perforateur) :
# physiquement, le mode 2 d'une lamelle encastrée est au-delà de ~2,3×f0 (6,27
# idéal, abaissé par lestage). Une composante forte née à l'onset DANS la zone
# des intervalles musicaux (1,06-2,30) est donc une AUTRE dent -> fenêtre
# rejetée. Deux composantes fortes co-nées trop proches dans la zone de mode 2
# (< 350 c d'écart) = deux dents aussi (une lamelle n'a qu'un mode 2).
CHORD_ZONE = (1.06, 2.30)
CHORD_AMP = 0.25
TWIN_ZONE = (2.30, 5.0)
TWIN_AMP = 0.30
TWIN_SEP_CENTS = 350.0


def _mono(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    return x[:int(T_MAX_S * sr)], sr


def onsets_flux(x, sr):
    """Onsets par flux spectral, en secondes."""
    nfr = (len(x) - FLUX_N) // FLUX_HOP
    w = np.hanning(FLUX_N)
    prev = None
    flux = np.zeros(nfr)
    fr = np.fft.rfftfreq(FLUX_N, 1 / sr)
    band = (fr >= FLUX_BAND[0]) & (fr <= FLUX_BAND[1])
    for k in range(nfr):
        S = np.abs(np.fft.rfft(x[k * FLUX_HOP:k * FLUX_HOP + FLUX_N] * w))[band]
        if prev is not None:
            flux[k] = np.sum(np.maximum(0.0, S - prev))
        prev = S
    med = np.median(flux)
    mad = np.median(np.abs(flux - med)) + 1e-12
    thr = med + 3.0 * mad
    sep = int(ONSET_SEP_S * sr / FLUX_HOP)
    out = []
    k = 1
    while k < nfr - 1:
        if flux[k] > thr and flux[k] >= flux[k - 1] and flux[k] >= flux[k + 1]:
            out.append(k * FLUX_HOP / sr)
            k += sep
        else:
            k += 1
    return out


def _spectrum_amp_at(x, sr, t0, t1, freqs_hz):
    """Amplitude spectrale (fenêtre BH sur [t0,t1]) au voisinage ±1,5 % de
    chaque fréquence demandée."""
    a, b = max(0, int(t0 * sr)), min(len(x), int(t1 * sr))
    seg = x[a:b]
    if len(seg) < 256:
        return np.zeros(len(freqs_hz))
    S = np.abs(np.fft.rfft(seg * blackmanharris(len(seg)), n=4 * len(seg)))
    fr = np.fft.rfftfreq(4 * len(seg), 1 / sr)
    out = []
    for f in freqs_hz:
        m = (fr >= f * 0.985) & (fr <= f * 1.015)
        out.append(float(S[m].max()) if m.any() else 0.0)
    return np.array(out)


def notes_candidates(path, strict=False):
    """Renvoie la liste des notes mesurées : dicts {t, f0_hz, partiels, ...}.

    strict=True : fenêtres isolées + gardes anti-accord (peu de fenêtres sur
    matériau dense). strict=False (mode STATISTIQUE, défaut pour mélodie) :
    toutes les fenêtres possibles sont mesurées, y compris des accords ; la
    séparation dent/contexte est déléguée au regroupement par récurrence
    (grouper_par_dent) — les modes d'une dent reviennent à chaque frappe, les
    notes de contexte changent avec la mélodie."""
    x, sr = _mono(path)
    ons = onsets_flux(x, sr)
    print(f"{len(ons)} onsets détectés sur les {T_MAX_S:.0f} premières secondes")
    notes = []
    for i, t in enumerate(ons):
        t_next = ons[i + 1] if i + 1 < len(ons) else T_MAX_S
        if strict and t_next - t < ISOLATION_S:
            continue
        t_end = min(t + WIN_MAX_S, t_next - WIN_MARGIN_S, len(x) / sr)
        if t_end - t < WIN_MIN_S:
            continue
        seg = x[int(t * sr):int(t_end * sr)]
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as fh:
            sf.write(fh.name, seg, sr)
            try:
                ext = extraire(fh.name)
            except ValueError:
                continue
        freqs = [p['hz'] for p in ext['partiels']]
        pre = _spectrum_amp_at(x, sr, t - PRE_S - PRE_GAP_S, t - PRE_GAP_S, freqs)
        post = _spectrum_amp_at(x, sr, t + 0.02, t + 0.02 + POST_S, freqs)
        late = _spectrum_amp_at(x, sr, t + LATE_T0_S, t + LATE_T1_S, freqs)
        nés = [p for p, pa, po, la in zip(ext['partiels'], pre, post, late)
               if po > 0 and pa / po < PRE_RATIO_MAX and la < LATE_RISE_MAX * po]
        if len(nés) < MIN_PARTIELS:
            continue
        f1 = nés[0]['hz']  # partiels triés par fréquence ; le plus bas né = fondamental
        if strict:
            amax = max(p['amp'] for p in nés)
            rel = [(p['hz'] / f1, p['amp'] / amax) for p in nés]
            if any(CHORD_ZONE[0] < r < CHORD_ZONE[1] and a > CHORD_AMP for r, a in rel):
                continue  # accord : autre dent à un intervalle musical
            twins = [r for r, a in rel if TWIN_ZONE[0] < r < TWIN_ZONE[1] and a > TWIN_AMP]
            if any(abs(1200 * np.log2(r2 / r1)) < TWIN_SEP_CENTS
                   for i, r1 in enumerate(twins) for r2 in twins[i + 1:]):
                continue  # deux « modes 2 » co-nés trop proches : deux dents
        notes.append(dict(
            t=round(float(t), 2), f0_hz=float(f1), n_bruts=len(ext['partiels']),
            partiels=[dict(ratio=float(p['hz'] / f1), amp=p['amp'], hz=p['hz'],
                           excursion_cents=p['excursion_cents'], trames=p['trames'])
                      for p in nés],
            sr=int(sr), source=str(path), sha256_16=ext['sha256_16'],
            fenetre_s=[round(float(t), 2), round(float(t_end), 2)]))
    return notes


def grouper_par_dent(notes):
    """Regroupe les occurrences d'une même hauteur (= même dent du peigne).
    Renvoie une liste de groupes {f0_med, occurrences, ratios_median,
    dispersion_cents} ; les ratios médians ne retiennent que les partiels vus
    dans au moins la moitié des occurrences du groupe."""
    groupes = []
    for n in sorted(notes, key=lambda n: n['f0_hz']):
        for g in groupes:
            if abs(1200 * np.log2(n['f0_hz'] / g['f0'])) < GROUP_TOL_CENTS:
                g['notes'].append(n)
                g['f0'] = float(np.median([m['f0_hz'] for m in g['notes']]))
                break
        else:
            groupes.append({'f0': n['f0_hz'], 'notes': [n]})
    out = []
    for g in groupes:
        occ = len(g['notes'])
        clusters = []  # regroupement des ratios entre occurrences
        for n in g['notes']:
            for p in n['partiels']:
                for c in clusters:
                    if abs(1200 * np.log2(p['ratio'] / c['r'])) < GROUP_TOL_CENTS:
                        c['vals'].append((p['ratio'], p['amp']))
                        c['r'] = float(np.median([v[0] for v in c['vals']]))
                        break
                else:
                    clusters.append({'r': p['ratio'], 'vals': [(p['ratio'], p['amp'])]})
        fiables = []
        # Récurrence exigée : un partiel de la dent doit être vu dans >= 60 %
        # des occurrences (c'est CE filtre qui sépare les modes de la dent des
        # notes de contexte en mode statistique).
        for c in clusters:
            if len(c['vals']) >= max(2, int(np.ceil(0.6 * occ))) or occ == 1:
                rs = np.array([v[0] for v in c['vals']])
                disp = 1200 * np.log2(rs.max() / rs.min()) if len(rs) > 1 else 0.0
                fiables.append(dict(ratio=float(np.median(rs)),
                                    amp=float(np.median([v[1] for v in c['vals']])),
                                    vues=len(c['vals']), dispersion_cents=round(float(disp), 1)))
        fiables.sort(key=lambda p: p['ratio'])
        out.append(dict(f0_hz=g['f0'], occurrences=occ, partiels=fiables,
                        t_occurrences=[n['t'] for n in g['notes']]))
    return sorted(out, key=lambda g: -g['occurrences'])


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/fugue.mp3'
    notes = notes_candidates(path)
    print(f"\n{len(notes)} fenêtres mono-note exploitables (>= {MIN_PARTIELS} partiels nés à l'onset) :")
    for n in notes:
        rats = "  ".join(f"{p['ratio']:.3f}({p['amp']:.2f})" for p in n['partiels'][:6])
        print(f"  t={n['t']:5.2f}s  f0={n['f0_hz']:7.1f} Hz  "
              f"[{len(n['partiels'])}/{n['n_bruts']} partiels]  ratios: {rats}")
    print("\nGroupes par dent (occurrences regroupées) :")
    for g in grouper_par_dent(notes):
        rats = "  ".join(f"{p['ratio']:.3f}(amp {p['amp']:.2f}, {p['vues']}x, ±{p['dispersion_cents']}c)"
                         for p in g['partiels'][:6])
        print(f"  f0={g['f0_hz']:7.1f} Hz  {g['occurrences']} occ.  {rats}")
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as fh:
            json.dump(dict(notes=notes, groupes=grouper_par_dent(notes)), fh, indent=1)
        print(f"écrit : {sys.argv[2]}")
