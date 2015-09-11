import yaml
import inspect
import importlib
from wrappers import FunctionWrapper


class Conjurer(object):

    """ Conjures recipes to create Tictacs. Also known as a parser."""

    # Labels we use in yaml file.
    PIPE = 'pipeline'
    LABEL = 'label'
    STEPS = 'steps'
    TRANS = 'transformer_list'
    ESTIMATOR = 'estimator'
    ESTIMATOR_PKG = 'estimator_pkg'
    ESTIMATOR_PARAMS = 'estimator_params'

    # labels we need:
    # LABEL - name for it in order to be able to refer to it afterwards.
    # ESTIMATOR - package the estimator class is in in order to load it
    # ESTIMATOR_PKG - name of the estimator class - needed to instantiate it
    # estimator params is considered to be empty if none it isnt specified
    MANDATORY_ESTIMATOR_LABELS = [
                                  LABEL,
                                  ESTIMATOR,
                                  ESTIMATOR_PKG,
                                  ]

    INHERITED_MODEL_FUNCTIONS = [
                                 'fit',
                                 'fit_transform',
                                 'fit_predict',
                                 'transform',
                                 'inverse_transform',
                                 'predict',
                                 'predict_proba',
                                 'predict_log_proba',
                                 'decision_function',
                                 'score',
                                 ]

    def __init__(self, recipe):
        """ Load recipe and parse it

        :recipe: str - filename - path to recipe to parse

        """
        # keep all estimators with labels so we can access them
        # also we don't want to make two instances of the same thing
        self.estimators = dict()
        # keep parsed definitions that we want to create object with
        self.parsed = dict()

    def parse(self):
        """ parse using this conjurer. Estimator definitions are converted
            to estimator instances while other labeled entries are kept as is
        :returns: Dictionary of parsed content.

        """
        try:
            with open(self.filename, 'r') as conf:
                # entries at first level of dictionary when yaml is parsed
                root_entries = yaml.load(conf.read())
                # iterate over keys and parse all labels apart from pipeline
                # this caches them and makes them available to be accessed
                # in pipeline using their label instead of repeating the
                # whole definition
                for key, val in root_entries.items():
                    try:
                        if key != Conjurer.PIPE:
                            self.parse_pipe(root_entries[key])
                    except ValueError:
                        # if we could not parse it, it means that it wasn't
                        # an estimator instance, append it to stuff we pass
                        # to class - will probably be handy for quick settings
                        self.parsed[key] = val
                # now we parse pipe - labels used earlier can be used
                self.model = self.parse_pipe(root_entries[Conjurer.PIPE])
                self.parsed.update(self.model.__dict__())
                # expose model methods on Tictac class
                class_instance = self.model.__class__
                for key, value in class_instance.__dict__.items():
                    if key in Conjurer.INHERITED_MODEL_FUNCTIONS:
                        self.parsed[key] = val
                return self.parsed
        except IOError:
            raise AttributeError('%s - filename specified not found'
                                 % self.filename)

    def parse_pipe(self, yaml_dict, depth=0):
        """ Recursively parse the dictionary returned by yaml
            and replace the estimator nodes with actual estimator
            instances.
        :yaml_dict: the dictionary we got from loading the yaml recipe
        :depth: how deep we are in the parse of the dictionary
        :returns: an estimator class instance

        """
        # check dict passed is not None
        if yaml_dict is None:
            raise ValueError('Found None entry in dictionary at depth %s'
                             % depth)
        # check we got a dict or a string
        if type(yaml_dict) is not dict:
            # if it is just a str - we lookup the label to see if we have
            # an estimator assigned to it
            if type(yaml_dict) is str:
                if yaml_dict in self.estimators:
                    return self.estimators[yaml_dict]
                else:
                    raise ValueError('Label "%s" that was used at depth %s '
                                     'does not correspond to the declaration '
                                     'of an estimator' % (yaml_dict, depth))
            raise TypeError('Expected estimator entry at depth %s to be a '
                            'dictionary of key - value pairs or to be None, '
                            'instead it was of type %s' % type(yaml_dict))
        # check if any mandatory keys are missing - we can't parse without them
        missing = Conjurer.missing_keys(yaml_dict)
        if missing:
            key_values = dict(zip(missing, ('value',) * len(missing)))
            raise ValueError('Dictionary at depth %s is missing the following '
                             'mandatory key value pairs: %s'
                             % (depth, key_values))
        # if dict has no estimator params - suppose an empty list
        try:
            params = yaml_dict[Conjurer.ESTIMATOR_PARAMS]
            # make sure params is not None
            if params is None:
                params = dict()
        except KeyError:
            params = dict()
        # parse the estimator parameter arguments
        param_keyvals = Conjurer.parse_params(params)
        # below is None if estimator has no nested estimators
        if param_keyvals is not None:
            # key determines whether it is a pipeline or feature union
            key, estim_dicts = param_keyvals
            # for each entry in the parameters - parse them
            # the should be estimators or labels of estimators defined
            # in the outer scope
            for index, entry in enumerate(estim_dicts):
                # check if we have a label
                if type(entry) is str:
                    label = entry
                elif type(entry) is dict:
                    label = entry[Conjurer.LABEL]
                else:
                    raise TypeError('Expected estimator entry to be a '
                                    'dictionary of key - value pairs or '
                                    'a label defined in the outer scope, but '
                                    'label was of type %s' % type(entry))
                # get the parsed estimator instance
                estimator = self.parse_pipe(entry, depth+1)
                # replace the entries in the list with a tuple
                # label, estimator instance as expected by sklearn
                estim_dicts[index] = (label, estimator)
                # remember it - one instance for each label
                # TODO add redefinition errors when there exist
                # different estimators with same label
                self.estimators[label] = estimator
            params[key] = estim_dicts
        label = yaml_dict[Conjurer.LABEL]
        estimator = yaml_dict[Conjurer.ESTIMATOR]
        package = yaml_dict[Conjurer.ESTIMATOR_PKG]
        pkg = importlib.import_module(package)
        est = getattr(pkg, estimator)
        # if what we imported is a class - we suppose it is an estimator
        if inspect.isclass(est):
            estimator_instance = est(**params)
        # otherwise we suppose it is a method that processes the input vector
        # and we wrap it in a class that calls the method on transform
        else:
            estimator_instance = FunctionWrapper(est, **params)
        # if params is None we have passed no options
        # remember it - one instance for each label
        # TODO add redefinition errors when there exist
        # different estimators with same label
        self.estimators[label] = estimator_instance
        return estimator_instance

    def parse_params(param_dict):
        """ Parse parameters dictionary of estimator.
            We basically conclude what type of estimator it is by checking the
            parameters.
            Pipeline estimators have a steps entry.
            FeatureUnion estimators have a transform_list entry.
            All others are handled as simple estimators, that don't have
            further nested estimators inside them.
        :param_dict: A dictionary containing the parameters for this estimator.
        :returns: key, list of estimator dicts or None if this is
                  a simple estimator

        """
        if param_dict is not None:
            # check if this is a pipeline or feature union - they contain steps
            # and tranformer_list accordingly
            if type(param_dict) is not dict:
                raise TypeError('Expected %s to be a dictionary of key - '
                                'value pairs or to be None, instead it was of '
                                'type %s' % (Conjurer.ESTIMATOR_PARAMS,
                                             type(param_dict)))
            param_keys = param_dict.keys()
            # if its a pipeline
            if Conjurer.STEPS in param_keys:
                return Conjurer.STEPS, param_dict[Conjurer.STEPS]
            # if its a feature union
            elif Conjurer.TRANS in param_keys:
                return Conjurer.TRANS, param_dict[Conjurer.TRANS]
        # it is a simple estimator - or None was passed
        return None

    def missing_keys(yaml_dict):
        """ Check whether the top level of the dictionary created from the
            yaml file has the mandatory labels needed to create the estimators

        :yaml_dict: A level of the dictionary representing an estimator node
        :returns: list - missing mandatory keys of yaml_dict
                  empty list if none

        """
        return [key for key in Conjurer.MANDATORY_ESTIMATOR_LABELS
                if key not in yaml_dict.keys()]


class Tictac(object):

    """ Loader for the yaml file - perform checking and instantiate content """

    def __init__(self, **kwargs):
        """ Initialize a tictac - maintain same api as sklearn to avoid
            compatibility problems."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """ Lets make this python console friendly """
        return '\n'.join([
                          '%s: %s' %
                          ('\t%s' % key.__repr__()
                           if hasattr(key, '__repr__')
                           else key, val)
                          for key, val in self.__dict__.items()
                          ])

    def _cleanup(self):
        """ Clean up this instance - remove all attributes

        """
        self.__dict__ = dict()
        self.__init__()

    def load_recipe(self, filename):
        """ Load a recipe into this instance - replaces old content

        :filename: str - path to the yaml file containing the recipe

        """
        # forget current content
        self._cleanup()
        self.__init__(**Conjurer(filename).parse())


def conjure(recipe):
    """ Conjure a Tictac from a recipe

    :recipe: str - path to the recipe to use to build the Tictac
    :returns: Tictac instance conjured according to recipe

    """
    tictac = Tictac()
    tictac.load_recipe(recipe)
    return tictac
