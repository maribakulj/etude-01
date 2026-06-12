# PASSATION — état du projet au moment de basculer vers le dépôt

*À lire en premier par toute instance qui reprend le travail. Résume où on en est, ce qui est établi, ce qui est encore une esquisse, et dans quel ordre avancer. Les trois autres documents (CADRAGE-v2, SPEC-v1) sont le contrat ; celui-ci est l'état d'avancement.*

---

## En une phrase

Système qui dérive du spectre d'un objet sonore une **grammaire contrapuntique** (règles de mouvement entre voix), en traitant ces règles comme des **règles de sélection** sur les coïncidences spectrales. Un premier test exploratoire confirme les trois prédictions enregistrées ; il reste à remplacer deux pièces « esquisse » par des pièces solides.

---

## Documents du dépôt (ordre de lecture)
1. `CADRAGE-v2.md` — le pourquoi : question, état de l'art, mécanisme (règles de sélection sur quasicristal spectral), substrat vs saillance, différenciateur vs systèmes génératifs.
2. `SPEC-v1-graphe-grammaire.md` — le quoi : les deux scalaires `C`/`Φ`, états et arêtes du graphe, gabarits de règles R1/R2/R3/R5, **prédictions P2/P5/P6 enregistrées avant calcul**, critères d'abandon.
3. `PASSATION.md` (ce fichier) — où on en est.
4. `test_noyau.py` + `plot_test.py` — le noyau de test jetable qui a produit le premier fait.

---

## Ce qui est ÉTABLI (premier test, prédictions tenues)

Test exploratoire exécuté. Les trois prédictions de la spec §5 sont confirmées :

- **P2 — validation sur le cas connu.** Sur timbre harmonique + récepteur humain, les pics de fusion `Φ` tombent sur octave (1200c), quinte (702c), quarte (498c) — exactement les consonances parfaites. La règle de sélection R2 y interdit le mouvement parallèle → **on retrouve l'interdiction des quintes/octaves parallèles à partir du seul spectre.** Le décompilateur reproduit Fux sur le connu.
- **P5 — la thèse forte.** Sur la boîte à musique (modes de cantilever 1 : 6.27 : 17.55 : …), les pics de fusion se déplacent : octave comprimée à 1165c, second pic à 870c, quinte disparue. **L'intervalle de "parallèles interdits" change avec le timbre → le contrepoint est timbre-dépendant au niveau du mouvement.**
- **P6 — substrat vs saillance.** En changeant le récepteur (bande critique), les pics de `Φ` (fusion) restent fixes tandis que les pics de `C` (consonance/rugosité) bougent. **La fusion est arithmétique (dans le signal) ; la rugosité dépend de l'oreille.** La séparation est visible dans les chiffres.

Aucun critère d'abandon de la spec §6 ne s'est déclenché. Le palier scientifique fort tient.

Robustesse : les résultats QUALITATIFS (les pics se déplacent avec le timbre ; la fusion est invariante par récepteur) sont arithmétiques et survivraient à un changement des constantes. C'est le socle fiable.

---

## Ce qui est encore ESQUISSE (à remplacer — chemin critique)

⚠️ **Ne pas confondre le signe de vie avec un résultat.** Matière première actuelle, par ordre de fragilité :

1. **La métrique de fusion `Φ` est un proxy fabriqué.** Définie comme coïncidence spectrale sous transposition avec noyau gaussien (largeur 25c choisie à la main). Motivée par le raisonnement cristallographique, mais **non validée contre des données de fusion perceptive**. Candidats sérieux à implémenter à la place : modèle de ségrégation de Kashino (1994, intégration multi-indices), harmonicité de Parncutt/Terhardt, tolérance d'accord de Darwin (~3-4%). **C'est la pièce centrale du projet — tout P5/P6 en dépend. Priorité absolue.**

2. **Le spectre de boîte à musique est analytique, pas mesuré.** Rapports de modes d'une poutre encastrée-libre (formule d'Euler-Bernoulli), amplitudes posées arbitrairement. À remplacer par **l'analyse d'un vrai enregistrement** (FFT + suivi de partiels) d'une boîte à musique réelle — c'est là que les amplitudes et l'inharmonicité réelles entrent. Sans ça, P5 reste une démonstration de principe.

3. **La rugosité `C` est la formule de Sethares avec ses constantes d'origine** (ajustées sur Plomp-Levelt 1965). Acceptable comme socle, mais c'est de l'empirique de seconde main et daté.

4. **Le récepteur "chauve-souris/fovéa" est grossièrement modélisé** (un simple rétrécissement de bande). Pour que P6 soit un vrai résultat, il faut un modèle de bande critique du rhinolophe tiré de la littérature bioacoustique.

5. **Le décrochage quasi-unisson** est géré par une restriction de domaine déclarée (`x_floor` = seconde mineure), justifiée mais à documenter comme décision de modélisation, pas à oublier.

---

## ORDRE DES TÂCHES (pour le dépôt)

### Étape 0 — mise en place
- Poser les 4 documents + le noyau à la racine.
- Trancher le langage. Rappel : Clojure était le candidat de bout en bout (règles-comme-données, Overtone, REPL live-coding). Le noyau actuel est en Python (jetable, pour le test). **Décision à acter** : réécrire le noyau en Clojure dès maintenant, ou garder Python pour la phase de validation numérique et migrer au moment du graphe/instrument. Recommandation : si Clojure, basculer tôt pour profiter du REPL ; mais la validation de `Φ` (tâche 1) est plus rapide à itérer en Python tant qu'on compare des formules. À toi.

### Étape 1 — solidifier la pièce centrale (LE chemin critique)
- Implémenter 2-3 métriques de fusion publiées, les comparer à la proxy actuelle sur le cas harmonique (doivent toutes reproduire P2, sinon elles sont fausses).
- Choisir, déclarer le choix, le figer pour tous les timbres comparés.

### Étape 2 — vrai matériau
- Enregistrer / récupérer un échantillon de boîte à musique réelle, extraire son spectre (partiels + amplitudes + enveloppes).
- Refaire P5 sur le spectre mesuré. **C'est ici que P5 passe de principe à résultat.**

### Étape 3 — le graphe-grammaire comme structure
- Implémenter états + arêtes (R1/R2/R3/R5 de la spec) → produire l'automate par (timbre × récepteur).
- Mesurer la **fraction de Fux récupérée** (critère §6.3) : combien des règles de première espèce tombent, qu'est-ce qui résiste.
- Analyse de sensibilité aux seuils `τ_C`, `τ_F` : règles robustes vs fragiles.

### Étape 4 — rendu + écoute (falsification)
- Synthèse additive avec exactement les partiels du modèle ; générer un exemple deux voix dans la grammaire dérivée ; écouter.
- L'écart entre "correct selon la grammaire" et "fonctionne à l'oreille" est le résultat le plus riche.

### Étape 5 (différé) — l'instrument navigable
- Le graphe 3D, le diagramme de phase, le morphing timbral. Esthétiquement central, scientifiquement redondant avec les étapes 1-4. Ne vient qu'après.

---

## Invariants (rappel, ne pas dériver)
- Deux scalaires distincts : `C` (vertical, dépend du récepteur), `Φ` (fusion, substrat arithmétique + fenêtre récepteur). Jamais mélangés ; la rugosité n'entre pas dans la fusion.
- Un graphe par (timbre × récepteur) ; la comparaison des graphes est le résultat.
- Récepteur = coordonnée explicite derrière un port, jamais présupposé enfoui.
- Les prédictions sont enregistrées ; on ne les réécrit pas après coup.
- Périmètre v1 = simultanéité, première espèce. Le séquentiel est une extension, pas un échec.
- Ça doit sonner.

---

## Statut épistémique honnête (à garder en tête pour thèse/article)
Ce qu'on a : une prédiction physique (depuis le spectre) de règles contrapuntiques, vérifiée sur le cas connu et montrant un déplacement timbre-dépendant. Ce qu'on n'a pas encore : la validation de la métrique de fusion contre du réel, et un spectre mesuré. La force du cadrage tient à ce que la prédiction PRÉCÈDE la mesure — préserver cette discipline à chaque étape est ce qui distingue ce projet d'un système génératif de plus.

---

## Mise à jour datée — 2026-06-11 (étapes 0 et 1 effectuées)

*Addendum append-only ; le texte ci-dessus est conservé tel quel comme état au moment de la passation.*

- **Étape 0 faite.** Documents + noyau posés à la racine du dépôt. **Langage acté : Python jusqu'à la fin de l'étape 2** (validation numérique = itération sur formules ; le noyau de référence est en Python ; ce qui migrerait ensuite est une fonction scalaire pure). Décision Clojure réexaminée à l'entrée de l'étape 3 (graphe/instrument), où règles-comme-données + Overtone + REPL commencent à payer.
- **Étape 1 faite — la métrique Φ est choisie, déclarée et figée.** Voir `DECISION-PHI.md` (le document de décision) ; résumé : 4 métriques de littérature implémentées (`metriques_fusion.py`) et comparées à la proxy (`comparaison_phi.py` + `comparaison_phi.png`). Toutes reproduisent P2 — le résultat du noyau n'était pas un artefact de la proxy. **Figée : coïncidence spectrale sous transposition, σ = 6,83 c (= spectral pitch similarity de Milne, constante publiée)** — la proxy d'origine était une instance non calibrée de ce modèle publié. Les gabarits d'harmonicité (crible Darwin/Moore, pitch virtuel Terhardt/Parncutt) passent P2 mais ont des pics ancrés aux rationnels des fondamentales → gardés comme modèles de contrôle du récepteur humain (utiles à l'étape 4), inaptes à porter P5. Périodicité de Stolzenburg = étalon arithmétique.
- **Kashino différé.** Référence identifiée : Kashino (1994), « A computational model of auditory segregation of two frequency components — evaluation and integration of multiple cues », *Electronics and Communications in Japan III*, 77(7). Modèle multi-indices dont les indices différenciants (attaques, modulation) sont hors périmètre v1 (simultanéité statique) ; à reprendre à l'étape « dynamique temporelle ». PDF non obtenu (paywall).
- **Fragilité n°1 reclassée, pas éteinte.** La pièce centrale passe de « proxy fabriquée, non validée contre rien » à « forme publiée + constante publiée + corroboration croisée par deux familles indépendantes sur le cas connu ». Ce qui manque toujours : une validation contre des données de fusion perceptive directes (cf. réserves dans `DECISION-PHI.md` §5).
- **Prochain chemin critique : étape 2** (spectre de boîte à musique MESURÉ, puis refaire P5 avec la Φ figée).
- **Étape 2 engagée (même jour).** Chaîne de mesure (suivi de partiels) écrite, paramétrée et **validée à l'aveugle sur synthétique avant toute donnée réelle** ; verdict P5 opérationnalisé et seuils déclarés — voir `ETAPE2-PROTOCOLE.md`. Matériau réel manquant : la politique réseau du conteneur bloque les sources d'échantillons (journal au §4 du protocole ; au passage, les « music box » des soundfonts GM sont démasquées — aucune n'est une vraie boîte). **En attente : enregistrement utilisateur OU élargissement d'allowlist.**
- **Étape 2 CONCLUE sur premier exemplaire réel (même jour).** Matériau : « Music box notes » 1-5 (Wikimedia Commons, CC BY-SA, notes isolées d'une vraie boîte). Verdict rendu par la chaîne figée : **P5 SANS OBJET — cas dégénéré (CADRAGE §9)**. Le timbre TENU mesuré est quasi sinusoïdal ({1 ; 10,53 à amp 0,10} sur la dent grave, 2 fichiers indépendants) → courbe Φ plate → ce son, en régime tenu, ne porte pas de structure de fusion. Ni confirmation ni infirmation de P5. Trois faits durs au passage (détail : protocole §7) : (1) **la fragilité n°2 est tranchée — les amplitudes analytiques 1/√k sont fausses en régime tenu** (modes réels ≥10× plus faibles que le fondamental) : le « signe de vie » P5 du test exploratoire reposait sur elles ; (2) la distorsion de chaîne (harmoniques exactes, prouvées dépendantes du niveau) aurait FABRIQUÉ une grammaire harmonique et un faux abandon — la qualification du matériau est une étape de plein droit ; (3) l'inharmonicité réelle des petites boîtes vit dans l'attaque (transitoire) → hors périmètre v1.
- **Chemin critique réorienté — trois options pour faire vivre P5** : (a) un exemplaire plus riche en tenu : grande boîte à cylindre, dents graves lestées (200-400 Hz) ; (b) **substitution d'exemplaire vers un timbre inharmonique riche en tenu : cloche/carillon, spectres mesurés publiés** (Harrison & MacConnachie 2024, déjà au CADRAGE §3) — testable en v1 immédiatement, substitution à déclarer ; (c) l'extension temporelle (attaques), déjà prévue comme étape ultérieure. Recommandation : (b) d'abord, (a) si un enregistrement qualifiant arrive, (c) à son heure.
- **2026-06-12 — Étape 2 CONCLUE (option (b) exécutée) : P5 TIENT sur cloche de carillon réelle.** Substitution déclarée (protocole §7). Source : matériaux publiés de Harrison & MacConnachie 2024 (dépôt GitHub du papier) — spectre représentatif de la cloche grave de la Westerkerk (11 partiels, fréquences ET amplitudes mesurées) + wav bruts. **Validation croisée : notre chaîne figée retrouve 9 partiels campanologiques nommés sur le bourdon brut (undeciem mesuré 2,587 vs publié 2,588).** Verdict figé : **P5 TIENT sur les deux entrées** (spectre publié ET notre extraction) — pics de fusion déplacés, argmax publié sur la tierce mineure propre de la cloche (307 c, Φ=1,28), pic déplacé le plus robuste ~888 c (nominal/tierce) ; octave/quinte persistent en pics secondaires (héritage de l'accordage). Conséquence R2 : l'interdit de parallèles se déplace sur les intervalles propres de la cloche. Nuance consignée : la HIÉRARCHIE des pics (argmax) dépend du profil d'amplitudes (substrat stable, saillance dépendante) — à trancher par l'analyse de sensibilité de l'étape 3. **Le palier scientifique « le mouvement est timbre-dépendant » est maintenant établi sur du réel mesuré, plus seulement sur l'analytique.**
- **Prochain chemin critique : étape 3 — le graphe-grammaire** (états R1, arêtes R2/R3/R5, fraction de Fux récupérée, sensibilité τ_C/τ_F), avec deux timbres réels en main : harmonique (contrôle) et cloche Westerkerk (mesuré publié). La question Clojure se rouvre ici, comme prévu.
- **2026-06-12 — Étape 3 FAITE : le graphe-grammaire existe et produit la carte.** Voir `ETAPE3-GRAPHE.md` (+ `graphe_grammaire.py`, `rugosite.py`, `etape3_fux.py` ; règles = données, traçabilité du seuillage jusqu'à la paire de partiels). Résultats : **fraction de Fux sur l'harmonique** — F2+F3 (parallèles/directes vers quinte-octave) RETROUVÉE et robuste (plateau 0,16 ; octave seule : 0,66), F4 (frontières unisson/octave) RETROUVÉE exacte, F1 (inventaire vertical) NON à tout seuil (Jaccard max 0,71 ; résidu mesuré : quarte admise, pics septimaux 10/7 et 7/4, tierce mineure sans pic), F5 = gabarit (imposé, pas dérivé). **Comparaison des automates** : interdits de parallèles {0, 702, 1200} (harmonique) → **{0, 307, 886}** (cloche) ; frontières {0, 1200} → **{0, 307}**. **Fait structurel : le cantus de Fux n'a AUCUNE réalisation légale dans la grammaire de la cloche** (le miroir du cantus, si) — le matériau mélodique est lui-même timbre-relatif. Réserves consignées au doc (convention Φ(unisson), compas d'une octave, fragilité R3-cloche selon τ_C).
- **Langage acté : Python jusqu'à l'étape 3 incluse ; la décision Clojure est reportée à l'étape 4** (rendu/écoute, Overtone/REPL = l'argument réel).
- **Prochain chemin critique : étape 4 — rendu + écoute (falsification)** : synthèse additive avec exactement les partiels des modèles (harmonique ET cloche Westerkerk mesurée), rendre les chemins légaux audibles, écouter où la grammaire dérivée fonctionne et où elle casse. L'écart « correct selon la grammaire » / « fonctionne à l'oreille » est le résultat le plus riche — et les résidus de l'étape 3 (unissons médians, états septimaux, quarte) sont les premiers points d'écoute.
