#required to start - {'environment': {'spider': {'visible': 'no'}}}

import random
from functools import partial

def do_nothing(memories):
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    return 0

def spider_visibility(memories, *, visibility_probability=0.5):
    #Updates whether the spider is visible or not.
    r = random.random()
    if r < visibility_probability:
        memories['environment']['spider']['visible'] = 'yes'
        print('spider is visible!!!!!!!!!')
    else:
        memories['environment']['spider']['visible'] = 'no'
        print('spider is not visible ***************')

def make_spider_productions(*, visibility_probability=0.5):
    """Set the probability of seeing the spider each time the actor fires."""
    if not 0 <= visibility_probability <= 1:
        raise ValueError('visibility_probability must be between 0 and 1.')
    return [{
        'matches': {'environment': {'spider': {'visible': '*'}}},
        'negations': {},
        'utility': 10,
        'action': partial(spider_visibility, visibility_probability=visibility_probability),
        'report': "spider",
    }]


spider_productions = make_spider_productions()


