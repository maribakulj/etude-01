# ETAPE4-ECOUTE — écoute exploratoire : protocole et prédictions enregistrées

*Daté du 2026-06-12 (v3, format par paires ; versions précédentes au §7).
Les prédictions ont été écrites avant l'écoute des stimuli concernés.
L'auditeur est l'auteur du projet. Consigne : répondre aux quatre questions
avant de lire les §2-§3. Texte révisé le 2026-10-28 (ton ; lecture du
verdict au §5) ; protocole, prédictions et réponses inchangés. Version
d'origine : `git show 9a03b9b:ETAPE4-ECOUTE.md`.*

---

## 1. Protocole v3 (à lire avant d'écouter — NE pas lire plus loin)

- **Matériel** : casque ou bonnes enceintes, volume modéré. Mono par
  construction.
- **Matériau** : 4 fichiers `paire_P1.wav` … `paire_P4.wav` (~16 s chacun).
  Chaque fichier contient deux extraits séparés par un silence. Chaque
  extrait : deux voix de même timbre, note contre note, notes articulées dont
  la résonance déborde (comme un carillon).
- **La question, une par fichier** : *dans quelle moitié les deux lignes se
  fondent-elles le plus en une seule coulée ?* Réponse : « moitié 1 » ou
  « moitié 2 » (+ « net » ou « léger » si tu veux qualifier).
- Le timbre n'a pas à « faire cloche » : c'est l'objet-modèle qu'on écoute
  (spectre publié + enveloppe commune), pas une imitation. La question n'est
  jamais le réalisme ni l'agrément — seulement : une coulée, ou deux lignes ?
- Réécoute librement chaque fichier avant de répondre.
- **Noter les quatre réponses avant de lire la suite.**

Grille : `P1: moitié _   P2: moitié _   P3: moitié _   P4: moitié _`

---

## 2. Contenu des paires — v3 (à lire après réponse)

| Paire | Moitié 1 | Moitié 2 | Ce qui est testé |
|---|---|---|---|
| P1 | harmonique, quintes parallèles (interdit R2-harm) | harmonique, chemin légal | E1 — cas connu (Fux) |
| P2 | cloche, chemin légal | cloche, tierces 307 c parallèles (interdit R2-cloche) | E2 — interdit propre à la cloche |
| P3 | cloche, quintes parallèles (~légal) | harmonique, quintes parallèles (interdit) | E3 — croisement : mêmes notes, timbre échangé |
| P4 | harmonique, tierces 307 c parallèles (légal) | cloche, tierces 307 c parallèles (interdit) | E4 — croisement symétrique |

Chemins légaux utilisés (sans unisson médian, cf. §7-v3) : harmonique
[1200, 387, 498, 969, 387, 814, 387, 618, 884, 387, 1200] ; cloche
[0, 809, 702, 307, 809, 307, 809, 307, 702, 307, 0] (cantus miroir).

## 3. Prédictions enregistrées (lettres v3)

- **E1 (contrôle, cas connu)** : P1 → moitié 1 (les quintes parallèles
  fusionnent plus que le légal, sur harmonique). *Si E1 tombe, c'est Fux
  qu'on échoue à reproduire à l'écoute : rendu ou Φ en cause.*
- **E2 (interdit propre à la cloche)** : P2 → moitié 2 (les tierces-de-cloche parallèles
  fusionnent plus que le légal de la cloche).
- **E3 (croisement)** : P3 → moitié 2 (les mêmes quintes parallèles
  fusionnent plus sur harmonique que sur cloche).
- **E4 (croisement symétrique)** : P4 → moitié 2 (les mêmes tierces 307 c
  fusionnent plus sur cloche que sur harmonique).

Confusions possibles, déclarées : sur P4-moitié 1 (307 c, harmonique), des
battements peuvent rendre le son rêche sans le fusionner — la question reste
« une coulée ou deux lignes », pas « doux ou rêche ».

## 4. Ce qui ferait échouer quoi

- **E3 et E4 tombent** → le déplacement de l'interdit n'a pas de réalité
  perceptive sur cette paire de timbres : la grammaire calculée pour la
  cloche n'est qu'un objet formel, et la coïncidence spectrale ne suffit pas
  à prédire la fusion.
- **E1 tombe** → problème en amont (rendu ou Φ) ; tout le reste est suspendu.
- **Seuls E2/E4 tombent** → Φ prédit la fusion sur l'harmonique mais pas sur
  l'inharmonique : la métrique ne vaudrait que pour les spectres harmoniques.

## 5. Verdict — rempli le 2026-06-12, 17 h 31 (réponses verbatim de l'auditeur)

Réponses : « P1 : moitié 1 se fond plus, + net ; P2 : moitié 2 ; P3 :
moitié 2 ; P4 : difficile mais moitié 2 un peu, plus net ».

| Prédiction | Prédit | Répondu | Verdict |
|---|---|---|---|
| E1 — quintes ∥ vs légal (harmonique) | moitié 1 | moitié 1, « net » | dans le sens prédit |
| E2 — légal vs tierces-de-cloche ∥ (cloche) | moitié 2 | moitié 2 | dans le sens prédit |
| E3 — quintes ∥ : cloche vs harmonique | moitié 2 | moitié 2 | dans le sens prédit |
| E4 — tierces 307 c ∥ : harmonique vs cloche | moitié 2 | moitié 2, « difficile, un peu » | dans le sens prédit (faible) |

4 réponses sur 4 dans le sens prédit (E4 jugée difficile).

Ce que cela permet de dire : pour cet auditeur, les stimuli ne contredisent
pas les prédictions. E1 indique que le rendu fait entendre une différence de
fusion sur le cas connu. E3 et E4 vont dans des sens opposés (harmonique plus
fondu pour les quintes, cloche plus fondue pour les tierces de 307 c), ce qui
rend moins probable qu'une impression générale du type « la cloche fusionne
toujours moins » explique tout ; mais E4 est faible.

Ce que cela ne permet pas de dire : que l'interdit de quintes dépend du
timbre à l'oreille en général. Limites :
- un seul auditeur, l'auteur du projet, qui connaissait l'hypothèse ;
  l'aveugle ne portait que sur l'ordre des moitiés et repose sur le fait que
  le mapping n'a pas été lu avant de répondre ;
- un seul essai par prédiction, sans répétition ni contrebalancement ; au
  hasard, 4 sur 4 arrive avec une probabilité de 1/16 (≈ 0,06) ;
- les stimuli ont été modifiés deux fois après les retours de ce même
  auditeur (§7) ;
- les sons sont synthétisés à partir des spectres du modèle, avec une
  enveloppe ajoutée ; ce ne sont pas des enregistrements d'instruments ;
- aucun modèle concurrent (rugosité seule, harmonicité) n'a fait de
  prédiction sur ces paires : on ne sait pas si Φ prédit mieux qu'eux ;
- les quintes parallèles sur cloche (P3, moitié 1) sont légales au seuil
  déclaré, mais ce statut est fragile (ETAPE3-GRAPHE.md §7).

Statut : retour exploratoire compatible avec l'hypothèse, à tester dans des
conditions indépendantes (`PROTOCOLE-TEST-INDEPENDANT.md`).

## 6. Rejouer

`python3 etape4_stimuli.py` — graine fixe ; ordre des moitiés et chemins dans
`etape4_mapping.json`.

---

## 7. Journal daté

### 2026-06-12 (17 h) — 1re écoute (stimuli v1, tenues statiques) : aucune voix distincte

Retour auditeur : « son de synthé, pas de différenciation de voix », y
compris sur les stimuli légaux. Le rendu statique (tenues stationnaires,
voix synchrones, même timbre, mono) supprime les indices temporels qui
permettent de séparer des voix. Le modèle v1, qui ignore le temps, ne suffit
donc pas à produire des stimuli où la question a un sens : il faut au moins
une articulation des notes, que le modèle ne contient pas.
Correction v2 : articulation par note identique partout (attaque 15 ms,
décroissance exponentielle globale — rapports de partiels donc Φ invariants
dans la note, vérifié ±1 %) ; lettres retirées à neuf.

### 2026-06-12 (17 h 20) — 2e écoute (stimuli v2, notation absolue 1-5) : tâche inadaptée

Retours auditeur : (i) sur B (chemin légal cloche, qui alternait unissons et
intervalles) — « une voix mais parfois 2 » : **l'auditeur a entendu la
structure du chemin légal sans la connaître** (l'alternance unisson/intervalle
était réelle). Observation isolée, à ne pas surinterpréter. (ii) « les autres pourraient toutes avoir
2 voix » : la notation absolue 1-5 sur 13 s ne discrimine pas — tâche trop
dure, effet de plafond/ambiguïté. (iii) « ça n'a pas le son de cloches » :
acté — le rendu est l'objet-modèle, pas une imitation ; reformulé dans la
consigne.

**Correction v3 (déclarée)** :
1. **Choix forcé par paires** — les prédictions E1-E4 sont des ordres ; on les
   teste directement : 4 fichiers, deux extraits dos à dos, « quelle moitié se
   fond le plus ? ». Tâche courante en psychoacoustique, en général plus
   sensible qu'une notation absolue.
2. **Tempo musical** (0,62 s/note) avec résonance débordante (les voix se séparent
   surtout grâce aux changements dans le temps) — enveloppe toujours identique partout, spectre du
   modèle inchangé à chaque instant.
3. **Chemins légaux sans unisson médian** (sélection de stimulus, pas
   changement de grammaire) : la fusion de l'unisson est triviale par
   construction et masquait la comparaison — et c'est la règle de Fux
   (unisson aux extrémités seulement), résidu déjà documenté à l'étape 3.
4. Stimuli v2 retirés (reproductibles via git) ; prédictions inchangées sur le
   fond, reformulées par paire.