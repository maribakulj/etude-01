# ETAPE2-PROTOCOLE — P5 sur spectre mesuré : protocole figé AVANT la mesure

*Daté du 2026-06-11. La chaîne de mesure est écrite, paramétrée et validée à
l'aveugle (sur synthétique) avant qu'aucun enregistrement réel ne soit entré
dans le système. C'est l'application à l'étape 2 de la discipline du projet :
la prédiction et l'instrument de mesure précèdent la donnée.*

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
- **Règle d'intégrité : après réception des données réelles, ni ces seuils ni
  les paramètres d'extraction ne se retouchent.** Toute retouche exige une
  entrée datée ici, avec justification, et invalide le caractère « à
  l'aveugle » du réglage concerné.

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
- **Soundfonts GM « music_box » démasqués à la sonde spectrale** — aucun n'est
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
conteneur. La sonde spectrale qui a démasqué les faux est elle-même un
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
```
