# -*- coding: utf-8 -*-
import unittest
import logging
from tictacs import from_recipe

recipe = 'recipe.yaml'
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


class TestSentinel(unittest.TestCase):

    """Docstring for TestSentinel. no fancy checking
    just assert we got no exceptions"""

    def test_1dlist(self):
        """test with one dimensional list"""
        l = [1, 2, 3, 4, 5]
        tictac = from_recipe(recipe)
        tictac.fit(l, l)

    def test_2dlist(self):
        """test with one dimensional list"""
        l = [[1, 2, 3, 4, 5], [2, 6, 10, 20]]
        tictac = from_recipe(recipe)
        tictac.fit(l, l)

    def test_2dlist_strings(self):
        """test with one dimensional list"""
        l = [['my', 'dog', 'is', 'blue'], ['my', 'cat', 'is', 'green']]
        tictac = from_recipe(recipe)
        tictac.fit(l, l)

if __name__ == '__main__':
    unittest.main()
