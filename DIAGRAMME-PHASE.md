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
