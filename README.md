# tictacs
Machine learning pipeline setup on tictacs.

## Status
[![Build Status](https://api.travis-ci.org/andreasgrv/tictacs.svg?branch=master)](https://travis-ci.org/andreasgrv/tictacs)

**This project has been abandoned for [mlconf](https://github.com/andreasgrv/mlconf), which is more general and doesn't
have the idea of a pipeline baked in.** This may be good or bad depending on your needs.

Reasons:

* Make the instantiation of classes more general and not dependent on scikit
learn

* Do not enforce pipeline constraints. While thinking of machine learning
processes as pipelines really helps, it can restrict the usage of the
library.

#### Versions

* v0.0.1  First version available - simple yaml parsing and conversion to a sklearn pipeline. Wraps pipeline in tictac object.
* v0.0.2  Minor changes in what wrapping function does, it now returns copies instead of modifying inplace.
* v0.0.3  Supports adding sentries to the pipeline for inspection purposes - eg: printing output, printing size of output and type of output at a certain point in the pipeline. Uses logging.

## Description
This module is an attempt to move the creation of machine learning pipelines away from the code and into the configuration files where they belong. When there, they can be processed much more easily and can even be automatically generated (TODO maybe) once this intermediate step exists.

Each tictac is meant to be a modular self contained approach to a machine learning task. We can manufacture a tictac using a recipe (a YAML file that specifies what components to use), and then compare it to other tictacs we made with different recipes. The following should be able to be configurable from the config files soon:
- Dataset loading
- Preprocessing
- Feature Extraction
- Parameter Selection
- Model Creation
- Model Evaluation

At the moment, the approach to creating a pipeline with all the above is based on the abstaction mechanism used in sklearn - that of estimators. Later on, it might be reasonable to decouple it from sklearn, so that it can be an abstraction that can use other machine learning libraries as well.

The pipeline creation is based on the the abstraction mechanism used in sklearn - that of estimators. So each action we perform on the data is modeled with a class. This class must implement the fit and transform methods in a way that is meaningful for the action.

## Installation

- git clone https://github.com/andreasgrv/tictacs
- cd tictacs
- pip install -r requirements.txt
- pip install --user -e .

If you want to run the examples you will need to install scikit learn (numpy and scipy are sklearn dependencies):

- pip install numpy scipy scikit-learn

## Examples

After following above installation from withing the root folder do:

>
	python examples/example.py -r recipes/example.yaml


To see an example with sentinel usage check out

> 
	python examples/example.py -r recipes/sentinel.yaml

## Naming
Influenced by a oneliner joke made by stand up comedian Milton Jones - in machine learning tasks we need tactics when tackling problems! (as well as humour to wiggle out of a tight spot when our system doesn't work).

## Licensing
3 clause BSD  - see LICENSE.txt
