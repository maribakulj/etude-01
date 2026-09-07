# Matériau mesuré

- `dent994.json` — spectre transposable de la dent la plus grave (f0 = 993,8 Hz)
  d'une boîte à musique réelle. Source : série « Music box notes » (fichiers 2
  et 4), Wikimedia Commons, CC BY-SA 4.0, déposée par l'utilisateur dans la
  conversation du 2026-06-11. Méthode et règles de nettoyage :
  `ETAPE2-PROTOCOLE.md` §7 (entrée « second matériau »). Les fichiers audio ne
  sont pas commités (attribution exacte à compléter) ; les mesures dérivées
  sont des faits, non soumis au droit d'auteur.

Rejouer le verdict : `python3 etape2_p5.py materiau/dent994.json`

- `cloche_westerkerk_publie.json` — spectre représentatif publié de la cloche
  grave du carillon de la Westerkerk : Harrison & MacConnachie (2024),
  « Consonance in the carillon », JASA 156(2), fichier
  `output/lower_bell_spectrum.csv` du dépôt
  github.com/pmcharrison/CarillonConsonancePaper. Entrée du verdict P5
  (substitution déclarée, ETAPE2-PROTOCOLE.md §7, 2026-06-12).
- `cloche_westerkerk_12c1_extraction.json` — extraction par NOTRE chaîne figée
  du bourdon brut `12-c1.wav` du même dépôt (contrôle de robustesse).

Rejouer : `python3 etape2_p5.py materiau/cloche_westerkerk_publie.json`
