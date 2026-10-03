
#from arc_templates.god_mode import *
from arc_templates.god_mode_actr import *

# The template supplies working memory and the environment, but no emotional memory.
print("Memories supplied by the template:")
print(memories)


working_memory.focusbuffer.state = 'bread1'

environment.bread1 = {'location': 'counter'}
environment.cheese = {'location': 'counter'}
environment.ham = {'location': 'counter'}
environment.bread2 = {'location': 'counter'}
ProceduralProductions = []

# def bread1(memories):
#     memories['working_memory']['focusbuffer']['state'] = 'cheese'
#     print(f"bread1. Updated working_memory: {memories['working_memory']}")
#     return 4 #set action completion for X cycles later
# def bread1_method(memories):
#     memories['environment']['bread1']['location'] = 'plate'
#     print(f"{memories['environment']}")
# ProceduralProductions.append({
#     'matches': {'working_memory': {'focusbuffer': {'state': 'bread1'}},
#                 'environment': {'bread1': {'location': 'counter'}}},
#     'negations': {},
#     'utility': 10,
#     'action': bread1,
#     'delayed_action': bread1_method,
#     'report': "bread1",
# })

def bread1(memories):
    memories.working_memory.focusbuffer.state = 'cheese'
    print(f"bread1. Updated working_memory: {memories.working_memory}")
    return 4  # Complete the delayed action 4 cycles later
def bread1_method(memories):
    memories.environment.bread1.location = 'plate'
    print(f"environment update: {memories.environment}")
ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'bread1'}},
        'environment': {'bread1': {'location': 'counter'}},
    },
    'negations': {},
    'utility': 10,
    'action': bread1,
    'delayed_action': bread1_method,
    'report': 'bread1',
})



def cheese(memories):
    memories.working_memory.focusbuffer.state = 'ham'
    print(f"cheese executed. Updated working_memory: {memories.working_memory}")
    print(f"environment update: {memories.environment}")
    return 4 #set action completion for X cycles later
def cheese_method(memories):
    memories.environment.cheese.location = 'plate'
    print(f"environment update: {memories.environment}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'cheese'}},
                'environment': {'bread1': {'location': 'plate'}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'delayed_action': cheese_method,
    'report': "cheese",
})

def ham(memories):
    memories.working_memory.focusbuffer.state = 'bread2'
    print(f"ham executed. Updated working_memory: {memories.working_memory}")
    print(f"environment update: {memories.environment}")
    print(f"ham executed. Updated working_memory: {memories.working_memory}")
    return 4 #set action completion for X cycles later
def ham_method(memories):
    memories.environment.ham.location = 'plate'
    print(f"environment update: {memories.environment}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'ham'}},
                'environment': {'cheese': {'location': 'plate'}, 'ham': {'location': 'counter'}}
                },
    'negations': {},
    'utility': 10,
    'action': ham,
    'delayed_action': ham_method,
    'report': "ham",
})

def bread2(memories):
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print(f"bread top executed. Updated working_memory: {memories['working_memory']}")
    print(f"environment update: {memories['environment']}")
    return 4 #set action completion for X cycles later
def bread2_method(memories):
    memories['environment']['bread2']['location'] = 'plate'
    print(f"environment update: {memories['environment']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'bread2'}},
                'environment': {'ham': {'location': 'plate'}, 'bread2': {'location': 'counter'}}
                },
    'negations': {},
    'utility': 10,
    'action': bread2,
    'delayed_action': bread2_method,
    'report': "bread2",
})


# Production system delays in ticks
ProductionSystem1_Countdown = 1

# Stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown]}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=20, millisecpercycle=50)
