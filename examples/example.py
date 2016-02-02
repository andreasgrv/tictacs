from argparse import ArgumentParser
from tictacs import from_recipe
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    parser = ArgumentParser(description='A tester of recipes for tic tacs')
    parser.add_argument('--recipe', '-r', required=True, dest='recipe',
                        help='Path to the file where the recipe to create '
                             'delicious tictacs resides. All recipes must be '
                             'written in yaml format.',
                        default='recipes/example.py')
    args = parser.parse_args()
    recipe = args.recipe
    print('Using recipe from file: %s' % recipe)
    texts = ['@sly_pedantic_octopus @glorified_ml I walked on ice yesterday,'
             ' but no one laughed when it broke #lol',
             '@blue_world I hate java #java #programming #hell',
             '@BarnieTheDinosaur raaawwwwr.',
             'omg that just happened. #omg #rofl #yolo'
             ]

    print('Creating model...')
    tictac = from_recipe(recipe)
    print('Fitting model...')
    tictac.fit(texts, [0, 1, 1, 1])
    print('Predicting with model...')
    res = tictac.predict(['#dog wtf omg java', '@blue yes broke #lol'])
    print('Predicted %s' % res)
