# Phase 1 — L'oreille à partir de données : résultats

*Calculés le 2026-10-28, après les commits du protocole (`53803c5`) et du code
(`f9712a9`). `PHASE1-PROTOCOLE.md` n'a pas été modifié. Rejouer :
`python3 -m pytest -q`.*

---

## 1. Verdicts

| Composant | Test | Sorte | Résultat |
|---|---|---|---|
| C1 ERB | valeurs à 100, 1000, 4000 Hz | cohérence | passe |
| C2 rugosité | maximum entre 0,15 et 0,45 bande critique | validation partielle | passe (0,18 à 0,23, voir §2) |
| C3 coïncidence | égalité avec Φ ; classement P8 > P5 > P4 | cohérence ; validation (sons harmoniques) | passe |
| C4 harmonicité | 0,5 % de désaccord regroupé, 4 % non | cohérence | passe |
| C5 (a) hauteur virtuelle | fondamentale absente → 200 Hz | validation | passe (200,0 Hz) |
| C5 (b) | décalage de hauteur → 202-206 Hz | validation | **échoue** (226,9 Hz) |
| C5 (c) | cloche Westerkerk → ±100 c de la prime | validation | **échoue** (54,3 Hz, soit −3993 c) |
| C6 limites | bornes pour un son harmonique à 220 Hz | cohérence | passe |
| C7 van Noorden | frontières à 100, 150, 200 ms | cohérence | passe |

Prédictions : O1 (tests de cohérence) vérifiée ; O2 (C2) vérifiée ; **O3
non vérifiée** ((a) passe, (b) échoue) ; **O4 non vérifiée**.

Les deux tests en échec sont gardés dans la suite, marqués comme échecs
attendus (`xfail` strict) : si un jour ils passent, la suite le signalera.

## 2. Valeurs mesurées

**C2.** Écart de dissonance maximale entre deux sons purs, modèle de Sethares :

| Fréquence basse | Écart au maximum | En bandes critiques [ZT80] | En ERB [GM90] |
|---|---|---|---|
| 250 Hz | 22,2 Hz | 0,21 | 0,43 |
| 500 Hz | 27,0 Hz | 0,23 | 0,34 |
| 1000 Hz | 36,5 Hz | 0,23 | 0,27 |
| 2000 Hz | 55,5 Hz | 0,18 | 0,23 |

Le résultat dépend fortement de l'échelle de bande choisie. Mesuré en bandes
critiques de Zwicker, il est proche du quart de Plomp & Levelt. Mesuré en
ERB, il va de 0,23 à 0,43, ce qui couvre aussi la valeur de Greenwood
(environ 40 %, à vérifier). C'est cohérent avec la remarque, citée au
protocole, selon laquelle la bande critique de Plomp & Levelt est large aux
basses fréquences. Le test passe, mais il ne départage pas les deux
références.

**C5.** Hauteur virtuelle, au réglage du registre (δ = 2 %, K = 16) :
- (a) 200,0 Hz, part d'amplitude expliquée 1,00 ;
- (b) 226,9 Hz, part expliquée 1,00 ;
- (c) 54,3 Hz, part expliquée 0,69.

## 3. Pourquoi C5 échoue, et sensibilité

La règle « la fondamentale la plus haute qui explique la plus grande part de
l'amplitude » ne tient qu'avec une tolérance assez fine :

- **(b)** Avec δ = 2 %, 226,9 Hz explique les trois partiels (rangs 8, 9 et
  10, écarts de 1,4 %, 0,1 % et 1,3 %), et c'est plus haut que 204 Hz.
- **(c)** Les partiels de la cloche ne sont pas harmoniques entre eux (tierce à
  1,194, etc.). Aucune fondamentale proche de la prime n'explique la plus
  grande part ; une fondamentale très grave (rang élevé, tolérance
  relativement large) en explique davantage.

Sensibilité (calculée après coup ; ces valeurs ne changent pas les
verdicts) :

| δ | K | (b) | (c), écart à la prime |
|---|---|---|---|
| 1 % | 10 | 204,2 Hz | −1206 c |
| 1 % | 16 | 204,0 Hz | −3993 c |
| 1 % | 20 | 204,0 Hz | −3993 c |
| 3 % | 10 | 226,9 Hz | −3092 c |
| 3 % | 16 | 226,9 Hz | −3090 c |
| 3 % | 20 | 226,9 Hz | −3089 c |

- (b) passe avec δ = 1 %, le bas de la plage de Moore et al. Le résultat
  dépend donc surtout de δ, que la donnée ne fixe qu'à un facteur 3 près.
- (c) échoue à tous les réglages. Dans le meilleur cas (δ = 1 %, K = 10), la
  hauteur tombe sur le bourdon, une octave sous la prime.

Le modèle simplifié ne retrouve pas la note de frappe. Les travaux cités par
la source secondaire attribuent celle-ci aux partiels aigus (nominale,
superquinte, octave nominale) et à une pondération spectrale que le modèle
simplifié n'a pas. Ajouter cette pondération maintenant serait ajuster le
modèle après avoir vu le résultat : ce n'est pas fait.

## 4. Conséquences pour la suite

Ce que prévoyait le protocole en cas d'échec de (c) s'applique : **la hauteur
des sons inharmoniques est « non modélisée »**, et la phase 2 n'utilisera pas
de hauteur virtuelle pour ces sons.

Cela touche directement C7. Les frontières de van Noorden s'expriment en
écart de hauteur, et pour la cloche on n'a pas de hauteur fiable. Une piste,
qui vient de la même source : au chapitre 3, van Noorden (1975, p. 24)
conclut que, dans les suites rapides, la cohérence temporelle demande la
**proximité en fréquence** des sons, et non une proximité de hauteur au sens
de la hauteur virtuelle. Cela permettrait de définir la proximité de deux
événements successifs par leurs partiels, sans passer par une hauteur. C'est
à décider et à justifier dans le protocole de la phase 2, avant le code.

Paramètres à ce stade : le registre compte 41 entrées (voir `REGISTRE.md`) ;
EXCLUSION et W_MIN restent « à remplacer », comme prévu.
