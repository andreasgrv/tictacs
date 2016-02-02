""" wrappers for functions to components """
import logging


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


class Sentinel(object):

    """ Wrapper for debugging and checking the flow of the pipeline.
        writes to a logger"""

    def __init__(self, x=None, y=None, shape=True, py_type=True):
        """ Create Sentinel that helps with printing what happens
        at a certain point in the pipeline.

        :x: print row x, by default prints all rows
        :y: print column y, by default prints all columns
        :shape: print the shape of the object at the sentinel (tuple format)
        :py_type: print type of python object that passed the sentinel
        """
        self.py_type = py_type
        self.shape = shape
        self.x = x
        self.y = y
        self.logger = logging.getLogger('tictacs.wrappers')

    def __repr__(self):
        """ User friendly string version
        :returns: str representation

        """
        return '%(__class__)s instance' % self.__dict__

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """ Not really a transform - just print """
        self.logger.info('\n-------- Tictacs printer -------\n')
        if self.py_type:
            self.logger.info('data type: %s' % type(X))
        if self.shape:
            if hasattr(X, 'shape'):
                self.logger.info('shape: (%s, %s)' % X.shape)
            elif hasattr(X, '__len__'):
                try:
                    first_elem = X[0]
                    if hasattr(first_elem, '__iter__'):
                        self.logger.info('shape: (%s, %s)' % (len(X),
                                                              len(first_elem)))
                except KeyError:
                    self.logger.info('shape: (%s, 1) - 1d list' % len(X))
            else:
                self.logger.error(
                    "unknown shape! couldn't find shape or __len__ "
                    "attributes on the object at current point in "
                    "pipeline")
        # print f
        try:
            # numpy support tuple indexing
            self.logger.info('data: \n%s' % X[self.x, self.y])
        except Exception:
            # try to index each dimension separately
            xcord = slice(self.x) if self.x is None else self.x
            ycord = slice(self.y) if self.y is None else self.y
            try:
                self.logger.info('data: \n%s' % X[xcord][ycord])
            except KeyError:
                # for some reason we have a one-dimensional object
                self.logger.info('data: \n%s' % X[xcord])
        print('\n--------------------------------\n')
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
        # no point in returning something else here
        return dict()
