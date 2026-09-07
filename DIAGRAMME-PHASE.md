# DIAGRAMME-PHASE — la grammaire comme fonction d'un paramètre physique continu

*Extension naturelle de l'étape 3, prévue au CADRAGE §7 (« diagramme de phase du
contrepoint au-dessus de l'espace timbral »). Ce n'est pas l'étape 5
(l'instrument), qui reste différée.*

**§1 est écrit et commité AVANT tout calcul.** L'historique git en fait foi :
le commit qui introduit ce fichier ne contient aucun code de balayage ni aucun
résultat. Les §2 et suivants sont ajoutés après, dans un commit séparé.

---

## 1. Dispositif et prédictions enregistrées (avant calcul)

### 1.1 L'axe : la corde raide

Un seul paramètre physique continu, le coefficient d'inharmonicité `B` d'une
corde raide :

```
f_n = n · f₀ · √(1 + B · n²)      n = 1..10,  amplitudes 1/n
```

Choisi pour trois raisons :

1. **Ancré aux deux bouts par des résultats déjà acquis.** À `B = 0`, la
   famille est *exactement* le timbre harmonique de contrôle des étapes 1 et 3
   (partiels `n`, roll-off `1/n`) — celui qui reproduit Fux. Quand `B` croît,
   `f_n → f₀·√B·n²`, un régime purement inharmonique de type barre.
2. **Physiquement réel et mesurable.** `B` se mesure sur de vrais instruments :
   ~10⁻⁴ pour les cordes médium d'un piano, ~10⁻³ et au-delà pour les basses
   d'un petit droit. Le diagramme fait donc des prédictions vérifiables hors
   du modèle.
3. **Continu.** C'est la condition pour qu'il y ait des *bifurcations* au sens
   du CADRAGE §7 : des valeurs de `B` où une règle apparaît ou disparaît.

### 1.2 Chaîne de calcul — inchangée, figée

Φ = coïncidence sous transposition, σ = 6,83 c (`DECISION-PHI.md`) ; C =
Sethares (`rugosite.py`) ; états, arêtes et seuils selon le schéma symétrique
déclaré à l'étape 3 (τ_C = milieu du plus large plateau ; τ_F = 0,226 × max Φ
fini du timbre). **Aucun paramètre n'est ré-ajusté pour ce balayage.**

### 1.3 Prédictions

- **D1 — ancrage bas (contrôle d'implémentation).** À `B = 0`, le diagramme
  reproduit exactement la grammaire harmonique de l'étape 3 : interdits de
  parallèles {unisson, 702, 1200}, frontières {unisson, 1200}. *Si D1 tombe,
  l'implémentation du balayage est fausse, rien d'autre n'est lisible.*

- **D2 — l'octave étirée (prédiction risquée, vérifiable À L'EXTÉRIEUR).**
  Quand `B` croît, le pic de Φ voisin de 1200 c se déplace vers l'**aigu**
  (> 1200 c), de quelques cents dès `B ≈ 10⁻⁴`. *C'est le phénomène d'octave
  étirée des pianos (courbe de Railsback), documenté depuis 1938 et jamais
  entré dans ce modèle : ni Φ, ni ses constantes, ni aucune étape antérieure
  n'ont vu de donnée d'accordage. Si le modèle le produit, c'est une
  validation externe de Φ ; s'il produit l'inverse (octave comprimée), c'est
  une réfutation nette.*

- **D3 — la grammaire est en escalier, pas continue.** Il existe au moins une
  valeur de `B` où l'ensemble des interdits de parallèles change (composition
  ou cardinalité), en restant stable de part et d'autre. *C'est la définition
  opératoire d'une bifurcation. Si l'ensemble des interdits varie de façon
  lisse et sans plateaux, ou ne varie pas du tout sur toute la plage, la
  notion de bifurcation ne s'applique pas à ce système et le §7 du CADRAGE
  tombe.*

- **D4 — la limite raide : disparition de l'octave.** À grand `B`, le spectre
  tend vers `f_n ∝ n²`, dont les coïncidences sous transposition tombent aux
  **carrés de rationnels simples** — 16/9 (996 c), 25/16 (766 c), 81/64
  (406 c) — et non aux rationnels simples eux-mêmes. Comme `2` n'est pas le
  carré d'un rationnel, **l'interdit de parallèles d'octave doit disparaître
  entièrement** dans cette limite. *Prédiction structurelle forte : un monde
  sonore où les octaves parallèles sont permises et où l'interdit se loge sur
  des intervalles sans nom dans notre solfège.*

### 1.4 Ce qui serait réfuté

| Observation | Conséquence |
|---|---|
| D1 tombe | balayage mal implémenté ; rien d'autre n'est interprétable |
| D2 donne une octave **comprimée** | Φ prédit l'inverse d'un fait d'accordage établi → borne de validité de la métrique révélée |
| D3 tombe (pas de plateaux) | pas de bifurcations : le CADRAGE §7 (diagramme de phase, « jouer le législateur ») n'a pas d'objet sur cet axe |
| Interdits identiques sur toute la plage | la grammaire ne dépend pas du timbre le long d'un axe physique réel → affaiblit P5 au-delà du cas cloche |

### 1.5 Livrables prévus

Trajectoires des pics de Φ en fonction de `B` ; diagramme de phase 2D
(`B` × τ_F) coloré par l'identité de l'ensemble des interdits, dont les
frontières entre régions sont les bifurcations ; table des bifurcations
détectées avec la règle qui bascule.

---

# 2. Résultats (calculés après le commit du §1)

Code : `famille_raide.py`, `diagramme_phase.py`. Rejouer :
`python3 diagramme_phase.py` (~20 s). Faits bruts :
`diagramme_phase_resultats.json`. Balayage : 81 valeurs, `B = 0` puis
`10⁻⁵ … 10¹` en log.

## 2.0 Modification déclarée de la chaîne

Une seule : le **compas d'analyse** passe de 1200 c (v1) à 1400 c pour le
balayage. Motif : sur un timbre dont l'octave se déplace, un compas fixé à
1200 c découperait justement le phénomène mesuré — le compas d'une octave est
une convention du monde harmonique, pas une donnée. Implémentation :
paramètre `cmax` ajouté à `graphe_grammaire.courbes` (défaut 1200 c). **Les
sorties des étapes 3 et 4 sont inchangées au bit près** (vérifié en relançant
`etape3_fux.py`). Φ, C, les seuils et le schéma symétrique de l'étape 3 : rien
d'autre n'est touché.

## 2.1 D1 — ancrage bas : **CONFIRMÉE**

À `B = 0`, dans la configuration exacte de l'étape 3 (compas 1200 c) :
états `[0, 387, 498, 618, 702, 814, 884, 969, 1200]`, interdits
`[0, 702, 1200]`, frontières `[0, 1200]` — identiques à l'étape 3. Le balayage
est correctement branché sur la chaîne existante.

## 2.2 D2 — l'octave étirée : **CONFIRMÉE**, et corroborée de l'extérieur

Le pic de fusion issu de l'octave, suivi par continuité, part **vers l'aigu**
dès que `B` croît :

| `B` | pic issu de l'octave | écart | contexte |
|---|---|---|---|
| 0 | 1200,00 c | 0,00 | timbre harmonique |
| 1,2·10⁻⁴ | 1200,86 c | **+0,86 c** | cordes médium d'un piano |
| 1,1·10⁻³ | 1203,40 c | **+3,40 c** | basses d'un droit |
| 1,1·10⁻² | 1227,66 c | +27,7 c | corde très raide |
| ≥ 10⁻¹ | > 1400 c | — | régime de barre |

**Ce que ça vaut, exactement.** L'étirement de l'octave des pianos est un fait
documenté depuis Railsback (1938) : les octaves centrales sont à peine
étirées, les extrêmes le sont jusqu'à ±30 cents. Notre modèle produit le bon
**signe**, le bon **ordre de grandeur** (moins d'un cent au médium, quelques
cents plus bas, des dizaines quand la raideur augmente), et la bonne
**dépendance** (croissante avec `B`) — alors que Φ a été figée à l'étape 1
pour des raisons entièrement étrangères (la fusion de deux voix), que ses
constantes viennent de Milne (2013), et qu'**aucune donnée d'accordage n'est
jamais entrée dans ce projet**.

*Ce n'est pas une explication nouvelle du phénomène* : l'étirement se dérive
déjà de l'inharmonicité par d'autres routes, notamment par minimisation de la
dissonance sensorielle (« Explaining the Railsback stretch in terms of the
inharmonicity of piano tones and sensory dissonance », JASA 138(4), 2015 —
c'est-à-dire par `C`, pas par `Φ`). C'est un **contrôle de cohérence externe** que la métrique
pouvait rater : une Φ mal choisie aurait donné une octave *comprimée*, ou
aucun déplacement. Elle donne le bon.

## 2.3 D3 — bifurcations : **CONFIRMÉE**, après durcissement du critère

**Correction méthodologique, à charge.** Le premier test comparait les
ensembles d'interdits arrondis au cent et comptait 57 « bifurcations ». C'était
faux : l'écrasante majorité n'étaient que la **dérive continue** des mêmes
règles (les interdits `{0, 729, 1217}` devenant `{0, 734, 1219}` quand le
spectre s'étire). Une dérive n'est pas une bifurcation. Critère durci retenu :
**une bifurcation est un changement de cardinalité** — une règle apparaît ou
disparaît. Résultat : **8 bifurcations**, 49 pas de simple dérive, et
**9 régions à nombre de règles constant** :

| `B` (seuil) | nombre d'interdits | ensemble |
|---|---|---|
| 0 → 6,5·10⁻³ | **3** | `{unisson, ~702, ~1200}` (dérivant jusqu'à `{0, 729, 1217}`) |
| 7,7·10⁻³ | 4 | `{0, 734, 1219, 1274}` |
| 2,6·10⁻² | 3 | `{0, 799, 1264}` |
| 1,1·10⁻¹ | 5 | `{0, 649, 777, 975, 1204}` |
| 2,1·10⁻¹ | 4 | … puis 5, 4, 5, 4 |

**Le fait le plus intéressant du balayage.** La première bifurcation tombe à
`B ≈ 7,7·10⁻³`, soit **un ordre de grandeur au-dessus des cordes de piano les
plus raides**. Sur toute la plage des instruments à cordes réels, la grammaire
garde donc sa **structure** — trois interdits : unisson, quinte, octave — et
seules leurs **positions** dérivent de quelques cents. La région stable
couvre 39 des 81 pas du balayage, `B` de 0 à 6,5·10⁻³.

Lecture : *le monde des cordes est tout entier dans une seule phase, et c'est
celle de Fux.* Si la grammaire du contrepoint a paru universelle pendant des
siècles, c'est peut-être que tous les instruments qui l'ont produite vivaient
du même côté de la première bifurcation. On peut nommer ce qu'il faudrait pour
en sortir : une raideur d'un ordre de grandeur au-dessus de celle d'une corde
de piano — ce que sont, précisément, les barres et les cloches.

## 2.4 D4 — limite raide : **CONFIRMÉE**

À `B = 10`, pics de Φ à 533, 630, **771**, **992**, 1163, 1393 c. Les repères
prédits, carrés de rationnels simples : 25/16 = **772,6 c** (pic mesuré à
1,6 c), 16/9 = **996,1 c** (pic à 4,1 c). Le troisième repère annoncé,
81/64 = 405,9 c, n'a pas de pic proche (127 c).

Et surtout : **l'octave a disparu des interdits** — à `B` max, ils valent
`{0, 771, 992, 1392}`. Un monde sonore où les octaves parallèles sont permises
et où l'interdit se loge sur des intervalles sans nom dans notre solfège. La
figure des trajectoires le montre autrement : le pic issu de la quinte quitte
702 c et converge vers 25/16 (772,6 c) ; celui issu de l'octave grimpe
au-delà du compas et se stabilise vers 1763 c ≈ 25/9 (1768 c), le carré de 5/3.

*Erratum sur le §1.3, sans effet sur la prédiction* : j'y avais écrit
« 25/16 (766 c) » — la valeur exacte est 772,6 c (erreur d'arithmétique dans la
rédaction des prédictions). Le pic mesuré est à 771 c, donc à 1,6 c de la
valeur exacte. Le §1 n'a pas été modifié, conformément à la règle du projet.

## 2.5 Figures

- `diagramme_phase_trajectoires.png` — haut : les pics de fusion suivis par
  continuité (le substrat) ; bas : la grammaire (états gris, interdits rouges)
  le long de `B`. On y voit d'un coup le long plateau de Fux, puis la dérive,
  puis l'éclatement.
- `diagramme_phase_2d.png` — le diagramme de phase proprement dit : nombre de
  règles anti-parallèles selon (`B`, τ_F). Les frontières de couleur sont les
  bifurcations ; la plage des pianos réels est entièrement dans une seule
  région.

## 2.6 Réserves

1. **Une seule famille spectrale.** La corde raide est un axe, pas l'espace des
   timbres. La cloche de l'étape 2 n'est pas sur cet axe (ses partiels ne
   suivent pas `n·√(1+Bn²)`) — le diagramme ne la contient donc pas.
2. **Le suivi par continuité peut sauter** quand deux pics se croisent ; un
   décrochage est visible vers `B ≈ 0,5` sur la trajectoire de l'octave.
3. **Rien n'a été écouté ici.** Les bifurcations sont calculées, pas
   entendues ; la falsification à l'oreille (étape 4) n'a porté que sur le
   couple harmonique/cloche.
4. Le rapport « écart d'octave ↔ `B` » est comparé à la littérature en ordre
   de grandeur, pas ajusté sur une courbe de Railsback mesurée.
