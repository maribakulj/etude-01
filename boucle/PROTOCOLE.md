# Boucle simulée, étape 1 : sans consigne — protocole et prédictions

*Écrit le 2026-10-28, et commité avant toute ligne de code de la boucle.
L'historique git en fait foi. Les résultats iront dans `RESULTATS.md`, dans
un commit séparé. Ce document ne sera pas modifié après les calculs ; toute
correction sera ajoutée datée à la fin.*

---

## 1. Question

Un son contient-il, dans l'organisation de ses partiels, de quoi déterminer
sa propre évolution ? Version opérationnelle pour cette étape : dans la
boucle décrite au §2, **la trajectoire produite dépend-elle davantage du son
de départ que des réglages de la boucle ?**

C'est le sens qu'on donne ici à « le son contient en puissance son
évolution ». Si les réglages comptent plus que le son, c'est la boucle qui
compose.

## 2. La boucle

**État.** Un ensemble de copies du son de départ S₀, chacune transposée de
*t* cents et affectée d'un poids *w*. Le mélange M est la réunion des
partiels de toutes les copies actives (amplitude d'un partiel = son
amplitude dans S₀ × *w*).

**Pas.** Un pas = une nouvelle copie de S₀ qui entre. À chaque pas :

1. **Mesure.** Pour chaque transposition candidate *t* (grille de 2 c dans le
   registre), on calcule la coïncidence entre S₀ transposé de *t* et le
   mélange M, avec le noyau de Φ (DECISION-PHI.md) :
   Σ_{i,j} a_i b_j exp(−(d_ij/σ)²), où d_ij est l'écart en cents entre le
   partiel *i* de la copie candidate et le partiel *j* du mélange.
2. **Coups possibles.** Les maxima locaux de cette courbe. Les candidats à
   moins de 100 c d'une copie active sont exclus (même zone hors domaine que
   Φ : une note à l'unisson d'une note qui sonne n'est pas un nouvel
   événement).
3. **Choix.** Selon la règle de transition (§3).
4. **Mise à jour.** Les poids des copies actives sont multipliés par
   exp(−1/τ) ; la nouvelle copie entre avec *w* = 1 ; les copies dont *w* <
   0,05 sont retirées.

Pas de consigne : la boucle ne cherche à atteindre ni à maintenir aucune
valeur. La seule chose qui guide le choix est la coïncidence entre le son et
ce qui sonne déjà.

**Choix fixés, déclarés comme tels.** Premier état : une copie à *t* = 0.
Registre : *t* ∈ [−1200 ; 2400] c. Longueur : 48 pas. En cas d'égalité
(à 1e-9 près), on prend le candidat le plus proche de la dernière copie, puis
le plus grave.

**Sorties.**
- *Mélodie* : la suite des transpositions *t*₁, *t*₂, …
- *Timbre* : le spectre du mélange à chaque pas (on en rapporte le nombre de
  copies actives et le centroïde spectral).
- La polyphonie (copies qui se superposent) n'est pas évaluée à cette étape.

## 3. Réglages que l'on fait varier

| Réglage | Valeurs |
|---|---|
| Règle de transition | `argmax` (le maximum le plus haut) ; `tirage` (tirage aléatoire parmi les maxima, probabilité ∝ hauteur⁴), graines 1, 2, 3 |
| τ (persistance des copies, en pas) | 1,5 ; 4 |
| σ (tolérance de coïncidence, en cents) | 6,83 ; 15 |

Soit 4 × 2 × 2 = 16 réglages par son.

## 4. Sons de départ

| Code | Son | Remarque |
|---|---|---|
| `harm` | harmonique, 10 partiels, amplitudes 1/k | référence |
| `cloche` | cloche Westerkerk, spectre publié | `materiau/` |
| `cloche12c1` | cloche Westerkerk, notre extraction | `materiau/` |
| `corde1e-3` | corde raide, B = 1e-3 | `famille_raide.py` |
| `corde1e-2` | corde raide, B = 1e-2 | idem |
| `corde1e-1` | corde raide, B = 1e-1 | idem |
| `dent994` | boîte à musique mesurée, presque sinusoïdale | contrôle négatif : pas de structure |
| `aleatoire` | 10 partiels à rapports tirés au hasard (log-uniforme sur [1 ; 8], graine 0), amplitudes 1/k | contrôle : spectre sans organisation particulière |

8 sons × 16 réglages = 128 trajectoires.

## 5. Mesures

**Distance entre deux trajectoires.** Moyenne de deux distances en variation
totale (½ Σ |p − q|) :
- entre les histogrammes des intervalles mélodiques *t*ₙ − *t*ₙ₋₁ (classes de
  50 c sur [−3600 ; 3600]) ;
- entre les histogrammes des positions *t* modulo 1200 (classes de 25 c).

**Rapport R.** R = (distance moyenne entre trajectoires de sons différents
au même réglage) / (distance moyenne entre trajectoires du même son à des
réglages différents). R > 1 : le son compte plus que les réglages.

**Test de permutation.** On permute au hasard les étiquettes de son à
l'intérieur de chaque réglage (1000 permutations, graine 0) et on recalcule
R. p = proportion de permutations avec R ≥ R observé.

**Trivialité d'une trajectoire.** Une trajectoire est dite triviale si, sur
ses 24 derniers pas, la suite des intervalles est périodique de période ≤ 4
(à 5 c près), **ou** si un même intervalle (à 10 c près) représente au moins
80 % de ses intervalles.

## 6. Prédictions (enregistrées avant tout calcul)

- **B1 — dynamique triviale.** Avec la règle `argmax`, les trajectoires de
  `harm` et de `cloche` sont triviales pour au moins 3 des 4 réglages
  `argmax` (τ × σ). Motif : sans consigne, la boucle risque de répéter
  l'intervalle de plus forte coïncidence.
- **B2 — l'intervalle dominant suit le son.** Avec `argmax` et σ = 6,83 :
  l'intervalle mélodique le plus fréquent de `cloche` est ±307 c (à 15 c
  près) ; celui de `harm` est ±1200 c ou ±702 c.
- **B3 — contrôle négatif.** `dent994` est le son dont les trajectoires
  varient le plus d'un réglage à l'autre (distance moyenne intra-son la plus
  élevée des 8 sons).
- **B4 — le son compte plus que les réglages.** R ≥ 2 et p < 0,01.

Ces prédictions sont celles que l'auteur de ce protocole juge probables ;
elles ne sont pas choisies pour être faciles à vérifier. B1 en particulier
est une prédiction *défavorable* à l'idée.

## 7. Lecture prévue des résultats

| B4 (son > réglages) | B1 (triviale) | Lecture |
|---|---|---|
| vraie | vraie | le son détermine bien sa trajectoire, mais dans cette boucle elle se réduit à la répétition de son intervalle le plus fort : « en puissance » seulement au sens faible |
| vraie | fausse | le son détermine une trajectoire non triviale : résultat intéressant, à écouter et à éprouver |
| fausse | — | ce sont les réglages qui composent ; la boucle n'est pas un bon dispositif pour l'idée |

Quel que soit le résultat, un R élevé ne dit rien de ce qu'on *entend* : la
coïncidence de partiels n'est pas validée comme mesure perceptive
(README.md, limite 5).

## 8. Fichiers prévus

- `boucle/boucle.py` — la boucle, les 128 trajectoires, les mesures.
- `boucle/rendu.py` — synthèse audio : une trajectoire par son, réglage
  `argmax`, τ = 4, σ = 6,83. Chaque copie sonne avec une décroissance
  exp(−temps/τ) cohérente avec les poids du modèle ; un pas = 0,45 s ;
  *t* = 0 ↔ 220 Hz. L'écoute ne fait pas partie du verdict.
- `boucle/RESULTATS.md` — résultats, sans modification de ce document.
