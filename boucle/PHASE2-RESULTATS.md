# Phase 2 — Boucle simulée v2, sans consigne : résultats

*Calculés le 2026-10-28, après les commits du protocole (`44aeaf8`) et du code
(`a4f66cb`). `PHASE2-PROTOCOLE.md` n'a pas été modifié. Rejouer :
`python3 boucle/phase2.py` (≈ 15 min), puis `python3 boucle/rendu_phase2.py`.
Données : `phase2_resultats.json` ; figure : `phase2_lignes.png` ; sons :
`sons/phase2_*.wav`.*

---

## 1. Mesure préalable : décroissance de la cloche

Sur l'enregistrement brut `12-c1.wav` (même empreinte que notre extraction de
l'étape 2) : T60 = 3,62 s, soit τ = 0,524 s. La valeur ne bouge pas sur les
12 combinaisons de réglages de la méthode testées
(`mesures/cloche_12c1_decroissance.json`). Cette mesure porte sur la
décroissance initiale (−5 à −25 dB), dominée par les partiels qui
s'éteignent vite ; le bourdon grave résonne plus longtemps.

## 2. Écarts au protocole

1. **Silences.** Cas non prévu : avec τ = 1,5 s, les copies actives finissent
   par couvrir tout le registre (à 1 ERB près ; dans le grave, 1 ERB dépasse
   1000 c). Aucune nouvelle copie ne serait alors résolue par l'oreille. Le
   code produit dans ce cas un pas sans événement. Cela concerne les sons
   synthétiques et `dent994` à τ = 1,5 s : 155 à 174 pas de silence sur 576 par
   son, soit environ 29 %. Aucun silence avec τ ≈ 0,5 s.
2. **Comparaison des réglages pour R.** Le τ mesuré de la cloche fait partie
   du son, pas des réglages : deux trajectoires sont « au même réglage »
   quand elles ont la même règle et la même période, et le même τ sauf si
   l'une a un τ mesuré. Ce point n'était pas précisé au protocole.
3. **Pas de secours** (maxima tous exclus, mais grille non couverte) : 59 au
   total, répartis sur les sons synthétiques et `dent994`.

## 3. Verdicts

| Prédiction | Résultat | Verdict |
|---|---|---|
| Q1 — lignes plus longues à T = 200 qu'à 100 ms, pour chaque son (variante A) | vrai pour 7 sons sur 8 ; faux pour `dent994` (2,17 → 1,68) | **non vérifiée** |
| Q2 — plus de la moitié des intervalles > 1200 c pour au moins 6 sons sur 8 (`argmax`) | 5 sons sur 8 (`cloche12c1` 0,33 ; `dent994` 0,50 ; `aleatoire` 0,27) | **non vérifiée** |
| Q3 — variante B : moins de 20 % des événements dans une ligne ≥ 4, pour tous les sons ; variante A à 200 ms : au moins un son au-dessus de 20 % | B : 0 % partout ; A à 200 ms : 17 à 97 % | **vérifiée** |
| Q4 — R_traj ≥ 1,5 avec p < 0,01 ; R_lignes < R_traj | R_traj = 1,42 (p < 0,001) ; R_lignes = 0,94 | **non vérifiée** |

**Lecture prévue (§6 du protocole).** R_traj est sous le seuil de 1,5. Sa
valeur est pratiquement celle de l'étape 1 (1,44) : le remplacement des
choix arbitraires n'a ni renforcé ni affaibli la dépendance au son. Elle
reste significative (le son compte plus que les réglages) mais modeste.
R_lignes est inférieur à 1 : **pour les lignes, ce sont les réglages,
surtout la période T, qui comptent plus que le son.**

**Critère de sortie de la phase (PLAN.md)** : « R significativement supérieur
à 1, avec un seuil fixé dans le protocole ». Le seuil fixé était 1,5 ; il
n'est pas atteint.

## 4. Mesures des lignes

Part des événements dans une ligne d'au moins 4 événements, variante A
(moyenne sur les règles et τ) :

| Son | T = 100 ms | T = 200 ms |
|---|---|---|
| harm | 0,32 | 0,78 |
| cloche | 0,32 | 0,91 |
| cloche12c1 | 0,51 | 0,97 |
| corde1e-3 | 0,25 | 0,71 |
| corde1e-2 | 0,30 | 0,73 |
| corde1e-1 | 0,41 | 0,68 |
| dent994 | 0,40 | 0,17 |
| aleatoire | 0,49 | 0,82 |

En variante B (frontière de fission, 1 demi-ton), aucune ligne de plus d'un
événement ne se forme : les pas sont toujours bien plus grands qu'un
demi-ton.

**Ce que ces lignes valent.** À T = 200 ms, la frontière de cohérence corrigée
pour sons complexes (période effective 260 ms) vaut 24 demi-tons. Presque
tous les pas de la boucle (pas médian proche d'une octave) sont en dessous.
Les lignes à ce tempo traduisent donc surtout la largeur de la frontière à
tempo lent, que n'importe quelle suite de sauts de moins de deux octaves
franchirait. R_lignes < 1 va dans le même sens. Par ailleurs, la période
effective de 260 ms dépasse la plage où la formule a été mesurée sur des sons
purs (jusqu'à 200 ms), même si les mesures sur sons complexes de van Noorden
(p. 73) vont jusqu'à 300 ms environ : c'est une extrapolation partielle.

## 5. Observation exploratoire : le contour a changé

Non prédite ; rapportée comme piste. Le zigzag de l'étape 1 a laissé place
à des montées et descentes à travers le registre (figure `phase2_lignes.png`) :

| Son | Changements de direction, étape 1 (`argmax`) | Phase 2 (`argmax`) | Phase 2 (`tirage`) |
|---|---|---|---|
| harm | 0,66 | 0,33 | 0,55 |
| cloche | 0,74 | 0,56 | 0,53 |
| cloche12c1 | 0,66 | 0,41 | 0,57 |
| corde1e-3 | 0,68 | 0,43 | 0,55 |
| aleatoire | 0,52 | 0,33 | 0,59 |

- Avec `argmax`, les changements de direction diminuent nettement. Avec
  `tirage`, ils restent proches de 0,5, la valeur d'une marche au hasard.
- Le pas médian reste proche de l'octave (1190 à 1410 c, sauf `aleatoire`,
  987 c, et `dent994`, 2781 c). Pour le son harmonique, ce sont des arpèges
  d'octaves (0, 1200, 2400, 3600, 4800 c), pas des mouvements conjoints.
- Explication probable, à vérifier : le registre est plus large qu'à
  l'étape 1, et l'exclusion d'1 ERB autour des copies récentes pousse les
  nouvelles copies à continuer dans la même direction tant que la place est
  libre. Ce serait alors un effet du mécanisme d'exclusion plus que du son.

## 6. Sensibilité (règle `argmax`, T = 150 ms)

La part d'événements en lignes (variante A) varie beaucoup avec l'exclusion
et W_MIN. Pour `corde1e-2`, elle va de 0,00 (exclusion 1,5 ERB) à 0,82
(0,5 ERB) ; pour `aleatoire`, de 0,20 (W_MIN 0,01) à 0,98 (W_MIN 0,1). Les
lignes dépendent donc fortement de deux réglages dont l'un (W_MIN) n'a pas de
fondement psychoacoustique établi. Détail dans `phase2_resultats.json`.

## 7. Ce que cela veut dire

- La dépendance de la trajectoire au son (R ≈ 1,4) survit au remplacement des
  choix arbitraires de l'étape 1, sans se renforcer.
- Des lignes, au sens du modèle d'oreille, apparaissent à tempo lent ; mais
  elles dépendent davantage du tempo, de l'exclusion et de W_MIN que du son.
  Le résultat « le son produit des lignes » n'est pas établi.
- Le contour a changé de nature, probablement sous l'effet du mécanisme
  d'exclusion.
- Rien de tout cela n'a été écouté. Les sons `sons/phase2_*.wav` sont faits
  pour cette écoute.
