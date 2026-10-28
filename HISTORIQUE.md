# Historique

*Remplace `PASSATION.md` le 2026-10-28. L'ancien fichier était une note de
passation entre sessions d'un assistant IA, complétée au fil des étapes ; son
texte d'origine est dans l'historique git
(`git show 9a03b9b:PASSATION.md`). Ici : ce qui a été fait, dans l'ordre, et
ce que chaque étape montre réellement. Le détail est dans les documents
d'étape.*

---

## 2026-06-11 — Noyau exploratoire

`test_noyau.py`, `plot_test.py`. Deux timbres analytiques (harmonique ;
boîte à musique d'après le modèle de poutre encastrée, amplitudes posées à la
main), deux « récepteurs » (largeur de bande critique normale ou réduite).

- P2 : sur l'harmonique, les maxima de Φ sont à l'octave, la quinte, la
  quarte. Attendu pour toute mesure de coïncidence de partiels.
- P5 : sur la boîte analytique, les maxima se déplacent (1165 c, 870 c).
  Ce résultat reposait sur des amplitudes inventées ; la mesure de
  l'étape 2 a montré qu'elles étaient irréalistes.
- P6 : les maxima de Φ ne bougent pas quand on change le récepteur, ceux de
  C bougent. Vrai par construction (CADRAGE.md §5).

## 2026-06-11 — Étape 1 : choix de Φ (`DECISION-PHI.md`)

Quatre mesures de la littérature implémentées et comparées. Toutes
retrouvent octave > quinte > quarte sur l'harmonique. Retenue : la
coïncidence de Milne, σ = 6,83 c. Ce choix favorise l'hypothèse
(CADRAGE.md §7, point 5). σ vient de données d'affinité mélodique, pas de
fusion.

## 2026-06-11 / 12 — Étape 2 : spectres mesurés (`ETAPE2-PROTOCOLE.md`)

- Chaîne d'extraction écrite et validée sur signaux synthétiques avant toute
  donnée réelle.
- Premier enregistrement (boîte à musique jouant une fugue, depuis une vidéo)
  : inutilisable, pas de verdict.
- Notes isolées d'une vraie boîte (Wikimedia Commons) : en régime tenu, le
  spectre est presque une sinusoïde ; Φ est plate ; pas de verdict.
- Substitution déclarée : cloche grave de la Westerkerk, spectre publié par
  Harrison & MacConnachie (2024). Les maxima de Φ sont déplacés (307 c en
  tête, puis 887 c) ; octave et quinte restent des maxima secondaires. Le
  critère « P5 tient » était peu exigeant (CADRAGE.md §7, point 3), et la
  particularité de la tierce mineure de cette cloche était déjà connue.

## 2026-06-12 — Étape 3 : grammaire et automates (`ETAPE3-GRAPHE.md`)

- Harmonique : interdits de parallèles {unisson, quinte, octave} au seuil
  déclaré ; ce seuil a été choisi pour obtenir ce résultat.
- L'inventaire des intervalles admis ne correspond à celui de Fux à aucun
  seuil (quarte admise, deux intervalles septimaux admis, pas de tierce
  mineure).
- Cloche : interdits {unisson, 307 c, 886 c}. Le seuil déclaré est à 0,002 du
  bord de la plage où ce résultat tient ; seul l'interdit à 307 c est robuste
  (ajout du 2026-10-28).
- Une première interprétation (« le cantus de Fux est rejeté par la
  grammaire de la cloche, le matériau mélodique dépend du timbre ») a été
  corrigée le jour même : le rejet venait de conventions du modèle, pas de Φ.

## 2026-06-12 — Étape 4 : écoute (`ETAPE4-ECOUTE.md`)

Quatre comparaisons par paires, prédictions écrites avant l'écoute. Après
deux versions de stimuli qui ne permettaient pas de répondre, la troisième a
donné 4 réponses sur 4 dans le sens prédit, par un seul auditeur qui
connaissait l'hypothèse. Au hasard, 4 sur 4 arrive une fois sur 16. C'est un
retour exploratoire, pas une validation.

## 2026-07-27 — CI Lean

Ajout d'un workflow qui installe Lean 4.32.1 et Mathlib et exporte la
chaîne d'outils (`lean-export/`). Rien du modèle n'y est formalisé.

## 2026-09-07 — Balayage de l'inharmonicité (`DIAGRAMME-PHASE.md`)

Spectre de corde raide, coefficient B de 0 à 10. Prédictions D1-D4 commitées
avant le calcul (commit `b3be72f`). Les quatre sont vérifiées, mais :
D2 (octave qui s'élargit quand B croît) et D4 (maxima sur des carrés de
rationnels quand B est grand) découlent directement de la formule de la
corde ; D3 (l'ensemble des interdits change de taille) a été évalué avec un
critère redéfini après un premier comptage ; la position du premier
changement dépend fortement du seuil (ajout du 2026-10-28).

## 2026-10-28 — Relecture critique et réécriture

À la suite d'une relecture externe : `README.md` (statut et limites),
`sensibilite_seuil.py` (sensibilité au seuil), `reproduire.sh` et
`requirements.txt`, chemins de sortie relatifs, brouillon de protocole de
test indépendant. Puis réécriture des documents pour retirer le vocabulaire
non défini, rendre visibles les biais et ramener les conclusions à ce que
les données permettent. Les prédictions, seuils et résultats chiffrés des
documents d'étape n'ont pas été modifiés.

## Suite envisagée

Ne pas étendre le modèle avant le test de `PROTOCOLE-TEST-INDEPENDANT.md`.
