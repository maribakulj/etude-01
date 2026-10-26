"""
test_extraction.py — validation bout-à-bout de la chaîne de mesure de l'étape 2,
exécutée AVANT toute donnée réelle (discipline anti-ajustement).

Deux tests :
  A. Signal synthétique PROPRE : modes de cantilever {1, 6.267, 17.55, 34.39},
     amplitudes du modèle analytique, décroissances égales. La chaîne doit
     retrouver les ratios à ±0,5 % et les amplitudes relatives à ±20 %.
  B. Signal synthétique RÉALISTE : mêmes modes, décroissances plus rapides pour
     les modes hauts, bruit de fond (-45 dB), légère désaccordure (+0,3 %). La
     chaîne doit retrouver les ratios à ±1 %, et la courbe Φ figée calculée sur
     le spectre EXTRAIT doit placer ses deux pics principaux à ±15 c des pics
     calculés sur le spectre INJECTÉ (la mesure n'introduit pas de biais de
     position — c'est la propriété requise pour P5).

Échec => code retour non nul. Ne pas modifier les seuils après coup.
"""

import sys

import numpy as np
import soundfile as sf

from extraction_spectre import extraire, spectre_pour_phi
from metriques_fusion import proxy_coincidence, peaks

SR = 44100
F0 = 261.6  # C4 : les 5 modes du cantilever restent en bande (mode 5 = 14,9 kHz < 16 kHz)
MODES = np.array([1.0, 6.267, 17.55, 34.39, 56.84])
AMPS = 1.0 / np.sqrt(np.arange(1, len(MODES) + 1))


def synth(decays, detune=0.0, noise_db=None, dur=3.0):
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for m, a, d in zip(MODES, AMPS, decays):
        f = F0 * m * (1.0 + detune)
        if f > SR / 2 * 0.95:
            continue
        x += a * np.exp(-t / d) * np.sin(2 * np.pi * f * t)
    if noise_db is not None:
        rng = np.random.default_rng(7)
        x += 10 ** (noise_db / 20) * np.max(np.abs(x)) * rng.standard_normal(len(t))
    # attaque douce 5 ms + silence initial 100 ms
    env = np.minimum(1.0, t / 0.005)
    x = np.concatenate([np.zeros(int(0.1 * SR)), x * env])
    return x / (1.05 * np.max(np.abs(x)))


def phi_curve(spec, cents):
    return np.array([proxy_coincidence(spec, 2 ** (c / 1200), w_cents=6.83) for c in cents])


def peak_positions(spec, n=3):
    cents = np.linspace(1.0, 1200.0, 1200)
    P = phi_curve(spec, cents)
    return sorted(cents[i] for i in peaks(P, cents, n=n))


def main():
    ok = True

    # ---- Test A : propre ----------------------------------------------------
    sf.write('/tmp/synth_A.wav', synth(decays=[1.2] * len(MODES)), SR)
    res = extraire('/tmp/synth_A.wav', f0_nominal_hz=F0)
    got = {round(p['ratio'], 3): p['amp'] for p in res['partiels']}
    print("Test A (propre) — partiels extraits :", got)
    for m, a in zip(MODES, AMPS):
        match = [r for r in got if abs(r - m) / m < 0.005]
        if not match:
            print(f"  ÉCHEC : mode {m} non retrouvé à ±0,5 %")
            ok = False
            continue
        rel = got[match[0]] / a
        if not (0.8 < rel < 1.25):
            print(f"  ÉCHEC : amplitude du mode {m} hors ±20 % (×{rel:.2f})")
            ok = False
    print(f"  => {'OK' if ok else 'ÉCHEC'}")

    # ---- Test B : réaliste --------------------------------------------------
    okB = True
    sf.write('/tmp/synth_B.wav',
             synth(decays=[1.5, 0.6, 0.25, 0.12, 0.07], detune=0.003, noise_db=-45.0), SR)
    resB = extraire('/tmp/synth_B.wav', f0_nominal_hz=F0)
    gotB = sorted(p['ratio'] for p in resB['partiels'])
    print("Test B (réaliste) — ratios extraits :", [round(r, 3) for r in gotB])
    for m in MODES:
        if not any(abs(r - m) / m < 0.01 for r in gotB):
            print(f"  ÉCHEC : mode {m} non retrouvé à ±1 %")
            okB = False

    inj = (MODES, AMPS)                      # spectre injecté
    mes = spectre_pour_phi(resB)             # spectre extrait
    p_inj = peak_positions(inj)
    p_mes = peak_positions(mes)
    print(f"  pics Φ (injecté) : {[f'{c:.0f}c' for c in p_inj]}")
    print(f"  pics Φ (mesuré)  : {[f'{c:.0f}c' for c in p_mes]}")
    if len(p_mes) != len(p_inj) or any(abs(a - b) > 15.0 for a, b in zip(p_inj, p_mes)):
        print("  ÉCHEC : la chaîne déplace les pics Φ de plus de 15 c")
        okB = False
    print(f"  => {'OK' if okB else 'ÉCHEC'}")

    return ok and okB


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
