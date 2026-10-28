# État d'avancement du plan (`PLAN.md`)

*Tenu à jour par la boucle de travail autonome à chaque itération. Une ligne
par unité de travail terminée, avec le commit correspondant.*

## Phase en cours

Phase 1 — L'oreille, à partir de données : prochaine unité = protocole de la
phase (composants, données publiées de référence, tolérances), avant tout
code.

## Fait

- Étape 1 de la boucle simulée (protocole `2a4e20d`, code `5942083`,
  résultats `fd4b0eb`) ; plan `92d5161`.
- Phase 0 terminée. Paquet, registre (28 paramètres : 1 oreille,
  20 techniques, 7 à remplacer), module `oreille/`, 8 tests (`501aaf1`).
  Critère de sortie rempli : `python3 boucle/boucle.py` puis `rendu.py`
  redonnent `resultats.json`, les 8 sons et la figure identiques au bit près.
  Défaut trouvé et corrigé : l'élagage du calcul de coïncidence supposait une
  grille couvrant tout le registre.

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
