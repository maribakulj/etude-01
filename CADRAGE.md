# Cadrage

*Réécrit le 2026-10-28. Il remplace `CADRAGE-v2.md` (version d'origine :
`git show 9a03b9b:CADRAGE-v2.md`). Le §8 dit ce qui a été retiré et pourquoi.*

---

## 1. La question

Dans la pratique savante occidentale, deux voix ne doivent pas avancer en
quintes ou en octaves parallèles. On explique souvent cette règle par la
perception : deux sons dont beaucoup de partiels coïncident tendent à être
entendus comme un seul son, et s'ils bougent ensemble, ils le restent. Cette
explication suppose des sons harmoniques (partiels à f, 2f, 3f…), comme la
voix, les cordes ou les tuyaux d'orgue.

Les cloches, les lames et beaucoup de sons de synthèse sont inharmoniques :
leurs partiels ne coïncident pas aux mêmes intervalles. Si l'explication
perceptive est la bonne, l'intervalle « à ne pas doubler en parallèle »
devrait changer avec le timbre.

Ce projet pose la question suivante : **peut-on calculer, à partir du spectre
d'un son, quels mouvements parallèles feraient fusionner deux voix de ce
timbre, et ce calcul correspond-il à ce qu'on entend ?**

Le périmètre est volontairement étroit : deux voix, note contre note
(première espèce), même timbre pour les deux voix, intervalles dans une
octave.

## 2. Travaux existants

La recherche bibliographique n'a pas été systématique. Ce qui suit est ce qui
a été lu ou repéré, pas un état de l'art complet.

**Consonance dépendante du timbre (l'aspect vertical).** C'est un domaine
établi. Sethares (*Tuning, Timbre, Spectrum, Scale*) calcule des courbes de
dissonance à partir des partiels et en tire des gammes adaptées à des sons
inharmoniques. Marjieh et al. (2024, *Nature Communications*) montrent, sur un
grand nombre de jugements, que les préférences de consonance changent quand on
manipule le timbre. Harrison & MacConnachie (2024, *JASA*) trouvent que sur
des cloches de carillon, la tierce mineure devient plus consonante et la
tierce majeure moins. Le projet ne revendique rien sur cet aspect.

**Règles de conduite des voix expliquées par la perception.** C'est
l'antécédent le plus direct, et la première version du cadrage l'omettait.
Huron (2001, « Tone and Voice: A Derivation of the Rules of Voice-Leading
from Perceptual Principles », *Music Perception* 19(1) ; développé dans
*Voice Leading*, MIT Press, 2016) dérive la plupart des règles classiques de
conduite des voix de quelques principes tirés de la recherche sur la
ségrégation des flux auditifs, dont un principe de fusion tonale qui couvre
les unissons, octaves et quintes parallèles. Wright & Bregman (1987) avaient
étudié comment la ségrégation des flux module la dissonance perçue en
polyphonie. Bregman (*Auditory Scene
Analysis*, 1990) est la référence générale sur la ségrégation des flux.
Ces travaux portent sur des sons harmoniques.

**Géométrie de la conduite des voix.** Tymoczko modélise la conduite des voix
comme des déplacements dans un espace d'accords, avec une distance en
demi-tons, sans référence au spectre. Le projet n'utilise pas ce modèle.

## 3. Ce que le projet essaie d'ajouter

À notre connaissance, et sous réserve d'une recherche plus complète : calculer
les interdits de mouvement parallèle **pour un spectre quelconque**, et
regarder comment ils changent d'un timbre à l'autre. Par rapport à Huron,
c'est une généralisation possible de son principe de fusion tonale à des
timbres inharmoniques, pas une explication nouvelle de la règle classique.

Si cela marche, l'apport serait modeste et pratique : proposer, pour un timbre
sans tradition d'écriture (une cloche, un son de synthèse), une liste de
mouvements parallèles à éviter si l'on veut garder deux voix distinctes. Le
projet ne prétend pas expliquer l'histoire des règles.

## 4. L'hypothèse de travail, en clair

1. Pour deux voix à un intervalle *i*, on calcule Φ(*i*), un indice de
   coïncidence des partiels : la somme, sur les paires de partiels des deux
   voix, de leur proximité en fréquence (noyau gaussien de largeur σ en
   cents), pondérée par les amplitudes. Formulation publiée : Milne (2013),
   voir `DECISION-PHI.md`.
2. Hypothèse : plus Φ(*i*) est élevé, plus deux voix qui avancent en
   parallèle à l'intervalle *i* sont entendues comme une seule.
3. Règle R2 du modèle : interdire le mouvement parallèle (et direct) vers les
   intervalles dont Φ dépasse un seuil τ_F.

Cette règle a été **posée**, pas découverte. Le modèle ne trouve pas que la
fusion compte ; il le suppose, puis calcule où elle se produit pour un
spectre donné. Sur un spectre harmonique, il retrouve les quintes et octaves
parce que le seuil a été choisi pour cela (README.md, limite 1).

**Ce que l'hypothèse ne couvre pas.** Les règles de Fux viennent de la
pratique, pas d'un calcul. D'autres facteurs pourraient expliquer tout ou
partie de l'interdit des parallèles : la rugosité, la perception de hauteur
(deux sons qui évoquent une même fondamentale), l'idéal stylistique
d'indépendance des voix, l'apprentissage culturel. Le projet ne teste pour
l'instant aucune de ces explications concurrentes. Le protocole
`PROTOCOLE-TEST-INDEPENDANT.md` prévoit de comparer au moins la rugosité.

## 5. Spectre et modèle d'audition

Deux quantités sont calculées séparément :

- **C(*i*)**, la consonance de Sethares, fondée sur la rugosité. Elle dépend
  de la largeur des bandes critiques, donc d'un modèle de l'oreille.
- **Φ(*i*)**, la coïncidence de partiels. Les positions de ses maxima ne
  dépendent que des rapports de fréquence du spectre ; seul σ représente
  l'oreille (la tolérance à partir de laquelle deux partiels comptent comme
  coïncidents).

Ce découpage est un choix de modélisation, pas un résultat. En particulier,
le test « P6 » du noyau exploratoire (changer de modèle d'oreille, les maxima
de Φ restent en place, ceux de C bougent) est vrai **par construction** : en
changeant σ, on change la largeur des pics de Φ, pas leur centre. Le
« récepteur chauve-souris » de ce test n'était qu'un rétrécissement des
bandes critiques, pas un modèle de l'audition d'un rhinolophe.

## 6. Choix de modélisation et leurs coûts

1. **Seuils.** Les courbes C et Φ sont continues ; les règles sont des seuils
   (τ_C pour les états admis, τ_F pour les interdits). Le choix du seuil
   change le résultat (`sensibilite_seuil.py`). On rapporte les plages de
   seuil sur lesquelles une règle tient ; une règle qui ne tient que sur une
   plage étroite est fragile.
2. **Gabarits de règles imposés.** Les formes des règles (R1 : état admis si
   C ≥ τ_C ; R2 : interdit parallèle si Φ ≥ τ_F ; R3 : début et fin sur le
   maximum de Φ ; R5 : préférence pour le mouvement contraire) sont écrites à
   la main. Le système en calcule les paramètres, pas la forme.
3. **Simultanéité statique.** Le modèle ignore l'attaque, la décroissance et
   le temps. La première écoute (ETAPE4-ECOUTE.md §7) a montré qu'un rendu
   sans articulation ne fait entendre aucune voix ; le rendu a donc dû
   ajouter une enveloppe que le modèle ne contient pas.
4. **Cas sans structure.** Un spectre très pauvre (quasi sinusoïdal) donne
   une courbe Φ plate ; le modèle ne dit alors rien. C'est arrivé avec la
   boîte à musique mesurée (ETAPE2-PROTOCOLE.md §7).
5. **Architecture.** (a) Le modèle d'oreille est un paramètre explicite des
   fonctions (largeur de bande critique, σ). (b) Les règles sont des données
   (`GABARITS` dans `graphe_grammaire.py`). (c) Chaque interdit garde la
   trace du seuil et de la paire de partiels qui l'a produit, pour qu'on
   puisse vérifier d'où il vient.

## 7. Biais et risques connus

Ces risques s'appliquent à tout le dépôt. Ils sont listés ici pour qu'on les
garde à l'esprit en lisant les résultats.

1. **Circularité de la calibration.** Le seuil τ_F a été choisi pour
   reproduire Fux sur le spectre harmonique. Ce cas ne peut pas servir de
   preuve.
2. **Chemins multiples d'analyse.** De nombreux choix ont été faits en cours
   de route, chacun déclaré : σ, schéma de seuils, règles de nettoyage des
   spectres, extension du compas à 1400 c, critère de bifurcation durci après
   un premier résultat, trois versions des stimuli d'écoute. Même déclarés,
   ces choix successifs donnent beaucoup de latitude pour obtenir un résultat
   « dans le sens prédit ».
3. **Critères de succès faciles à satisfaire.** Le verdict P5 de l'étape 2
   « tient » si un seul maximum de Φ est déplacé de plus de 25 c par rapport
   au cas harmonique. Pour un spectre nettement inharmonique, c'est presque
   garanti par l'arithmétique. De même, l'octave étirée (D2) et les maxima sur
   des carrés de rationnels (D4) du balayage d'inharmonicité découlent
   directement de la formule de la corde raide ; n'importe quelle mesure de
   coïncidence les produirait.
4. **Choix de matériau orienté.** La cloche a été retenue après l'échec de la
   boîte à musique, et elle est connue (Harrison & MacConnachie 2024) pour
   avoir une tierce mineure particulière. Trouver un pic de Φ à cet
   intervalle est en partie une relecture de leurs données, pas un test
   risqué.
5. **Choix de métrique orienté.** Φ a été préférée aux mesures d'harmonicité
   notamment parce qu'elle *peut* déplacer les interdits avec le timbre
   (DECISION-PHI.md §3, critère 2). Les mesures d'harmonicité, qui modélisent
   la perception de hauteur humaine, prédisaient au contraire des interdits
   ancrés aux rapports simples. On a donc retenu la métrique compatible avec
   l'hypothèse.
6. **Écoute non indépendante.** Les jugements d'écoute viennent d'une seule
   personne qui connaissait l'hypothèse, et les stimuli ont été modifiés deux
   fois après ses retours.
7. **Cohérence produite par un assistant IA.** Le code et la plupart des
   documents ont été rédigés avec un assistant IA, au fil d'une conversation
   où la même instance proposait les hypothèses, écrivait les tests et
   interprétait les résultats. La cohérence entre les documents n'est donc pas
   une preuve : elle peut venir de la même source. Les relectures externes
   (comme celle qui a motivé cette réécriture) sont la principale protection.

## 8. Retiré de la version d'origine, et pourquoi

- **« Quasicristal spectral », « règles de sélection », « symétries du
  réseau spectral », « élément de matrice ».** Ces analogies avec la
  cristallographie et la spectroscopie n'étaient ni définies
  mathématiquement ni utilisées dans le code. L'ensemble des transpositions
  qui font coïncider des partiels n'est pas un groupe, et un spectre de
  quelques partiels n'est pas un quasicristal. Le modèle se décrit sans elles
  (§4).
- **« Décompilation / recompilation » des règles.** Métaphore sans contenu
  opératoire.
- **« Diagramme de phase », « transition de phase », « bifurcation ».** Les
  noms de fichiers sont gardés, mais il s'agit simplement de l'ensemble des
  interdits calculé le long d'un paramètre de spectre, et des valeurs où cet
  ensemble change de taille. Rien n'indique qu'il s'agisse de transitions au
  sens physique (README.md, limite 3).
- **Le récepteur « rhinolophe ».** Jamais modélisé au-delà d'un changement de
  largeur de bande (§5).
- **« Jouer le législateur », l'instrument navigable dans l'espace des
  timbres.** Idée de création, pas une partie de la recherche ; différée sans
  date.
- **Comparaison avec les systèmes génératifs appris.** Elle n'apportait rien
  à la question et suggérait une portée plus large que celle du projet.
- **Choix de langage (Clojure).** Hors sujet pour la question ; le projet est
  en Python.
