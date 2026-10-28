"""Make a sandwich, recall its side order, and switch on the coffee machine.

GOMS supplies the visual, motor, and symbolic DM modules.
Production conditions remain dictionaries. Retrieval is requested through
working-memory buffers and handled by the symbolic DM production system.
After the final motor command, the coffee machine finishes independently.
"""

from arc_templates.GOMS import *
from environment_actors.coffee_machine import CoffeeMachineProductions

# -------------------------
# Initialize Memories
# -------------------------
# Populate the template's views so they stay connected to memories.
# Conditions remain dictionaries; actions can access the same data with dots.
working_memory.focusbuffer = {'state': 'bread1'} # start condition
working_memory.motor_buffer = {'state': 'no_action'}  # No motor action scheduled.
working_memory.visual_representation_buffer = {}
working_memory.DM_output_buffer = {}
working_memory.visual_command_buffer = {'state': 'scan'}  # Continuously scan.
working_memory.DM_command_buffer = {'state': 'normal'}  # No retrieval requested yet.
working_memory.DM_retieval_buffer = {}

memories.declarative_memory = {'fries': {'name': 'fries',
                                'condition': 'good',
                                'side_order': 'yes',
                                'utility':4},
                      'house_salad': {'name': 'house_salad',
                                      'condition': 'good',
                                      'side_order': 'yes',
                                      'utility':1},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'no',
                                  'utility':5},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'yes',
                                       'utility':10},
                      }
declarative_memory = memories.declarative_memory


environment.bread1 = {'location': 'counter'}
environment.cheese = {'location': 'counter'}
environment.ham = {'location': 'counter'}
environment.bread2 = {'location': 'counter'}
environment.coffee_cup = {'status': 'empty'}
environment.coffee_switch = {'position': 'up'}
# Motor productions update this environment through the same memories view.

# The coffee machine keeps its own state, separate from the agent's memory.
memories.coffee_memory = {'state': {'status': 'off'}}

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
    # Set retrieval conditions
    memories.working_memory.DM_retieval_buffer.matches = {'side_order': 'yes'}
    memories.working_memory.DM_retieval_buffer.negations = {'condition': 'bad'}
    # tell DM to work on the retrival
    #memories.working_memory.DM_command_buffer.state = 'retrieve'
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
    memories.working_memory.focusbuffer.state = 'make_coffee'
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'memory_retrieved'}}},
    'negations': {},
    'utility': 10,
    'action': announce_side,
    'report': "announce_side",
})


def start_coffee(memories):
    motorbuffer = memories.working_memory.motor_buffer
    motorbuffer.state = 'do_action'
    motorbuffer.env_object = 'coffee_switch'
    motorbuffer.slot = 'position'
    motorbuffer.newslotvalue = 'down'
    motorbuffer.delay = 3
    memories.working_memory.focusbuffer.state = 'end'
    print('procedural module: bread is on the sandwich, sandwich is completed')
    print('procedural module: pressing the coffee switch; no more procedural steps.')


ProceduralProductions.append({
    'matches': {'working_memory': {
        'focusbuffer': {'state': 'make_coffee'},
        # The hand must be free, and vision must confirm the top bread is on the plate.
        'motor_buffer': {'state': 'no_action'},
        'visual_representation_buffer': {
            'bread2': {'location': 'plate'},
            'coffee_switch': {'position': 'up'},
        },
    }},
    'negations': {},
    'utility': 10,
    'action': start_coffee,
    'report': 'start_coffee',
})


# -------------------------
# Production Systems Setup
# -------------------------
ProductionSystem1_Countdown = 1  # For procedural productions.
ProductionSystem2_Countdown = 1  # For motor productions.
ProductionSystem3_Countdown = 1  # For visual productions (vision system).
ProductionSystem4_Countdown = 1  # For DM symbolic productions.
ProductionSystem5_Countdown = 1  # For the independent coffee machine.


DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown,
    'ProductionSystem3': ProductionSystem3_Countdown,
    'ProductionSystem4': ProductionSystem4_Countdown,
    'ProductionSystem5': ProductionSystem5_Countdown,
}

AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown],
    'ProductionSystem3': [VisualProductions, ProductionSystem3_Countdown],
    'ProductionSystem4': [DM_Symbolic_Productions, ProductionSystem4_Countdown],
    'ProductionSystem5': [CoffeeMachineProductions, ProductionSystem5_Countdown],
}


# -------------------------
# Initialize and Run the Production Cycle
# -------------------------
ps = ProductionCycle()
# Keep the engine running after the agent ends so the machine can finish pouring.
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=35, millisecpercycle=50)
