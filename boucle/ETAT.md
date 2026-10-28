# État d'avancement du plan (`PLAN.md`)

*Tenu à jour par la boucle de travail autonome à chaque itération. Une ligne
par unité de travail terminée, avec le commit correspondant.*

## Phase en cours

Phase 2 — Boucle v2 sans consigne. Prochaine unité : protocole de la phase
2, avec en particulier la mesure de proximité entre événements successifs
pour les sons inharmoniques (la hauteur virtuelle n'est pas fiable pour eux,
PHASE1-RESULTATS.md §4), et le remplacement d'EXCLUSION, W_MIN, T_MIN/T_MAX,
TAUS et DUREE_PAS.

## Fait

- Étape 1 de la boucle simulée (protocole `2a4e20d`, code `5942083`,
  résultats `fd4b0eb`) ; plan `92d5161`.
- Phase 0 terminée. Paquet, registre (29 paramètres : 1 oreille,
  21 techniques, 7 à remplacer), module `oreille/`, 8 tests (`501aaf1`).
  Critère de sortie rempli : `python3 boucle/boucle.py` puis `rendu.py`
  redonnent `resultats.json`, les 8 sons et la figure identiques au bit près.
  Défaut trouvé et corrigé : l'élagage du calcul de coïncidence supposait une
  grille couvrant tout le registre.

- Phase 1 terminée (`f9712a9` code, résultats dans `PHASE1-RESULTATS.md`).
  Tests de cohérence et C2 passent ; la hauteur virtuelle échoue sur le son
  à partiels décalés et sur la cloche (note de frappe non retrouvée). La
  hauteur des sons inharmoniques est donc « non modélisée ».

## En attente d'une personne ou de matériel

- Écoutes de fin de phase (retours, pas preuves) : à faire par le porteur du
  projet à chaque phase terminée.
- Phase 4 : participants, cadre éthique, éventuelle collaboration.
- Phase 5 : haut-parleur, micro, ordinateur relié à la session.
- Phase 6 : mesure de latence sur une vraie machine audio.
- Phase 7 : auditeurs, compositeurs.

## Journal

- 2026-10-28 : fichier créé ; boucle autonome lancée.
- 2026-10-28 : phase 0 terminée.
- 2026-10-28 : phase 1 terminée ; 2 validations sur 3 de la hauteur virtuelle échouent.
- 2026-10-28 : protocole de la phase 1 (sources lues : van Noorden 1975 en
  texte intégral, Moore et al. 1986 en résumé ; les autres marquées à vérifier).
