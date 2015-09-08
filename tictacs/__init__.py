import os
import yaml
import importlib

# Labels we use in yaml file.
PIPE = 'pipeline'
LABEL = 'label'
STEPS = 'steps'
TRANS = 'transformer_list'
ESTIMATOR = 'estimator'
ESTIMATOR_PKG = 'estimator_pkg'
ESTIMATOR_PARAMS = 'estimator_params'

# labels we need:
# LABEL - a name for it in order to be able to refer to it afterwards.
# ESTIMATOR - the package the estimator class is in in order to load it
# ESTIMATOR_PKG - the name of the estimator class in order to instantiate it
# estimator params is considered to be empty if none it isnt specified
MANDATORY_ESTIMATOR_LABELS = [
                              LABEL,
                              ESTIMATOR,
                              ESTIMATOR_PKG,
                              ]


def missing_keys(yaml_dict):
    """ Check whether the top level of the dictionary created from the
        yaml file has the mandatory labels needed to create the estimators

    :yaml_dict: A level of the dictionary representing an estimator node
    :returns: list - missing mandatory keys of yaml_dict - empty list if none

    """
    return [key for key in MANDATORY_ESTIMATOR_LABELS
            if key not in yaml_dict.keys()]


def parse_params(param_dict):
    """ Parse parameters dictionary of estimator.
        We basically conclude what type of estimator it is by checking the
        parameters.
        Pipeline estimators have a steps entry.
        FeatureUnion estimators have a transform_list entry.
        All others are handled as simple estimators, that don't have
        further nested estimators inside them.
    :param_dict: A dictionary containing the parameters for this estimator.
    :returns: label, list of estimator dicts or None if this is
              a simple estimator

    """
    if param_dict is not None:
        # check if this is a pipeline or feature union - they contain steps
        # and tranformer_list accordingly
        if type(param_dict) is not dict:
            raise TypeError('Expected %s to be a dictionary of key - '
                            'value pairs or to be None, instead it was of '
                            'type %s' % (ESTIMATOR_PARAMS, type(param_dict)))
        param_keys = param_dict.keys()
        # if its a pipeline
        if STEPS in param_keys:
            return STEPS, param_dict[STEPS]
        # if its a feature union
        elif TRANS in param_keys:
            return TRANS, param_dict[TRANS]
    # it is a simple estimator - or None was passed
    return None


def parse_pipe(yaml_dict, depth=0):
    """ Recursively parse the dictionary returned by yaml
        and replace the estimator nodes with actual estimator
        instances
    :returns: a Pipeline object

    """
    # check dict passed is not None
    if yaml_dict is None:
        raise ValueError('Found None entry in dictionary at depth %s' % depth)
    # check we got a dict
    if type(yaml_dict) is not dict:
        raise TypeError('Expected estimator entry to be a dictionary of key - '
                        'value pairs or to be None, instead it was of type %s'
                        % type(yaml_dict))
    # check if any mandatory keys are missing - we can't parse without them
    missing = missing_keys(yaml_dict)
    if missing:
        key_values = dict(zip(missing, ('value',) * len(missing)))
        raise ValueError('Dictionary at depth %s is missing the following '
                         'mandatory key value pairs: %s'
                         % (depth, key_values))
    # if dict has no estimator params - suppose an empty list
    params = yaml_dict[ESTIMATOR_PARAMS]
    deeper = parse_params(params)
    if deeper is not None:
        label, deeper_estimators = deeper
        for index, estimator in enumerate(deeper_estimators):
            deeper_estimators[index] = (estimator[LABEL],
                                        parse_pipe(estimator, depth+1))
        params[label] = deeper_estimators
    estimator = yaml_dict[ESTIMATOR]
    package = yaml_dict[ESTIMATOR_PKG]
    pkg = importlib.import_module(package)
    est = getattr(pkg, estimator)
    # if params is None we have passed no options
    return est(**params) if params is not None else est()


class Tictac(object):

    """ Loader for the yaml file - perform checking and instantiate content """
    CONF_ENV_VAR = 'TICTAC_CONF'
    # Pipe API entries we expect.
    DATASET_LABEL = 'dataset'

    def __init__(self, filename=None):
        """ Initialize a tictac from file with its configuration """
        if filename:
            self.filename = filename
        else:
            try:
                # if filename was not specified - attempt reading
                # environment variable
                self.filename = os.environ[Tictac.CONF_ENV_VAR]
            except KeyError:
                raise ValueError("filename not specified and %s environment "
                                 "variable is not set - do not know what "
                                 "config to read!" % Tictac.CONF_ENV_VAR)
        try:
            with open(self.filename, 'r') as conf:
                entries = yaml.load(conf.read())
                # self.dataset = Dataset(**entries[Tictac.DATASET_LABEL])
                self.pipe = parse_pipe(entries[PIPE])
        except IOError:
            raise AttributeError('%s - filename specified not found'
                                 % self.filename)

    def __getattr__(self, name):
        """ Make parsed pipe attributes accessible as if they were ours

        :name: The attribute to get
        :returns: Access the attribute from pipe instance if it wasnt
                  found in our own

        """
        return getattr(self.pipe, name)

    def __repr__(self):
        """ Lets make this python console friendly """
        return '\n'.join([
                          '%s: %s' %
                          ('\t%s' % key.__repr__()
                           if hasattr(key, '__repr__')
                           else key, val)
                          for key, val in self.__dict__.items()
                          ])


# class Dataset(BaseEstimator, TransformerMixin):

#     """Docstring for Dataset. """

#     def __init__(self, **kwargs):
#         """ Initialize a dataset loader

#         :**kwargs: This is a pretty abstract class :P

#         """
#         BaseEstimator.__init__(self)
#         TransformerMixin.__init__(self)
#         for key, val in kwargs.items():
#             setattr(self, key, val)

#     def __repr__(self):
#         """ Lets make this python console friendly """
#         return '\n'.join([
#                           '%s: %s' %
#                           ('\t%s' % key.__repr__()
#                            if hasattr(key, '__repr__')
#                            else key, val)
#                           for key, val in self.__dict__.items()
#                           ])
