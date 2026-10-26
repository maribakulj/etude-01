# Cadrage — Le contrepoint comme règles de sélection sur les symétries d'un spectre

*Document de travail, v2. État : pré-prototype, prêt pour un premier test empirique. À amender après le test du §11.*

---

## 0. En une phrase

Construire un système qui prend le spectre d'un objet sonore et en dérive une **grammaire de mouvement entre voix** — une syntaxe contrapuntique propre à ce timbre — en traitant les règles de conduite des voix comme des *règles de sélection* sur les symétries de la structure spectrale.

---

## 1. La question

Les règles classiques du contrepoint (l'écriture d'espèces de Fux) peuvent se relire comme la trace d'un phénomène physique : la consonance et la dissonance dépendent en partie de la structure des partiels — alignements, rapports simples, battements entre partiels voisins. Une part des préceptes — quels intervalles sont stables, comment la dissonance se prépare et se résout, pourquoi deux voix en quintes parallèles tendent à se confondre en une seule — peut se relire comme des énoncés sur des spectres, durcis en règles pédagogiques.

Conséquence : **si ces règles tiennent à une structure spectrale, elles ne valent que pour les spectres qui les ont produites** — les sons quasi harmoniques (voix, cordes, tuyaux). Un spectre inharmonique — cloche, lamelle de boîte à musique, timbre de synthèse — possède une structure de coïncidences différente, donc *devrait* porter une grammaire différente.

**Question centrale :** peut-on dériver, du seul spectre d'un objet, non pas une gamme (déjà fait, cf. §3) mais une **syntaxe du mouvement** — ce qui se prépare, se résout, quels mouvements préservent ou détruisent l'indépendance des lignes — cohérente avec ce timbre ?

Formulation courte : **chaque monde sonore a-t-il sa propre grammaire contrapuntique, inscrite dans son spectre ?**

---

## 2. Une précision historique qui renforce le cadrage

Le contrepoint n'est pas le plus ancien exemple de compilation d'un continu en symbolique discret : l'écriture alphabétique compile la parole, le monocorde pythagoricien compile des longueurs de corde, la prosodie quantitative compile des durées. Mais tous ces exemples compilent des **états** — un lexique, une gamme, un inventaire. La revendication fine, qui tient :

> Le contrepoint est peut-être le plus ancien exemple de compilation d'une physique en **grammaire du mouvement** — des règles sur les trajectoires, pas sur les positions. La préparation/résolution est de la gestion temporelle d'une grandeur physique : un système de contrôle, pas un dictionnaire.

Réserve d'honnêteté à garder : les règles de Fux n'ont pas été dérivées de la physique mais de la **pratique** — des siècles d'itération empirique sur ce qui sonnait, la physique n'arrivant qu'après (Helmholtz) comme explication rétrospective. Donc le projet n'est pas une compilation mais une **décompilation suivie d'une recompilation pour une autre cible**. Cette formulation est plus forte : elle donne un critère de validation clair — *retrouver une part de Fux comme sortie du système sur un spectre quasi harmonique valide le décompilateur.*

---

## 3. Où c'est neuf, où ça ne l'est PAS

À tenir avec rigueur, sous peine de réfutation immédiate.

### Déjà fait — l'étage vertical (NE RIEN REVENDIQUER ICI)
La dérivation d'une **gamme** ou d'un **vocabulaire d'accords** depuis un spectre est un champ mûr :
- Sethares, *Tuning, Timbre, Spectrum, Scale* : courbes de dissonance dépendantes du timbre, échelles pour sons inharmoniques, accordage adaptatif, validation gamelan.
- Bohlen-Pierce : gamme sur harmoniques impaires, affinité documentée avec la clarinette. Geste « grammaire de l'objet » — mais au niveau gamme.
- Accordage par entropie / harmonicité : échelles dérivées de la coïncidence de partiels.
- **Marjieh, Harrison, Lee, Deligiannaki & Jacoby (2024, Nature Communications, ~235 000 jugements) :** les préférences de consonance se remodèlent par manipulation timbrale, jusqu'à des préférences pour intervalles inharmoniques.
- **Harrison & MacConnachie (2024) :** sur un timbre de carillon, la tierce mineure devient consonance forte et la tierce majeure devient dissonante — inversion par rapport au timbre harmonique. C'est la « grammaire de l'objet » réalisée sur une vraie cloche — **mais statique, verticale.**

### Pas fait — l'étage de la syntaxe du mouvement (LE PROJET)
Personne ne dérive du spectre les **règles de conduite des voix** : la grammaire du mouvement, l'indépendance des lignes dans le temps, les conditions de fusion vs ségrégation.

Et la raison de l'arrêt est identifiable (ce qui renforce le projet) :
- Sethares borne sa théorie : la consonance sensorielle ne dit rien du **mouvement**.
- Harrison & Pearce ont prévu d'inclure la rugosité dans un modèle d'harmonie puis l'ont **abandonnée** car trop dépendante du *voicing* — donc imprévisible au niveau abstrait des classes de hauteur. **La difficulté qui les fait reculer — dépendance au voicing et au temps — est exactement la matière du contrepoint.**

### L'intersection vide, nommée précisément
- Tymoczko construit l'espace de conduite des voix comme un orbifold, mais sa métrique est l'efficacité abstraite du déplacement (demi-tons parcourus), en douze hauteurs, **sans spectre**.
- Sethares / Marjieh donnent la **verticale** pour un timbre quelconque.
- La tradition de la ségrégation des flux (Bregman) modélise la **perception**, jamais sa conversion en grammaire générative pour un timbre arbitraire.

> **L'inédit : un espace de conduite des voix métré par le spectre.** La géométrie de Tymoczko, mais où « proche » signifie « fort recouvrement de partiels pour ce timbre », et où les régions interdites sont les lieux de fusion des flux. Le mouvement dérivé de la physique, pour un timbre quelconque, n'existe pas.

---

## 4. Le mécanisme central : règles de sélection sur un quasicristal spectral

C'est le cœur du projet et sa contribution propre.

### Le spectre comme réseau
Place les partiels d'un spectre harmonique sur l'axe des fréquences : f, 2f, 3f… C'est un réseau régulier à une dimension. Transposer une voix = multiplier ses fréquences par un rapport = une translation sur l'axe logarithmique. Deux voix séparées d'un intervalle r partagent des partiels là où r est un rapport simple n/m — d'où la coïncidence maximale aux intervalles justes.

**Donc « quels intervalles sont consonants » = quelles mises à l'échelle envoient les partiels sur les partiels = les symétries du réseau spectral.** La dérivation de gamme trouve le groupe de symétrie du spectre. *Acquis (Sethares).*

### Le pas neuf : le mouvement comme règle de sélection
Analogie avec la spectroscopie : la symétrie statique dit quels états existent ; les **règles de sélection** disent quelles transitions entre états sont permises (une transition est interdite quand la symétrie annule son élément de matrice).

Transposé : la symétrie du spectre fixe la gamme (quels états) ; la dynamique fixe quels mouvements de voix préservent ou détruisent la ségrégation.

**Le résultat clé :** un mouvement parallèle dans un intervalle de forte coïncidence est un mouvement qui *préserve la symétrie* — les deux voix translatent du même pas, la structure de partiels partagés est conservée, les deux flux retombent sur la même orbite → ils **fusionnent**. L'interdiction des quintes et octaves parallèles est donc une *règle de sélection contre le mouvement symétrie-préservant qui effondre deux orbites en une*. Le mouvement contraire brise la conservation → les pistes de partiels divergent → la ségrégation tient.

On obtient une **raison structurelle à la plus vieille règle du contrepoint** — et elle se transpose : sur une cloche, l'intervalle « parallèle interdit » n'est plus la quinte mais le porteur de coïncidence forte de *ce* spectre. **C'est la bifurcation, rendue prédictible.**

### Deux garde-fous d'honnêteté (à ne jamais lâcher)
1. **Quasicristal, pas cristal.** Un spectre inharmonique (p. ex. 1 : 6,27 : 17,55) n'a pas de fondamentale ni de périodicité — ce n'est pas un réseau régulier. Mais il a des pics de coïncidence nets sous certaines mises à l'échelle : ordre à longue portée sans périodicité, pics de diffraction nets. C'est un **quasicristal sonore**. C'est l'analogie juste.
2. **La forme, pas le contenu.** Une règle de sélection physique annule *exactement* un élément de matrice (théorie des représentations). Ici la « règle » est un **seuil mou sur une courbe de fusion continue**. La cristallographie donne la *forme* (la symétrie gouverne les transitions permises), pas le *contenu* (qui reste statistique et dépendant du récepteur). Revendiquer la forme ; jamais l'exactitude du contenu.

---

## 5. Substrat vs saillance : ce qui est dans l'objet, ce qui est dans le récepteur

Tension à trancher : peut-on dériver la grammaire de l'objet **lui-même**, sans présupposer un récepteur particulier ?

Réponse nette, et c'est une distinction structurante :
- **Substrat (indépendant du récepteur) :** la structure de coïncidence des partiels, l'auto-similarité sous transposition. Elle existe pour n'importe quel récepteur résonant — c'est de l'arithmétique sur le spectre.
- **Saillance (dépendante du récepteur) :** quelles propriétés de cette structure comptent. La rugosité de Plomp-Levelt dépend de la **bande critique**, qui est une propriété d'une cochlée, pas du signal. La rugosité est donc déjà un fait *hybride*.

**Conséquence d'architecture (centrale, non négociable) :** le modèle de cohérence vit **derrière une interface échangeable** — un « port » où le récepteur est un *paramètre explicite*, pas un présupposé enfoui. On y branche : analyseur idéal plat (substrat pur), cochlée humaine, ou tout autre récepteur. **L'écart entre les grammaires obtenues selon le récepteur EST un résultat** : il mesure ce que chaque récepteur ajoute à la structure brute.

### La sonde décisive : un récepteur radicalement non humain
Pour rendre la distinction substrat/saillance empirique plutôt que rhétorique, on branche un récepteur dont la structure de bandes critiques est connue *et* extrême. Le rhinolophe (chauve-souris) a une « fovéa acoustique » : sa cochlée surreprésente massivement une bande étroite (autour de sa fréquence d'écholocation), avec une résolution très fine là et grossière ailleurs — une structure de bandes critiques radicalement non humaine.

Expérience de pensée qui tranche le §5 : envoie le **même** complexe physique de deux partiels au récepteur-humain et au récepteur-rhinolophe.
- La structure de coïncidence (recouvrement, autocorrélation sous transposition) est **identique** — c'est le substrat.
- La rugosité diffère **du tout au tout** — car les bandes critiques diffèrent. Ce qui est lisse pour l'un est rugueux pour l'autre, selon la région.

Le récepteur exotique dit donc *lequel des mécanismes est libre de récepteur* (la coïncidence) et lequel ne l'est pas (la rugosité). Et il justifie le port mieux qu'aucun argument abstrait : le récepteur est une coordonnée, le rhinolophe en est un réglage extrême.

### Reformulation de la thèse, plus honnête et plus forte
> L'objet a une **structure de symétrie invariante** (le quasicristal). Une **grammaire** est ce qu'un récepteur donné en extrait. Le vrai produit du système est l'application **(spectre × récepteur) → grammaire**, dont l'humain et le rhinolophe sont deux évaluations qui encadrent l'espace.

« Grammaire de l'objet » reste le cap, mais le récepteur est devenu une coordonnée déclarée, pas un présupposé caché. Inattaquable sur la question du sujet percevant. C'est aussi, métaphoriquement exact, **deux expériences de diffraction sur le même quasicristal** : la structure est invariante, ce que chaque sonde résout diffère.

---

## 6. Pourquoi ce n'est pas un énième système génératif

La famille dominante de la génération musicale (DeepBach, Coconet, Music Transformer, modèles à diffusion, NotaGen…) partage trois présupposés que ce projet n'a pas :
1. Elle **apprend une distribution** sur des séquences symboliques à partir d'un **corpus**.
2. Elle travaille en tempérament égal à douze.
3. Elle suppose un timbre harmonique **sans jamais le nommer comme variable**.

« Correction » y signifie conformité au style appris.

**Différenciateurs :**
- Pas de corpus : les règles sont dérivées de la physique d'un **seul timbre**. C'est la seule option pour les timbres qui n'ont pas de corpus — *une cloche n'a pas de Bach.*
- La sortie n'est pas une pièce plausible : c'est le **jeu de règles**, et plus profondément la **carte (espace des timbres → espace des grammaires)**. Aucun système appris ne produit cette carte, parce que le timbre n'est pas pour lui un degré de liberté.
- Statut épistémique opposé : un système appris dit « ce mouvement est probable vu le corpus » ; ce système dit « ce mouvement préserve l'indépendance sur ce timbre **parce que** tel fait spectral » — **explicatif et falsifiable à l'oreille**, pas seulement descriptif.

---

## 7. La forme de l'instrument : jouer le législateur

Si la grammaire est une fonction discrète d'un paramètre timbral continu, alors il existe des **bifurcations** : des points de l'espace des timbres où une règle apparaît ou disparaît.

L'instrument intéressant n'est pas celui qui joue des notes mais celui qui **se déplace dans l'espace des timbres pendant que la polyphonie tourne**, et qui rend audibles les transitions de phase de la grammaire. *On ne joue pas la musique, on joue le législateur ; la musique est la jurisprudence.*

Objet cartographiable qui en découle : un **diagramme de phase du contrepoint** au-dessus de l'espace timbral — régions stables, frontières où une règle bascule. Artefact visuel-épistémologique qui *ne pourrait pas exister sans le dispositif* — c'est le critère anti-gadget : le système doit produire des choses impossibles sans lui (pièces dans des grammaires inédites, la carte, le diagramme de phase), pas de simples démos « ça change avec le timbre ».

---

## 8. À quoi ça sert (réponse à « est-ce un gadget ? »)

Pas une preuve (la dépendance consonance/timbre est établie). Une **opérationnalisation** :
1. **Comble un décalage réel.** Timbres infinis offerts par la synthèse, syntaxe héritée des voix harmoniques. Donner à un monde sonore sa conduite des voix cohérente : besoin réel des compositeurs xenharmoniques, spectraux, du sound design. *Sethares leur a donné des gammes ; personne ne leur a donné le mouvement.*
2. **Instrument contrefactuel — théorie exécutable.** « À quoi ressemblerait le contrepoint si nos instruments dominants avaient été des cloches ? » devient jouable et audible.
3. **Prédictions falsifiables.** Une grammaire dérivée prédit que tel mouvement, sur tel timbre, préserve l'indépendance des voix. Testable par écoute. Les **échecs** sont le résultat le plus riche : là où une grammaire dérivée sonne « correcte » mais ne fonctionne pas à l'oreille, on localise ce que la cognition et la culture ajoutent.

---

## 9. Faisabilité

### Léger (jours)
- Courbes de dissonance : somme pondérée d'interactions par paires de partiels. Implémentations connues.
- Dérivation d'échelle : minima locaux de la courbe.
- Compilation d'un automate depuis une hiérarchie de consonances : construction de graphe.
- Génération : recherche de chemin / petit solveur de contraintes.
- **Synthèse additive avec exactement les partiels ayant servi à dériver la grammaire** → cohérence modèle/son garantie par construction.
- Spectres **analytiques** en v1 (pas d'analyse audio) : FM via fonctions de Bessel ; lamelle de boîte à musique = poutre en flexion, modes ≈ 1 : 6,27 : 17,55.

### Modéré (semaines)
- **Métrique de fusion** : pas de modèle consensuel. Candidats — harmonicité du spectre combiné, similarité spectrale. Choix à assumer et déclarer. *C'est le cœur dur : la fusion porte le contrepoint (cf. §4), la consonance verticale est l'acquis facile.*
- **Dynamique temporelle** : partiels enveloppés (attaque, décroissance) → fusion fonction du temps, pas scalaire. Calcul image par image. C'est de là que sortent les règles de préparation/résolution.

### La vraie difficulté (décisions de modélisation, non computationnelle)
- **Seuil continu → discret.** Les métriques sont des courbes ; les règles, des seuils. *Où couper* est un choix. Bonne nouvelle : le système rend explicite ce que Fux faisait implicitement. Et un seuil se balaye : **règles robustes** (stables sur la plage) = dans le signal au sens fort ; **règles fragiles** (qui basculent avec le curseur) = convention, identifiée règle par règle. L'analyse de sensibilité est une méthode de mesure, pas un aveu d'arbitraire.
- **Gabarits de règles en v1.** Le système instancie des gabarits conçus à la main (« tout état au-dessus du seuil de fusion F est interdit en mouvement parallèle » etc.), il n'invente pas des *formes* de règles. Compilateur de **paramètres**, oui ; de **concepts**, étape ultérieure.

### Cas dégénéré
Spectre très pauvre → courbe plate → pas de structure → pas de grammaire. Le système doit savoir dire « ce son ne porte pas de contrepoint ». Résultat en soi.

---

## 10. Architecture (valable quel que soit le langage)

1. **Récepteur derrière un port.** Interface `cohérence(spectre_a, spectre_b, intervalle, t, récepteur)`. Le récepteur (analyseur plat, humain, rhinolophe…) est un paramètre. Seul choix vraiment irréversible : ne jamais souder le récepteur au reste.
2. **Règles = données**, pas code. Représentation déclarative dès le jour 1.
3. **Spectres analytiques en v1.**
4. **Traçabilité du seuillage seulement.** Chaque règle émise garde *quel seuil et quelle interaction de partiels* l'a produite — non par principe de provenance généralisée, mais parce que c'est ce qui distingue règle robuste et règle fragile (§9). Tracer là où la trace est l'objet d'étude, pas partout.

### Note langage
Noyau numérique **petit** (dizaines de partiels, O(n²), millisecondes par recompilation) → pas de besoin de calcul matriciel massif. **Clojure** est cohérent de bout en bout : règles-comme-données natives, satisfaction par contraintes, synthèse via Overtone/SuperCollider, et un **REPL** qui permet de redéfinir le spectre à chaud et d'entendre la grammaire se recompiler — maquette de l'expérience finale dès le mode texte. Limite : garder les boucles chaudes disciplinées sur la JVM. Tradition utile à connaître : contrepoint par contraintes (Strasheela/Oz, FuxCP/Gecode).

---

## 11. Prochaine action : le test, avec critère durci

Un test empirique d'une demi-journée, **deux timbres × deux récepteurs**, trois mesures.

- Timbres : quasi harmonique ; boîte à musique (modes ≈ 1 : 6,27 : 17,55).
- Récepteurs sur le port : humain ; rhinolophe (bandes critiques à fovéa acoustique).
- Mesures :
  1. **Écart entre timbres** — les conditions de fusion de deux voix diffèrent-elles selon le timbre ? *(Le contrepoint dépend-il du son ?)*
  2. **Écart entre récepteurs** — pour un même timbre, la grammaire diffère-t-elle entre humain et rhinolophe ? *(La règle est-elle dans le signal ou dans le récepteur ?)*
  3. **Fraction de Fux récupérée** — quelle part des règles classiques (sur spectre quasi harmonique, récepteur humain) tombe comme règles de sélection spectrales, et **qu'est-ce qui résiste** ? Le résidu est soit de la convention pure (résultat : mesure de la convention), soit le signe qu'il manque un second principe au-delà de « fusion par symétrie ».
- Critère de bifurcation (bonus) : existe-t-il un chemin continu entre les deux spectres le long duquel une règle bascule ?

Si les écarts 1 et 2 sont non triviaux **et** que la mesure 3 récupère une fraction substantielle de Fux, ce n'est pas un gadget : c'est un instrument qui **sépare ce qui appartient au monde de ce qui appartient à qui écoute**, et qui mesure ce que la tradition a ajouté par-dessus.

La spec d'implémentation s'écrit *après* le test, et sous forme de **liste d'hypothèses avec critères d'abandon**, pas de cahier des charges figé.

---

## Invariants à ne pas perdre
- Le contrepoint = règles de sélection sur les symétries du quasicristal spectral. *(C'est le cœur ; tout le reste en découle.)*
- Forme groupale solide, contenu (seuils) mou et dépendant du récepteur — ne jamais confondre les deux.
- Récepteur = coordonnée explicite derrière un port, pas présupposé. Substrat (coïncidence) vs saillance (rugosité).
- Le produit réel = la carte (spectre × récepteur) → grammaire, pas une pièce.
- La fusion des voix est le cœur dur ; la consonance verticale est l'acquis facile.
- Règles = données. Traçabilité limitée au seuillage.
- Ça doit sonner.
