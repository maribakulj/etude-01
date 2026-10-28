"""
limites.py — limites de la hauteur mélodique (C6) : zone de transposition où
la hauteur virtuelle d'un son reste dans [limite basse ; limite haute].
PHASE1-PROTOCOLE.md §4, C6. Les deux limites sont « à vérifier ».
"""

import numpy as np

from boucle.registre import val
from boucle.oreille.harmonicite import hauteur_virtuelle


def plage_transposition(ratios, amps, f_ref):
    """(t_min, t_max) en cents, relatifs à f_ref, tels que la hauteur virtuelle
    du son (partiels ratios × f_ref × 2^(t/1200)) reste dans les limites.
    La hauteur virtuelle se transpose avec le son (même structure de rangs),
    sauf effet de la limite basse sur les candidats, négligé ici."""
    h, _ = hauteur_virtuelle(np.asarray(ratios) * f_ref, amps)
    return (1200.0 * np.log2(val('LIMITE_BASSE_HZ') / h),
            1200.0 * np.log2(val('LIMITE_HAUTE_HZ') / h))
