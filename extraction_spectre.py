"""
extraction_spectre.py — Étape 2 : extraire d'un enregistrement réel le spectre
d'une note isolée (partiels : fréquences relatives + amplitudes), avec
contrôles de qualité, pour alimenter la métrique Φ figée (DECISION-PHI.md).

Discipline anti-ajustement : cette chaîne est écrite et VALIDÉE (voir
test_extraction.py) AVANT réception de tout enregistrement réel de boîte à
musique. Aucun paramètre ne sera retouché après réception sans entrée datée
dans ETAPE2-PROTOCOLE.md.

Méthode : suivi de partiels multi-trames.
  1. Détection d'onset (enveloppe d'énergie), saut de la zone d'attaque.
  2. STFT (fenêtre Hann, zero-padding) ; pics locaux par trame.
  3. Regroupement des pics en raies ; une raie n'est un PARTIEL que si elle
     persiste sur une fraction minimale des trames ET reste stable en
     fréquence (< MAX_WANDER_CENTS d'excursion). Ceci élimine bruit de fond,
     résonances de salle transitoires et artefacts.
  4. Amplitude d'un partiel = maximum observé dans les AMP_WINDOW_S premières
     secondes après l'onset (proxy déclaré du poids du partiel dans la phase
     quasi stationnaire de la note ; v1 = simultanéité, pas d'enveloppes).
  5. Fondamental f1 = raie la plus forte à moins de 150 c du nominal si un
     nominal est fourni, sinon la plus basse raie à moins de 30 dB du max.

Formats lisibles : wav, flac, ogg ; mp3 si libsndfile >= 1.1.
Sortie : dict / JSON {source, sha256, f0_hz, partiels:[{ratio, amp, hz,
excursion_cents, trames}], parametres}.
"""

import hashlib
import json
import sys

import numpy as np
import soundfile as sf
from scipy.signal.windows import blackmanharris

# --- Paramètres de la chaîne (figés avant données réelles) -------------------
WIN_S = 0.12              # fenêtre d'analyse (s)
HOP_S = 0.04              # pas entre trames (s)
ZPAD = 8                  # facteur de zero-padding
ATTACK_S = 0.015          # zone d'attaque sautée après l'onset (s)
MAX_FRAMES = 60
FMIN, FMAX = 60.0, 16000.0
PEAK_FLOOR = 2e-3         # seuil de pic, relatif au max de la trame
LINE_TOL = 0.012          # regroupement des pics en raies (1,2 %)
# Persistance ABSOLUE (≥4 trames = 160 ms), pas en fraction des trames totales :
# les modes hauts d'une lamelle décroissent vite (déjà ~0,1 s sur le synthétique
# réaliste) et une exigence proportionnelle à la durée du fichier les éliminait
# (constaté par test_extraction.py avant données réelles).
MIN_FRAMES_ABS = 4
MIN_FRAMES_FRAC = 0.08    # garde-fou résiduel pour les fichiers très courts
MAX_WANDER_CENTS = 20.0   # excursion de fréquence maximale d'un vrai partiel
# Rejet des bourdonnements : une raie qui couvre la quasi-totalité des trames
# SANS décroître (ventilation, secteur, drone de salle) n'est pas un mode de
# note pincée.
DRONE_SPAN_FRAC = 0.6
DRONE_DECAY_MIN = 0.7     # amplitude finale < 70 % de l'initiale exigée
AMP_WINDOW_S = 0.30       # fenêtre de lecture de l'amplitude après onset
DB_KEEP = -50.0           # partiels conservés : à moins de 50 dB du plus fort


def _onset_index(x, sr):
    """Onset = première trame courte dont l'énergie dépasse 10 % du max."""
    n = max(1, int(0.01 * sr))
    e = np.convolve(x ** 2, np.ones(n) / n, mode='same')
    thr = 0.1 * e.max()
    return int(np.argmax(e >= thr))


def _frames_peaks(x, sr, i0):
    """Liste, par trame, des pics spectraux (freq, amp)."""
    N = int(WIN_S * sr)
    hop = int(HOP_S * sr)
    out = []
    k = 0
    while True:
        a = i0 + k * hop
        k += 1
        if a + N > len(x) or len(out) >= MAX_FRAMES:
            break
        # Blackman-Harris : lobes secondaires à -92 dB. Avec Hann (-31 dB), les
        # lobes du fondamental passent PEAK_FLOOR et fabriquent des partiels
        # fantômes (constaté par test_extraction.py avant données réelles).
        seg = x[a:a + N] * blackmanharris(N)
        S = np.abs(np.fft.rfft(seg, n=ZPAD * N))
        fr = np.fft.rfftfreq(ZPAD * N, 1.0 / sr)
        m = (fr > FMIN) & (fr < FMAX)
        S, fr = S[m], fr[m]
        if S.max() <= 0:
            out.append([])
            continue
        thr = S.max() * PEAK_FLOOR
        pk = [(fr[i], S[i]) for i in range(2, len(S) - 2)
              if S[i] == max(S[i - 2:i + 3]) and S[i] > thr]
        out.append(sorted(pk, key=lambda t: -t[1])[:25])
    return out


def _group_lines(frames):
    """Regroupe les pics de trames successives en raies persistantes."""
    lines = []
    for k, pk in enumerate(frames):
        for f, a in pk:
            for L in lines:
                if abs(f - L['f']) / L['f'] < LINE_TOL:
                    L['obs'].append((k, f, a))
                    L['f'] = float(np.median([o[1] for o in L['obs']]))
                    break
            else:
                lines.append({'f': f, 'obs': [(k, f, a)]})
    return lines


def extraire(path, f0_nominal_hz=None):
    """Extrait le spectre d'une note isolée. Renvoie un dict (cf. docstring)."""
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(float)
    if len(x) < sr // 4:
        raise ValueError("enregistrement trop court (<0,25 s)")
    i0 = _onset_index(x, sr) + int(ATTACK_S * sr)
    frames = _frames_peaks(x, sr, i0)
    nf = len(frames)
    if nf < MIN_FRAMES_ABS:
        raise ValueError(f"trop peu de trames analysables ({nf})")
    need = max(MIN_FRAMES_ABS, int(MIN_FRAMES_FRAC * nf))
    amp_frames = max(1, int(round(AMP_WINDOW_S / HOP_S)))

    partiels = []
    for L in _group_lines(frames):
        # Statistiques sur la partie VIVANTE de la raie : une fois le mode
        # décru dans le bruit, la raie continue d'agréger des pics de bruit
        # voisins et son excursion apparente gonfle (constaté par
        # test_extraction.py). On ne garde que les observations à moins de
        # 35 dB du maximum propre de la raie.
        amax_line = max(o[2] for o in L['obs'])
        alive = [o for o in L['obs'] if o[2] >= amax_line * 10 ** (-35 / 20)]
        ks = sorted({o[0] for o in alive})
        if len(ks) < need:
            continue
        fs = np.array([o[1] for o in alive])
        wander = 1200.0 * np.log2(fs.max() / fs.min())
        if wander > MAX_WANDER_CENTS:
            continue
        L = dict(f=float(np.median(fs)), obs=alive)
        amps_seq = [o[2] for o in sorted(L['obs'], key=lambda o: o[0])]
        if len(ks) > DRONE_SPAN_FRAC * nf and len(amps_seq) >= 6:
            head = float(np.median(amps_seq[:3]))
            tail = float(np.median(amps_seq[-3:]))
            if tail > DRONE_DECAY_MIN * head:
                continue  # bourdonnement stationnaire, pas un mode de note
        early = [o[2] for o in L['obs'] if o[0] < amp_frames]
        if not early:
            continue
        partiels.append(dict(hz=float(np.median(fs)), amp=float(max(early)),
                             excursion_cents=float(wander), trames=len(ks)))
    if len(partiels) < 3:
        raise ValueError(f"seulement {len(partiels)} partiel(s) stable(s) — "
                         "enregistrement inutilisable en l'état")
    partiels.sort(key=lambda p: p['hz'])
    amax = max(p['amp'] for p in partiels)

    # fondamental
    if f0_nominal_hz:
        cand = [p for p in partiels
                if abs(1200.0 * np.log2(p['hz'] / f0_nominal_hz)) < 150.0]
        if not cand:
            raise ValueError("aucune raie à moins de 150 c du nominal fourni")
        f1 = max(cand, key=lambda p: p['amp'])['hz']
    else:
        fortes = [p for p in partiels if p['amp'] > amax * 10 ** (-30 / 20)]
        f1 = fortes[0]['hz']

    keep = []
    for p in partiels:
        db = 20.0 * np.log10(p['amp'] / amax)
        if db < DB_KEEP or p['hz'] < f1 * 0.97:
            continue
        keep.append(dict(ratio=float(p['hz'] / f1), amp=float(p['amp'] / amax),
                         hz=p['hz'], excursion_cents=round(p['excursion_cents'], 2),
                         trames=p['trames']))

    with open(path, 'rb') as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()[:16]
    return dict(source=str(path), sha256_16=digest, sr=int(sr),
                f0_hz=float(f1), n_trames=nf, partiels=keep,
                parametres=dict(win_s=WIN_S, hop_s=HOP_S, zpad=ZPAD,
                                line_tol=LINE_TOL, max_wander_cents=MAX_WANDER_CENTS,
                                amp_window_s=AMP_WINDOW_S, db_keep=DB_KEEP))


def spectre_pour_phi(extraction):
    """Convertit une extraction en (ratios, amps) pour metriques_fusion."""
    r = np.array([p['ratio'] for p in extraction['partiels']])
    a = np.array([p['amp'] for p in extraction['partiels']])
    return r, a


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 extraction_spectre.py fichier.wav [f0_nominal_hz] [sortie.json]")
        sys.exit(1)
    f0 = float(sys.argv[2]) if len(sys.argv) > 2 else None
    res = extraire(sys.argv[1], f0)
    print(f"source : {res['source']}  (sha256:{res['sha256_16']}, {res['n_trames']} trames)")
    print(f"f0 = {res['f0_hz']:.2f} Hz ; {len(res['partiels'])} partiels :")
    for p in res['partiels']:
        print(f"  ratio {p['ratio']:7.4f}  amp {p['amp']:.3f}  ({p['hz']:8.1f} Hz, "
              f"±{p['excursion_cents']:.1f}c, {p['trames']} trames)")
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as fh:
            json.dump(res, fh, indent=1)
        print(f"écrit : {sys.argv[3]}")
