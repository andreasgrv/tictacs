""" wrappers for functions to components """


class FunctionWrapper(object):

    """ Wrapper for stateless transformer. Sometimes we dont need
        information about the data in order to transform it, so this
        class lets you wrap a function into an estimator object"""

    def __init__(self, function, *args, **kwargs):
        """ Initialize the wrapper. Import the package and instantiate
            an instance of the function passing the arguments"""
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ transform data

        :X: The input to transform
        :returns: A tranformation of X implemented in function

        """
        self.function(X, *self.args, **self.kwargs)
        return X


class PrintWrapper(object):

    """ Wrapper for stateless transformer. Sometimes we dont need
        information about the data in order to transform it, so this
        class lets you wrap a function into an estimator object"""

    def __init__(self):
        """ Initialize the wrapper. """
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ Not really a transform - just print """
        for each in X:
            print(each)
        return X
