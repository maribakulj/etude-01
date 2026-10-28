# Registre des paramètres

*Généré par `python3 boucle/registre.py` à partir de `boucle/registre.py`. Ne pas modifier à la main.*

## Oreille (données publiées)

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `SIGMA_MILNE` | 6.83 | tolérance (cents) du noyau de coïncidence entre partiels | Milne (2013) ; valeur par défaut du paquet hrep de Harrison. Ajustée sur des données d'affinité mélodique, pas de fusion (DECISION-PHI.md §5); test : `test_oreille.py::test_coincidence_egale_phi_publiee` |

## Choix techniques

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `PAS_GRILLE` | 2.0 | pas (cents) de la grille des transpositions candidates | sensibilité : à faire (phase 2) ; les maxima sont affinés par interpolation parabolique |
| `EGALITE` | 1e-09 | tolérance numérique pour déclarer deux maxima égaux | sensibilité : à faire (phase 2) |
| `N_PAS` | 48 | nombre de pas d'une trajectoire (durée d'observation) | sensibilité : à faire (phase 2) |
| `SIGMA_LARGE` | 15.0 | variante large de la tolérance, utilisée comme réglage | sensibilité : influence mesurée par R (étape 1, RESULTATS.md) |
| `EXPOSANT_TIRAGE` | 4 | règle `tirage` : probabilité ∝ hauteur du maximum ^ exposant | sensibilité : influence de la règle mesurée par R (étape 1) ; exposant lui-même : à faire (phase 2) |
| `GRAINES_TIRAGE` | (1, 2, 3) | graines de la règle `tirage` | sensibilité : influence mesurée par R (étape 1) |
| `GRAINE_ALEATOIRE` | 0 | graine du son de contrôle `aleatoire` et des permutations | sensibilité : à faire (phase 2) |
| `ALEATOIRE_N` | 10 | nombre de partiels du son de contrôle `aleatoire` | sensibilité : à faire (phase 2) |
| `ALEATOIRE_RAPPORT_MAX` | 8.0 | rapport maximal des partiels du son `aleatoire` | sensibilité : à faire (phase 2) |
| `BIN_INTERVALLES` | 50.0 | largeur (cents) des classes d'intervalles mélodiques | sensibilité : à faire (phase 2) |
| `BIN_POSITIONS` | 25.0 | largeur (cents) des classes de positions modulo l'octave | sensibilité : à faire (phase 2) |
| `N_PERMUTATIONS` | 1000 | permutations du test de R | sensibilité : précision de p : ±0,001 environ |
| `TRIVIAL_FENETRE` | 24 | pas finaux examinés pour la périodicité (PROTOCOLE.md §5) | sensibilité : à faire (phase 2) |
| `TRIVIAL_PERIODE_MAX` | 4 | période maximale testée | sensibilité : à faire (phase 2) |
| `TRIVIAL_TOL_PERIODE` | 5.0 | tolérance (cents) de la périodicité | sensibilité : à faire (phase 2) |
| `TRIVIAL_TOL_DOMINANT` | 10.0 | tolérance (cents) de l'intervalle dominant | sensibilité : à faire (phase 2) |
| `TRIVIAL_PART` | 0.8 | part à partir de laquelle un intervalle domine | sensibilité : à faire (phase 2) |
| `DOMINANT_TOL` | 15.0 | tolérance (cents) pour compter l'intervalle dominant (B2) | sensibilité : à faire (phase 2) |
| `SR_RENDU` | 22050 | fréquence d'échantillonnage du rendu audio | sensibilité : sans effet sur les trajectoires ; partiels au-dessus de 0,45×SR omis |
| `ATTAQUE_RENDU` | 0.005 | attaque (s) d'une copie au rendu, anti-clic | sensibilité : sans effet sur les trajectoires |
| `FONDU_RENDU` | 0.03 | fondu (s) à l'arrêt d'une copie au rendu, anti-clic | sensibilité : sans effet sur les trajectoires |

## Hérités de l'étape 1, à remplacer

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `T_MIN` | -1200.0 | borne basse (cents) du registre | à remplacer par : région d'existence de la hauteur pour ce son (phase 1) |
| `T_MAX` | 2400.0 | borne haute (cents) du registre | à remplacer par : région d'existence de la hauteur pour ce son (phase 1) |
| `EXCLUSION` | 100.0 | zone (cents) exclue autour d'une copie active | à remplacer par : seuil de distinction de deux sons simultanés, tiré de données de discrimination et de fusion (phase 1) |
| `W_MIN` | 0.05 | poids sous lequel une copie est retirée | à remplacer par : seuil d'audibilité dans le mélange (masquage, phase 1) |
| `TAUS` | (1.5, 4.0) | persistance des copies (en pas) | à remplacer par : durée de résonance mesurée du son de départ (phase 2) |
| `DUREE_PAS` | 0.45 | durée (s) d'un pas au rendu | à remplacer par : moment d'un nouvel événement dépendant du son et de l'oreille (phase 2, PLAN.md §4) |
| `F0_RENDU` | 220.0 | fréquence (Hz) de t = 0 au rendu | à remplacer par : fréquence mesurée du son de départ |

Restent : 7 paramètres à remplacer, 15 analyses de sensibilité à faire.
