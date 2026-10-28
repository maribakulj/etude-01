# Plan de développement : de la boucle simulée au prototype

*Rédigé le 2026-10-28, après l'étape 1 (`RESULTATS.md`). Ce plan peut
évoluer ; chaque modification sera datée en fin de document. Les durées sont
des estimations grossières, à réviser à la fin de chaque phase.*

---

## 1. Objectifs

Construire un système qui traite un son comme ce qui détermine sa propre
évolution, et qui produit à partir de lui :

1. **une mélodie**, c'est-à-dire des suites de hauteurs entendues comme des
   lignes ;
2. **une polyphonie**, c'est-à-dire plusieurs lignes entendues comme
   distinctes ;
3. **une évolution du timbre**, celle du mélange sonore lui-même.

Le système doit exister en deux versions :
- **boucle simulée**, où tout passe par le calcul ;
- **boucle acoustique**, où le son passe réellement par un haut-parleur, une
  pièce et un micro.

Il doit tourner dans deux régimes :
- **sans consigne**, où la seule chose qui guide l'évolution est la relation
  entre le son et ce qui sonne déjà ;
- **exploratoire**, avec une seule consigne déclarée : aller vers ce qui n'a
  pas encore été entendu.

Le prototype final est un instrument : on lui donne un son (un fichier, ou un
son joué au micro), et il le déploie en temps réel.

## 2. La politique « zéro règle arbitraire »

### 2.1 Ce qui est interdit

Toute règle venant de la théorie musicale : gamme, tempérament, mode,
intervalles permis ou interdits, rythme, mètre, forme, cadence, règle de
conduite des voix. Aucune de ces notions n'apparaît dans le code.

### 2.2 Ce qui est permis, et seulement cela

Chaque nombre et chaque mécanisme du système doit relever de l'une de ces
quatre sources :

| Source | Exemple | Exigence |
|---|---|---|
| **Le son** | partiels, amplitudes, durée de résonance mesurée | mesuré ou publié, avec sa provenance |
| **L'oreille** | largeur des bandes critiques, seuil de séparation de deux notes successives | une donnée psychoacoustique publiée, citée, et reproduite par un test du code |
| **La consigne** | « aller vers le non-entendu » | déclarée comme un choix, jamais présentée comme un fait |
| **Un choix technique inévitable** | pas de la grille de calcul | accompagné d'une analyse de sensibilité montrant qu'il ne change pas les conclusions |

Un paramètre qui ne rentre dans aucune case est retiré, ou devient un objet
d'étude explicite.

### 2.3 Ce que cette politique ne peut pas garantir

Le modèle de l'oreille reste un modèle : il simplifie, et ses composants
peuvent être faux pour des sons inharmoniques (c'est déjà le cas de Φ, non
validé comme mesure de fusion). La règle de transition de la boucle est
elle-même un mécanisme ; on ne peut pas l'éliminer, seulement mesurer son
influence. C'est le rôle du critère « le son compte plus que les réglages »
(§5).

### 2.4 Le registre : la politique rendue vérifiable

Tous les paramètres sont définis dans un seul module, `registre.py`. Chacun
porte sa valeur, sa source (une des quatre cases), sa référence, et le nom du
test qui la vérifie. Un test automatique échoue si :
- un module du système contient une constante numérique de modélisation qui
  n'est pas dans le registre ;
- une entrée « oreille » n'a pas de test qui reproduit sa donnée publiée ;
- une entrée « choix technique » n'a pas d'analyse de sensibilité.

Un document `REGISTRE.md` est généré à partir du module. Il dit, ligne par
ligne, d'où vient chaque nombre.

## 3. Ce qu'on a déjà, et ce qui doit changer

**Acquis réutilisables :**
- la chaîne d'extraction de spectre, validée ;
- la coïncidence Φ et la rugosité C, avec leurs tests ;
- les mesures de hauteur par gabarit (crible harmonique, hauteur virtuelle) ;
- la boucle de l'étape 1 et sa mesure « son contre réglages » ;
- la discipline protocole → code → résultats.

**Choix de l'étape 1 qui violent la politique, et leur remplacement :**

| Choix actuel | Pourquoi c'est arbitraire | Remplacement prévu |
|---|---|---|
| registre fixe [−1200 ; 2400] c | choisi à la main | la zone où le modèle d'oreille donne une hauteur nette pour ce son (région d'existence de la hauteur), dans les limites de l'audition |
| exclusion de 100 c autour d'une copie | reprise de la zone hors domaine de Φ | une nouvelle copie n'est un nouvel événement que si l'oreille la distingue de celles qui sonnent ; seuil tiré des données de discrimination et de fusion |
| τ (persistance des copies) | choisi parmi deux valeurs | la durée de résonance mesurée du son de départ |
| un pas toutes les 0,45 s | choisi à la main | voir §4, phase 2 : le moment d'un nouvel événement dépend du son et de l'oreille, ou devient un objet d'étude explicite |
| départage des égalités | choisi à la main | conservé comme choix technique, avec sensibilité |
| mesure de la seule coïncidence | ignore la continuité entre notes successives | ajout du regroupement séquentiel (phase 1) |

## 4. Les phases

Chaque phase suit le même schéma : protocole et prédictions commités avant le
code ; code ; résultats sans réécriture du protocole ; décision de passage à
la phase suivante selon des critères fixés à l'avance.

### Phase 0 — Fondations (≈ 1 semaine)

- Structurer `boucle/` en paquet Python (`pyproject.toml`), avec ses tests.
- Créer `registre.py` et le test du §2.4. Y reporter les choix de l'étape 1,
  marqués « à remplacer ».
- Isoler le modèle d'oreille dans un module à part (`oreille/`), avec une
  interface unique : on lui donne un son (ou un mélange), il rend des
  mesures.

*Critère de sortie :* les résultats de l'étape 1 sont reproduits à
l'identique avec le nouveau code.

### Phase 1 — L'oreille, à partir de données (≈ 3 à 4 semaines)

Chaque composant n'entre dans le modèle que s'il reproduit une donnée
publiée, par un test automatique.

| Composant | Rôle dans le système | Donnée de validation (à vérifier dans les sources) |
|---|---|---|
| Bandes critiques (ERB) | base de la rugosité et de la résolution | formule ERB de Glasberg & Moore (1990) |
| Rugosité | évolution du timbre, tension du mélange | courbe de Plomp & Levelt (1965) |
| Coïncidence (Φ) | fusion de sons simultanés, hypothèse 1 | constante de Milne ; classement de fusion de Stumpf, DeWitt & Crowder (1987) |
| Harmonicité (fondamentale commune) | fusion de sons simultanés, hypothèse 2 | seuils de désaccord de Moore, Glasberg & Peters (1986) |
| Hauteur virtuelle | hauteur perçue d'un son, y compris inharmonique | modèle de Terhardt / Parncutt ; note de frappe des cloches, documentée en campanologie |
| Région d'existence de la hauteur | registre utilisable pour un son | données de Ritsma (1962) et suivantes |
| Regroupement séquentiel | quand une suite de notes forme une ligne | frontières de cohérence temporelle et de fission de van Noorden (1975) |
| Mémoire auditive | ce qui compte comme « déjà entendu » (régime exploratoire) | durée de la mémoire sensorielle auditive, quelques secondes (sources à établir) |

**Point de décision important.** Coïncidence et harmonicité prédisent la même
chose pour les sons harmoniques, et des choses différentes pour les sons
inharmoniques. Le système ne doit pas trancher par décision, comme l'a fait
le choix de Φ. Les deux restent implémentées comme des variantes, et le
choix revient à la phase 4 (test d'écoute). D'ici là, toutes les analyses
sont faites avec les deux.

*Critère de sortie :* chaque composant passe son test de reproduction, ou est
retiré et remplacé par une variante plus simple déclarée.

### Phase 2 — Boucle simulée v2, sans consigne (≈ 3 semaines)

- Remplacer les choix arbitraires de l'étape 1 (§3) par des valeurs issues du
  son ou de l'oreille.
- **Mélodie et polyphonie par la perception, pas par la génération.** La
  boucle produit des événements ; le regroupement séquentiel du modèle
  d'oreille les répartit en lignes, comme le ferait un auditeur. Une
  « mélodie » est une ligne ainsi formée ; la « polyphonie » est le nombre et
  la structure de ces lignes. Rien n'impose qu'il y en ait.
- **Rétroaction.** C'est ici que la boucle devient cybernétique au sens
  strict : ce que l'oreille modélisée entend (lignes, fusion, rugosité) sert
  à choisir l'événement suivant, en plus de la coïncidence.
- **Le moment des événements.** Deux options, à trancher dans le protocole de
  la phase : (a) un nouvel événement quand le mélange a assez décru pour
  qu'une nouvelle attaque soit perçue comme distincte, ce qui dépend de la
  résonance du son et de données de masquage ; (b) un rythme régulier
  traité comme un réglage, avec mesure de son influence.

*Prédictions à écrire dans le protocole, par exemple :* les lignes formées
par l'oreille modélisée sont plus longues pour les sons dont la résonance est
longue ; le réseau de hauteurs d'un son nouveau se prédit à partir de ses
seuls intervalles de forte coïncidence.

*Critère de sortie :* le son compte plus que les réglages (R significativement
supérieur à 1, avec un seuil fixé dans le protocole), et l'oreille modélisée
trouve au moins une ligne de plus de quelques notes pour au moins une partie
des sons. Sinon, documenter l'échec et revoir la phase 1 avant d'aller plus
loin.

### Phase 3 — Régime exploratoire (≈ 2 semaines)

- Consigne unique, déclarée : choisir, parmi les coups que le son rend
  possibles, celui qui mène à l'état le moins semblable à ce que la mémoire
  auditive contient encore.
- « Semblable » se mesure dans l'espace des grandeurs du modèle d'oreille
  (hauteurs, fusion, rugosité, lignes), pas dans un espace musical.
- Comparer aux trajectoires sans consigne : la nouveauté recherchée
  produit-elle des lignes, ou casse-t-elle celles qui se formaient ?

*Critère de sortie :* même critère « son contre réglages » que la phase 2,
avec la consigne comprise dans les réglages.

### Phase 4 — Test d'écoute (en parallèle, à partir de la phase 1 ; ≈ 4 à 6 semaines)

C'est la phase qui vérifie que le modèle d'oreille correspond à de vraies
oreilles. Sans elle, tout le reste repose sur un modèle non validé.

- **4a. Coïncidence ou harmonicité ?** Sons construits pour que les deux
  hypothèses prédisent des fusions opposées ; jugements par paires ;
  auditeurs naïfs ; protocole pré-enregistré (repris de
  `PROTOCOLE-TEST-INDEPENDANT.md`). Le résultat décide quelle variante le
  système garde.
- **4b. Les lignes du modèle sont-elles celles qu'on entend ?** Sur des
  extraits produits par la boucle, comparer le nombre de lignes entendues par
  les auditeurs à celui que donne le modèle.
- **Ce qu'il faut :** des participants en nombre (expérience en ligne
  possible), et le cadre éthique de ton institution. Une collaboration avec
  un laboratoire qui fait ce type d'expériences (par exemple le groupe de
  Harrison et Jacoby) serait le moyen le plus solide.

*Critère de sortie :* une variante de fusion retenue sur données ; un accord
mesuré entre lignes du modèle et lignes entendues. Si l'accord est mauvais,
la phase 2 est à refaire avec le modèle corrigé.

### Phase 5 — Boucle acoustique (≈ 3 semaines, sur ton ordinateur)

- Chaîne : synthèse ou échantillon → haut-parleur → pièce → micro → analyse
  par la chaîne d'extraction existante → modèle d'oreille → événement
  suivant.
- Le son analysé est celui qui revient de la pièce : les résonances de la
  pièce entrent dans le son et dans son évolution, sans qu'on les modélise.
- Calibrage : latence, niveaux, bruit de fond, retour direct
  haut-parleur-micro.
- Mesure : la pièce devient un facteur de plus dans le critère « son contre
  réglages ». On compare les trajectoires de la même source dans deux pièces
  différentes, et en boucle simulée.
- **Ce qu'il faut :** un haut-parleur, un micro, une pièce, et ton
  ordinateur relié à cette session (Remote Control) ou un script que tu
  lances toi-même.

*Critère de sortie :* boucle stable sur au moins 5 minutes, sans larsen ; un
résultat mesuré sur ce que la pièce change.

### Phase 6 — Le prototype en temps réel (≈ 4 à 6 semaines)

- Moteur temps réel. On choisira la technique sur mesure de latence : Python
  si la latence tient, sinon synthèse déléguée à un moteur audio (par exemple
  SuperCollider) piloté par le calcul en Python.
- Entrées : un fichier, une bibliothèque de sons mesurés, ou un son capté au
  micro, analysé à la volée.
- Contrôles exposés : la source, le régime (sans consigne ou exploratoire),
  simulé ou acoustique. Les réglages techniques restent visibles avec leur
  provenance (le registre affiché dans l'interface).
- Sorties : audio, et une visualisation en direct des lignes que l'oreille
  modélisée entend.
- Enregistrement de chaque session (son, paramètres, trajectoire) pour
  qu'elle soit rejouable et analysable.

*Critère de sortie :* une session d'au moins 10 minutes, rejouable à
l'identique à partir de son enregistrement.

### Phase 7 — Évaluation et création (≈ 4 semaines)

- Pièces réalisées avec le prototype, sur plusieurs sons.
- Écoutes avec des auditeurs et des compositeurs : retours qualitatifs, et
  une mesure simple (le public entend-il des lignes ? les attribue-t-il au
  son de départ ?).
- Documentation finale : ce que le système fait, ce que le son « contient »
  selon les mesures, ce qui reste du mécanisme, et toutes les limites.

## 5. Le critère qui traverse tout le projet

À chaque phase, la même question : **la trajectoire dépend-elle davantage du
son que du système ?** On la mesure en faisant varier d'un côté les sons, de
l'autre tout ce qui n'est pas le son (règle de transition, choix techniques,
consigne, pièce). Si le système compte plus que le son, l'idée « le son
contient son évolution » n'est pas soutenue dans ce dispositif, et on le
dit.

## 6. Risques et sorties de secours

| Risque | Signe | Réponse prévue |
|---|---|---|
| Le modèle de regroupement séquentiel ne marche pas sur des sons inharmoniques | test de phase 1 ou désaccord en phase 4b | revenir à van Noorden seul, déclaré comme simplification |
| La coïncidence perd contre l'harmonicité (phase 4a) | résultat d'écoute | garder l'harmonicité ; l'idée « chaque son a son réseau » s'affaiblit, et on le documente |
| Aucune ligne n'émerge (phase 2) | l'oreille modélisée ne trouve que des notes isolées | résultat en soi : dans ce dispositif, le son contient des hauteurs mais pas de lignes |
| Le système compte plus que le son | R proche de 1 | le prototype reste un instrument de création, présenté comme tel |
| La boucle acoustique est instable | larsen, dérive | réduire le gain, ajouter de l'amortissement mesuré ; sinon, rester en simulation avec réponse impulsionnelle de pièce, en le disant |
| Le temps réel est trop lent | latence | calcul allégé (moins de partiels, grille plus grossière), avec sensibilité vérifiée |

## 7. Ce qu'il faudra de toi

- Des sons nouveaux à faire entrer (enregistrements), pour que les prédictions
  portent sur des sons que le système n'a jamais vus.
- Les décisions sur le test d'écoute : recrutement, cadre éthique,
  collaboration éventuelle.
- Le matériel pour la boucle acoustique.
- Tes écoutes à chaque phase, consignées comme retours, pas comme preuves.

## 8. Ordre et durée

| Phase | Dépend de | Durée estimée |
|---|---|---|
| 0 Fondations | — | 1 semaine |
| 1 Oreille | 0 | 3 à 4 semaines |
| 2 Boucle v2 sans consigne | 1 | 3 semaines |
| 3 Régime exploratoire | 2 | 2 semaines |
| 4 Test d'écoute | 1 (préparation), puis résultats attendus avant la fin de la phase 6 | 4 à 6 semaines, en parallèle |
| 5 Boucle acoustique | 2 | 3 semaines |
| 6 Temps réel | 3, 5 | 4 à 6 semaines |
| 7 Évaluation et création | 6 | 4 semaines |

Total : environ 5 à 7 mois, selon le temps disponible et la phase 4.
