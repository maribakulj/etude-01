#!/usr/bin/env bash
# reproduire.sh — rejoue toutes les expériences commitées et régénère figures,
# JSON et stimuli à la racine du dépôt. Aucun paramètre du modèle n'est modifié.
#
#   pip install -r requirements.txt
#   ./reproduire.sh            # sortie complète dans journal_reproduction.txt
#
# Non rejoués ici (entrée audio non commitée, cf. materiau/README.md) :
# extraction_spectre.py et segmentation_notes.py sur les enregistrements bruts.
set -euo pipefail
cd "$(dirname "$0")"
export MPLBACKEND=Agg

etape() { echo; echo "===== $* ====="; "$@"; }

{
  # Auto-tests et validation de la chaîne de mesure
  etape python3 metriques_fusion.py
  etape python3 test_extraction.py

  # Étape 1 — choix de Φ
  etape python3 test_noyau.py
  etape python3 plot_test.py
  etape python3 comparaison_phi.py
  etape python3 diag_famille_A.py

  # Étape 2 — verdicts P5 sur spectres mesurés
  etape python3 etape2_p5.py materiau/dent994.json etape2_p5_dent994.png
  etape python3 etape2_p5.py materiau/cloche_westerkerk_publie.json etape2_p5_cloche.png
  etape python3 etape2_p5.py materiau/cloche_westerkerk_12c1_extraction.json etape2_p5_cloche_12c1.png

  # Étape 3 — graphe-grammaire et fraction de Fux
  etape python3 etape3_fux.py

  # Étape 4 — stimuli d'écoute (graine fixe)
  etape python3 etape4_stimuli.py

  # Diagramme de phase (~20 s)
  etape python3 diagramme_phase.py

  # Audit de sensibilité au seuil (lit les résultats ci-dessus, STATUT.md)
  etape python3 sensibilite_seuil.py
} 2>&1 | tee journal_reproduction.txt

echo
echo "OK — vérifier les écarts avec : git status --short"
