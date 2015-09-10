# tictacs
Machine learning pipeline setup on steroids (on tictacs actually).

### Status
This is a work in progress

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

## Examples

After following above installation from withing the root folder do:
> python examples/example.py -r recipes/example.yaml

## Naming
Influenced by a oneliner joke made by stand up comedian Milton Jones - in machine learning tasks we need tactics when tackling problems! (as well as humour to wiggle out of a tight spot when our system doesn't work).

## 3 clause BSD License

tictacs - simplified machine learning pipeline construction

Copyright © 2015 Andreas Grivas
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of the organization nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY Andreas Grivas ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Andreas Grivas BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
