import numpy as np

CENTS = lambda r: 1200.0*np.log2(r)
RATIO = lambda c: 2.0**(c/1200.0)

# ---------------------------------------------------------------------------
# Timbres : liste de (fréquence relative, amplitude)
# ---------------------------------------------------------------------------
def harmonic(n=10):
    k = np.arange(1, n+1)
    return k.astype(float), 1.0/k          # rolloff 1/k

def music_box(n=5):
    # Modes d'une lame encastrée-libre (cantilever) : 1 : 6.267 : 17.55 : 34.39 : 56.84
    modes = np.array([1.0, 6.267, 17.55, 34.39, 56.84])[:n]
    amps  = 1.0/np.sqrt(np.arange(1, len(modes)+1))   # décroissance douce
    return modes, amps

# ---------------------------------------------------------------------------
# C(r) : rugosité (modèle de dissonance de Sethares / Plomp-Levelt)
#   bw_scale module la largeur de bande critique => paramètre "récepteur"
# ---------------------------------------------------------------------------
def sethares_pair(f1, f2, a1, a2, bw_scale=1.0):
    b1, b2 = 3.5, 5.75
    s1, s2, xstar = 0.0207, 18.96, 0.24
    fmin = np.minimum(f1, f2)
    s = xstar/((s1*fmin + s2)*bw_scale)
    df = np.abs(f2 - f1)
    return a1*a2*(np.exp(-b1*s*df) - np.exp(-b2*s*df))

def roughness(spec, r, f0=261.6, bw_scale=1.0):
    fA, aA = spec
    # voix A à f0, voix B = A transposée de r
    F = np.concatenate([fA*f0, fA*f0*r])
    A = np.concatenate([aA, aA])
    tot = 0.0
    for i in range(len(F)):
        for j in range(i+1, len(F)):
            tot += sethares_pair(F[i], F[j], A[i], A[j], bw_scale)
    return tot

# ---------------------------------------------------------------------------
# Phi(r) : fusion = coïncidence spectrale sous transposition
#   (recouvrement de {f_i} avec {r f_j}), noyau gaussien en cents.
#   w = fenêtre de tolérance => paramètre "récepteur".
#   Les PICS (localisation) sont arithmétiques = substrat ;
#   w ne change que leur finesse/hauteur = saillance.
# ---------------------------------------------------------------------------
def fusion(spec, r, w_cents=25.0):
    # Fusion = recouvrement spectral entre la voix A {f_i} et la voix B = {r f_j}.
    # On NE compte une coincidence que si elle vient de partiels DISTINCTS
    # (un partiel de A alignant un partiel de B). Le terme i=j à r=1
    # (partiel alignant sa propre copie) est trivial : deux voix a l'unisson
    # ne fusionnent pas, elles SONT la meme note. On l'exclut.
    f, a = spec
    fa = f[:,None]; fb = r*f[None,:]
    ab = a[:,None]*a[None,:]
    d  = 1200.0*np.log2(fa/fb)                  # ecart en cents A_i vs B_j
    K  = np.exp(-(d/w_cents)**2)
    same = (np.abs(d) < 1e-6) & (np.arange(len(f))[:,None]==np.arange(len(f))[None,:])
    K = np.where(same, 0.0, K)                  # retire la self-coincidence i=j
    return np.sum(ab*K)

# ---------------------------------------------------------------------------
# Balayage sur une octave (unisson -> octave), résolution fine
# ---------------------------------------------------------------------------
cents = np.linspace(1, 1200, 1200)
rs = RATIO(cents)

JUST = {  # repères d'intervalles justes (cents)
 'm2':111.7,'M2':203.9,'m3':315.6,'M3':386.3,'P4':498.0,'TT':590.2,
 'P5':702.0,'m6':813.7,'M6':884.4,'m7':1017.6,'M7':1088.3,'P8':1200.0}

def peaks(curve, x, n=6, min_sep=40, x_floor=100.0):
    # x_floor : on ignore la zone de quasi-unisson (< seconde mineure ~100c).
    # La fusion y est maximale (sons tres proches) mais ce n'est pas le domaine
    # de R2 : l'unisson et les micro-intervalles sont exclus en amont du
    # contrepoint (ecart minimal entre voix, pas de croisement). R2 gouverne
    # le mouvement PARALLELE entre intervalles >= seconde.
    idx = np.argsort(curve)[::-1]
    chosen=[]
    for i in idx:
        if x[i] < x_floor:
            continue
        if all(abs(x[i]-x[j])>min_sep for j in chosen):
            chosen.append(i)
        if len(chosen)>=n: break
    return sorted(chosen, key=lambda i:-curve[i])

def nearest_interval(c):
    name=min(JUST, key=lambda k:abs(JUST[k]-c)); return name, JUST[name], c-JUST[name]

def report(spec, label, bw=1.0, w=25.0):
    C = np.array([-roughness(spec, r, bw_scale=bw) for r in rs])  # consonance = -rugosité
    P = np.array([ fusion(spec, r, w_cents=w)       for r in rs])
    print(f"\n=== {label} ===")
    print("  Pics de FUSION Phi (=> intervalle de 'parallèles interdits' par R2) :")
    for i in peaks(P, cents):
        nm,jc,dev = nearest_interval(cents[i])
        print(f"    {cents[i]:7.1f} cents  ~ {nm:3s} (just {jc:6.1f}, écart {dev:+5.1f})   Phi={P[i]:.3f}")
    print("  Pics de CONSONANCE C (=> intervalles verticaux admis, gate R1) :")
    Cn = (C-C.min())/(C.max()-C.min())
    for i in peaks(Cn, cents):
        nm,jc,dev = nearest_interval(cents[i])
        print(f"    {cents[i]:7.1f} cents  ~ {nm:3s} (just {jc:6.1f}, écart {dev:+5.1f})")
    return C, P

Ch, Ph = report(harmonic(),  "HARMONIQUE  (recepteur humain)")
Cb, Pb = report(music_box(), "BOITE A MUSIQUE  (recepteur humain)")

# ---------------------------------------------------------------------------
# P6 : substrat vs saillance. Change le 'recepteur' (bande critique) et regarde
#   si les PICS de Phi bougent (ils ne devraient pas) vs la consonance (devrait bouger)
# ---------------------------------------------------------------------------
print("\n\n########## P6 : substrat (Phi) vs saillance (C) selon le recepteur ##########")
def peak_locs(curve, n=4):
    return sorted([cents[i] for i in peaks(curve, cents, n=n)])

for bw,w,tag in [(1.0,25.0,"recepteur HUMAIN (bande std)"),
                 (0.35,8.0,"recepteur type FOVEA (bande etroite, haute resolution)")]:
    C = np.array([-roughness(harmonic(), r, bw_scale=bw) for r in rs])
    P = np.array([ fusion(harmonic(), r, w_cents=w)       for r in rs])
    Cn=(C-C.min())/(C.max()-C.min())
    print(f"\n  [{tag}]")
    print(f"    pics CONSONANCE C : {[f'{c:.0f}' for c in peak_locs(Cn)]}")
    print(f"    pics FUSION   Phi : {[f'{c:.0f}' for c in peak_locs(P)]}")
