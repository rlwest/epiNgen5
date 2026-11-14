"""Visual fear associations and a shared calm-down production.

Copy a sample fear rule into your model for each feared object. Replace the
placeholder name and its full slot dictionary with the visual condition
that should trigger fear. Add CalmProduction to your model's list once.

Initialize emotional_buffer.emotion_state to CALM and register
AmygdalaProductions as one system so fear and calm compete by utility.
"""

FEAR = '01001010'
CALM = '00000000'


def feel_fear(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = FEAR
    print('AMYGDALA: fear active')


def calm_down(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = CALM
    print('AMYGDALA: calm restored')


AmygdalaProductions = []

AmygdalaProductions.append({
    'matches': {
        'working_memory': {
            'visual_representation_buffer': {'fear_item_1': {'visible': 'yes'}},
        },
    },
    'negations': {},
    'utility': 10,
    'action': feel_fear,
    'report': 'fear item 1',
})

AmygdalaProductions.append({
    'matches': {
        'working_memory': {
            'visual_representation_buffer': {'fear_item_2': {'visible': 'yes'}},
        },
    },
    'negations': {},
    'utility': 10,
    'action': feel_fear,
    'report': 'fear item 2',
})

CalmProduction = {
    'matches': {'working_memory': {'emotional_buffer': {'emotion_state': FEAR}}},
    'negations': {},
    'utility': 1,
    'action': calm_down,
    'report': 'calm down',
}
AmygdalaProductions.append(CalmProduction)

REQUIRES = {
    'working_memory_buffers': ['visual_representation_buffer', 'emotional_buffer'],
    'memories_keys': ['working_memory'],
}
