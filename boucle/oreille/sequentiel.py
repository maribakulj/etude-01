"""
sequentiel.py — regroupement séquentiel (C7), d'après van Noorden (1975).

Pour deux événements successifs séparés d'un écart de hauteur I (demi-tons)
à la période T (ms, d'une attaque à la suivante) :
  - sous la frontière de fission (≈ 1 demi-ton) : même ligne, obligatoirement ;
  - sous la frontière de cohérence temporelle : même ligne possible ;
  - au-delà : lignes séparées.
Frontière de cohérence pour T > 100 ms : 0,15 × (T − 100) demi-tons ; en
dessous, proche de la frontière de fission. Pour des sons complexes, la
période limite est environ 60 ms plus courte à intervalle égal (p. 73),
d'où T_eff = T + 60 ms.

Données obtenues avec des sons purs (et, p. 73, des sons harmoniques à
spectre plat). Leur application à des sons inharmoniques est une hypothèse
non testée (PHASE1-PROTOCOLE.md, C7).
"""

from boucle.registre import val


def frontiere_fission():
    return val('FISSION_DEMITONS')


def frontiere_coherence(T_ms, complexe=True):
    T = T_ms + (val('DECALAGE_COMPLEXE_MS') if complexe else 0.0)
    return max(frontiere_fission(), val('TCB_PENTE') * (T - val('TCB_GENOU_MS')))


def relation(ecart_cents, T_ms, complexe=True):
    i = abs(ecart_cents) / 100.0
    if i < frontiere_fission():
        return 'meme_ligne'
    if i < frontiere_coherence(T_ms, complexe):
        return 'possible'
    return 'separees'
