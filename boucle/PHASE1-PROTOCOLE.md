# Phase 1 — L'oreille à partir de données : protocole

*Écrit le 2026-10-28 et commité avant le code de la phase. Les résultats
iront dans `PHASE1-RESULTATS.md`. Ce document ne sera pas modifié après les
calculs ; toute correction sera ajoutée datée à la fin.*

---

## 1. But

Construire les composants du modèle de l'oreille dont la boucle aura besoin
(PLAN.md, phase 1). Chacun doit reproduire une donnée publiée par un test
automatique. Un composant qui échoue est retiré ou remplacé par une variante
plus simple, déclarée.

## 2. Deux sortes de tests, à ne pas confondre

- **Validation** : le composant reproduit une donnée qui n'a pas servi à
  régler ses paramètres. C'est une vraie épreuve, qui peut échouer.
- **Cohérence** : le paramètre du composant est tiré de la donnée elle-même.
  Le test vérifie seulement que le code applique correctement la donnée. Il
  ne peut échouer que par erreur de programmation.

Les résultats rapporteront séparément les deux sortes. Seules les validations
comptent comme indices que le composant représente l'oreille.

## 3. Provenance des données

| Réf. | Source | Statut de la vérification |
|---|---|---|
| [vN75] | van Noorden (1975), *Temporal coherence in the perception of tone sequences*, thèse, TH Eindhoven | **lue** dans le texte intégral (pure.tue.nl) : p. 15-16 et p. 73 |
| [MGP86] | Moore, Glasberg & Peters (1986), JASA 80(2), 479 et suiv., doi:10.1121/1.394043 | **lue** : résumé et première page |
| [PL65] | Plomp & Levelt (1965), JASA 38, 548-560 | résumé, via une source secondaire ; à vérifier dans le texte |
| [GM90] | Glasberg & Moore (1990), Hearing Research 47, 103-138 | formule confirmée par plusieurs implémentations publiques ; texte original non lu, à vérifier |
| [ZT80] | Zwicker & Terhardt (1980), JASA 68 : formule de la bande critique | de mémoire ; à vérifier |
| [PPK01] | Pressnitzer, Patterson & Krumbholz (2001), JASA 109, 2074-2084 | résumé, via une source secondaire ; à vérifier |
| [SD90] | Semal & Demany (1990), Music Perception 8(2), 165-175 | résumé ; à vérifier |
| [SRC62] | Schouten, Ritsma & Cardozo (1962), « Pitch of the residue », JASA 34 | de mémoire ; à vérifier |
| [Cloches] | note de frappe des cloches : Terhardt & Seewann (1984) ; synthèse de Hibbert (hibberts.co.uk) | source secondaire seulement ; à vérifier |

Aucune valeur marquée « à vérifier » ne sera présentée comme établie dans les
résultats.

## 4. Composants, données et tolérances

### C1 — Largeur des filtres auditifs (ERB)

- **Donnée [GM90]** : ERB(f) = 24,7 × (4,37 f/1000 + 1) Hz.
- **Test (cohérence)** : valeurs à 100, 1000 et 4000 Hz (35,5 ; 132,6 ;
  456,5 Hz) à 0,1 Hz près.
- **Usage prévu** : unité de résolution fréquentielle pour les phases
  suivantes.

### C2 — Rugosité de deux sons purs

- **Donnée [PL65]** : la dissonance maximale de deux sons purs se produit
  pour un écart d'environ un quart de la bande critique. Greenwood (1991,
  à vérifier) donne plutôt environ 40 % avec une autre estimation de la bande
  critique : on rapporte donc les deux références.
- **Composant** : modèle de Sethares déjà utilisé (`rugosite.py`), dont les
  constantes ont été ajustées sur la courbe de Plomp-Levelt.
- **Test (validation partielle)** : pour une fréquence basse de 250, 500,
  1000 et 2000 Hz, position du maximum de dissonance divisée par la bande
  critique de [ZT80]. Tolérance : entre 0,15 et 0,45 pour chaque fréquence.
  La validation n'est que partielle, puisque les constantes ont été ajustées
  sur la même courbe.

### C3 — Coïncidence de partiels (Φ)

- **Donnée** : σ = 6,83 c (Milne ; DECISION-PHI.md), classement de fusion
  octave > quinte > quarte (Stumpf ; DeWitt & Crowder 1987).
- **Tests existants** : égalité avec Φ (cohérence) ; classement (validation
  sur sons harmoniques seulement).

### C4 — Harmonicité : regroupement des partiels par fondamentale commune

- **Donnée [MGP86]** : un partiel désaccordé d'un son complexe harmonique
  est entendu à part au-delà d'un désaccord de 1 à 3 % de sa fréquence selon
  les auditeurs ; 1,1 % en moyenne pour les quatre premiers harmoniques à
  410 ms de durée. Les seuils augmentent d'un facteur 3 à 5 quand la durée
  passe de 1610 à 50 ms.
- **Composant** : pour un ensemble de partiels, on cherche la fondamentale
  qui en explique la plus grande part d'énergie, un partiel étant « expliqué »
  s'il est à moins de δ d'un harmonique de cette fondamentale. δ vient de
  [MGP86] : 2 % (milieu de la plage 1-3 %), avec sensibilité à 1 % et 3 %.
- **Test (cohérence)** : un harmonique désaccordé de 0,5 % reste regroupé ;
  désaccordé de 4 %, il ne l'est plus.
- **Rôle** : seconde hypothèse de fusion, concurrente de C3 ; les deux sont
  gardées jusqu'au test d'écoute (PLAN.md, phase 4).

### C5 — Hauteur virtuelle

- **Composant** : recherche de la fondamentale dont les sous-harmoniques
  rendent le mieux compte des partiels, pondérés par leur amplitude, avec la
  tolérance δ de C4 (forme simplifiée du modèle de Terhardt, déclarée comme
  telle).
- **Tests (validation)** :
  - (a) son harmonique sans fondamentale (harmoniques 3 à 10 de 200 Hz) :
    hauteur à 200 Hz, à 1 % près ;
  - (b) décalage de hauteur [SRC62, à vérifier] : partiels à 1840, 2040 et
    2240 Hz (série de 200 Hz décalée de 40 Hz) : hauteur entre 202 et 206 Hz
    (la référence, de mémoire, est d'environ 204 Hz) ;
  - (c) cloche Westerkerk (spectre publié) : hauteur dans ±100 c de la prime
    ([Cloches], source secondaire : la note de frappe est environ une octave
    sous la nominale, c'est-à-dire proche de la prime pour une cloche bien
    accordée).
- Si (c) échoue, la hauteur des sons inharmoniques est marquée « non
  modélisée » pour la suite, et la phase 2 n'utilisera pas de hauteur pour
  ces sons.

### C6 — Limites de la hauteur mélodique

- **Données** : limite basse environ 30 Hz [PPK01, à vérifier] ; limite haute
  environ 4,7 kHz pour des sons purs [SD90, à vérifier], mais des travaux plus
  récents (Oxenham et al. 2011, à vérifier) mettent en doute l'existence d'une
  limite à 5 kHz pour des sons complexes.
- **Usage prévu** : remplacer le registre fixe [−1200 ; 2400] c par la zone
  où la hauteur virtuelle (C5) du son transposé reste dans [30 Hz ; 4,7 kHz].
- **Test (cohérence)** : bornes appliquées correctement pour le son
  harmonique de référence à 220 Hz.

### C7 — Regroupement séquentiel (lignes)

- **Données [vN75]**, sons purs alternés ABAB, 1 kHz, 35 dB SL, durée 40 ms :
  - frontière de fission : environ 1 demi-ton, pratiquement indépendante de
    la période T entre 0,1 et 0,4 s (p. 15) ;
  - frontière de cohérence temporelle : pour T > 100 ms, Ic ≈ 0,15 × (T − 100)
    demi-tons, T en ms (p. 16) ; en dessous de 100 ms, à peu près
    horizontale et proche de la frontière de fission ;
  - sons complexes harmoniques à spectre plat : pour un même intervalle, la
    période limite est en moyenne environ 60 ms plus courte que pour des sons
    purs (p. 73), ce qui revient à décaler la frontière de 60 ms vers les
    tempos rapides.
- **Composant** : deux événements successifs sont dans la même ligne
  « obligatoirement » si l'écart de hauteur est sous la frontière de fission,
  « possiblement » s'il est sous la frontière de cohérence (avec la
  correction pour sons complexes), et sont séparés au-delà.
- **Test (cohérence)** : valeurs aux périodes 100, 150, 200 ms.
- **Hypothèse non testée, déclarée** : appliquer ces frontières à des sons
  inharmoniques, avec la hauteur virtuelle de C5 comme hauteur. Rien dans
  [vN75] ne porte sur ces sons ; c'est un point à éprouver en phase 4.

### Reportés

- **Mémoire auditive** (régime exploratoire) : protocole de la phase 3.
- **Audibilité dans le mélange** (remplacement de W_MIN) et **distinction de
  deux sons simultanés** (remplacement d'EXCLUSION) : sources non encore
  établies ; traités dans le protocole de la phase 2. Ces deux paramètres
  restent marqués « à remplacer ».

## 5. Prédictions

- **O1.** Les tests de cohérence (C1, C4, C6, C7, et l'égalité de C3)
  passent. Leur échec signalerait une erreur de programmation, pas un fait
  sur l'oreille.
- **O2.** C2 : le maximum de dissonance de Sethares tombe entre 0,15 et
  0,45 bande critique aux quatre fréquences.
- **O3.** C5 (a) et (b) passent.
- **O4.** C5 (c) : la hauteur virtuelle calculée pour la cloche Westerkerk est
  à ±100 c de la prime. C'est la prédiction la plus incertaine : le modèle
  est simplifié et la cloche a des partiels graves forts (bourdon à 0,497,
  tierce à 1,194).

## 6. Critère de sortie

Tous les composants passent leur test, ou sont retirés ou simplifiés avec une
entrée datée. Le registre contient chaque nouveau paramètre avec sa source et
son test. La reproduction de l'étape 1 reste identique (aucun composant
nouveau n'est encore utilisé par la boucle).
