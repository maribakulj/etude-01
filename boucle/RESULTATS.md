# Boucle simulée, étape 1 : résultats

*Calculés le 2026-10-28, après les commits du protocole (`2a4e20d`) et du code
(`5942083`). `PROTOCOLE.md` n'a pas été modifié. Rejouer :
`python3 boucle/boucle.py` (≈ 3 min), puis `python3 boucle/rendu.py`.
Données : `resultats.json` ; figure : `trajectoires.png` ; sons :
`sons/boucle_<son>.wav`.*

---

## 1. Verdicts des prédictions

| Prédiction | Résultat | Verdict |
|---|---|---|
| B1 — trajectoires `argmax` de `harm` et `cloche` triviales (≥ 3/4) | 0/4 et 0/4 triviales | **non vérifiée** |
| B2 — intervalle mélodique dominant : ±307 c pour `cloche`, ±1200 ou ±702 c pour `harm` | `harm` : ±1200 c (oui) ; `cloche` : ±1517 c (non) | **non vérifiée** |
| B3 — `dent994` est le son le plus variable d'un réglage à l'autre | distance intra-son 0,72, la plus élevée (suivant : `harm`, 0,57) | **vérifiée** |
| B4 — R ≥ 2 et p < 0,01 | R = 1,44 ; p < 0,001 | **non vérifiée** |

Lecture prévue au protocole (§7) pour B4 fausse : « ce sont les réglages qui
composent ». Ce verdict est maintenu tel quel. Il faut toutefois le nuancer :
R est significativement supérieur à 1, donc le son compte plus que les
réglages, mais beaucoup moins que le facteur 2 annoncé.

Sur B2, la prédiction confondait deux choses : l'intervalle de plus forte
coïncidence d'un son avec lui-même, et l'intervalle entre deux notes
successives. Or chaque nouvelle note se place par rapport à *tout* ce qui
sonne, pas par rapport à la note précédente.

**Écart au protocole.** 98 pas sur 6144 n'avaient aucun candidat (tous les
maxima tombaient dans les zones d'exclusion). Le code a alors pris le
meilleur point libre de la grille, une règle de secours non prévue au
protocole. Ces 98 pas concernent tous `dent994` avec σ = 15 et τ = 4.

## 2. Ce que montrent les trajectoires (observations exploratoires)

Ces observations n'étaient pas prédites. Elles sont rapportées comme des
pistes, pas comme des résultats.

**a. Le son fixe l'ensemble des hauteurs.** Sur le son harmonique, la
trajectoire `argmax` passe par 0, −1200, 1200, 2400, 498, −702, 1698, −204,
996, 294, 90… Ce sont des positions du réseau pythagoricien, engendré par
l'octave et la quinte (ton de 204 c, tierce de 294 c, limma de 90 c). Sur les
16 réglages, 45 à 100 % des notes sont à moins de 2 c de ce réseau (avec au
plus ±12 quintes), contre 5 à 7 % pour des positions tirées au hasard.

L'explication est arithmétique : chaque nouvelle copie se place à une
octave ou une quinte d'une copie qui sonne, et ces positions s'enchaînent.
C'est la construction pythagoricienne classique (empiler des quintes), que la
boucle retrouve sans qu'on la lui ait donnée. Ce n'est pas une découverte ;
c'est la vérification qu'un principe connu sort bien du mécanisme.

Pour la cloche, la même mécanique s'appuie sur ses propres intervalles de
forte coïncidence, autour de 307 c et 1210 c (son octave légèrement
étirée) : par exemple 1517 = 1210 + 307, puis −307, −614, −921. Avec les deux
générateurs de plus forte coïncidence calculés sur la cloche seule
(1517 et 1210 c), 27 % des notes sont à moins de 3 c de leur réseau, contre
4 % au hasard. Le rapprochement est plus faible et moins net que pour
l'harmonique.

**b. La boucle fixe le mouvement, et il ne ressemble pas à une mélodie.**
Toutes les trajectoires, quel que soit le son, ont la même allure : un
zigzag qui saute d'une à deux octaves à chaque pas et balaie tout le
registre. Cela vient du mécanisme, pas du son : les zones autour des copies
qui sonnent encore sont exclues, et les coïncidences fortes avec les copies
plus anciennes se trouvent loin. Le rapport R calculé sur les seuls
intervalles mélodiques vaut 1,8 ; sur les seules positions modulo l'octave,
1,14.

**c. Le contrôle négatif se comporte comme prévu.** Sur `dent994` (presque
sinusoïdal), la courbe de coïncidence est plate. Avec `argmax`, la
trajectoire suit uniquement la règle de départage des égalités : des rampes
régulières de 190 c. C'est la boucle seule qui « compose ».

## 3. Ce que cela veut dire pour l'idée

- **Ce que le son contient vraiment, dans cette boucle :** un réseau de
  hauteurs engendré par ses intervalles de forte coïncidence. Pour le son
  harmonique, c'est le réseau pythagoricien ; pour la cloche, un réseau
  construit sur sa tierce mineure et son octave étirée. C'est une version
  précise et vérifiable de « en puissance ».
- **Ce que le son ne contient pas, dans cette boucle :** une mélodie. La
  boucle ne mesure que la coïncidence entre sons *simultanés*. Elle n'a
  aucune notion de continuité d'une note à la suivante, qui est ce qui fait
  qu'on entend une suite de notes comme une ligne : en psychoacoustique, une
  suite reste un seul flux si les sauts sont petits pour le tempo (van
  Noorden, 1975). Sans cet ingrédient, la « mélodie » est un balayage du
  registre.
- **Le timbre :** le mélange compte jusqu'à 12 copies actives et son
  centroïde varie (valeurs dans `resultats.json`), mais cette étape ne mesure
  rien qui permette de dire si cette évolution est perceptible ou structurée.

## 4. Limites

- Toutes les mesures portent sur la coïncidence de partiels, qui n'est pas
  validée comme mesure perceptive (README.md, limite 5).
- Le registre, l'exclusion de 100 c, la longueur et le départage des
  égalités sont des choix fixés ; seuls la règle, τ et σ ont été variés.
- Les observations du §2 ont été faites après avoir vu les trajectoires.
  Elles demandent à être prédites puis testées sur d'autres sons avant
  d'avoir un statut.
- Personne n'a encore écouté les sons produits.

## 5. Suite possible

1. Ajouter à la mesure un terme de continuité séquentielle tiré de données
   psychoacoustiques (la frontière de cohérence temporelle de van Noorden),
   pour voir si une ligne mélodique émerge ou non.
2. Prédire, avant calcul, le réseau de hauteurs de sons nouveaux (autres
   cloches, lames, cordes) à partir de leurs seuls intervalles de forte
   coïncidence, puis vérifier que la boucle le produit.
3. Le régime exploratoire (étape 2 du plan).
