# DIAGRAMME-PHASE — balayage de l'inharmonicité

*Le nom du fichier est historique. « Diagramme de phase » désigne ici
seulement l'ensemble des interdits calculé le long d'un paramètre de spectre,
et « bifurcation » une valeur où cet ensemble change de taille ; rien
n'indique qu'il s'agisse de transitions au sens physique.*

*Le §1 a été commité avant tout calcul (commit `b3be72f`, sans code ni
résultat) ; les §2 et suivants dans un commit séparé. Texte révisé le
2026-10-28 (ton ; notes de relecture marquées « Note 2026-10-28 ») ;
prédictions et chiffres inchangés. Version d'origine :
`git show 9a03b9b:DIAGRAMME-PHASE.md`.*

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
3. **Continu.** On peut donc chercher des valeurs de `B` où une règle
   apparaît ou disparaît.

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

- **D2 — l'octave étirée.**
  Quand `B` croît, le pic de Φ voisin de 1200 c se déplace vers l'**aigu**
  (> 1200 c), de quelques cents dès `B ≈ 10⁻⁴`. *C'est le phénomène d'octave
  étirée des pianos (courbe de Railsback), documenté depuis 1938 et jamais
  entré dans ce modèle : ni Φ, ni ses constantes, ni aucune étape antérieure
  n'ont vu de donnée d'accordage. Si le modèle le produit, c'est une
  validation externe de Φ ; s'il produit l'inverse (octave comprimée), c'est
  une réfutation nette.*

  *Note 2026-10-28 : D2 n'était pas risquée. Pour une corde raide, le 2ᵉ
  partiel de la voix grave est au-dessus de 2 f₀, si bien que sa coïncidence
  avec la fondamentale de la voix aiguë se produit au-delà de 1200 c. Toute
  mesure de coïncidence de partiels donne ce résultat ; c'est d'ailleurs
  l'explication connue de l'étirement des octaves de piano. D2 vérifie
  l'implémentation, pas Φ comme modèle de fusion.*

- **D3 — la grammaire est en escalier, pas continue.** Il existe au moins une
  valeur de `B` où l'ensemble des interdits de parallèles change (composition
  ou cardinalité), en restant stable de part et d'autre. *C'est la définition
  opératoire d'une bifurcation. Si l'ensemble des interdits varie de façon
  lisse et sans plateaux, ou ne varie pas du tout sur toute la plage, la
  notion de bifurcation ne s'applique pas à ce système et le §7 du cadrage d'origine
  tombe.*

  *Note 2026-10-28 : le critère de bifurcation a été redéfini après un
  premier comptage (§2.3), et le résultat dépend du seuil (§2.7).*

- **D4 — la limite raide : disparition de l'octave.** À grand `B`, le spectre
  tend vers `f_n ∝ n²`, dont les coïncidences sous transposition tombent aux
  **carrés de rationnels simples** — 16/9 (996 c), 25/16 (766 c), 81/64
  (406 c) — et non aux rationnels simples eux-mêmes. Comme `2` n'est pas le
  carré d'un rationnel, **l'interdit de parallèles d'octave doit disparaître
  entièrement** dans cette limite.

  *Note 2026-10-28 : comme D2, D4 découle directement de la forme du spectre
  (f_n ∝ n²) ; elle ne teste pas la perception.*

### 1.4 Ce qui serait réfuté

| Observation | Conséquence |
|---|---|
| D1 tombe | balayage mal implémenté ; rien d'autre n'est interprétable |
| D2 donne une octave **comprimée** | Φ prédit l'inverse d'un fait d'accordage établi → borne de validité de la métrique révélée |
| D3 tombe (pas de plateaux) | l'ensemble des interdits ne change pas par paliers sur cet axe |
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

## 2.1 D1 — ancrage bas : vérifiée

À `B = 0`, dans la configuration exacte de l'étape 3 (compas 1200 c) :
états `[0, 387, 498, 618, 702, 814, 884, 969, 1200]`, interdits
`[0, 702, 1200]`, frontières `[0, 1200]` — identiques à l'étape 3. Le balayage
est correctement branché sur la chaîne existante.

## 2.2 D2 — l'octave étirée : vérifiée

Le pic de fusion issu de l'octave, suivi par continuité, part **vers l'aigu**
dès que `B` croît :

| `B` | pic issu de l'octave | écart | contexte |
|---|---|---|---|
| 0 | 1200,00 c | 0,00 | timbre harmonique |
| 1,2·10⁻⁴ | 1200,86 c | **+0,86 c** | cordes médium d'un piano |
| 1,1·10⁻³ | 1203,40 c | **+3,40 c** | basses d'un droit |
| 1,1·10⁻² | 1227,66 c | +27,7 c | corde très raide |
| ≥ 10⁻¹ | > 1400 c | — | régime de barre |

**Ce que cela vaut.** L'étirement des octaves de piano est documenté depuis
Railsback (1938). Le modèle produit le bon signe, le bon ordre de grandeur et
la bonne dépendance à `B`. Mais, comme dit en note de D2, c'est une
conséquence arithmétique du spectre de corde raide : n'importe quelle mesure
de coïncidence de partiels le produirait, et l'étirement s'explique déjà de
cette façon, ainsi que par la minimisation de la dissonance sensorielle
(« Explaining the Railsback stretch in terms of the inharmonicity of piano
tones and sensory dissonance », JASA 138(4), 2015). C'est un contrôle de
l'implémentation, pas une validation de Φ comme modèle de fusion.

## 2.3 D3 — changements de l'ensemble des interdits : vérifiée, avec un critère redéfini

**Changement de critère après un premier résultat.** Le premier test comparait les
ensembles d'interdits arrondis au cent et comptait 57 « bifurcations ». C'était
faux : l'écrasante majorité n'étaient que la **dérive continue** des mêmes
règles (les interdits `{0, 729, 1217}` devenant `{0, 734, 1219}` quand le
spectre s'étire). Une dérive n'est pas un changement de règle. Critère
retenu, défini après avoir vu ce premier comptage : un changement du
**nombre** d'interdits. Résultat, au seuil déclaré : 8 changements, 49 pas de simple dérive, et
9 régions à nombre d'interdits constant :

| `B` (seuil) | nombre d'interdits | ensemble |
|---|---|---|
| 0 → 6,5·10⁻³ | **3** | `{unisson, ~702, ~1200}` (dérivant jusqu'à `{0, 729, 1217}`) |
| 7,7·10⁻³ | 4 | `{0, 734, 1219, 1274}` |
| 2,6·10⁻² | 3 | `{0, 799, 1264}` |
| 1,1·10⁻¹ | 5 | `{0, 649, 777, 975, 1204}` |
| 2,1·10⁻¹ | 4 | … puis 5, 4, 5, 4 |

Au seuil déclaré, le premier changement tombe à `B ≈ 7,7·10⁻³`, au-dessus
des valeurs habituelles des cordes de piano ; en dessous, les trois interdits
(unisson, quinte, octave) restent et leurs positions dérivent de quelques
cents. La région à trois interdits couvre 39 des 81 pas du balayage.

*Note 2026-10-28 : la version d'origine en tirait une lecture historique (« le
monde des cordes est tout entier dans une seule phase, celle de Fux », et
l'universalité apparente des règles s'expliquerait par là). Cette lecture
n'est pas soutenue : la position du premier changement dépend du seuil
(de 9,4·10⁻⁴ à 1,1·10⁻¹ selon τ_F, §2.7), le seuil a été calibré sur le cas
harmonique, et ce premier changement vient d'un nouvel interdit à 1274 c,
dans la zone ouverte par l'extension du compas (§2.0).*

## 2.4 D4 — limite raide : vérifiée

À `B = 10`, pics de Φ à 533, 630, **771**, **992**, 1163, 1393 c. Les repères
prédits, carrés de rationnels simples : 25/16 = **772,6 c** (pic mesuré à
1,6 c), 16/9 = **996,1 c** (pic à 4,1 c). Le troisième repère annoncé,
81/64 = 405,9 c, n'a pas de pic proche (127 c).

L'octave n'est plus dans les interdits : à `B` max, ils valent
`{0, 771, 992, 1392}`. La figure des trajectoires le montre autrement : le pic issu de la quinte quitte
702 c et converge vers 25/16 (772,6 c) ; celui issu de l'octave grimpe
au-delà du compas et se stabilise vers 1763 c ≈ 25/9 (1768 c), le carré de 5/3.

*Erratum sur le §1.3, sans effet sur la prédiction* : j'y avais écrit
« 25/16 (766 c) » — la valeur exacte est 772,6 c (erreur d'arithmétique dans la
rédaction des prédictions). Le pic mesuré est à 771 c, donc à 1,6 c de la
valeur exacte. Le §1 n'a pas été modifié, conformément à la règle du projet.

## 2.5 Figures

- `diagramme_phase_trajectoires.png` — haut : les maxima de Φ suivis par
  continuité ; bas : états (gris) et interdits (rouge) le long de `B`, au
  seuil déclaré.
- `diagramme_phase_2d.png` — nombre d'interdits de parallèles selon `B` et
  τ_F. Cette figure montre aussi que les frontières entre régions dépendent
  de τ_F.

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

## 2.7 Addendum daté — 2026-10-28 : sensibilité au seuil

La localisation de la 1re bifurcation (B ≈ 7,7e-3) et le nombre de
bifurcations (8) valent pour τ_F = 0,226. Balayé sur τ_F ∈ [0,10 ; 0,40], la
1re bifurcation se déplace de 9,4e-4 à 1,1e-1 et le nombre de bifurcations
varie de 1 à 18 (`sensibilite_seuil.py`, README.md limite 3). La lecture
« la grammaire garde sa structure sur toute la plage des cordes réelles » ne
tient donc qu'à seuil fixé. Le §1 et les verdicts D1-D4 ne sont pas modifiés.
