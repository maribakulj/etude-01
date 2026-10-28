"""
registre.py — la provenance de chaque paramètre de la boucle (PLAN.md §2.4).

Tout nombre qui intervient dans la modélisation est défini ici, et nulle part
ailleurs dans le paquet `boucle`. Chaque entrée porte sa source :

  'son'         mesuré ou publié sur le son lui-même ;
  'oreille'     donnée psychoacoustique publiée, reproduite par un test ;
  'consigne'    but déclaré comme un choix ;
  'technique'   choix inévitable, avec analyse de sensibilité (faite ou
                prévue, et dans ce cas marquée « à faire ») ;
  'a_remplacer' choix arbitraire hérité de l'étape 1, à remplacer par une
                valeur issue du son ou de l'oreille (PLAN.md §3).

Les tests de `boucle/tests/test_registre.py` vérifient ces exigences.
`python3 boucle/registre.py` régénère `boucle/REGISTRE.md`.
"""

import os
from dataclasses import dataclass

SOURCES = ('son', 'oreille', 'consigne', 'technique', 'a_remplacer')


@dataclass(frozen=True)
class Param:
    valeur: object
    source: str
    description: str
    reference: str = ''
    test: str = ''           # test qui reproduit la donnée (source 'oreille')
    sensibilite: str = ''    # analyse faite, ou « à faire (phase N) »
    remplacement: str = ''   # pour 'a_remplacer' : ce qui doit le remplacer


PARAMS = {
    # --- Son ----------------------------------------------------------------
    'TAU_CLOCHE_S': Param(
        0.524, 'son', "constante de décroissance (s) de l'amplitude de la cloche "
        "Westerkerk (bourdon 12-c1), utilisée pour les deux spectres de cette cloche",
        reference="mesurée : boucle/mesures/cloche_12c1_decroissance.json "
                  "(T60 = 3,62 s, Schroeder −5 à −25 dB)"),
    'F_REF_CLOCHE_HZ': Param(
        544.8, 'son', "fréquence (Hz) de la prime de la cloche, pour t = 0",
        reference="notre extraction de 12-c1.wav, materiau/cloche_westerkerk_12c1_extraction.json"),
    'F_REF_DENT994_HZ': Param(
        993.8, 'son', "fréquence (Hz) de la dent mesurée, pour t = 0",
        reference="materiau/dent994.json"),

    # --- Oreille ------------------------------------------------------------
    'SIGMA_MILNE': Param(
        6.83, 'oreille',
        "tolérance (cents) du noyau de coïncidence entre partiels",
        reference="Milne (2013) ; valeur par défaut du paquet hrep de Harrison. "
                  "Ajustée sur des données d'affinité mélodique, pas de fusion "
                  "(DECISION-PHI.md §5)",
        test='test_oreille.py::test_coincidence_egale_phi_publiee'),

    'ERB_A': Param(
        24.7, 'oreille', "ERB(f) = A × (B f/1000 + 1) : constante A (Hz)",
        reference="Glasberg & Moore (1990), Hearing Research 47, 103-138 "
                  "(formule confirmée par des implémentations publiques ; texte à vérifier)",
        test='test_oreille.py::test_erb'),
    'ERB_B': Param(
        4.37, 'oreille', "ERB : constante B", reference="idem ERB_A",
        test='test_oreille.py::test_erb'),
    'BC_ZWICKER': Param(
        (25.0, 75.0, 1.4, 0.69), 'oreille',
        "bande critique (Hz) = c0 + c1 (1 + c2 (f/1000)²)^e, utilisée pour situer "
        "le maximum de rugosité (C2)",
        reference="Zwicker & Terhardt (1980), JASA 68 — de mémoire, à vérifier",
        test='test_oreille.py::test_rugosite_maximum_quart_de_bande'),
    'DELTA_HARMONICITE': Param(
        0.02, 'oreille', "écart relatif sous lequel un partiel est expliqué par un "
        "harmonique (C4, C5)",
        reference="Moore, Glasberg & Peters (1986), JASA 80(2) : seuils de 1 à 3 % "
                  "selon les auditeurs (résumé lu) ; milieu de la plage",
        test='test_oreille.py::test_harmonique_desaccorde',
        sensibilite="faite pour C5 (PHASE1-RESULTATS.md §3) : à 1 %, le test de "
                    "décalage de hauteur passe ; à 2 et 3 %, il échoue"),
    'LIMITE_BASSE_HZ': Param(
        30.0, 'oreille', "limite basse de la hauteur mélodique (C5, C6)",
        reference="Pressnitzer, Patterson & Krumbholz (2001), JASA 109 — résumé "
                  "via source secondaire, à vérifier",
        test='test_oreille.py::test_plage_transposition'),
    'LIMITE_HAUTE_HZ': Param(
        4700.0, 'oreille', "limite haute de la hauteur mélodique, sons purs (C6)",
        reference="Semal & Demany (1990), Music Perception 8(2) — résumé, à vérifier ; "
                  "contestée pour les sons complexes (Oxenham et al. 2011, à vérifier)",
        test='test_oreille.py::test_plage_transposition'),
    'FISSION_DEMITONS': Param(
        1.0, 'oreille', "frontière de fission (demi-tons), T entre 0,1 et 0,4 s (C7)",
        reference="van Noorden (1975), thèse TH Eindhoven, p. 15 (lue)",
        test='test_oreille.py::test_frontieres_van_noorden'),
    'TCB_PENTE': Param(
        0.15, 'oreille', "pente de la frontière de cohérence (demi-tons par ms) (C7)",
        reference="van Noorden (1975), p. 16 : Ic = 0,15 (T − 100) (lue)",
        test='test_oreille.py::test_frontieres_van_noorden'),
    'TCB_GENOU_MS': Param(
        100.0, 'oreille', "période (ms) du coude de la frontière de cohérence (C7)",
        reference="van Noorden (1975), p. 15-16 (lue)",
        test='test_oreille.py::test_frontieres_van_noorden'),
    'DECALAGE_COMPLEXE_MS': Param(
        60.0, 'oreille', "décalage de période (ms) pour des sons complexes (C7)",
        reference="van Noorden (1975), p. 73 : sons harmoniques à spectre plat (lue)",
        test='test_oreille.py::test_frontieres_van_noorden'),

    'LIGNE_FERMETURE_MS': Param(
        200.0, 'oreille', "au-delà de cette période (ms), une ligne est close : "
        "c'est la borne haute de la plage où la frontière de cohérence a été mesurée",
        reference="van Noorden (1975), p. 14 : mesures pour 48 ≤ T ≤ 200 ms (lue)",
        test='test_phase2.py::test_lignes_van_noorden'),
    'EXCLUSION_ERB': Param(
        1.0, 'oreille', "une candidate est exclue si son partiel dominant est à moins "
        "de ce nombre d'ERB de celui d'une copie active (non résolue)",
        reference="Plomp (1964), JASA 36, résolution des partiels — à vérifier ; ERB de C1",
        test='test_phase2.py::test_exclusion_erb',
        sensibilite="0,5 et 1,5 ERB (PHASE2-PROTOCOLE.md §4)"),

    # --- Choix techniques ---------------------------------------------------
    'PERIODES_MS': Param(
        (100.0, 150.0, 200.0), 'technique', "périodes T entre événements (réglage varié)",
        sensibilite="influence mesurée par R (phase 2) ; bornes dans la plage de van Noorden"),
    'TAUS_SYNTH_S': Param(
        (0.5, 1.5), 'technique', "persistance (s) des sons sans décroissance mesurée",
        sensibilite="influence mesurée par R (phase 2)"),
    'F_REF_SYNTH_HZ': Param(
        220.0, 'technique', "fréquence (Hz) de t = 0 pour les sons synthétiques",
        sensibilite="à faire (phase 3)"),
    'W_MIN_SENS': Param(
        (0.01, 0.1), 'technique', "valeurs de sensibilité pour W_MIN (phase 2)",
        sensibilite="c'est elle-même une analyse de sensibilité"),
    'BIN_INTERVALLES_ETENDUS': Param(
        9600.0, 'technique', "étendue (± cents) des histogrammes d'intervalles en phase 2, "
        "le registre étant plus large qu'à l'étape 1",
        sensibilite="sans effet tant qu'aucun intervalle ne dépasse la borne (vérifié au calcul)"),
    'K_HARMONIQUES': Param(
        16, 'technique', "rang harmonique maximal considéré par la hauteur virtuelle "
        "(C4, C5) ; même valeur que le gabarit de Parncutt déjà utilisé (_HMAX)",
        sensibilite="faite pour C5 (PHASE1-RESULTATS.md §3) : 10, 16, 20 ; "
                    "sans effet sur le verdict"),
    'EGALITE_PART': Param(
        1e-9, 'technique', "tolérance d'égalité entre parts d'amplitude expliquées (C5)",
        sensibilite="à faire (phase 2)"),
    'PAS_GRILLE': Param(
        2.0, 'technique', "pas (cents) de la grille des transpositions candidates",
        sensibilite="à faire (phase 2) ; les maxima sont affinés par "
                    "interpolation parabolique"),
    'EGALITE': Param(
        1e-9, 'technique', "tolérance numérique pour déclarer deux maxima égaux",
        sensibilite="à faire (phase 2)"),
    'N_PAS': Param(
        48, 'technique', "nombre de pas d'une trajectoire (durée d'observation)",
        sensibilite="à faire (phase 2)"),
    'SIGMA_LARGE': Param(
        15.0, 'technique', "variante large de la tolérance, utilisée comme réglage",
        sensibilite="influence mesurée par R (étape 1, RESULTATS.md)"),
    'EXPOSANT_TIRAGE': Param(
        4, 'technique', "règle `tirage` : probabilité ∝ hauteur du maximum ^ exposant",
        sensibilite="influence de la règle mesurée par R (étape 1) ; "
                    "exposant lui-même : à faire (phase 2)"),
    'GRAINES_TIRAGE': Param(
        (1, 2, 3), 'technique', "graines de la règle `tirage`",
        sensibilite="influence mesurée par R (étape 1)"),
    'GRAINE_ALEATOIRE': Param(
        0, 'technique', "graine du son de contrôle `aleatoire` et des permutations",
        sensibilite="à faire (phase 2)"),
    'ALEATOIRE_N': Param(
        10, 'technique', "nombre de partiels du son de contrôle `aleatoire`",
        sensibilite="à faire (phase 2)"),
    'ALEATOIRE_RAPPORT_MAX': Param(
        8.0, 'technique', "rapport maximal des partiels du son `aleatoire`",
        sensibilite="à faire (phase 2)"),
    'BIN_INTERVALLES': Param(
        50.0, 'technique', "largeur (cents) des classes d'intervalles mélodiques",
        sensibilite="à faire (phase 2)"),
    'BIN_POSITIONS': Param(
        25.0, 'technique', "largeur (cents) des classes de positions modulo l'octave",
        sensibilite="à faire (phase 2)"),
    'N_PERMUTATIONS': Param(
        1000, 'technique', "permutations du test de R",
        sensibilite="précision de p : ±0,001 environ"),
    'TRIVIAL_FENETRE': Param(
        24, 'technique', "pas finaux examinés pour la périodicité (PROTOCOLE.md §5)",
        sensibilite="à faire (phase 2)"),
    'TRIVIAL_PERIODE_MAX': Param(
        4, 'technique', "période maximale testée", sensibilite="à faire (phase 2)"),
    'TRIVIAL_TOL_PERIODE': Param(
        5.0, 'technique', "tolérance (cents) de la périodicité", sensibilite="à faire (phase 2)"),
    'TRIVIAL_TOL_DOMINANT': Param(
        10.0, 'technique', "tolérance (cents) de l'intervalle dominant", sensibilite="à faire (phase 2)"),
    'TRIVIAL_PART': Param(
        0.8, 'technique', "part à partir de laquelle un intervalle domine", sensibilite="à faire (phase 2)"),
    'DOMINANT_TOL': Param(
        15.0, 'technique', "tolérance (cents) pour compter l'intervalle dominant (B2)",
        sensibilite="à faire (phase 2)"),
    'SR_RENDU': Param(
        22050, 'technique', "fréquence d'échantillonnage du rendu audio",
        sensibilite="sans effet sur les trajectoires ; partiels au-dessus de 0,45×SR omis"),
    'ATTAQUE_RENDU': Param(
        0.005, 'technique', "attaque (s) d'une copie au rendu, anti-clic",
        sensibilite="sans effet sur les trajectoires"),
    'FONDU_RENDU': Param(
        0.03, 'technique', "fondu (s) à l'arrêt d'une copie au rendu, anti-clic",
        sensibilite="sans effet sur les trajectoires"),

    'MESURE_BRUIT_S': Param(
        2.0, 'technique', "durée (s) de fin d'enregistrement servant à estimer le bruit "
        "de fond (mesure de décroissance)",
        sensibilite="rapportée dans boucle/mesures/cloche_12c1_decroissance.json"),
    'MESURE_LISSAGE_S': Param(
        0.05, 'technique', "lissage (s) de l'enveloppe pour arrêter l'intégration",
        sensibilite="rapportée dans boucle/mesures/cloche_12c1_decroissance.json"),
    'MESURE_FACTEUR_BRUIT': Param(
        2.0, 'technique', "l'intégration s'arrête quand l'enveloppe vaut ce facteur × bruit",
        sensibilite="rapportée dans boucle/mesures/cloche_12c1_decroissance.json"),

    # --- Hérités de l'étape 1, à remplacer (PLAN.md §3) ----------------------
    'T_MIN': Param(
        -1200.0, 'a_remplacer', "borne basse (cents) du registre",
        remplacement="région d'existence de la hauteur pour ce son (phase 1)"),
    'T_MAX': Param(
        2400.0, 'a_remplacer', "borne haute (cents) du registre",
        remplacement="région d'existence de la hauteur pour ce son (phase 1)"),
    'EXCLUSION': Param(
        100.0, 'a_remplacer', "zone (cents) exclue autour d'une copie active",
        remplacement="seuil de distinction de deux sons simultanés, tiré de "
                     "données de discrimination et de fusion (phase 1)"),
    'W_MIN': Param(
        0.05, 'technique', "poids sous lequel une copie est retirée",
        sensibilite="0,01 et 0,1 (PHASE2-PROTOCOLE.md §2) ; aucune donnée de masquage "
                    "établie, donc pas de remplacement"),
    'TAUS': Param(
        (1.5, 4.0), 'a_remplacer', "persistance des copies (en pas)",
        remplacement="durée de résonance mesurée du son de départ (phase 2)"),
    'DUREE_PAS': Param(
        0.45, 'a_remplacer', "durée (s) d'un pas au rendu",
        remplacement="moment d'un nouvel événement dépendant du son et de "
                     "l'oreille (phase 2, PLAN.md §4)"),
    'F0_RENDU': Param(
        220.0, 'a_remplacer', "fréquence (Hz) de t = 0 au rendu",
        remplacement="fréquence mesurée du son de départ"),
}


def val(nom):
    return PARAMS[nom].valeur


def en_markdown():
    lignes = ["# Registre des paramètres",
              "",
              "*Généré par `python3 boucle/registre.py` à partir de "
              "`boucle/registre.py`. Ne pas modifier à la main.*",
              ""]
    titres = {'son': 'Son', 'oreille': 'Oreille (données publiées)',
              'consigne': 'Consigne déclarée', 'technique': 'Choix techniques',
              'a_remplacer': "Hérités de l'étape 1, à remplacer"}
    for src in SOURCES:
        items = [(n, p) for n, p in PARAMS.items() if p.source == src]
        if not items:
            continue
        lignes += [f"## {titres[src]}", "",
                   "| Paramètre | Valeur | Rôle | Provenance / sensibilité |",
                   "|---|---|---|---|"]
        for n, p in items:
            prov = '; '.join(x for x in (p.reference, p.test and f"test : `{p.test}`",
                                         p.sensibilite and f"sensibilité : {p.sensibilite}",
                                         p.remplacement and f"à remplacer par : {p.remplacement}")
                             if x)
            lignes.append(f"| `{n}` | {p.valeur} | {p.description} | {prov} |")
        lignes.append("")
    a_faire = sum('à faire' in p.sensibilite for p in PARAMS.values())
    a_rempl = sum(p.source == 'a_remplacer' for p in PARAMS.values())
    lignes += [f"Restent : {a_rempl} paramètres à remplacer, "
               f"{a_faire} analyses de sensibilité à faire.", ""]
    return '\n'.join(lignes)


if __name__ == '__main__':
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'REGISTRE.md')
    with open(chemin, 'w') as fh:
        fh.write(en_markdown())
    print(f'Écrit : {chemin}')
