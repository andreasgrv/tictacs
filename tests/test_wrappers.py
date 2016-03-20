# -*- coding: utf-8 -*-
import pytest
import logging
from tictacs import from_recipe
from tictacs.wrappers import FunctionWrapper

recipe = 'recipe.yaml'
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def add_five(X):
    """ intricate and involved function to check we can pickle
    a function wrapper object """
    return X+5


class TestSentinel(object):

    """no fancy checking yet, just assert we got no exceptions"""

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


class TestFunctionWrapper(object):

    """test repr and pickling. Note that function we are wrapping must be
    defined in module scope"""

    def test_repr(self, capfd):
        """test function wrapper repr works"""
        fw = FunctionWrapper(len)
        print(fw)
        out, err = capfd.readouterr()
        assert out.rstrip() == 'FunctionWrapper representation of: <built-in function len>'

    def test_pickle(self, capfd, tmpdir):
        """test normal pickling works with module level function"""
        fw = FunctionWrapper(add_five)
        print(fw)
        out, err = capfd.readouterr()
        assert err == ''
        tmpdir.join('exemplar').dump(fw)

    def test_pickle_failure(self, capfd, tmpdir):
        """test pickling a class member function will fail"""
        fw = FunctionWrapper(self.unpicklable_func)
        print(fw)
        out, err = capfd.readouterr()
        assert err == ''
        with pytest.raises(TypeError):
            tmpdir.join('exemplar').dump(fw)

    def unpicklable_func(self, X):
        """i am unpiclable as a member function
        - not because i am intricate and involved"""
        return X+5
