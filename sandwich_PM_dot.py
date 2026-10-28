# Make a ham and cheese sandwich using perception and motor commands.
# ActR-ish supplies ProductionCycle, VisualProductions, and MotorProductions.
# The visual module scans the environment into working memory.
# The motor module carries out commands from the motor buffer after a delay.
# Declarative memory productions are imported but not scheduled in this model.

from arc_templates.PM import *

# -------------------------
# Initialize Memories
# -------------------------

# Populate the template's views so they stay connected to memories.
# Whole-chunk assignments copy; slot assignments edit the current chunk.
working_memory.focusbuffer = {'state': 'bread1'}
working_memory.motor_buffer = {'state': 'no_action'}
working_memory.visual_representation_buffer = {
    'bread1': {'location': 'counter'},
    'cheese': {'location': 'counter'},
    'ham': {'location': 'counter'},
    'bread2': {'location': 'counter'},
}
working_memory.visual_command_buffer = {'state': 'scan'}

environment.bread1 = {'location': 'counter'}
environment.cheese = {'location': 'counter'}
environment.ham = {'location': 'counter'}
environment.bread2 = {'location': 'counter'}

# -------------------------
# Define Procedural Productions (Sandwich Steps)
# Conditions remain dictionaries and match the visual representation buffer.
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
    print("bread1 production executed: focus updated to 'cheese'; motor action scheduled for bread1.")

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
    print("cheese production executed: focus updated to 'ham'; motor action scheduled for cheese.")

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
    print("ham production executed: focus updated to 'bread2'; motor action scheduled for ham.")

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
    print("bread2 production executed: focus updated to 'done'; motor action scheduled for bread2.")

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
# -------------------------

def announce_sandwich(memories):
    print("Ham and cheese sandwich is ready!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    memories.working_memory.focusbuffer.state = 'finished'


ProceduralProductions.append({
    'matches': {
        # Wait until vision confirms the top bread has reached the plate.
        'working_memory': {
            'focusbuffer': {'state': 'done'},
            'visual_representation_buffer': {'bread2': {'location': 'plate'}},
        }
    },
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
})
# -------------------------



# -------------------------
# Production Systems Setup
# -------------------------
ProductionSystem1_Countdown = 1  # For procedural productions.
ProductionSystem2_Countdown = 1  # For motor productions.
ProductionSystem3_Countdown = 1  # For visual productions (vision system).

DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown,
    'ProductionSystem3': ProductionSystem3_Countdown,
}

AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown],
    'ProductionSystem3': [VisualProductions, ProductionSystem3_Countdown],
}


# -------------------------
# Initialize and Run the Production Cycle
# -------------------------
ps = ProductionCycle()
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=30, millisecpercycle=50)
