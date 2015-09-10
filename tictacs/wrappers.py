""" wrappers for functions to components """
import importlib


class FunctionWrapper(object):

    """ Wrapper for stateless transformer. Sometimes we dont need
        information about the data in order to transform it, so this
        class lets you wrap a function into an estimator object"""

    def __init__(self, func_name, pkg_name, *args, **kwargs):
        """ Initialize the wrapper. Import the package and instantiate
            an instance of the function passing the arguments"""
        pkg = importlib.import_module(pkg_name)
        func = getattr(pkg, func_name)
        self.function = func(*args, **args)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ transform data

        :X: The input to transform
        :returns: A tranformation of X implemented in function

        """
        self.function(X)
        return X
