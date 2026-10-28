"""Vérifie la politique « zéro règle arbitraire » (PLAN.md §2.4)."""

import ast
import os
import re

from boucle import registre
from boucle.registre import PARAMS, SOURCES

PAQUET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(PAQUET, 'tests')


def test_sources_valides():
    for nom, p in PARAMS.items():
        assert p.source in SOURCES, nom
        assert p.description, nom


def test_oreille_a_un_test_qui_existe():
    for nom, p in PARAMS.items():
        if p.source != 'oreille':
            continue
        assert p.reference, f'{nom} : référence manquante'
        fichier, _, fonction = p.test.partition('::')
        chemin = os.path.join(TESTS, fichier)
        assert os.path.exists(chemin), f'{nom} : {fichier} introuvable'
        assert re.search(rf'^def {re.escape(fonction)}\(', open(chemin).read(), re.M), \
            f'{nom} : test {fonction} introuvable'


def test_technique_a_une_sensibilite():
    for nom, p in PARAMS.items():
        if p.source == 'technique':
            assert p.sensibilite, f'{nom} : sensibilité ni faite ni prévue'


def test_a_remplacer_dit_par_quoi():
    for nom, p in PARAMS.items():
        if p.source == 'a_remplacer':
            assert p.remplacement, nom


def _est_numerique(noeud):
    if isinstance(noeud, ast.Constant):
        return isinstance(noeud.value, (int, float)) and not isinstance(noeud.value, bool)
    if isinstance(noeud, ast.UnaryOp):
        return _est_numerique(noeud.operand)
    if isinstance(noeud, (ast.Tuple, ast.List)):
        return any(_est_numerique(e) for e in noeud.elts)
    return False


def _modules():
    for racine, dossiers, fichiers in os.walk(PAQUET):
        dossiers[:] = [d for d in dossiers if d not in ('tests', '__pycache__')]
        for f in fichiers:
            if f.endswith('.py') and f != 'registre.py':
                yield os.path.join(racine, f)


def test_aucune_constante_hors_registre():
    """Aucune constante numérique de niveau module en dehors du registre.
    Limite connue : les littéraux à l'intérieur des fonctions (conversions
    d'unités, 1200 c par octave…) ne sont pas contrôlés."""
    fautes = []
    for chemin in _modules():
        arbre = ast.parse(open(chemin).read())
        for n in arbre.body:
            if isinstance(n, ast.Assign) and _est_numerique(n.value):
                cibles = [t.id for t in n.targets if isinstance(t, ast.Name)]
                fautes.append(f'{os.path.relpath(chemin, PAQUET)}: {cibles}')
    assert not fautes, 'constantes hors registre : ' + ', '.join(fautes)


def test_registre_md_a_jour():
    with open(os.path.join(PAQUET, 'REGISTRE.md')) as fh:
        assert fh.read() == registre.en_markdown(), \
            'REGISTRE.md périmé : lancer python3 boucle/registre.py'
