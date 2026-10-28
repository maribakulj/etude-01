# DECISION-PHI — choix de la métrique de fusion Φ (étape 1)

*Daté du 2026-06-11. Les critères de sélection ont été écrits avant de
regarder les courbes des candidates sur un timbre inharmonique (§3). Texte
révisé le 2026-10-28 (ton, et réserve ajoutée au §3) ; décision et chiffres
inchangés. Version d'origine : `git show 9a03b9b:DECISION-PHI.md`.*

---

## 1. Décision

Φ retenue : coïncidence spectrale sous transposition, noyau gaussien
σ = 6,83 cents.

C'est la *spectral pitch similarity* de Milne (2013 ; Milne, Laney & Sharp 2016)
appliquée entre la voix A et la voix B transposée — soit l'option 2 du choix
laissé ouvert par la SPEC §7 (« autocorrélation spectrale sous transposition »).
La proxy d'origine du noyau avait exactement cette forme avec une fenêtre de
25 c choisie à la main : elle était donc une instance non calibrée d'un modèle
publié. On la conserve sous sa forme publiée, en remplaçant la seule constante
fabriquée (25 c) par la constante de la littérature (σ = 6,83 c, valeur par
défaut du package `hrep` de Harrison, ajustée sur données perceptives par
Milne).

Implémentation de référence : `metriques_fusion.proxy_coincidence(spec, r,
w_cents=6.83)`, entrée `'proxy_milne'` du registre `METRIQUES`. σ est le
seul paramètre qui représente l'oreille : 6,83 c pour l'oreille humaine dans
ce modèle. Toutes les étapes suivantes utilisent cette fonction.

## 2. Verdicts de la comparaison (timbre harmonique + récepteur humain)

Reproduire : `python3 comparaison_phi.py` (figure : `comparaison_phi.png`).

| Métrique | P2 (éliminatoire) | Pics | Port stable¹ | Pics mobiles avec le timbre² |
|---|---|---|---|---|
| Proxy d'origine (w=25c) | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | OUI |
| Proxy = Milne (σ=6,83c), retenue | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | OUI |
| Crible harmonique Darwin/Moore | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | NON (ancré aux rationnels) |
| Pitch virtuel Terhardt/Parncutt | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | NON (ancré aux rationnels) |
| Périodicité Stolzenburg (étalon) | ✓ | ~1200 / ~702 / 872 c³ | N/A | NON (aveugle par construction) |

¹ Déplacement maximal des pics quand on resserre la tolérance σ. Attendu ~0
par construction : σ règle la largeur des pics, pas leur position.
² Test de testabilité de P5, **binaire** : les positions des pics
diffèrent-elles entre timbre harmonique et boîte à musique ? On ne lit jamais
*où* vont les pics inharmoniques (cf. §3).
³ Fonction en escalier (plateaux de rationalisation) ; pics aux rapports justes
à la résolution des plateaux près ; son 3ᵉ pic M6 (872 c ~ 5/3, périodicité 3 =
celle de la quarte) est conforme au modèle publié.

Aucune métrique n'est éliminée par P2 : toutes donnent octave > quinte
(> quarte). Ce n'est pas surprenant : sur un spectre harmonique, toutes ces
mesures reviennent à favoriser les rapports de fréquence simples. P2 vérifie
l'implémentation, il ne départage pas les modèles. La hiérarchie
complète de fusion empirique (Stumpf ; DeWitt & Crowder 1987) sort des gabarits
famille A évalués à la fondamentale commune : P8 > P5 > P4 > {M3, M6} > m3.

## 3. Critères de sélection et discipline

P2 ne départage pas (toutes passent). Le choix s'est fait sur les critères
ci-dessous, sans regarder la position des pics inharmoniques des candidates :
le harnais ne sort qu'un oui/non (positions identiques ou différentes entre
harmonique et boîte à musique).

1. **Pics immobiles quand σ change.** Toutes conformes.
2. **Pics qui peuvent bouger avec le timbre.** Seule la famille B
   (coïncidence) a des pics mobiles avec le timbre. La périodicité n'utilise que le rapport de
   fondamentales. Les gabarits famille A, dans leur forme « fondamentale
   commune », lisent le spectre (les valeurs changent) mais leurs pics restent
   ancrés aux rapports rationnels des fondamentales : ils ne peuvent pas
   *déplacer* l'interdit de parallèles, ce que l'hypothèse du projet demande.
3. **Correspondance avec l'hypothèse.** L'hypothèse est « deux voix fusionnent
   quand leurs partiels coïncident » ; la coïncidence sous transposition la
   mesure directement. Les gabarits famille A mesurent autre chose : « l'union
   des deux voix ressemble-t-elle à un seul son harmonique ? », c'est-à-dire
   une perception de hauteur fondée sur des sons harmoniques.
4. **Une seule constante (σ), publiée.**

**Réserve ajoutée le 2026-10-28.** Les critères 2 et 3 reviennent à retenir
la métrique compatible avec l'hypothèse. Or la famille A modélise un
mécanisme bien documenté de la perception humaine (le regroupement des
partiels par fondamentale commune), et elle prédit des interdits ancrés aux
rapports simples quel que soit le timbre. Ce désaccord entre familles est en
lui-même une question empirique, que le choix de Φ a tranchée par décision
plutôt que par test. Le protocole de test indépendant devrait inclure un
modèle de la famille A parmi les concurrents.

## 4. Statut des candidates non retenues (conservées comme contrôles)

- `proxy_w25` : mêmes positions de pics que la forme figée, pics plus larges ;
  reléguée (sa seule constante était sans provenance).
- `sieve_darwin`, `virtual_pitch` : gardées comme modèles de contrôle de
  l'oreille humaine (elles reproduisent P2 et la hiérarchie de Stumpf). Elles
  resserviront naturellement à l'étape écoute/falsification (étape 4), où la
  question « est-ce que ça sonne fusionné pour un humain ? » est précisément la
  leur. Constantes : seuils de mistuning 3 %→8 % (Moore, Glasberg & Peters
  1985) pour le crible ; poids root-support {10,5,3,2,1} (Parncutt 1988) pour
  le pitch virtuel.
- `periodicity` (Stolzenburg 2015, tolérance 1 %) : étalon arithmétique de P2,
  validé contre les dénominateurs publiés (auto-test du module).

## 5. Réserves

1. **Provenance de σ = 6,83 c.** Ajustée par Milne sur des données d'*affinité
   mélodique* (spectres de classes de hauteur), pas sur des jugements directs
   de fusion de dyades. C'est la meilleure ancre publiée pour cette forme, pas
   une validation contre des données de fusion. La validation perceptive
   directe reste à faire (matériau possible : DeWitt & Crowder 1987 ;
   Marjieh et al. 2024). Statut : forme publiée, constante publiée, accord
   avec les autres mesures sur le cas harmonique ; pas validée contre des
   données de fusion.
2. **Famille A implémentée en forme simplifiée.** Gabarit cosinus à la
   fondamentale commune (rationalisation 1 %, horizon harmonique H=16), pas le
   modèle Terhardt/Parncutt complet (audibilité, masquage, saillances). Un
   Terhardt complet générerait des candidats de pitch virtuel aux
   sous-harmoniques de chaque partiel — y compris inharmonique — et pourrait
   avoir des pics partiellement mobiles ; son prior harmonique demeurerait.
   Validation effectuée : poids root-support et hiérarchie de Stumpf ; pas de
   comparaison bit à bit avec `parn88` (runtime R indisponible ici).
3. **Journal de la comparaison.** La première implémentation famille A
   (maximum sur fondamentale libre) échouait P2 ; diagnostic : verrouillage sur
   la fondamentale de la voix A seule (mesure d'auto-harmonicité, pas de
   fusion). Corrigée en évaluation à la fondamentale commune f0/m — la lecture
   littérale de SPEC §1. Démonstration conservée : `diag_famille_A.py`. Sans ce
   diagnostic, Parncutt aurait été éliminé à tort par P2.

## 6. Rapport à la SPEC

SPEC §1 donne la définition verbale de Φ (« se laisse décrire par une
fondamentale commune » — qui penche vers l'option gabarit) ; SPEC §7 déclare
explicitement la forme analytique ouverte entre trois options et exige que le
choix soit déclaré et identique pour tous les timbres et récepteurs. Le présent
document est cette déclaration : **option 2, autocorrélation spectrale sous
transposition**. C et Φ restent séparés ; prédictions et critères d'abandon
de la SPEC sont inchangés.

## 7. Rejouer

```
pip install -r requirements.txt
python3 metriques_fusion.py    # auto-test : constantes & périodicités publiées
python3 comparaison_phi.py     # verdicts P2/port/mobilité + figure
python3 diag_famille_A.py      # archive : pourquoi la fondamentale commune
```
