# PROTOCOLE-TEST-DECISIF — pré-enregistrement (BROUILLON, non figé)

*Brouillon du 2026-10-28. Rien ici n'est encore engageant : le protocole
devient pré-enregistré au moment du commit-tag `prereg-v1` (§8). Les
décisions ouvertes, que seul le porteur du projet peut trancher, sont listées
au §9. Contexte et motifs : README.md, « Limites connues ».*

---

## 1. Question

Sur des sons **non utilisés pour construire ou calibrer le modèle**, la fusion
spectrale Φ dérivée du timbre prédit-elle quels mouvements parallèles des
auditeurs naïfs entendent comme « une seule voix », **mieux que** des modèles
plus simples ?

Un succès serait le premier résultat substantiel du projet. Un échec
délimiterait ce qu'une explication spectrale du contrepoint peut porter. Les
deux sont publiables et seront consignés de la même façon.

## 2. Hypothèses

- **H1 (principale).** Pour deux extraits à deux voix, même timbre, note contre
  note, différant par l'intervalle tenu en mouvement parallèle, les auditeurs
  choisissent comme « plus fondu » l'extrait dont l'intervalle a le Φ le plus
  élevé *pour ce timbre*.
- **H2 (comparative, celle qui compte).** Sur les essais critiques (§4.3), les
  prédictions de M_Φ concordent avec les choix plus souvent que celles de
  M_harm et de M_rug.

H1 seule ne suffit pas : sur la plupart des paires, Φ, la rugosité et la
simplicité des rapports prédisent la même chose. Seule H2, sur les essais où
les modèles divergent, peut départager.

## 3. Modèles concurrents (tous figés avant toute écoute)

Chaque modèle attribue un score à un (timbre, intervalle) ; il prédit
« l'extrait au score le plus élevé fusionne plus ».

| Code | Modèle | Dépend du timbre ? | Score |
|---|---|---|---|
| **M_Φ** | modèle du projet | oui | Φ(i) sur le spectre mesuré, σ = 6,83 c |
| **M_harm** | interdit traditionnel | non | Φ(i) sur le spectre harmonique de référence (équivaut au classement des rapports simples) |
| **M_rug** | rugosité seule | oui | −C(i), la consonance de Sethares sur le spectre mesuré, avec un signe à figer au §9 (plus lisse → plus fondu, a priori) |

**Prédicteur continu, sans seuil.** Les tests utilisent Φ brut, pas
l'ensemble seuillé à τ_F : README.md, limites 1-3, montre que les ensembles
seuillés sont sensibles à τ_F. Aucun seuil n'intervient dans ce protocole.

**Gel du modèle.** Code au commit-tag `prereg-v1` ; paramètres :
σ = 6,83 c, C de Sethares (paramètres de `metriques_fusion.py`), chaîne
d'extraction de `extraction_spectre.py`. Interdit après le tag : changer σ,
la chaîne d'extraction, le règlement de nettoyage des spectres, le signe de
M_rug, ou ajouter un modèle « qui aurait marché ».

## 4. Matériel

### 4.1 Timbres (jamais utilisés à ce jour dans le projet)

Deux instruments réels spectralement distincts, plus un contrôle :

- **T1 et T2** : deux instruments réels à §9, choisis pour que M_Φ et M_rug
  divergent. Candidats : une cloche à **tierce majeure** (profil qui déplace le
  pic de fusion de 307 c vers ~400 c, donc une prédiction de M_Φ qui
  s'inverse par rapport à la cloche Westerkerk) ; une lame de métallophone
  (vibraphone ou gamelan), dont les modes sont accordés selon un autre
  schéma.
- **T0 (contrôle)** : timbre harmonique réel (orgue, voix tenue ou cordes
  frottées), qui vérifie que la tâche reproduit le connu.

Exclus : le spectre harmonique synthétique de calibration, la cloche
Westerkerk et la boîte à musique, déjà vus par le modèle.

### 4.2 Mesure des spectres — avant toute prédiction

Pour chaque timbre : enregistrement (source, licence, sha256), extraction par
la chaîne figée, JSON commité dans `materiau/`. **Les prédictions sont
calculées puis commitées après** les spectres, sans retouche des spectres
ensuite.

### 4.3 Essais

Pour chaque timbre, toutes les paires d'intervalles parmi les états R1, en
excluant l'unisson et en se limitant au compas de l'octave, sont classées :

- **critiques** : M_Φ prédit l'inverse de M_rug **ou** de M_harm ;
- **concordants** : les trois modèles sont d'accord (ils servent à vérifier que
  la tâche fonctionne).

La sélection est faite **par script** (à écrire, `selection_essais.py`) à
partir des seules prédictions, avant toute écoute. Visée : au moins
12 paires critiques et 8 concordantes par timbre.

### 4.4 Rendu

Mêmes chemins mélodiques pour tous les timbres. Durées et enveloppes
identiques. Loudness égalisée (LUFS) par extrait. Transpositions
aléatoires dans une fenêtre fixe, pour que le registre ne soit pas un indice.
Rendu à partir des échantillons enregistrés transposés, et non d'une
resynthèse additive des partiels, sauf décision contraire au §9.

## 5. Tâche et plan

- **Choix forcé par paires (2AFC)**, comme ETAPE4 v3 : « dans quelle moitié
  les deux lignes se fondent-elles le plus en une seule ? ».
- **Ordre des moitiés** contrebalancé : chaque paire présentée dans les deux
  ordres. **Ordre des essais** randomisé par participant ; timbres entremêlés.
- **Essais pièges** (≥ 10 %) : une moitié à l'unisson contre une moitié à
  voix largement écartées et en mouvement contraire. Ils servent à repérer
  l'inattention.
- **Double aveugle** : l'application de passation tire la randomisation ;
  l'expérimentateur n'en voit pas le mapping avant la fin de la collecte.
- **Pilote** (N ≈ 3, non analysé, consigné) : uniquement pour régler le volume
  et la durée. Toute modification issue du pilote est commitée avant `prereg-v1`.

## 6. Participants

- Auditeurs **naïfs** quant à l'hypothèse ; aucune personne ayant lu ce dépôt.
- Audition déclarée normale ; casque obligatoire.
- **Taille** : N fixé à §9 par une simulation de puissance, faite avant le tag
  avec `analyse_prereg.py` sur données simulées. Cible indicative : N ≥ 20.
- **Exclusion** (seule règle admise) : moins de 80 % de réussite aux essais
  pièges. Fixée maintenant, appliquée sans regarder les autres réponses.

## 7. Analyse (script écrit et testé sur données simulées avant collecte)

- **Mesure primaire** : pour chaque modèle M, la proportion d'essais
  **critiques** où le choix du participant concorde avec la prédiction de M.
- **Test de H2** : régression logistique à effets mixtes (participant et paire
  en effets aléatoires) ; comparaison M_Φ contre M_rug et M_Φ contre M_harm
  par différence de concordance appariée par participant, avec IC à 95 %
  par bootstrap sur les participants.
- **Contrôle de validité** : sur les essais concordants, la concordance doit
  dépasser le hasard. Sinon, la tâche est invalide et le résultat est
  « non concluant », pas « réfuté ».
- **Règles de décision (figées)** :
  - **Succès** : la concordance de M_Φ dépasse celle de M_rug **et** celle de
    M_harm, avec IC à 95 % des deux différences au-dessus de 0, sur T1 et T2
    pris ensemble, sans effet contraire significatif sur l'un des deux.
  - **Échec** : au moins une des deux différences a un IC à 95 % entièrement
    ≤ 0, ou M_Φ ne dépasse pas le hasard sur les essais critiques.
  - **Non concluant** : tout le reste. Consigné tel quel, sans lecture
    favorable.
- **Analyses exploratoires** (étiquetées comme telles, hors conclusions) :
  effet par timbre, gradient de Φ, temps de réponse.

## 8. Gel

Le tag `prereg-v1` est posé **quand** les fichiers suivants sont commités :
1. ce document, complété (§9 tranché) ;
2. les spectres mesurés de T0, T1, T2 (§4.2) ;
3. les prédictions des trois modèles et la liste des essais (§4.3) ;
4. `analyse_prereg.py`, exécuté sur données simulées, avec sa sortie ;
5. les stimuli rendus, avec leurs hash.

Après le tag : collecte, puis analyse par le script tel quel. Toute déviation
est consignée datée dans un §10 « Déviations », sans réécriture des sections
précédentes (règle déjà en usage dans le projet).

## 9. Décisions ouvertes (au porteur du projet)

1. Le choix des instruments T1, T2 et T0, et la source des enregistrements
   (prise de son propre, ou dépôt public sous licence).
2. Le recrutement (entourage, plateforme en ligne, cours) et le cadre éthique
   ou de consentement requis par l'institution.
3. Le signe de M_rug : « plus lisse → plus fondu » est l'hypothèse naturelle.
   À confirmer.
4. Rendu par échantillons transposés (§4.4) ou resynthèse.
5. Faut-il ajouter une tâche objective secondaire, par exemple reconnaître une
   mélodie dans une voix (la fusion la gêne), en plus du jugement subjectif ?
