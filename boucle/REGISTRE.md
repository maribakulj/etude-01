# Registre des paramètres

*Généré par `python3 boucle/registre.py` à partir de `boucle/registre.py`. Ne pas modifier à la main.*

## Son

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `TAU_CLOCHE_S` | 0.524 | constante de décroissance (s) de l'amplitude de la cloche Westerkerk (bourdon 12-c1), utilisée pour les deux spectres de cette cloche | mesurée : boucle/mesures/cloche_12c1_decroissance.json (T60 = 3,62 s, Schroeder −5 à −25 dB) |
| `F_REF_CLOCHE_HZ` | 544.8 | fréquence (Hz) de la prime de la cloche, pour t = 0 | notre extraction de 12-c1.wav, materiau/cloche_westerkerk_12c1_extraction.json |
| `F_REF_DENT994_HZ` | 993.8 | fréquence (Hz) de la dent mesurée, pour t = 0 | materiau/dent994.json |

## Oreille (données publiées)

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `SIGMA_MILNE` | 6.83 | tolérance (cents) du noyau de coïncidence entre partiels | Milne (2013) ; valeur par défaut du paquet hrep de Harrison. Ajustée sur des données d'affinité mélodique, pas de fusion (DECISION-PHI.md §5); test : `test_oreille.py::test_coincidence_egale_phi_publiee` |
| `ERB_A` | 24.7 | ERB(f) = A × (B f/1000 + 1) : constante A (Hz) | Glasberg & Moore (1990), Hearing Research 47, 103-138 (formule confirmée par des implémentations publiques ; texte à vérifier); test : `test_oreille.py::test_erb` |
| `ERB_B` | 4.37 | ERB : constante B | idem ERB_A; test : `test_oreille.py::test_erb` |
| `BC_ZWICKER` | (25.0, 75.0, 1.4, 0.69) | bande critique (Hz) = c0 + c1 (1 + c2 (f/1000)²)^e, utilisée pour situer le maximum de rugosité (C2) | Zwicker & Terhardt (1980), JASA 68 — de mémoire, à vérifier; test : `test_oreille.py::test_rugosite_maximum_quart_de_bande` |
| `DELTA_HARMONICITE` | 0.02 | écart relatif sous lequel un partiel est expliqué par un harmonique (C4, C5) | Moore, Glasberg & Peters (1986), JASA 80(2) : seuils de 1 à 3 % selon les auditeurs (résumé lu) ; milieu de la plage; test : `test_oreille.py::test_harmonique_desaccorde`; sensibilité : faite pour C5 (PHASE1-RESULTATS.md §3) : à 1 %, le test de décalage de hauteur passe ; à 2 et 3 %, il échoue |
| `LIMITE_BASSE_HZ` | 30.0 | limite basse de la hauteur mélodique (C5, C6) | Pressnitzer, Patterson & Krumbholz (2001), JASA 109 — résumé via source secondaire, à vérifier; test : `test_oreille.py::test_plage_transposition` |
| `LIMITE_HAUTE_HZ` | 4700.0 | limite haute de la hauteur mélodique, sons purs (C6) | Semal & Demany (1990), Music Perception 8(2) — résumé, à vérifier ; contestée pour les sons complexes (Oxenham et al. 2011, à vérifier); test : `test_oreille.py::test_plage_transposition` |
| `FISSION_DEMITONS` | 1.0 | frontière de fission (demi-tons), T entre 0,1 et 0,4 s (C7) | van Noorden (1975), thèse TH Eindhoven, p. 15 (lue); test : `test_oreille.py::test_frontieres_van_noorden` |
| `TCB_PENTE` | 0.15 | pente de la frontière de cohérence (demi-tons par ms) (C7) | van Noorden (1975), p. 16 : Ic = 0,15 (T − 100) (lue); test : `test_oreille.py::test_frontieres_van_noorden` |
| `TCB_GENOU_MS` | 100.0 | période (ms) du coude de la frontière de cohérence (C7) | van Noorden (1975), p. 15-16 (lue); test : `test_oreille.py::test_frontieres_van_noorden` |
| `DECALAGE_COMPLEXE_MS` | 60.0 | décalage de période (ms) pour des sons complexes (C7) | van Noorden (1975), p. 73 : sons harmoniques à spectre plat (lue); test : `test_oreille.py::test_frontieres_van_noorden` |
| `LIGNE_FERMETURE_MS` | 200.0 | au-delà de cette période (ms), une ligne est close : c'est la borne haute de la plage où la frontière de cohérence a été mesurée | van Noorden (1975), p. 14 : mesures pour 48 ≤ T ≤ 200 ms (lue); test : `test_phase2.py::test_lignes_van_noorden` |
| `EXCLUSION_ERB` | 1.0 | une candidate est exclue si son partiel dominant est à moins de ce nombre d'ERB de celui d'une copie active (non résolue) | Plomp (1964), JASA 36, résolution des partiels — à vérifier ; ERB de C1; test : `test_phase2.py::test_exclusion_erb`; sensibilité : 0,5 et 1,5 ERB (PHASE2-PROTOCOLE.md §4) |

## Choix techniques

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `PERIODES_MS` | (100.0, 150.0, 200.0) | périodes T entre événements (réglage varié) | sensibilité : influence mesurée par R (phase 2) ; bornes dans la plage de van Noorden |
| `TAUS_SYNTH_S` | (0.5, 1.5) | persistance (s) des sons sans décroissance mesurée | sensibilité : influence mesurée par R (phase 2) |
| `F_REF_SYNTH_HZ` | 220.0 | fréquence (Hz) de t = 0 pour les sons synthétiques | sensibilité : à faire (phase 3) |
| `EXEMPLES_ECOUTE_PHASE2` | (('harm', 150.0), ('harm', 200.0), ('cloche', 150.0), ('cloche', 200.0), ('cloche12c1', 200.0), ('aleatoire', 200.0)) | trajectoires rendues en audio pour l'écoute (règle argmax, τ le plus court) | sensibilité : sans effet sur les verdicts : sélection d'exemples d'écoute |
| `W_MIN_SENS` | (0.01, 0.1) | valeurs de sensibilité pour W_MIN (phase 2) | sensibilité : c'est elle-même une analyse de sensibilité |
| `BIN_INTERVALLES_ETENDUS` | 9600.0 | étendue (± cents) des histogrammes d'intervalles en phase 2, le registre étant plus large qu'à l'étape 1 | sensibilité : sans effet tant qu'aucun intervalle ne dépasse la borne (vérifié au calcul) |
| `K_HARMONIQUES` | 16 | rang harmonique maximal considéré par la hauteur virtuelle (C4, C5) ; même valeur que le gabarit de Parncutt déjà utilisé (_HMAX) | sensibilité : faite pour C5 (PHASE1-RESULTATS.md §3) : 10, 16, 20 ; sans effet sur le verdict |
| `EGALITE_PART` | 1e-09 | tolérance d'égalité entre parts d'amplitude expliquées (C5) | sensibilité : à faire (phase 2) |
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
| `MESURE_BRUIT_S` | 2.0 | durée (s) de fin d'enregistrement servant à estimer le bruit de fond (mesure de décroissance) | sensibilité : rapportée dans boucle/mesures/cloche_12c1_decroissance.json |
| `MESURE_LISSAGE_S` | 0.05 | lissage (s) de l'enveloppe pour arrêter l'intégration | sensibilité : rapportée dans boucle/mesures/cloche_12c1_decroissance.json |
| `MESURE_FACTEUR_BRUIT` | 2.0 | l'intégration s'arrête quand l'enveloppe vaut ce facteur × bruit | sensibilité : rapportée dans boucle/mesures/cloche_12c1_decroissance.json |
| `W_MIN` | 0.05 | poids sous lequel une copie est retirée | sensibilité : 0,01 et 0,1 (PHASE2-PROTOCOLE.md §2) ; aucune donnée de masquage établie, donc pas de remplacement |

## Hérités de l'étape 1, à remplacer

| Paramètre | Valeur | Rôle | Provenance / sensibilité |
|---|---|---|---|
| `T_MIN` | -1200.0 | borne basse (cents) du registre | à remplacer par : région d'existence de la hauteur pour ce son (phase 1) |
| `T_MAX` | 2400.0 | borne haute (cents) du registre | à remplacer par : région d'existence de la hauteur pour ce son (phase 1) |
| `EXCLUSION` | 100.0 | zone (cents) exclue autour d'une copie active | à remplacer par : seuil de distinction de deux sons simultanés, tiré de données de discrimination et de fusion (phase 1) |
| `TAUS` | (1.5, 4.0) | persistance des copies (en pas) | à remplacer par : durée de résonance mesurée du son de départ (phase 2) |
| `DUREE_PAS` | 0.45 | durée (s) d'un pas au rendu | à remplacer par : moment d'un nouvel événement dépendant du son et de l'oreille (phase 2, PLAN.md §4) |
| `F0_RENDU` | 220.0 | fréquence (Hz) de t = 0 au rendu | à remplacer par : fréquence mesurée du son de départ |

Restent : 6 paramètres à remplacer, 17 analyses de sensibilité à faire.
