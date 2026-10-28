# Étude 01 — interdits de mouvement parallèle calculés à partir d'un spectre

*État au 2026-10-28. Ce fichier dit ce qui est implémenté, ce qui ne l'est
pas, et ce que les résultats permettent de conclure. En cas de désaccord avec
un document d'étape, c'est ce fichier qui fait foi.*

## Ce que c'est

Un ensemble de scripts Python exploratoires autour d'une question : si
l'interdit des quintes et octaves parallèles vient de ce que deux voix dont
les partiels coïncident tendent à se fondre en une seule, alors l'intervalle
à éviter devrait changer avec le timbre. Peut-on le calculer pour un spectre
donné, et le calcul correspond-il à ce qu'on entend ?

L'idée que les règles de conduite des voix s'expliquent par la perception
n'est pas nouvelle : Huron (2001, *Music Perception* 19(1)) les dérive de
principes de ségrégation des flux auditifs, pour des sons harmoniques. Ce
projet essaie d'appliquer une idée de ce type à des spectres quelconques.
Contexte et travaux existants : `CADRAGE.md`.

À partir d'un spectre (liste de partiels), les scripts calculent :

- C(i), la consonance de Sethares (fondée sur la rugosité), qui décide quels
  intervalles sont admis (règle R1, seuil τ_C) ;
- Φ(i), un indice de coïncidence des partiels (formulation de Milne,
  σ = 6,83 c), qui décide vers quels intervalles le mouvement parallèle est
  interdit (règle R2, seuil τ_F) ;
- un automate (intervalles admis × mouvements autorisés) et des
  contrepoints légaux pour un cantus donné.

Les formes de ces règles sont écrites à la main ; le système en calcule les
paramètres pour chaque spectre.

## Ce qui existe

| Élément | Statut |
|---|---|
| Mesures C et Φ, avec auto-tests | `metriques_fusion.py`, `rugosite.py` |
| Extraction de spectre depuis un WAV | `extraction_spectre.py`, validée sur signaux synthétiques (`test_extraction.py`) |
| Règles R1/R2/R3/R5, automate, recherche de chemin | `graphe_grammaire.py` |
| Spectres réels | 2 : une note de boîte à musique (spectre presque sinusoïdal, donc sans résultat) et une cloche de carillon (spectre publié par Harrison & MacConnachie, 2024) |
| Balayage d'inharmonicité | une famille synthétique (corde raide), un seul schéma de seuils |
| Écoute | 1 auditeur (l'auteur), qui connaissait l'hypothèse, 4 comparaisons |
| `lean-export/` | workflow CI qui installe Lean et Mathlib ; aucun énoncé du modèle n'y est formalisé |
| Tests | auto-tests et validation de l'extraction ; pas de suite de tests unitaires |

## Limites connues

1. **Le cas harmonique ne prouve rien.** τ_F (0,226 × max Φ fini du timbre)
   a été choisi au milieu de la plage de seuils qui reproduit Fux sur le
   spectre harmonique (ETAPE3-GRAPHE.md §1.4). Cette plage va de 0,143 à
   0,309 : en dessous, R2 interdit aussi les quartes et sixtes parallèles ;
   au-dessus, les quintes parallèles deviennent permises. Ce qui reste sans
   calibration, c'est le classement Φ(P8) > Φ(P5) > Φ(P4) > Φ(M6) > Φ(M3),
   qui correspond à la hiérarchie connue des rapports simples.

2. **Le résultat sur la cloche dépend du seuil.** Au seuil déclaré, la cloche
   interdit les parallèles vers {unisson, 307 c, 886 c} et permet quintes et
   octaves. Cet ensemble ne tient que pour τ_F ∈ [0,224 ; 0,346] : 0,002 sous
   la valeur déclarée, quintes et octaves redeviennent interdites. Seul
   l'interdit à 307 c (la tierce mineure de la cloche) tient à tout seuil, et
   la particularité de cet intervalle sur cette cloche était déjà connue
   (Harrison & MacConnachie, 2024).

3. **Le balayage d'inharmonicité dépend du seuil.** Le premier changement de
   l'ensemble des interdits à B ≈ 7,7·10⁻³ ne tient que pour τ_F ≈ 0,20-0,25 ;
   ailleurs il va de 9,4·10⁻⁴ à 1,1·10⁻¹, et le nombre de changements varie
   de 1 à 18 sur τ_F ∈ [0,10 ; 0,40] (8 au seuil déclaré). Au seuil déclaré,
   ce premier changement vient d'un interdit à 1274 c, dans la zone ouverte
   en étendant l'analyse au-delà de l'octave.

4. **Plusieurs « prédictions vérifiées » étaient presque garanties.**
   L'octave qui s'élargit avec l'inharmonicité (D2) et les maxima sur des
   carrés de rationnels (D4) découlent directement de la formule de la corde
   raide. Le critère « P5 tient » (au moins un maximum de Φ déplacé de plus
   de 25 c) est presque toujours satisfait par un spectre inharmonique. La
   stabilité des maxima de Φ quand on change de modèle d'oreille (P6) est
   vraie par construction. Ces résultats vérifient l'implémentation, pas
   l'hypothèse.

5. **Φ n'est pas validé comme mesure de fusion perceptive.** Sa formulation
   est publiée, mais σ = 6,83 c vient de données d'affinité mélodique, pas de
   jugements de fusion. Et Φ a été préférée aux mesures d'harmonicité en
   partie parce qu'elle permet aux interdits de changer avec le timbre
   (DECISION-PHI.md §3) : on a retenu la métrique compatible avec
   l'hypothèse.

6. **L'écoute est exploratoire.** 4 réponses sur 4 dans le sens prédit, par
   un seul auditeur informé, sans répétition ni contrebalancement, après
   deux révisions des stimuli suivant ses retours. Au hasard, 4 sur 4 arrive
   une fois sur 16 (p ≈ 0,06). Aucun modèle concurrent n'a fait de
   prédiction sur ces mêmes stimuli.

7. **Le code et les documents ont été écrits avec un assistant IA.** La même
   instance proposait les hypothèses, écrivait les tests et interprétait les
   résultats. Que les documents se confirment les uns les autres n'est donc
   pas une preuve indépendante.

Les chiffres des points 1 à 3 sont produits par `python3 sensibilite_seuil.py`.
Les autres biais connus sont détaillés dans `CADRAGE.md` §7.

## Prochaine étape

Pas d'extension du modèle (nouvelles règles, nouveaux timbres, nouveaux
balayages) tant que l'hypothèse n'a pas été testée dans des conditions
indépendantes. Brouillon du protocole : `PROTOCOLE-TEST-INDEPENDANT.md`.

## Boucle simulée (`boucle/`)

Une deuxième piste, séparée du modèle de grammaire : une boucle où chaque
nouvelle copie du son entre là où elle coïncide le plus avec ce qui sonne
déjà, sans gamme ni règle musicale. Question : la trajectoire dépend-elle
plus du son de départ que des réglages de la boucle ? Étape 1 (sans
consigne) : 1 prédiction sur 4 vérifiée. Le son compte plus que les réglages,
mais moins que prévu (R = 1,44 au lieu de ≥ 2). Observation non prédite : le
son fixe un réseau de hauteurs (le réseau pythagoricien pour le son
harmonique), tandis que la boucle fixe un mouvement qui n'a rien d'une
mélodie. Détails : `boucle/PROTOCOLE.md`, `boucle/RESULTATS.md`.
Plan jusqu'au prototype, sans règle musicale arbitraire : `boucle/PLAN.md`.

## Reproduire

```bash
pip install -r requirements.txt
./reproduire.sh
```

Le script rejoue toutes les expériences commitées (~4 min) et écrit le journal
dans `journal_reproduction.txt`. Rejoué le 2026-10-28 avec les versions de
`requirements.txt` : les JSON et WAV régénérés sont identiques octet pour
octet à ceux du dépôt, et les verdicts sont inchangés. Les PNG diffèrent
seulement par le rendu de la version de matplotlib. `extraction_spectre.py`
et `segmentation_notes.py` ne sont pas rejoués sur les enregistrements bruts,
qui ne sont pas commités (cf. `materiau/README.md`).

## Documents

1. `CADRAGE.md` — la question, les travaux existants, les biais connus.
2. `HISTORIQUE.md` — ce qui a été fait, dans l'ordre, et ce que chaque étape montre.
3. `SPEC-v1-graphe-grammaire.md` — modèle et prédictions, enregistrés avant calcul.
4. `DECISION-PHI.md` — choix de la mesure Φ (étape 1).
5. `ETAPE2-PROTOCOLE.md` — spectres mesurés (étape 2).
6. `ETAPE3-GRAPHE.md` — règles et automates (étape 3).
7. `ETAPE4-ECOUTE.md` — écoute exploratoire (étape 4).
8. `DIAGRAMME-PHASE.md` — balayage de l'inharmonicité.
9. `PROTOCOLE-TEST-INDEPENDANT.md` — brouillon du test indépendant.

Les documents d'étape ont été révisés le 2026-10-28 (ton, vocabulaire,
réserves) ; leurs prédictions, seuils et résultats chiffrés sont inchangés.
Les versions d'origine sont dans l'historique git (commit `9a03b9b`).
