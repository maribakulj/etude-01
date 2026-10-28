# Phase 2 — Boucle simulée v2, sans consigne : protocole

*Écrit le 2026-10-28 et commité avant le code de la phase. Résultats dans
`PHASE2-RESULTATS.md`. Ce document ne sera pas modifié après les calculs ;
toute correction sera ajoutée datée à la fin.*

---

## 1. Ce qui change par rapport à l'étape 1

La boucle garde son principe : une nouvelle copie du son entre à chaque pas,
choisie parmi les maxima de coïncidence avec ce qui sonne (PROTOCOLE.md §2).
Trois changements :

1. les choix arbitraires de l'étape 1 sont remplacés par des valeurs issues du
   son ou de l'oreille, ou déclarés comme réglages dont on mesure l'influence
   (§2) ;
2. le temps devient réel (périodes en millisecondes) ;
3. l'oreille modélisée **écoute** la suite d'événements et la répartit en
   lignes (§3). Ces lignes sont des résultats, pas des contraintes.

**Pas de consigne, donc pas de préférence pour les lignes.** Utiliser les
lignes pour choisir l'événement suivant, par exemple en favorisant leur
continuation, reviendrait à introduire un but. Ce sera le rôle du régime
exploratoire (phase 3). En phase 2, l'oreille n'intervient dans le choix que
par une contrainte de perception : un événement que l'oreille ne distingue
pas d'un autre qui sonne déjà n'est pas un nouvel événement (§2, exclusion).

## 2. Remplacements

| Paramètre de l'étape 1 | Remplacement | Source |
|---|---|---|
| T_MIN, T_MAX (registre fixe) | une copie est admise si son partiel le plus fort est dans [30 Hz ; 4,7 kHz] | limites de la hauteur mélodique (C6, à vérifier), appliquées au partiel dominant, puisque la hauteur virtuelle n'est pas fiable pour les sons inharmoniques (PHASE1-RESULTATS.md §4). Les deux limites ont été mesurées sur des sons purs ([SD90]) ou des sons complexes ([PPK01]) : les appliquer à un partiel est une approximation déclarée |
| EXCLUSION (100 c) | une candidate est exclue si son partiel le plus fort est à moins d'**1 ERB** du partiel correspondant d'une copie active | deux sons purs séparés de moins d'environ une bande auditive ne sont pas résolus (Plomp 1964, « The ear as a frequency analyzer », JASA 36, à vérifier) ; ERB de C1. Sensibilité : 0,5 et 1,5 ERB |
| W_MIN (retrait à 0,05) | **non remplacé** : aucune donnée de masquage n'a été établie pour ce cas. Devient un choix technique, avec sensibilité : 0,01 ; 0,05 ; 0,1 | — |
| TAUS (persistance en pas) | persistance en secondes. Cloche : constante de décroissance mesurée sur l'enregistrement brut `12-c1.wav` (dépôt public de Harrison & MacConnachie) par intégration inverse de Schroeder et ajustement linéaire entre −5 et −25 dB ; τ = T60 / ln(1000). Sons synthétiques (harmonique, cordes, aléatoire) : pas de décroissance propre, donc choix technique, τ ∈ {0,5 ; 1,5} s. `dent994` : enregistrement non commité, même choix technique | le son (cloche) ; technique sinon |
| DUREE_PAS (0,45 s) | période T entre deux événements, **réglage varié** : 100, 150 et 200 ms | bornes de la plage où van Noorden a mesuré la frontière de cohérence (48 à 200 ms, [vN75] p. 14) : on reste dans la plage des données |
| F0_RENDU (220 Hz) | fréquence absolue de t = 0 : cloche, 544,8 Hz (notre extraction de `12-c1`) ; `dent994`, 993,8 Hz (mesurée) ; sons synthétiques : 220 Hz, choix technique | le son, quand il est mesuré |

## 3. L'oreille écoute : formation des lignes

Les événements sont examinés dans l'ordre. Pour chaque nouvel événement, on
considère les lignes existantes et, pour chacune, son dernier événement :

- **proximité** entre deux événements = |Δt|, l'écart de transposition en
  cents. Pour deux copies du même son, c'est l'écart en fréquence de chaque
  partiel avec son correspondant : c'est la « proximité en fréquence » que
  van Noorden ([vN75] p. 24) identifie comme condition de la cohérence dans
  les suites rapides. Aucune hauteur virtuelle n'est utilisée ;
- **période** = temps écoulé depuis le dernier événement de la ligne ;
- l'événement peut rejoindre la ligne si |Δt| est sous la frontière de
  cohérence de C7 (correction pour sons complexes comprise) à cette période ;
- s'il peut en rejoindre plusieurs, il rejoint celle dont le dernier
  événement est le plus proche en |Δt| ; sinon, il ouvre une nouvelle ligne ;
- une ligne dont le dernier événement remonte à plus de 200 ms est **close** :
  au-delà, les données de van Noorden ne disent rien.

Deux variantes, issues de la même source (rôle de l'attention, [vN75]
p. 13 et 16) :
- **A, l'auditeur cherche l'unité** : frontière de cohérence (ci-dessus) ;
- **B, l'auditeur cherche la séparation** : frontière de fission (1 demi-ton).

Ce mécanisme d'affectation est un choix technique (algorithme glouton) ; il
est déclaré au registre. Hypothèse non testée : les frontières mesurées sur
des sons purs et harmoniques valent pour les sons inharmoniques.

**Mesures des lignes** : nombre de lignes, longueur moyenne (en événements),
part des événements dans une ligne d'au moins 4 événements.

## 4. Plan de calcul

- **Sons** : les 8 sons de l'étape 1.
- **Réglages** : règle (`argmax` ; `tirage`, graines 1, 2, 3) × période T
  (100, 150, 200 ms) × τ pour les sons synthétiques (0,5 ; 1,5 s) ; pour la
  cloche, τ mesuré. σ fixé à 6,83 c. N = 48 événements.
- **Sensibilité** (sur la règle `argmax` seulement) : exclusion à 0,5 et
  1,5 ERB ; W_MIN à 0,01 et 0,1.
- **Son contre réglages** : rapport R comme à l'étape 1, sur les
  trajectoires (R_traj) et sur les mesures de lignes (R_lignes, distance =
  écart relatif moyen des trois mesures).

## 5. Prédictions (enregistrées avant tout calcul)

- **Q1 — le tempo agit sur les lignes dans le sens des données.** Pour chaque
  son, en variante A, la longueur moyenne des lignes est plus grande à
  T = 200 ms qu'à T = 100 ms (moyenne sur les règles). C'est attendu par
  construction, puisque la frontière de cohérence s'élargit avec T : il s'agit
  d'un contrôle, pas d'un résultat.
- **Q2 — le zigzag persiste.** Avec la règle `argmax`, plus de la moitié des
  intervalles entre événements successifs dépassent 1200 c pour au moins 6
  des 8 sons. Motif : le mécanisme qui produisait le zigzag (exclusion autour
  des copies actives, coïncidences fortes avec les copies anciennes) est
  toujours là, et l'exclusion d'1 ERB est plus large que les 100 c d'avant.
- **Q3 — peu de lignes.** Conséquence de Q2 : en variante B, moins de 20 % des
  événements appartiennent à une ligne d'au moins 4 événements, pour tous les
  sons. En variante A, à T = 200 ms, au moins un son dépasse 20 %.
- **Q4 — le son compte plus que les réglages** : R_traj ≥ 1,5 avec p < 0,01 ;
  R_lignes < R_traj (les lignes dépendent davantage du tempo, qui est un
  réglage).

## 6. Lecture prévue

- Si Q2 et Q3 se vérifient, la conclusion de l'étape 1 tient avec une oreille
  mieux fondée : sans consigne, la boucle produit des hauteurs, pas des
  lignes. Il faudra alors une consigne (phase 3) pour qu'il y ait des lignes,
  et le dire.
- Si des lignes se forment (Q3 réfutée), on les écoute et on cherche ce qui
  dans le son les produit.
- Si R_traj < 1,5, la dépendance au son mesurée à l'étape 1 ne survit pas au
  remplacement des choix arbitraires : c'est un résultat négatif à rapporter
  tel quel.

## 7. Données externes

`12-c1.wav` provient du dépôt public github.com/pmcharrison/CarillonConsonancePaper
(Harrison & MacConnachie 2024). Seule la mesure dérivée (T60, τ) est
commitée, pas l'audio.
