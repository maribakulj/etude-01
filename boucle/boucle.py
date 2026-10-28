"""
boucle.py — lanceur de l'étape 1, gardé pour que la commande du protocole
(`python3 boucle/boucle.py`) reste valide. Le code est dans etape1.py.
"""

import os
import sys

if __name__ == '__main__':
    ICI = os.path.dirname(os.path.abspath(__file__))
    # Le dossier du script masquerait le paquet `boucle` : on le retire du chemin.
    sys.path[:] = [p for p in sys.path if os.path.abspath(p or '.') != ICI]
    sys.path.insert(0, os.path.dirname(ICI))
    from boucle.etape1 import main
    main()
