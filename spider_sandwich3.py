"""Make a sandwich and recall a side order while a spider changes visibility."""

from arc_templates.ActR_Emotion import *
# Set declarative memory parameters. Zero turns off a memory effect.
ACTRISH_SUBSYMBOLIC_PARAMETERS.update(noise_scalar=0.0, decay_amount=0.0, spreading_boost=0.0)

from environment_actors.spiderProductions import make_spider_productions
# Probability per spider check (0 = always hidden, 1 = always visible).
spider_productions = make_spider_productions(visibility_probability=0.5)

# -------------------------
# Initialize Memories
# -------------------------
working_memory.focusbuffer = {'state': 'bread1'}
working_memory.motor_buffer = {'state': 'no_action'}
working_memory.visual_representation_buffer = {}
working_memory.emotional_buffer = {'emotion_state': CALM}
working_memory.visual_command_buffer = {'state': 'scan'}
working_memory.DM_command_buffer = {'state': 'normal'}
working_memory.DM_output_buffer = {}
working_memory.DM_retieval_buffer = {
    'matches': {'side_order': 'yes', 'condition': 'good'},
    'negations': {'condition': 'bad'},
}

memories.declarative_memory = {
    'fries': {'name': 'fries', 'condition': 'good', 'side_order': 'yes', 'utility': 4},
    'house_salad': {'name': 'house_salad', 'condition': 'good', 'side_order': 'no', 'utility': 1},
    'poutine': {'name': 'poutine', 'condition': 'good', 'side_order': 'yes', 'utility': 5},
    'ceasar_salad': {'name': 'ceasar_salad', 'condition': 'bad', 'side_order': 'no', 'utility': 10},
}

environment.bread1 = {'location': 'counter'}
environment.cheese = {'location': 'counter'}
environment.ham = {'location': 'counter'}
environment.bread2 = {'location': 'counter'}
environment.spider = {'visible': 'no'}

# -------------------------
# Amygdala Productions
# -------------------------
AmygdalaProductions = []

# Adapted from fear_item_1 in modules/amygdala2.py. For another feared object,
# copy this rule and edit its visual match and report.
AmygdalaProductions.append({
    'matches': {
        'working_memory': {
            'visual_representation_buffer': {'spider': {'visible': 'yes'}},
        },
    },
    'negations': {},
    'utility': 10,
    'action': feel_fear,
    'report': 'fear of a visible spider',
})
AmygdalaProductions.append(CalmProduction)

# -------------------------
# Define Procedural Productions (Sandwich Steps)
# -------------------------
ProceduralProductions = []

def bread1(memories):
    # Set up motor action to move bread1 from 'counter' to 'plate'
    motorbuffer = memories.working_memory.motor_buffer
    motorbuffer.state = 'do_action'
    motorbuffer.env_object = 'bread1'
    motorbuffer.slot = 'location'
    motorbuffer.newslotvalue = 'plate'
    motorbuffer.delay = 4
    # Update the focus for the next production.
    memories.working_memory.focusbuffer.state = 'cheese'
    print("procedural module !!!!!!!!!!!!!!!! bread1 production executed: focus updated to 'cheese'; motor action scheduled for bread1.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'bread1'},
             'visual_representation_buffer': {'bread1': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'report': "bread1",
})
# -------------------------

def cheese(memories):
    motorbuffer = memories.working_memory.motor_buffer
    motorbuffer.state = 'do_action'
    motorbuffer.env_object = 'cheese'
    motorbuffer.slot = 'location'
    motorbuffer.newslotvalue = 'plate'
    motorbuffer.delay = 4
    memories.working_memory.focusbuffer.state = 'ham'
    print("procedural module !!!!!!!!!!!!!!!! cheese production executed: focus updated to 'ham'; motor action scheduled for cheese.")

ProceduralProductions.append({
    'matches': {
        'working_memory':
            {'focusbuffer': {'state': 'cheese'},
            'visual_representation_buffer': {'bread1': {'location': 'plate'},
                                             'cheese': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})
# -------------------------

def ham(memories):
    motorbuffer = memories.working_memory.motor_buffer
    motorbuffer.state = 'do_action'
    motorbuffer.env_object = 'ham'
    motorbuffer.slot = 'location'
    motorbuffer.newslotvalue = 'plate'
    motorbuffer.delay = 4
    memories.working_memory.focusbuffer.state = 'bread2'
    print("procedural module !!!!!!!!!!!!!!!! ham production executed: focus updated to 'bread2'; motor action scheduled for ham.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'ham'},
        'visual_representation_buffer': {
            'cheese': {'location': 'plate'},
            'ham': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})
# -------------------------

def bread2(memories):
    motorbuffer = memories.working_memory.motor_buffer
    motorbuffer.state = 'do_action'
    motorbuffer.env_object = 'bread2'
    motorbuffer.slot = 'location'
    motorbuffer.newslotvalue = 'plate'
    motorbuffer.delay = 4
    memories.working_memory.focusbuffer.state = 'done'
    print("procedural module !!!!!!!!!!!!!!!! bread2 production executed: focus updated to 'done'; motor action scheduled for bread2.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'bread2'},
        'visual_representation_buffer': {
            'ham': {'location': 'plate'},
            'bread2': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})


def announce_sandwich(memories):
    print("procedural module !!!!!!!!!!!!!!!! Ham and cheese sandwich is almost ready, just adding the bread")
    print("while I am adding the bread I will recall if there was a side order")
    memories.working_memory.focusbuffer.state = 'sandwich_done'
    memories.working_memory.DM_retieval_buffer.matches = {'side_order': 'no', 'condition': 'good'}
    memories.working_memory.DM_retieval_buffer.negations = {'condition': 'bad'}
    memories.working_memory.DM_command_buffer.state = 'retrieve_partial'

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'done'}}},
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
})

def announce_side(memories):
    print("procedural module !!!!!!!!!!!!!!!! I recall the side order was")
    print(memories.working_memory.DM_output_buffer)
    memories.working_memory.focusbuffer.state = 'end'
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'memory_retrieved'}}},
    'negations': {},
    'utility': 10,
    'action': announce_side,
    'report': "announce_side",
})


# -------------------------
# Production Systems Setup
# -------------------------
AllProductionSystems, DelayResetValues = setup_production_systems(
    groups={
        'ProceduralSystem': ProceduralProductions,
        'MotorSystem': MotorProductions,
        'VisionSystem': VisualProductions,
        'DeclarativeMemorySystem': DM_Symbolic_Productions,
        'DeclarativeMemorySubsymbolicSystem': DM_Subsymbolic_Productions,
        'SpiderSystem': spider_productions,
        'AmygdalaSystem': AmygdalaProductions,
    },
    # Each number is in 50 ms cycles. A countdown of 1 allows firing every cycle.
    countdowns={
        'ProceduralSystem': 1,
        'MotorSystem': 1,
        'VisionSystem': 1,
        'DeclarativeMemorySystem': 1,
        'DeclarativeMemorySubsymbolicSystem': 1,
        'SpiderSystem': 1,
        'AmygdalaSystem': 1,
    },
)

ps = ProductionCycle()
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=25, millisecpercycle=50)
