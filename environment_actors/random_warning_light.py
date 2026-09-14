"""Random warning signal for the space-station teaching model.

The signal stands for an unspecified new problem at the station. Its timing is
random so that a warning can also arrive during an ordered reset.
"""

import random


random_warning_light_productions = []


def maybe_turn_on_warning_light(memories):
    actor_state = memories['warning_light_memory']['state']
    actor_state['checks'] += 1
    if random.random() < actor_state['probability']:
        memories['environment']['warning_light']['state'] = 'on'
        print('ENVIRONMENT ACTOR: a new problem turned the warning light on')
    else:
        print('ENVIRONMENT ACTOR: warning light stayed off')


random_warning_light_productions.append({
    'matches': {
        'environment': {'warning_light': {'state': 'off'}},
        'warning_light_memory': {
            'state': {'probability': '*', 'checks': '*'},
        },
    },
    'negations': {},
    'utility': 10,
    'action': maybe_turn_on_warning_light,
    'report': 'random warning-light check',
})


REQUIRES = {
    'memories_keys': ['environment', 'warning_light_memory'],
    'environment_objects': ['warning_light'],
}
