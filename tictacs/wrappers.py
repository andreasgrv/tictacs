""" wrappers for functions to components """
# TODO - move thes to extend class depending on case


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

    def __repr__(self):
        """ User friendly string version
        :returns: str representation

        """
        return '%(__class__)s wrapping function %(function)s\n' % self.__dict__

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ transform data

        :X: The input to transform
        :returns: A tranformation of X implemented in function

        """
        X = self.function(X, *self.args, **self.kwargs)
        return X

    def get_params(self, deep=True):
        """Get parameters for this estimator.
        Parameters
        ----------
        deep: boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.
        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        out = dict()
        out['function'] = self.function
        return out


class PrintWrapper(object):

    """ Wrapper for stateless transformer. Sometimes we dont need
        information about the data in order to transform it, so this
        class lets you wrap a function into an estimator object"""

    def __init__(self):
        """ Initialize the wrapper. """
        pass

    def __repr__(self):
        """ User friendly string version
        :returns: str representation

        """
        return '%(__class__)s instance' % self.__dict__

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ Not really a transform - just print """
        for each in X:
            print(each)
        return X

    def get_params(self, deep=True):
        """Get parameters for this estimator.
        Parameters
        ----------
        deep: boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.
        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        return dict()
