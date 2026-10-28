# ETAPE3-GRAPHE — le graphe-grammaire : automates, fraction de Fux, sensibilité

*Daté du 2026-06-12. États et arêtes (R1/R2/R3/R5), un automate par
(timbre × modèle d'oreille), part des règles de Fux retrouvée (SPEC §6.3),
sensibilité aux seuils τ_C et τ_F. Périmètre v1 : simultanéité, première
espèce, deux voix, compas d'une octave. Texte révisé le 2026-10-28 (ton ;
notes de relecture ; §7 ajouté) ; décisions et chiffres inchangés. Version
d'origine : `git show 9a03b9b:ETAPE3-GRAPHE.md`.*

Code : `graphe_grammaire.py` (gabarits = données, traçabilité du seuillage),
`rugosite.py` (le scalaire C, jamais mélangé à Φ), `etape3_fux.py` (harnais).
Rejouer : `python3 etape3_fux.py`.

---

## 1. Décisions de modélisation (déclarées)

1. **Grille d'états par colonne = maxima locaux de C(i)** pour ce timbre et
   ce modèle d'oreille (la méthode de Sethares pour dériver une gamme), puis
   admission R1 (C ≥ τ_C). L'unisson est un état (pic de C).
2. **Cantus en cents, identique pour tous les timbres comparés** (ici le
   cantus dorien de Fux, 12-TET) ; le contrepoint choisit ses intervalles
   dans la grille du timbre. Seul le timbre change entre les comparaisons.
3. **Φ(unisson) := +∞ par convention déclarée** (la mesure exclut la
   coïncidence d'un partiel avec lui-même ; deux voix à l'unisson sont
   considérées comme une seule). Conséquences : R2
   interdit toujours parallèle/direct vers l'unisson ; l'unisson admis est
   toujours état de frontière R3.
4. **Seuils, même règle pour tous les timbres** : τ_C = milieu du plus large
   plateau du timbre ; τ_F = même niveau relatif pour tous les timbres
   (0,226 × max Φ fini du timbre), fixé une fois sur le spectre harmonique,
   au milieu de la plage de seuils qui y reproduit Fux. Les plateaux complets
   sont rapportés (SPEC §7).
   *Note 2026-10-28 : τ_F est donc calibré pour que le cas harmonique donne
   le résultat de Fux. Ce cas ne peut plus servir de test (§7).*
5. **Traçabilité** : chaque arête supprimée garde (mouvement, Φ d'arrivée,
   τ_F, paire de partiels dominante). Exemple sur l'harmonique : l'interdit
   d'arrivée directe sur la quinte est porté par la paire (3,2) — 3ᵉ
   harmonique du grave contre 2ᵉ de l'aigu, écart 0 c ; l'octave par (2,1).

## 2. Timbre harmonique, oreille humaine (contrôle) — règles de Fux retrouvées

Grille candidate (pics de C, Sethares, roll-off 1/k) : unisson, 387 (M3), 498
(P4), **618 (≈10/7, septimal)**, 702 (P5), 814 (m6), 884 (M6), **969 (≈7/4,
septimal)**, 1200 (P8). *Pas de pic de tierce mineure* (épaule, pas maximum).

| Règle de Fux (1re espèce) | Verdict | Détail |
|---|---|---|
| F2+F3 — pas de parallèles ni de directes vers unisson/quinte/octave | retrouvée, **par calibration** | τ_F a été choisi dans la plage (largeur relative 0,16) qui donne exactement {P5, P8} (+ unisson par convention). « Pas de parallèles d'octave » tient sur une plage de 0,66, mais c'est attendu : l'octave est le maximum de Φ fini de ce timbre |
| F4 — commencer/finir sur unisson/octave | retrouvée | frontières R3 = {0, 1200}, conséquence directe de la forme de R3 (argmax Φ = octave) |
| F1 — inventaire vertical = consonances de Fux | non, à aucun seuil | meilleur recouvrement (indice de Jaccard : taille de l'intersection / taille de l'union) 0,71, pour {0, 702, 814, 884, 1200} ; écarts détaillés ci-dessous |
| F5 — préférence du mouvement contraire | imposée | forme écrite à la main (CADRAGE.md §6), pas un résultat ; v1 n'en règle que les poids |

**Écarts sur F1 :**
1. **La quarte** : maximum de C fort (0,71), donc admise dès que les tierces
   le sont. Son interdiction chez Fux ne vient pas de la rugosité. Explication
   possible, non testée : dans la pratique, la quarte est traitée par rapport
   à la basse, ce que le modèle v1 ne représente pas.
2. **Les intervalles septimaux** (618 ≈ 10/7, 969 ≈ 7/4) : maxima de C pour
   un timbre 1/k à 10 partiels, absents du système de Fux. Cela peut venir du
   modèle de timbre choisi (10 partiels, amplitudes 1/k) autant que d'un
   filtrage historique ; on ne peut pas trancher ici.
3. **La tierce mineure manquante** (pas de maximum local) : la courbe C est
   trop plate dans cette zone pour ce timbre. Limite du modèle de Sethares tel
   qu'utilisé ici.

Déviations du chemin légal vs la pratique (résidu côté arêtes) : unissons en
milieu de pièce (Fux les réserve aux extrémités — règle absente des gabarits
v1) ; usage des états septimaux. À retenir pour l'étape 4 (écoute) : c'est là
qu'on entendra si ces « légalités » fonctionnent.

## 3. Cloche Westerkerk (spectre publié), oreille humaine

Grille candidate : unisson, **307 (m3 de cloche)**, 395 (M3), 702 (P5), 809
(m6), **886 (M6 de cloche — 2ᵉ consonance du timbre, C=0,94)**, 1020 (m7),
1200 (P8). Cohérence externe : Harrison & MacConnachie trouvent M3 devenue
dissonante sur carillon — notre 395 est le plus faible pic (C=0,452) ; la
force de la M6 vient de la paire nominal/tierce de la cloche.

Automate illustratif (mêmes règles de seuils que le contrôle) :

| | Harmonique | Cloche Westerkerk |
|---|---|---|
| États (R1) | 0, 387, 498, 618, 702, 814, 884, 969, 1200 | 0, **307**, 395, 702, 809, **886**, 1020, 1200 |
| Interdits de parallèles (R2) | **0, 702, 1200** | **0, 307, 886** |
| Frontières (R3) | **0, 1200** | **0, 307** |

Au seuil déclaré, les interdits de parallèles passent de {unisson, quinte,
octave} à {unisson, tierce de cloche, sixte de cloche}, et les frontières
(début et fin) deviennent l'unisson ou la tierce de cloche.

*Note 2026-10-28 : ce résultat dépend du seuil. L'ensemble {0, 307, 886} ne
tient que pour τ_F ∈ [0,224 ; 0,346], et le seuil déclaré (0,226) est à 0,002
du bord inférieur, sous lequel quinte et octave redeviennent interdites
(§7). Seul l'interdit à 307 c est robuste. Rien n'indique encore que ces
interdits correspondent à ce qu'on entend.*

**Fait structurel (formulation corrigée le 2026-06-12, voir note)** : aux
seuils déclarés, le cantus de Fux n'a aucune réalisation légale dans
l'automate v1 de la cloche, alors que son miroir en a une (unisson · P5 · m3 ·
unisson · P5 · unisson · P5 · unisson · P5 · m3 · unisson). Matrice de
contrôle complète (chemin légal ?) :

| | cantus de Fux | cantus miroir |
|---|---|---|
| grammaire harmonique | OUI | OUI |
| grammaire cloche (v1) | **NON** | OUI |

**Note de correction (2026-06-12)** — la première rédaction concluait « le
matériau mélodique est timbre-relatif » ; c'était surinterprété. Le balayage montre que le rejet est **indépendant de τ_F**
(il tient de τ_F=0,05 à 1,20) : ce n'est donc pas le paysage de fusion R2 de
la cloche qui rejette le cantus. Le mécanisme réel est la conjonction de
trois choix v1 : (i) **R3-argmax strict** — la frontière de la cloche est
basse dans l'octave (307 c) ; (ii) **la convention Φ(unisson)=+∞** — toute
arrivée parallèle/directe à l'unisson est tuée, et en cadence descendante
l'unisson n'est approchable par aucun mouvement contraire ; (iii) **l'espace
d'action v1** — contrepoint au-dessus, compas ≤ octave, pas d'équivalence
d'octave. Une cadence descendante ne peut conclure sur un état de frontière
que par mouvement contraire depuis EN dessous ; sous 307 c il n'y a que
l'unisson, lui-même inaccessible. La grammaire harmonique échappe au problème
parce que sa frontière (l'octave) est haute — l'arrivée M6→P8 par mouvement
contraire est précisément la clausule classique.

Énoncé retenu : dans v1, la grammaire dérivée de la cloche n'admet pas de
cadence descendante (sa conclusion naturelle est ascendante,
vers la tierce-de-cloche) — conséquence dérivée, testable à l'oreille à
l'étape 4. Ce qui dissoudrait le rejet, à tester comme variantes déclarées :
un R3 adouci (frontière = états à Φ ≥ fraction du max : 886 c entrerait, et
la cadence descendante 1020→886 par contraire existerait), un compas de
douzième, ou la voix de contrepoint EN dessous du cantus. L'énoncé général
« un cantus écrit pour un timbre peut être rejeté par la grammaire d'un
autre » reste vrai comme possibilité démontrée dans v1, pas comme fait sur
les cloches.

## 4. Sensibilité : règles robustes / fragiles (extraits des plateaux)

- **Robustes** : « pas de parallèles d'octave » (harmonique, plateau relatif
  0,66 ; attendu, voir §2) ; « l'interdit cloche contient la tierce-de-cloche » (plateau 0,62 —
  c'est le dernier interdit à disparaître quand τ_F monte) ; frontières
  harmoniques {0, 1200} (stables sur tout τ_C où l'octave est admise).
- **Moyennes** : {P5, P8} exactement (0,16) ; {m3, M6} de cloche exactement
  (0,12).
- **Fragiles** : l'inventaire F1 exact (n'existe à aucun τ_C) ; la frontière
  R3 de la cloche bascule 307 ↔ 886 selon τ_C (la tierce-de-cloche n'est un
  état que si τ_C < 0,452 ; au-dessus, c'est la sixte qui devient à la fois
  frontière et premier interdit), comme le maximum de Φ à l'étape 2 dépendait
  du profil d'amplitudes.

## 5. Ce que l'étape ne conclut pas

- R5 est imposée : la préférence pour le mouvement contraire est posée, pas
  dérivée. Il faudrait un autre principe que la fusion pour l'expliquer.
- Les chemins légaux n'ont pas encore été écoutés. « Correct selon la grammaire » vs
  « fonctionne à l'oreille » est exactement l'étape 4, et c'est là que les
  résidus ci-dessus deviennent des données.
- La grammaire cloche hérite des nuances de l'étape 2 (profil d'amplitudes →
  hiérarchie des pics Φ) ; les plateaux en absorbent une partie, pas tout.

## 6. Langage

L'étape 3 est restée en Python, comme le reste du projet.

## 7. Addendum daté — 2026-10-28 : calibration et marge de la cloche

- Le résultat « F2+F3 : OUI » sur l'harmonique est **par construction** :
  τ_F a été fixé au milieu de la fenêtre qui le produit (§1.4). Il ne compte
  pas comme prédiction.
- Sur la cloche, l'ensemble d'interdits {0, 307, 886} tient pour
  τ_F ∈ [0,224 ; 0,346]. La valeur déclarée 0,226 est à **0,002** du bord
  inférieur, sous lequel P5 et P8 redeviennent interdites
  (`sensibilite_seuil.py`). Seul l'interdit à 307 c est robuste au seuil.
