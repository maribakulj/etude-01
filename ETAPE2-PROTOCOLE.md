# ETAPE2-PROTOCOLE — P5 sur spectre mesuré : protocole figé avant la mesure

*Daté du 2026-06-11. La chaîne de mesure a été écrite, paramétrée et validée
sur signaux synthétiques avant qu'aucun enregistrement réel ne soit analysé.
Les §1, §4 et §5 décrivent l'état au 2026-06-11. Texte révisé le 2026-10-28
(ton ; notes de relecture marquées « Note 2026-10-28 ») ; seuils, règles et
résultats inchangés. Version d'origine :
`git show 9a03b9b:ETAPE2-PROTOCOLE.md`.*

---

## 1. État

- **Chaîne de mesure : prête et validée.** (`extraction_spectre.py`,
  `test_extraction.py`, `etape2_p5.py`)
- **Matériau réel : pas encore obtenu** — la politique réseau du conteneur
  bloque toutes les sources d'échantillons standard (voir journal §4). En
  attente d'un enregistrement utilisateur ou d'un élargissement d'allowlist
  (§5).

## 2. Prédictions et seuils déclarés avant la mesure

- **P5 structurel** (SPEC §5, enregistré avant tout calcul) : les pics de
  fusion `Φ` de la boîte à musique se déplacent par rapport au cas harmonique ;
  l'« intervalle de parallèles interdits » de R2 se déplace avec eux.
- **Prédiction quantitative du modèle analytique** (Euler-Bernoulli, modes
  1 : 6,267 : 17,55 : 34,39 : 56,84, amplitudes 1/√k) avec la **Φ figée**
  (σ = 6,83 c, DECISION-PHI.md), calculée et déclarée le 2026-06-11, avant
  toute donnée réelle :
  - pics principaux à **1165 c** (Φ=0,288) puis **870 c** (Φ=0,224) ;
  - référence harmonique : 1200 / 702 / 498 c (P2, validée à l'étape 1).
- **Verdict opérationnalisé** (`etape2_p5.py`) :
  - pics principaux = pics hors zone quasi-unisson (<100 c) d'au moins 5 % du
    pic maximal ;
  - coïncidence mesuré↔harmonique si écart ≤ **25 c** ;
  - **P5 tient** si au moins un pic principal mesuré est déplacé OU si
    l'octave/la quinte harmonique n'a aucun correspondant mesuré ; **P5
    échoue** (critère d'abandon SPEC §6.2) si les structures coïncident.
  - Justification du seuil 25 c : nettement au-dessus de la tolérance validée
    de la chaîne (±15 c, §3) et de la JND d'accordage (~10 c) ; en dessous du
    plus petit déplacement prédit par l'analytique (35 c pour l'octave
    comprimée).
- Règle : après réception des données réelles, ni ces seuils ni les
  paramètres d'extraction ne sont modifiés. Toute modification demande une
  entrée datée ici, avec justification, et le réglage concerné n'est alors
  plus « fixé avant la donnée ».

*Note 2026-10-28 : ce critère est peu exigeant. Pour un spectre nettement
inharmonique, il est presque certain qu'au moins un maximum de Φ s'écarte de
plus de 25 c des maxima harmoniques. « P5 tient » signifie donc surtout que
le spectre mesuré est inharmonique et assez riche ; le contenu informatif est
dans la position des maxima, pas dans le verdict.*

## 3. Chaîne de mesure (figée)

`extraction_spectre.py` — suivi de partiels multi-trames : onset par enveloppe
d'énergie ; STFT Blackman-Harris (lobes -92 dB), zero-padding ×8 ; regroupement
des pics en raies ; un partiel = raie persistante (≥4 trames), stable (<20 c
d'excursion sur sa partie *vivante*, c.-à-d. à moins de 35 dB de son propre
max), non stationnaire (rejet des bourdonnements) ; amplitude = max des 300
premières ms après onset. Tous les paramètres sont dans l'en-tête du module.

Validation à l'aveugle (`test_extraction.py`, code retour non nul si échec) :

| Test | Signal | Résultat |
|---|---|---|
| A | 5 modes cantilever propres, décroissances égales | ratios ≤0,07 % d'erreur ; amplitudes exactes |
| B | décroissances réalistes (×20 entre modes), bruit −45 dB, désaccord +0,3 % | ratios ≤0,1 % ; **pics Φ sur spectre extrait à ≤1 c des pics sur spectre injecté** |

Journal des défauts trouvés par cette validation (et corrigés avant toute
donnée réelle) : fenêtre Hann → partiels fantômes par lobes secondaires
(corrigé : Blackman-Harris) ; persistance exigée en fraction de la durée →
perte des modes hauts à décroissance rapide (corrigé : persistance absolue) ;
raies nourries par le bruit après la mort du mode → excursion apparente gonflée
(corrigé : statistiques sur la partie vivante de la raie).

## 4. Journal du matériau (recherche du 2026-06-11)

Réseau du conteneur : seuls `github.com` / `raw.githubusercontent.com` /
`codeload.github.com` / PyPI répondent. Bloqués : freesound.org, Wikimedia
(commons/upload), archive.org, zenodo.org, huggingface.co.

- **Wikimedia Commons « Music box notes 1…13.ogg »** (CC BY-SA, notes isolées
  d'une vraie boîte) : la cible idéale, identifiée mais inaccessible d'ici.
- **Soundfonts GM « music_box » écartés après analyse spectrale** — aucun n'est
  une boîte à musique : FluidR3 = barre *accordée* (mode 2 à 4,000× sur toutes
  les notes, signature type vibraphone) ; MusyngKite et FatBoy = quasi
  harmoniques (type célesta). Même verdict pour les « boîtes à musique »
  d'applications web : synthèse à ratios entiers (spectre harmonique creux,
  donc *périodique*) — les utiliser fausserait P5 qualitativement, leurs pics
  de coïncidence tombant sur les rationnels comme un timbre harmonique.
- **VCSL (CC0)** : les dossiers « Kalimba » contiennent des mbiras à
  bourdonneurs ; spectres pollués, inutilisables proprement. *(Une kalimba
  propre — lamelle encastrée pincée, même physique d'Euler-Bernoulli — reste
  un plan B légitime ; ce serait une substitution d'exemplaire à déclarer.)*

Conclusion : pas de vrai enregistrement de boîte à musique accessible depuis ce
conteneur. La sonde spectrale qui les a écartés est elle-même un
sous-produit utile de l'étape (réutilisée dans `extraction_spectre.py`).

## 5. Ce qu'il faut pour conclure l'étape 2 (l'un OU l'autre)

1. **Un enregistrement utilisateur** : 3 notes isolées ou plus (laisser sonner
   chaque note ≥1,5 s ; notes graves de préférence — plus de modes en bande),
   micro proche de la boîte, pièce calme, **wav ou flac de préférence**
   (ogg/mp3 acceptés), sans normalisation ni effet ; si possible, noter les
   hauteurs jouées. Déposer le fichier dans la conversation suffit.
2. **OU élargir l'allowlist réseau** de l'environnement (réglages Claude Code
   web) : `freesound.org`, `commons.wikimedia.org` + `upload.wikimedia.org`,
   `archive.org`.

## 6. Rejouer

```
python3 test_extraction.py                            # doit finir OK / OK (exit 0)
python3 extraction_spectre.py note.wav [f0_hz] out.json
python3 etape2_p5.py out.json                         # verdict P5 + figure
python3 etape2_p5.py --analytique                     # démo sans mesure
python3 segmentation_notes.py melodie.mp3 notes.json  # front-end mélodie (§7)
```

---

## 7. Entrées datées (modifications et matériau postérieurs au gel)

### 2026-06-11 — premier matériau reçu : mélodie au lieu de notes isolées. Verdict P5 : non rendu.

**Reçu** : enregistrement d'une boîte à manivelle à bande perforée jouant la
fugue en ré mineur de Bach (~51 s, mp3 stéréo 44,1 kHz ; bruit de manivelle ;
voix humaine après ~30 s — analyse limitée à 0-30 s). Matériau hors
spécification §5 (mélodie polyphonique dense, ~3 notes/s, 93 onsets en 30 s).

**Ajout déclaré (couche de sélection uniquement)** : `segmentation_notes.py` —
onsets par flux spectral ; fenêtres mono-note bornées par l'onset suivant ;
gardes de naissance (un partiel doit naître à l'onset : absent avant, sans
renforcement tardif) ; regroupement statistique des occurrences par dent avec
exigence de récurrence (un partiel doit être vu dans ≥60 % des occurrences).
**Les paramètres d'extraction, la métrique Φ et les seuils du verdict n'ont pas
été touchés. Φ n'a pas été évaluée sur ce matériau.**

**Résultat de la qualification — le matériau ne qualifie pas, pour quatre
raisons indépendantes de Φ :**
1. **Distorsion de chaîne** : des doubles à ×2,000 exact de composantes fortes
   apparaissent sur des dents différentes (1,997 ±3 c sur la dent à 555,7 Hz,
   2×1,597 sur la dent à 621,4 Hz). Une lamelle encastrée n'a pas de mode à
   2,0 : c'est une 2de harmonique de distorsion (saturation micro/compression),
   qui injecte un faux partiel harmonique dans chaque spectre mesuré.
2. **Contamination polyphonique démontrée** : le diagnostic « ping d'attaque »
   (fenêtres de 50 ms post-onset, moyennées par dent) montre des composantes à
   fréquence absolue fixe partagées entre dents distinctes (926, 829, 1251 Hz)
   — les autres voix qui résonnent, vues comme de faux « modes » à des ratios
   différents par chaque dent.
3. **Indécidabilité sur musique tonale** : le contexte harmonique se répète
   avec la dent (ex. : la dent à 555,7 Hz ~C#5 co-frappée avec E6 à chaque
   harmonie de dominante → composante récurrente à 2,38 indiscernable d'un
   mode). La statistique de récurrence, conçue pour un contexte variable, ne
   sépare plus mode et contexte.
4. **Limite de chaîne sur matériau dense** : fenêtres réduites à 0,26-1,0 s
   par la densité ; un mode 2 réel à décroissance rapide (<0,15 s) peut rester
   sous l'exigence de persistance (4 trames = 0,24 s). Son absence ici n'est
   donc pas une mesure de son absence.

**Décision** : pas de verdict P5 sur ce matériau (un « P5 échoue » sur spectre
contaminé serait un faux critère d'abandon ; un « P5 tient » serait tout aussi
invalide). La chaîne, la segmentation et les diagnostics ont fonctionné :
c'est la qualification qui a arrêté la mesure, pas un réglage.

**Matériau demandé (précisé — facile avec une boîte à bande perforée)** :
perforer une bande avec des notes isolées — une seule note à la fois, ~3-4 s
entre deux trous, chaque note répétée 3-5 fois, sur 3-5 dents différentes (les
plus graves de préférence) ; manivelle lente et régulière ; micro à 10-20 cm,
niveau modéré (pas de saturation), sans AGC ni normalisation si possible ;
personne ne parle ; wav/flac de préférence, sinon mp3 à haut débit. Le bruit de
manivelle n'est pas un problème (large bande : rejeté par les filtres).

*Mise à jour (même jour)* : l'utilisateur n'a pas de boîte physique (le
matériau reçu était un rip YouTube). Matériau attendu désormais : la série
Wikimedia Commons « Music box notes 1…13 » (notes isolées d'une vraie boîte,
CC BY-SA — la cible identifiée au §4), téléchargée par l'utilisateur et
déposée dans la conversation, ou récupérée directement si l'allowlist réseau
est élargie.

### 2026-06-11 — second matériau reçu : « Music box notes 1-5 » (Wikimedia Commons, CC BY-SA), notes isolées. Qualifiant.

**Reçu** : 5 fichiers ogg (44,1 kHz, ~3-7 s), 1 à 3 frappes par fichier, notes
différentes par frappe (gamme échantillonnée sur ~994-2650 Hz). Niveaux sains
(pic ≤0,42, pas d'écrêtage). Voie de traitement : découpage par attaque
(enveloppe, +12 dB, séparation 0,4 s), extraction figée par segment.

**Constats de mesure** (avant tout calcul de Φ) :
- chaque frappe : fondamental dominant + composantes faibles ;
- harmoniques exactement entières (2,000 / 2,999, ±0,3 %) faibles, dont le
  niveau varie entre fichiers pour la même dent (994 Hz : 2,0 à amp 0,17 dans
  le fichier fort, absente dans le fichier faible) → **distorsion de chaîne
  dépendante du niveau, démontrée en interne** ;
- un mode inharmonique récurrent : **10,53× sur la dent 994 Hz, vu dans deux
  fichiers indépendants** (amp 0,13 et 0,07) ;
- composantes faibles sous le fondamental (0,89-0,94×) et à ~1,29-1,46×
  non récurrentes entre dents : sonnerie sympathique de dents voisines.

**Règles de nettoyage, déclarées ici avant tout calcul de Φ** — le spectre de
la dent retenu pour Φ est le spectre transposable de la note (ce que la voix
emporte quand elle se transpose), donc :
1. exclusion des ratios entiers exacts (|ratio − n| < 0,01, n = 2, 3, 4) :
   artefacts de chaîne prouvés ci-dessus (une lamelle encastrée n'a pas de
   modes harmoniques exacts) ;
2. exclusion des composantes sous 0,97×f0 et des composantes non récurrentes
   entre frappes de la même dent : dents voisines sympathiques et contexte —
   elles ne se transposent pas avec la voix ;
3. exclusion des frappes-accords (≥2 composantes fortes dans la zone des
   intervalles musicaux 1,06-2,30).
4. **Garde de dégénérescence** (ajoutée ici car le harnais figé suppose une
   courbe structurée ; elle ne peut qu'empêcher un verdict, jamais en
   fabriquer un) : si max Φ(mesuré) sur (100 c, 1200 c) < 5 % du pic d'octave
   du cas harmonique de référence, la courbe est déclarée plate → cas
   dégénéré du CADRAGE.md §6.4 (« spectre très pauvre → pas de structure → pas de
   grammaire ») → verdict P5 : sans objet sur cet exemplaire (ni confirmé ni
   infirmé). Déclaré après lecture des spectres extraits mais avant tout
   calcul de Φ sur ce matériau.

**Spectre retenu** (dent la plus grave, la mieux établie — 2 fichiers
indépendants) : f0 = 993,8 Hz ; partiels transposables {1,000 : amp 1,00 ;
10,53 : amp 0,10 (médiane des deux observations)}. Conservé dans
`materiau/dent994.json`.

**Résultat (verdict rendu par la chaîne figée + garde déclarée) :**

> **P5 : sans objet sur cet exemplaire — cas dégénéré.** La courbe Φ du
> spectre mesuré nettoyé est plate (max Φ = 0,0000 contre 0,7318 au pic
> d'octave harmonique) : le timbre tenu de cette boîte, tel que mesuré, est
> quasi sinusoïdal ({1 ; 10,53 à amp 0,10} — aucune paire de partiels ne
> tombe dans l'octave) et **ne porte pas de structure de fusion**. C'est le
> cas dégénéré prévu par CADRAGE.md §6.4 (« ce son ne porte pas de contrepoint ») :
> un résultat légitime, ni confirmation ni infirmation de P5.

**Sensibilité (démonstration, pas un verdict)** : en gardant les
harmoniques de distorsion ({2,000 : 0,17 ; 2,999 : 0,08}), Φ pique à 1200 c
(0,170) puis 701 c (0,014) — la distorsion de chaîne fabrique une grammaire
harmonique et aurait déclenché à tort le critère d'abandon SPEC §6.2
(« les pics coïncident »). Sans l'étape de qualification du matériau, un
artefact d'enregistrement aurait été pris pour un résultat.

**Implications** :
1. **Les amplitudes du modèle analytique sont contredites par la mesure** : les
   amplitudes analytiques (1/√k → mode 2 à 0,71) sont fausses en régime tenu
   pour ce type de boîte — les modes inharmoniques réels y sont ≥10× plus
   faibles que le fondamental. Le premier résultat P5 du test exploratoire
   reposait sur ces amplitudes irréalistes.
2. **Portée limitée à l'exemplaire** : petit peigne aigu (dents mesurées
   994-2650 Hz ; le mode 10,53 de la dent grave sort à 10,5 kHz, en limite de
   bande). Une grande boîte à cylindre à dents graves lestées (f0 200-400 Hz,
   modes en pleine bande, sustain plus long) peut porter un timbre tenu plus
   riche : P5 y reste testable tel quel.
3. **Sur ces petites boîtes, l'inharmonicité semble surtout présente dans
   l'attaque** (le « ping » bref), ce qui relève de la dimension temporelle,
   hors périmètre v1 (simultanéité statique). Hypothèse non vérifiée ici.
4. **Alternative v1 immédiate** : des timbres inharmoniques riches en régime
   tenu existent et sont documentés (cloches, carillons — cf. Harrison &
   MacConnachie 2024 cités au CADRAGE.md §2) : P5 peut être testé en v1 sur un
   spectre de cloche mesuré publié, en déclarant la substitution d'exemplaire.

**Attribution du matériau** : série « Music box notes » 1-5, Wikimedia
Commons, licence CC BY-SA 4.0, fichiers déposés par l'utilisateur dans la
conversation. Les fichiers audio ne sont pas commités au dépôt : l'attribution
exacte (auteur) est à compléter (page Commons inaccessible depuis le
conteneur). Seules les mesures dérivées (faits) sont conservées
(`materiau/dent994.json`).

### 2026-06-12 — substitution d'exemplaire déclarée : cloche de carillon (Westerkerk), spectre mesuré publié

**Décision validée par l'utilisateur** (option (b) de la réorientation) : P5
étant sans objet sur la petite boîte (timbre tenu dégénéré), on teste le
déplacement des pics de fusion sur un timbre inharmonique riche en tenu : une
cloche de carillon. La prédiction structurelle P5 (SPEC §5 : les pics de Φ se
déplacent avec le timbre, donc l'interdit de parallèles R2 aussi) s'applique
telle quelle ; seul l'exemplaire change, et ce document le déclare.

**Source (publiée)** : Harrison & MacConnachie (2024), « Consonance in
the carillon », J. Acoust. Soc. Am. 156(2). Matériaux du papier sur GitHub
(pmcharrison/CarillonConsonancePaper) : enregistrements bruts des cloches du
carillon de la Westerkerk + spectres extraits par les auteurs
(`output/lower_bell_spectrum.csv` : 11 partiels, rapports de fréquence mesurés
relatifs à la prime + amplitudes — hum 0,497/1,40 ; prime 1/1 ; tierce
1,194/1,29 ; quint 1,500/0,17 ; nominal 1,992/0,35 ; undeciem 2,588/0,27 ;
duodeciem 2,986/0,35 ; III-4 3,296/0,23 ; octave sup. 4,129/0,23 ; quarte sup.
5,381/0,19 ; sixte sup. 6,721/0,09).

**Règles, déclarées avant tout calcul de Φ sur ce matériau :**
1. Entrée du verdict = le spectre publié `lower_bell_spectrum` tel quel (aucun
   nettoyage de notre main ; les règles de nettoyage de l'entrée « boîte à
   musique » étaient propres à ce matériau-là et ne s'appliquent pas — une
   cloche est accordée vers des rapports rationnels, ses quasi-entiers sont
   réels).
2. Seuils du verdict et garde de dégénérescence : inchangés (25 c ; 5 %).
3. Contrôle de robustesse (rapporté, non décisionnel) : le même verdict relancé
   sur le spectre que notre chaîne figée extrait du wav brut du bourdon
   `12-c1.wav` du même dépôt.

**Validation croisée de la chaîne sur réel publié (avant verdict)** : sur
`12-c1.wav` brut, la chaîne figée retrouve 9 partiels nommés de la
campanologie : 0,497 (hum), 1,000 (prime), 1,185 (tierce), 1,981 (nominal),
2,501 (deciem), 2,587 (undeciem — publié : 2,588), 2,973 (duodeciem), 3,268
(III-4), 4,113 (octave sup.) — aux écarts cloche-à-cloche près. La chaîne de
mesure est donc validée sur matériau réel contre une extraction publiée
indépendante.

**Résultat (verdict de la chaîne figée) :**

> **P5 tient sur la cloche de carillon — sur les deux entrées.**
> - Spectre publié (`materiau/cloche_westerkerk_publie.json`) : pics Φ à
>   **307 c** (Φ=1,28, argmax — la tierce mineure propre de la cloche, paire
>   tierce/prime 1,194), **887 c** (0,45, paire nominal/tierce), 1193 c (0,41,
>   quasi-octave), 701 c (0,29, quinte accordée), 394 c, 454 c. Quatre pics
>   principaux déplacés (dont l'argmax, à 191 c du plus proche pic
>   harmonique) ; octave et quinte persistent en pics secondaires.
> - Contrôle de robustesse (notre extraction du bourdon brut,
>   `materiau/cloche_westerkerk_12c1_extraction.json`) : même famille de pics
>   (1183 / 889 / 703 / 295 / 462 c) → verdict tient également.
>
> Conséquence pour R2 : sur ce timbre, les intervalles de plus forte
> coïncidence ne sont plus seulement l'octave et la quinte. Le maximum le plus
> stable entre les deux profils d'amplitudes est vers 888 c ; selon le
> profil, la tierce mineure vers 307 c passe en tête. Octave et quinte restent
> des maxima secondaires, ce qui s'explique par l'accordage des cloches par
> les fondeurs.

**Nuance** : le maximum (la forme forte de P5, et l'entrée de R3) dépend du
profil d'amplitudes — tierce en tête sur le
spectre représentatif publié (hum/tierce lourdes), quasi-octave en tête sur
notre extraction mono-cloche (nominal lourd). Les positions des pics
sont stables ; leur ordre dépend de la convention d'amplitude et de la
cloche. À examiner à l'étape 3 par le balayage de τ_F.

**Rapport avec Harrison & MacConnachie** : ils trouvent, du côté de la
consonance, la tierce mineure devenue consonante sur carillon ; Φ désigne le
même intervalle comme maximum de coïncidence.

*Note 2026-10-28 : la version d'origine présentait cela comme deux mécanismes
indépendants qui convergent. C'est discutable : les deux résultats
viennent, au moins en grande partie, du même fait spectral (le partiel de tierce de la cloche, à 1,194 ×
la prime, coïncide avec la prime de l'autre voix à environ 307 c). Leur
accord était attendu, et ce résultat dépend en partie de données déjà
publiées sur ce même instrument.*
