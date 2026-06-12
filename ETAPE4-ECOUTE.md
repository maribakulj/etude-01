# ETAPE4-ECOUTE — écoute de falsification : protocole et prédictions enregistrées

*Daté du 2026-06-12 (v3 — format par paires ; journal des versions au §7).
Les prédictions sont ENREGISTRÉES AVANT toute écoute des stimuli concernés.
L'auditeur (l'utilisateur) est le tribunal. Discipline : répondre aux quatre
questions AVANT de lire les §2-§3.*

---

## 1. Protocole v3 (à lire avant d'écouter — NE PAS lire plus loin)

- **Matériel** : casque ou bonnes enceintes, volume modéré. Mono par
  construction.
- **Matériau** : 4 fichiers `paire_P1.wav` … `paire_P4.wav` (~16 s chacun).
  Chaque fichier contient DEUX extraits séparés par un silence. Chaque
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

## 2. Contenu des paires — v3 (à lire APRÈS réponse)

| Paire | Moitié 1 | Moitié 2 | Ce qui est testé |
|---|---|---|---|
| P1 | harmonique, quintes parallèles (interdit R2-harm) | harmonique, chemin légal | E1 — le connu (Fux) |
| P2 | cloche, chemin légal | cloche, tierces 307 c parallèles (interdit R2-cloche) | E2 — le neuf, intra-cloche |
| P3 | cloche, quintes parallèles (~légal) | harmonique, quintes parallèles (interdit) | E3 — croisement : mêmes notes, timbre échangé |
| P4 | harmonique, tierces 307 c parallèles (légal) | cloche, tierces 307 c parallèles (interdit) | E4 — croisement symétrique |

Chemins légaux utilisés (sans unisson médian, cf. §7-v3) : harmonique
[1200, 387, 498, 969, 387, 814, 387, 618, 884, 387, 1200] ; cloche
[0, 809, 702, 307, 809, 307, 809, 307, 702, 307, 0] (cantus miroir).

## 3. Prédictions enregistrées (lettres v3)

- **E1 (contrôle, le connu)** : P1 → moitié 1 (les quintes parallèles
  fusionnent plus que le légal, sur harmonique). *Si E1 tombe, c'est Fux
  qu'on échoue à reproduire à l'écoute : rendu ou Φ en cause.*
- **E2 (le neuf)** : P2 → moitié 2 (les tierces-de-cloche parallèles
  fusionnent plus que le légal de la cloche).
- **E3 (croisement décisif)** : P3 → moitié 2 (les mêmes quintes parallèles
  fusionnent plus sur harmonique que sur cloche).
- **E4 (croisement symétrique)** : P4 → moitié 2 (les mêmes tierces 307 c
  fusionnent plus sur cloche que sur harmonique).

Confusions possibles, déclarées : sur P4-moitié 1 (307 c, harmonique), des
battements peuvent rendre le son RÊCHE sans le fusionner — la question reste
« une coulée ou deux lignes », pas « doux ou rêche ».

## 4. Ce qui ferait échouer quoi (falsification)

- **E3 et E4 tombent** → le déplacement de l'interdit n'a pas de réalité
  perceptive sur cette paire de timbres : P5 perceptif réfuté ; la
  grammaire-cloche redevient un objet formel (résultat §8.3 du CADRAGE :
  la coïncidence spectrale ne suffit pas à la fusion).
- **E1 tombe** → problème en amont (rendu ou Φ) ; tout le reste est suspendu.
- **Seuls E2/E4 tombent** → Φ prédit la fusion sur l'harmonique mais pas sur
  l'inharmonique : la borne de validité de la métrique est localisée — c'est
  une mesure, pas une défaite.

## 5. Verdict (à remplir après l'écoute)

Réponses de l'auditeur : `P1: _  P2: _  P3: _  P4: _`
E1 : __ ; E2 : __ ; E3 : __ ; E4 : __
Commentaires libres :

## 6. Rejouer

`python3 etape4_stimuli.py` — graine fixe ; ordre des moitiés et chemins dans
`etape4_mapping.json`.

---

## 7. Journal daté

### 2026-06-12 (17 h) — 1re écoute (stimuli v1, tenues statiques) : échec de plancher, consigné comme donnée

Retour auditeur : « son de synthé, pas de différenciation de voix » — y
compris sur les stimuli légaux. **Donnée, pas simple bug** : le rendu
statique littéral (tenues stationnaires, voix synchrones, même timbre, mono)
supprime tous les indices d'événement de la scène auditive ; sans événements,
pas de voix à séparer. L'idéalisation « simultanéité statique » de v1, rendue
telle quelle, ne produit pas l'explanandum. La dimension temporelle passe
d'« extension » (CADRAGE §9) à « précondition » pour toute écoute.
Correction v2 : articulation par note identique partout (attaque 15 ms,
décroissance exponentielle GLOBALE — rapports de partiels donc Φ invariants
dans la note, vérifié ±1 %) ; lettres retirées à neuf.

### 2026-06-12 (17 h 20) — 2e écoute (stimuli v2, notation absolue 1-5) : tâche inadaptée ; un micro-résultat au passage

Retours auditeur : (i) sur B (chemin légal cloche, qui alternait unissons et
intervalles) — « une voix mais parfois 2 » : **l'auditeur a entendu la
structure du chemin légal sans la connaître** (l'alternance unisson/intervalle
était réelle). Micro-datum positif. (ii) « les autres pourraient toutes avoir
2 voix » : la notation ABSOLUE 1-5 sur 13 s ne discrimine pas — tâche trop
dure, effet de plafond/ambiguïté. (iii) « ça n'a pas le son de cloches » :
acté — le rendu est l'objet-modèle, pas une imitation ; reformulé dans la
consigne.

**Correction v3 (déclarée)** :
1. **Choix forcé par paires** — les prédictions E1-E4 sont des ordres ; on les
   teste directement : 4 fichiers, deux extraits dos à dos, « quelle moitié se
   fond le plus ? ». Tâche standard en psychoacoustique, beaucoup plus
   sensible que la notation absolue.
2. **Tempo musical** (0,62 s/note) avec résonance débordante (la ségrégation
   vit dans le mouvement) — enveloppe toujours identique partout, spectre du
   modèle inchangé à chaque instant.
3. **Chemins légaux sans unisson médian** (sélection de STIMULUS, pas
   changement de grammaire) : la fusion de l'unisson est triviale par
   construction et masquait la comparaison — et c'est la règle de Fux
   (unisson aux extrémités seulement), résidu déjà documenté à l'étape 3.
4. Stimuli v2 retirés (reproductibles via git) ; prédictions inchangées sur le
   fond, reformulées par paire.