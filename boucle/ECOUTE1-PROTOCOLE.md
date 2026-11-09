# Écoute 1 — trajectoire de la boucle contre ordre mélangé

*Écrit le 2026-11-09, avant l'écoute. La correspondance entre fichiers et
versions est tenue hors du dépôt jusqu'à la réponse, puis commitée avec le
verdict dans `ECOUTE1-RESULTATS.md`.*

## Question

Les lignes que l'auditeur entend viennent-elles de l'ordre des notes produit
par la boucle, ou seulement du tempo et de l'articulation ?

## Matériel

Deux paires de fichiers, `boucle/sons/ecoute1_A1.wav` / `A2` (son
harmonique) et `ecoute1_B1.wav` / `B2` (cloche Westerkerk). Dans chaque paire,
l'un est une trajectoire de la phase 2 (règle `argmax`, T = 200 ms, τ le plus
court), l'autre contient **exactement les mêmes notes dans un ordre mélangé
au hasard**, au même tempo et avec le même rendu. L'ordre des deux fichiers
est tiré au hasard (graine au registre). Script : `boucle/ecoute1.py`.

## Consigne

Pour chaque paire, écouter les deux fichiers (autant de fois que voulu) et
répondre : **dans lequel entends-tu le plus de lignes**, c'est-à-dire des
notes qui se suivent et forment un trajet continu, plutôt que des notes
isolées ? Réponse : 1 ou 2, éventuellement « pas de différence ». Un mot
facultatif sur ce qui fait la différence.

## Prédiction du modèle d'oreille (calculée avant l'écoute)

Variante A (frontière de cohérence de van Noorden) :

| Paire | Original | Mélangé |
|---|---|---|
| A (harmonique) | 6 lignes, 88 % des notes dans une ligne d'au moins 4 | 25 lignes, 31 % |
| B (cloche) | 4 lignes, 94 % | 26 lignes, 16 % |

Le modèle prédit donc que, dans chaque paire, l'auditeur entend plus de
lignes dans l'original.

## Ce que chaque issue voudrait dire

- **L'original est désigné dans les deux paires** : l'ordre produit par la
  boucle crée des lignes audibles, et le modèle va dans le bon sens.
- **Pas de différence** : les lignes entendues tiennent au tempo et à
  l'articulation ; le modèle surestime l'effet de l'ordre.
- **Le mélangé est désigné** : le modèle se trompe de sens.

## Limites, déclarées d'avance

Un seul auditeur, qui connaît le projet et a vu la figure des lignes ; une
seule paire par son ; deux essais au total, donc au hasard, désigner
l'original deux fois arrive une fois sur quatre. C'est un retour, pas une
preuve.
