# DECISION-PHI — choix de la métrique de fusion Φ (étape 1)

*Daté du 2026-06-11. Document de décision exigé par la PASSATION (étape 1 :
« choisir, déclarer le choix, le figer pour tous les timbres comparés »). Les
critères de sélection ci-dessous ont été déclarés AVANT tout regard sur les
courbes inharmoniques des candidates (verrou anti-circularité, cf. §3).*

---

## 1. Décision

**Φ figée = coïncidence spectrale sous transposition, noyau gaussien σ = 6,83 cents.**

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
w_cents=6.83)`, entrée `'proxy_milne'` du registre `METRIQUES`. La fenêtre σ
est LE paramètre récepteur (le « port ») : humain ≈ 6,83 c ; autre récepteur =
autre σ. Toute la suite du projet (étapes 2+) consomme cette fonction.

## 2. Verdicts de la comparaison (timbre harmonique + récepteur humain)

Reproduire : `python3 comparaison_phi.py` (figure : `comparaison_phi.png`).

| Métrique | P2 (éliminatoire) | Pics | Port stable¹ | Pics mobiles avec le timbre² |
|---|---|---|---|---|
| Proxy d'origine (w=25c) | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | OUI |
| **Proxy = Milne (σ=6,83c)** | **✓** | **1200,0 / 702,0 / 498,0 c** | **✓ (0 c)** | **OUI** |
| Crible harmonique Darwin/Moore | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | NON (ancré aux rationnels) |
| Pitch virtuel Terhardt/Parncutt | ✓ | 1200,0 / 702,0 / 498,0 c | ✓ (0 c) | NON (ancré aux rationnels) |
| Périodicité Stolzenburg (étalon) | ✓ | ~1200 / ~702 / 872 c³ | N/A | NON (aveugle par construction) |

¹ Déplacement maximal des pics quand on resserre la fenêtre récepteur — doit
être ~0 (invariant substrat/saillance : la fenêtre règle la finesse, pas la
position).
² Test de testabilité de P5, **binaire** : les positions des pics
diffèrent-elles entre timbre harmonique et boîte à musique ? On ne lit jamais
*où* vont les pics inharmoniques (cf. §3).
³ Fonction en escalier (plateaux de rationalisation) ; pics aux rapports justes
à la résolution des plateaux près ; son 3ᵉ pic M6 (872 c ~ 5/3, périodicité 3 =
celle de la quarte) est conforme au modèle publié.

**Aucune métrique n'est éliminée par P2.** Toutes reproduisent octave > quinte
(> quarte). Fait notable : les deux familles indépendantes (coïncidence ET
harmonicité-gabarit) plus l'étalon de périodicité retrouvent la même structure
— le résultat P2 du noyau n'était pas un artefact de la proxy. La hiérarchie
complète de fusion empirique (Stumpf ; DeWitt & Crowder 1987) sort des gabarits
famille A évalués à la fondamentale commune : P8 > P5 > P4 > {M3, M6} > m3.

## 3. Critères de sélection et discipline

P2 ne départage pas (toutes passent — attendu : c'est un critère de *contrôle*,
pas de sélection). Le choix s'est fait sur les critères structurels déclarés au
plan, **sans regarder la position des pics inharmoniques d'aucune candidate**
— sinon on aurait sélectionné la métrique qui « confirme » P5, c'est-à-dire
réécrit la prédiction après coup. Le harnais ne sort qu'un binaire
(positions identiques / différentes).

1. **Conformité au port (invariant substrat/saillance).** Toutes conformes :
   pics immobiles sous resserrement de fenêtre.
2. **Capacité à porter P5 (testabilité).** Seule la famille B (coïncidence) a
   des pics mobiles avec le timbre. La périodicité n'utilise que le rapport de
   fondamentales. Les gabarits famille A, dans leur forme « fondamentale
   commune », lisent le spectre (les valeurs changent) mais leurs pics restent
   ancrés aux rapports rationnels des fondamentales : ils ne peuvent pas
   *déplacer* l'interdit de parallèles, qui est la thèse même du projet.
3. **Fidélité au mécanisme du CADRAGE §4.** La thèse est « fusion = mouvement
   préservant les symétries du réseau spectral de CE timbre » : la coïncidence
   sous transposition est l'opérationnalisation directe. Les gabarits famille A
   opérationnalisent autre chose : « l'union ressemble-t-elle à UN son
   harmonique ? » — ils embarquent le prior harmonique du système de pitch
   humain. Légitime comme modèle du récepteur, pas comme substrat.
4. **Sobriété et provenance des constantes.** Une seule constante (σ), publiée.

## 4. Statut des candidates non retenues (conservées comme contrôles)

- `proxy_w25` : mêmes positions de pics que la forme figée, pics plus larges ;
  reléguée (sa seule constante était sans provenance).
- `sieve_darwin`, `virtual_pitch` : **validées comme modèles de contrôle du
  récepteur humain** (elles reproduisent P2 et la hiérarchie de Stumpf). Elles
  resserviront naturellement à l'étape écoute/falsification (étape 4), où la
  question « est-ce que ça sonne fusionné pour un humain ? » est précisément la
  leur. Constantes : seuils de mistuning 3 %→8 % (Moore, Glasberg & Peters
  1985) pour le crible ; poids root-support {10,5,3,2,1} (Parncutt 1988) pour
  le pitch virtuel.
- `periodicity` (Stolzenburg 2015, tolérance 1 %) : étalon arithmétique de P2,
  validé contre les dénominateurs publiés (auto-test du module).

## 5. Réserves d'honnêteté (à garder pour thèse/article)

1. **Provenance de σ = 6,83 c.** Ajustée par Milne sur des données d'*affinité
   mélodique* (spectres de classes de hauteur), pas sur des jugements directs
   de fusion de dyades. C'est la meilleure ancre publiée pour cette forme, pas
   une validation contre des données de fusion. La validation perceptive
   directe reste devant nous (matériau possible : DeWitt & Crowder 1987 ;
   Marjieh et al. 2024). Le statut de la pièce centrale passe donc de « proxy
   fabriquée, non validée » à « forme publiée, constante publiée, corroborée
   structurellement par deux familles indépendantes sur le cas connu » — pas
   encore « validée contre données de fusion ».
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

## 6. Rapport à la SPEC (rien n'est réécrit)

SPEC §1 donne la définition verbale de Φ (« se laisse décrire par une
fondamentale commune » — qui penche vers l'option gabarit) ; SPEC §7 déclare
explicitement la forme analytique ouverte entre trois options et exige que le
choix soit déclaré et identique pour tous les timbres et récepteurs. Le présent
document est cette déclaration : **option 2, autocorrélation spectrale sous
transposition**. Les invariants tiennent inchangés : substrat arithmétique
(positions des coïncidences) + fenêtre récepteur (σ) ; C et Φ jamais mélangés ;
prédictions et critères d'abandon intacts.

## 7. Rejouer

```
pip install numpy matplotlib
python3 metriques_fusion.py    # auto-test : constantes & périodicités publiées
python3 comparaison_phi.py     # verdicts P2/port/mobilité + figure
python3 diag_famille_A.py      # archive : pourquoi la fondamentale commune
```
