# Spec v1 — graphe-grammaire et prédictions

*Document enregistré avant le premier calcul (commit `9ec9fbb`, 2026-06-11).
Texte révisé le 2026-10-28 : ton, vocabulaire, et notes de relecture
ajoutées en fin de section (marquées « Note 2026-10-28 »). Le contenu des
prédictions (§5) et des critères d'abandon (§6) n'a pas été modifié.
Version d'origine : `git show 9a03b9b:SPEC-v1-graphe-grammaire.md`.*

**Périmètre v1** : deux voix, première espèce (note contre note), un seul
intervalle vertical par temps, compas d'une octave. Pas de dissonance à
préparer ni à résoudre, donc pas de règle séquentielle. Le séquentiel
(conduite mélodique, espèces supérieures) est hors périmètre.

---

## 1. Les deux quantités calculées à partir du spectre

Pour un timbre, un modèle d'oreille et un intervalle `i` :

- **C(i), consonance verticale** : l'opposé de la rugosité (battements entre
  partiels proches). Dépend de la largeur des bandes critiques, donc du
  modèle d'oreille. Modèle de Sethares.
- **Φ(i), tendance à la fusion** : mesure de coïncidence entre les partiels
  de la voix A et ceux de la voix B transposée de `i`. Élevée = beaucoup de
  partiels coïncident. Les positions des maxima ne dépendent que du spectre ;
  la tolérance qui décide si deux partiels « coïncident » représente
  l'oreille. (La forme exacte a été fixée à l'étape 1, `DECISION-PHI.md`.)

La rugosité C n'entre pas dans Φ. Motif : deux sons rugueux restent souvent
entendus comme deux ; rugosité et fusion sont traitées comme des mécanismes
distincts. C décide quels intervalles sont admis ; Φ décide quels mouvements
sont interdits.

## 2. Les états

État = un intervalle vertical admis pour ce timbre. Le graphe se déroule sur
un cantus firmus de N notes : N colonnes, chacune contenant les intervalles
possibles au-dessus de la note du cantus.

Le mouvement est porté par l'arête, pas par l'état : la règle anti-parallèle
se vérifie sur (intervalle précédent, mouvement, intervalle courant).

- **R1 — admission.** Un intervalle `i` est un état si `C(i) ≥ τ_C`.

## 3. Les arêtes et les règles

Une arête relie un état de la colonne `t` à un état de la colonne `t+1`. Le
mouvement du cantus étant donné, l'arête fixe le type de mouvement :
parallèle, direct, contraire ou oblique.

- **R2 — interdit de fusion.** Une arête en mouvement parallèle ou direct qui
  arrive sur un intervalle `i` avec `Φ(i) ≥ τ_F` est supprimée.
  Motif supposé : deux voix qui avancent ensemble vers un intervalle où
  beaucoup de partiels coïncident risquent d'être entendues comme une seule.
  Sur un spectre harmonique, cela correspond à « pas de quintes ni d'octaves
  parallèles ». Non implémenté : un seuil distinct, plus permissif, pour le
  mouvement direct.
- **R3 — début et fin.** Premier et dernier état = `argmax Φ`. Sur un spectre
  harmonique, cela donne l'octave ou l'unisson, comme la règle classique.
- **R5 — préférence de mouvement.** Le mouvement contraire et oblique est
  favorisé, le mouvement direct vers une consonance forte pénalisé (poids
  d'arête, pas suppression).

Hors périmètre v1 : limite du nombre de tierces ou sixtes parallèles
consécutives (demande une mémoire, donc du séquentiel) ; sauts, ambitus,
croisements.

*Note 2026-10-28 : les formes de R1, R2, R3 et R5 sont écrites à la main. Le
système calcule seulement où elles s'appliquent pour un spectre donné.*

## 4. Ce que le graphe produit

- Un automate par (timbre × modèle d'oreille). La comparaison des automates
  montre en quoi les règles calculées diffèrent d'un timbre à l'autre.
- Une réalisation légale du contrepoint = un chemin dans le graphe.
- Mesures lisibles directement : états par colonne, arêtes, arêtes
  supprimées par R2, position de `argmax Φ`.

## 5. Prédictions (enregistrées avant calcul)

### Bloc A — timbre harmonique, oreille humaine (cas de contrôle)

- **P1.** C(i) désigne comme consonants : octave, quinte, quarte, tierces et
  sixtes.
- **P2.** Φ(i) est maximale à l'unisson et à l'octave, puis à la quinte. R2
  supprime donc les arêtes parallèles et directes vers octave et quinte, ce
  qui correspond à « pas de quintes ni d'octaves parallèles ».
- **P3.** R3 place le début et la fin sur l'octave ou l'unisson.

*Note 2026-10-28 : le texte d'origine de P2 disait « Si cette prédiction
tombe, le décompilateur est validé sur le cas connu ». C'était une erreur :
il fallait lire « invalidé », comme le confirme le §6.1.*

### Bloc B — boîte à musique (modes ≈ 1 : 6,27 : 17,55), oreille humaine

- **P4.** L'ensemble des intervalles consonants C(i) change par rapport au
  bloc A. Direction attendue, par analogie avec Harrison & MacConnachie sur
  les cloches : certains intervalles habituellement dissonants peuvent
  devenir plus consonants, et inversement (par exemple tierce mineure plus
  consonante, tierce majeure moins).
- **P5.** `argmax Φ` change : l'intervalle de fusion maximale n'est plus
  l'octave ou la quinte, mais celui où les modes inharmoniques coïncident le
  mieux après transposition. L'intervalle interdit en parallèle par R2 change
  donc aussi. L'octave elle-même peut perdre sa place, puisque doubler la
  fréquence n'aligne pas {1 ; 6,27 ; 17,55} comme {1 ; 2 ; 3…}. Le calcul
  dira où se trouve le nouveau maximum ; la prédiction est seulement qu'il se
  déplace.

*Note 2026-10-28 : pour un spectre nettement inharmonique, le déplacement des
maxima de Φ est presque garanti par l'arithmétique. P5 était donc une
prédiction peu risquée.*

### Bloc C — timbre harmonique, oreille humaine contre oreille à bandes étroites

- **P6.** Entre les deux modèles d'oreille, C(i) diffère nettement, tandis que
  les maxima de Φ restent aux mêmes positions (seule leur largeur change).
  Humain et autre récepteur seraient donc en désaccord sur la consonance mais
  d'accord sur la position des interdits de parallèles.

*Note 2026-10-28 : P6 est vraie par construction, puisque changer la
tolérance de Φ change la largeur de ses pics, pas leur centre
(CADRAGE.md §5). Le second récepteur (désigné « rhinolophe » dans la version
d'origine) était un simple rétrécissement de bande, pas un modèle de
l'audition d'une chauve-souris.*

## 6. Critères d'abandon (enregistrés avant le test)

1. **Cas connu.** Si, sur l'harmonique avec oreille humaine, Φ ne culmine pas
   aux consonances parfaites (P2 échoue), la mesure de fusion est fausse. On
   la corrige avant toute autre chose.
2. **Dépendance au timbre.** Si les maxima de Φ de la boîte à musique
   coïncident avec ceux de l'harmonique (P5 échoue), les interdits de
   mouvement ne dépendent pas du timbre dans ce modèle. Le projet se réduit
   alors à un outil de composition.
3. **Part de Fux retrouvée.** Sur l'harmonique, quelle fraction des règles de
   première espèce de Fux est retrouvée par R1, R2, R3, R5 ? Si presque
   aucune, il manque au modèle autre chose que la fusion. Si une part
   importante, ce qui manque indique soit une convention, soit le
   séquentiel non couvert.
4. **Séparation spectre / oreille.** Si, entre les deux modèles d'oreille, les
   maxima de Φ bougent autant que ceux de C (P6 échoue), la séparation entre
   ce qui dépend du spectre et ce qui dépend de l'oreille ne tient pas dans
   le modèle.

*Note 2026-10-28 : le critère 3 dépend de τ_F, qui a ensuite été choisi pour
retrouver Fux (ETAPE3-GRAPHE.md §1.4). Son résultat n'est donc pas
informatif sur l'harmonique.*

## 7. Ce que ce document ne fixe pas

- Les valeurs de τ_C et τ_F : on les fait varier pour voir quelles règles
  tiennent sur une large plage et lesquelles basculent.
- La forme exacte de Φ (ajustement à une série harmonique, coïncidence sous
  transposition, ou gabarit harmonique) : à choisir au moment du calcul, à
  déclarer, et identique pour tous les timbres comparés.
- Le langage de programmation.
