"""
erb.py — largeur des filtres auditifs (C1) et bande critique de Zwicker (pour C2).

PHASE1-PROTOCOLE.md §4, C1 et C2. Constantes dans boucle/registre.py.
"""

from boucle.registre import val


def erb(f):
    """ERB (Hz) à la fréquence f (Hz) [GM90]."""
    a, b = val('ERB_A'), val('ERB_B')
    return a * (b * f / 1000.0 + 1.0)


def bande_critique(f):
    """Bande critique (Hz) à la fréquence f (Hz) [ZT80, à vérifier]."""
    c0, c1, c2, e = val('BC_ZWICKER')
    return c0 + c1 * (1.0 + c2 * (f / 1000.0) ** 2) ** e
