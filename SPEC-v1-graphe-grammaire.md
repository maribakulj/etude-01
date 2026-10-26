# Spec v1 — Le graphe-grammaire et ses prédictions

*Document d'enregistrement. Sa valeur tient à ce qu'il soit écrit AVANT tout calcul et non révisé après. Toute modification postérieure au premier test doit être datée et justifiée séparément — on ne réécrit pas une prédiction après avoir vu le résultat.*

**Périmètre v1 : contrepoint de simultanéité, première espèce, deux voix.** Note contre note, un seul intervalle vertical par temps. Ce périmètre est choisi parce qu'il est *purement simultané* : pas de dissonance à préparer/résoudre (tout vertical est consonant), donc aucune règle séquentielle n'est requise. C'est exactement le domaine où le mécanisme « fusion par préservation de symétrie » est le plus fort et le mieux fondé. Le séquentiel (conduite mélodique interne, préparation/résolution des espèces supérieures) est **hors périmètre**, marqué comme extension.

---

## 1. Les deux scalaires que le spectre compile

Tout part de deux fonctions dérivées du spectre, distinctes et à ne jamais confondre. Pour un timbre donné et un récepteur donné, et pour chaque intervalle `i` :

- **C(i) — consonance verticale.** Inverse de la rugosité (battements entre partiels voisins). Dépend de la bande critique → **dépend du récepteur**. C'est l'axe « ça sonne lisse ou rêche ». Acquis type Sethares.
- **Φ(i) — tendance à la fusion.** Harmonicité du spectre combiné : quand les deux voix sonnent à l'intervalle `i`, à quel point l'union de leurs partiels (voix A + voix B transposée de `i`) se laisse décrire par une fondamentale commune. Élevé = les deux voix se fondent en un seul objet. **Le substrat (les pics de coïncidence) est arithmétique, indépendant du récepteur ; seule la fenêtre de tolérance qui décide quelles coïncidences "comptent" dépend du récepteur.**

**Règle d'hygiène absolue :** la rugosité `C` n'entre PAS dans la métrique de fusion. Deux sons rugueux restent souvent perçus comme deux ; rugosité et fusion sont des mécanismes dissociés. `C` gouverne quels états existent (axe vertical) ; `Φ` gouverne quels mouvements fusionnent les voix (axe contrapuntique).

---

## 2. Les états du graphe

> **État = (intervalle vertical, qualifié par son statut de consonance C pour ce timbre).**

Le treillis se déroule sur un cantus firmus de N notes : N colonnes, chaque colonne = les intervalles verticaux possibles au-dessus de la note de cantus à cet instant.

Décision explicite : l'état ne mémorise PAS à lui seul le mouvement entrant. Le mouvement est porté par l'**arête** (cf. §3). La règle anti-parallèle se vérifie donc sur le triplet (intervalle précédent, mouvement, intervalle courant), ce que la structure en treillis fournit naturellement (chaque arête connaît sa colonne de départ et d'arrivée).

Existence d'un état (gate de consonance) :
- **R1 — Gate vertical.** Un intervalle `i` n'est un état admissible que si `C(i) ≥ τ_C`. En première espèce, tout vertical doit être consonant ; les intervalles rêches pour ce timbre n'ont pas d'état. *C'est R1 qui définit la liste des nœuds par colonne, et c'est la part « déjà acquise » (dérivation de la hiérarchie de consonance).*

---

## 3. Les arêtes et leurs gabarits

Une **arête** relie un état de la colonne `t` à un état de la colonne `t+1`. Comme la note de cantus est donnée à chaque temps, l'arête est entièrement déterminée par le mouvement de la voix de contrepoint. Le couple (mouvement du cantus imposé, mouvement du contrepoint choisi) fixe le **type de mouvement** : parallèle / direct (similaire) / contraire / oblique.

Les gabarits ci-dessous **génèrent ou suppriment** les arêtes. Une arête supprimée n'existe pas dans le graphe (elle n'est pas « barrée » ; on peut la matérialiser séparément pour l'analyse, comme adjacence sans arête).

- **R2 — Règle de sélection anti-fusion (LE gabarit porteur de prédiction).**
  Une arête en mouvement **parallèle ou direct** arrivant à un intervalle `i` tel que `Φ(i) ≥ τ_F` est **supprimée**.
  *Justification : mouvement parallèle vers un intervalle de forte coïncidence = mouvement préservant la symétrie spectrale → les orbites de partiels restent confondues → fusion → perte d'indépendance des voix. C'est la généralisation spectrale de « pas de quintes/octaves parallèles ».*
  Raffinement noté, non implémenté en v1 : le mouvement direct (similaire) vers haut-Φ peut recevoir un seuil distinct, plus permissif que le parallèle strict (analogue des « quintes directes/cachées », tolérées sous conditions).

- **R3 — Contraintes de frontière (dérivées, pas imposées).**
  Premier et dernier état contraints à `argmax Φ` (l'intervalle le plus fusionnel = le plus stable/résolu).
  *Conséquence dérivée : la pièce commence et finit sur l'intervalle le plus « parfait » de ce timbre. Sur timbre harmonique → octave/unisson, ce qui recouvre la règle classique. Sur un autre timbre → l'intervalle que SON spectre désigne comme le plus fusionnel.*

- **R5 — Préférence de type de mouvement (graduée, pondère les arêtes survivantes).**
  Parmi les arêtes admissibles, le mouvement contraire/oblique est préféré ; le mouvement direct vers consonance forte est pénalisé sans être interdit. Implémenté comme poids d'arête, pas comme suppression. *Recouvre la préférence classique pour le mouvement contraire.*

Hors périmètre v1, à marquer comme extensions :
- **R6 (séquentiel-accumulatif) :** limite du nombre de tierces/sixtes parallèles consécutives. C'est aussi de l'anti-fusion, mais *accumulée dans le temps* → nécessite un état à mémoire, donc séquentiel. Différé.
- **Conduite mélodique interne, sauts, ambitus, croisements :** séquentiel et/ou contraintes de registre. Différé.

---

## 4. Ce que le graphe produit

- Un **automate par (timbre × récepteur)**. Le timbre harmonique compile vers un graphe ; la boîte à musique vers un autre. La comparaison des deux graphes EST le résultat « le contrepoint dépend du son ».
- Une composition légale = un **chemin** dans le graphe.
- Mesures lisibles directement sur la structure, sans aucune 3D : nombre d'états par colonne, nombre d'arêtes, ensemble des arêtes supprimées par R2, position de `argmax Φ`.

---

## 5. PRÉDICTIONS (enregistrées avant calcul)

### Bloc A — Timbre harmonique + récepteur humain (cas de contrôle : doit reproduire le connu)

- **P1.** `C(i)` désigne comme consonants : octave, quinte, quarte, tierces et sixtes (majeures/mineures). *Recouvre l'ensemble de consonance classique. Sanity check.*
- **P2 (validation centrale).** `Φ(i)` est maximal à l'unisson et l'octave, puis à la quinte. Donc R2 supprime les arêtes parallèles/directes vers octave et quinte → **on retrouve « pas de quintes ni d'octaves parallèles »**. *Si cette prédiction tombe, le décompilateur est validé sur le cas connu.*
- **P3.** R3 place début/fin sur octave/unisson. *Recouvre la règle de frontière classique.*

### Bloc B — Boîte à musique (poutre encastrée, modes ≈ 1 : 6,27 : 17,55) + récepteur humain

- **P4.** L'ensemble de consonance `C(i)` se déplace par rapport au Bloc A. Direction prédite (cohérente avec Harrison & MacConnachie sur timbre de cloche) : des intervalles habituellement dissonants peuvent devenir lisses et inversement (p. ex. tierce mineure ↗ consonance, tierce majeure ↘). 
- **P5 (la prédiction décisive).** `argmax Φ` se déplace : l'intervalle le plus fusionnel n'est PLUS la quinte/octave, mais l'intervalle où les modes inharmoniques se réalignent le mieux sous transposition. **Donc l'« intervalle de parallèles interdit » de R2 se déplace** vers cet intervalle. Prédiction forte et risquée : même l'octave peut perdre son statut fusionnel privilégié, car doubler la fréquence ne réaligne pas {1 ; 6,27 ; 17,55} comme elle réaligne {1 ; 2 ; 3…}. *Le calcul servira à dire OÙ se place le nouveau pic ; la prédiction structurelle est qu'il se déplace et pourquoi.*

### Bloc C — Timbre harmonique, récepteur humain vs récepteur rhinolophe (le résultat épistémologique)

- **P6 (substrat vs saillance, testable).** Entre les deux récepteurs :
  - `C(i)` (rugosité) **diffère nettement** — la rugosité dépend de la bande critique, et celle du rhinolophe est radicalement non humaine.
  - `Φ(i)` (fusion) garde ses **pics co-localisés** — parce que la coïncidence de partiels est arithmétique, donc commune aux deux récepteurs ; seule la *finesse* des pics change (fenêtre de tolérance).
  - **Conséquence prédite : humain et rhinolophe sont en DÉSACCORD sur la consonance verticale mais en ACCORD sur la localisation grossière des règles de parallèles.** *Si vrai : la part « dans le signal » et la part « dans l'oreille » sont séparées et mesurées. C'est le résultat le plus original.*

---

## 6. CRITÈRES D'ABANDON / DE FALSIFICATION (écrits avant le test)

Dans l'ordre où ils doivent être vérifiés :

1. **Test de la métrique sur le cas connu.** Si, sur harmonique + humain, `Φ` ne pique PAS aux consonances parfaites (P2 échoue) → **la métrique de fusion est fausse. Arrêt. On la corrige avant tout le reste.** C'est le vrai premier contrôle : reproduire le connu avant de prétendre au neuf.

2. **Le mouvement est-il timbre-dépendant ?** Si les pics de `Φ` de la boîte à musique COÏNCIDENT avec ceux de l'harmonique (pas de déplacement, P5 échoue) → **le contrepoint n'est pas timbre-dépendant au niveau du mouvement.** Le palier scientifique « fort » tombe ; le projet se réduit à sa valeur de création (donner une grammaire jouable à des timbres sans corpus). On l'aura su en une demi-journée.

3. **Complétude du mécanisme.** Sur harmonique + humain, quelle fraction des règles de première espèce de Fux (R1, R2, R3, R5 ci-dessus) est récupérée ? Si quasi nulle → le mécanisme « fusion par symétrie » est incomplet, il manque un second principe (à chercher). Si substantielle → le décompilateur fonctionne, et ce qui résiste mesure soit la convention pure, soit le périmètre séquentiel non couvert (les deux sont des résultats, pas des échecs).

4. **Séparabilité substrat/saillance.** Si, entre humain et rhinolophe, les pics de `Φ` se déplacent autant que `C` (P6 échoue) → la distinction substrat/saillance ne tient pas dans le modèle, et la thèse « grammaire de l'objet » doit être réexaminée. Résultat négatif, mais informatif.

---

## 7. Ce que ce document NE fixe pas (décisions repoussées, à dessein)

- Les valeurs numériques des seuils `τ_C`, `τ_F` : ce sont précisément les curseurs de l'analyse de sensibilité. On ne les fige pas ; on les balaye et on observe quelles règles sont robustes (stables sur la plage) vs fragiles (basculent avec le seuil).
- La forme analytique exacte de l'harmonicité combinée `Φ` (ajustement à une série, ou autocorrélation spectrale sous transposition, ou template harmonique) : à choisir au moment du calcul, mais le choix doit être déclaré et le même pour tous les timbres et récepteurs comparés.
- Le langage et l'architecture : sans objet pour le test, qui peut se faire dans n'importe quel environnement de calcul.

---

## Invariants de la spec
- Deux scalaires : `C` (vertical, dépend du récepteur) et `Φ` (fusion, substrat arithmétique + fenêtre récepteur). Jamais confondus.
- États = intervalles admis par le gate de consonance R1. Arêtes = mouvements, filtrés par R2 (anti-fusion) et R3 (frontières), pondérés par R5.
- R2 est le gabarit porteur de prédiction : il déplace l'interdit de parallèles selon le timbre.
- Un graphe par (timbre × récepteur) ; la comparaison des graphes est le résultat.
- Les prédictions du §5 et les critères d'abandon du §6 sont enregistrés avant calcul et ne se réécrivent pas après.
