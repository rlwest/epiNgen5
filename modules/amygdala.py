
"""Teaching examples of amygdala productions.

Each example maps a visual condition to an emotional state. Model builders
can keep, change, or remove these productions for their own projects.
"""

# -------------------------
# Define Amygdala Productions (Vision)
# -------------------------
AmygdalaProductions = []

# Spider example.
def fear_spider(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = '01001010' # neural state for fear
    print('amygdala is detecting a fearful situation !!!!!!!!!!!!!!!!!!!!!!!!')
AmygdalaProductions.append({
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'yes'}}}},
    'negations': {},
    'utility': 10,
    'action': fear_spider,
    'report': "fear_spider",
})

def spider_calm_down(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = '00000000' # neural state for fear
    print('amygdala is detecting relatively calm situation &&&&&&&&&&&&&&&&&&&&&&&&&&&')
AmygdalaProductions.append({
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'no'}}}},
    'negations': {},
    'utility': 10,
    'action': spider_calm_down,
    'report': "spider_calm_down",
})


# Faulty warning-light example.
def amygdala_warning(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = '01001010'
    print('AMYGDALA: visually detected warning; fear state active')


AmygdalaProductions.append({
    'matches': {
        'working_memory': {
            'visual_representation_buffer': {
                'warning_light': {'state': 'on'}
            }
        }
    },
    'negations': {},
    'utility': 10,
    'action': amygdala_warning,
    'report': 'amygdala detects warning light'
})


def amygdala_calm(memories):
    memories['working_memory']['emotional_buffer']['emotion_state'] = '00000000'
    print('AMYGDALA: warning light is off; calm emotional state restored')


AmygdalaProductions.append({
    'matches': {
        'working_memory': {
            'visual_representation_buffer': {
                'warning_light': {'state': 'off'}
            }
        }
    },
    'negations': {},
    'utility': 10,
    'action': amygdala_calm,
    'report': 'amygdala detects warning light off'
})


# Optional “contract” / assumptions
REQUIRES = {
    "working_memory_buffers": ["visual_representation_buffer", "emotional_buffer"],
    "memories_keys": ["working_memory"],
}
