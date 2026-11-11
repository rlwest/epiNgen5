# The recipe is stored in declarative memory as four chunks, one per sandwich step.
# Each chunk names a task and gives the cue for the next one. Two production rules
# repeat: one retrieves the cued chunk, and the other prints that the task is done
# and advances the cue. The ingredient locations stay fixed throughout the run.

from arc_templates.GOMS import *
from cognitive_functions.retrieve import retrieve_memory_chunk


# The sandwich goal cues the first task. Each chunk supplies the cue for the next.
working_memory.focusbuffer = {'state': 'retrieve', 'cue': 'make_ham_cheese_sandwich'}

memories.declarative_memory = {
    'bread_bottom': {
        'cue': 'make_ham_cheese_sandwich', 'unit_task': 'Move bread bottom',
        'next_cue': 'bread_bottom_done', 'utility': 10,
    },
    'cheese': {
        'cue': 'bread_bottom_done', 'unit_task': 'Move cheese',
        'next_cue': 'cheese_done', 'utility': 10,
    },
    'ham': {
        'cue': 'cheese_done', 'unit_task': 'Move ham',
        'next_cue': 'ham_done', 'utility': 10,
    },
    'bread_top': {
        'cue': 'ham_done', 'unit_task': 'Move bread top',
        'next_cue': 'end', 'utility': 10,
    },
}

ProceduralProductions = []


def get_next_unit_task(memories):
    wm = memories.working_memory
    chunk = retrieve_memory_chunk(memories.declarative_memory, {'cue': wm.focusbuffer.cue})
    if chunk == {'name': 'no_match'}:
        raise ValueError(f"No unit task matches the cue '{wm.focusbuffer.cue}'")
    wm.unit_task = chunk
    wm.focusbuffer.state = 'do'
    print(f"Retrieved: {wm.unit_task.unit_task}")

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'retrieve'}}},
    'negations': {}, 'utility': 10,
    'action': get_next_unit_task, 'report': 'get next unit task',
})


def do_unit_task(memories):
    wm = memories.working_memory
    print(f"{wm.unit_task.unit_task} done.")
    wm.focusbuffer.cue = wm.unit_task.next_cue
    if wm.focusbuffer.cue == 'end':
        wm.focusbuffer.state = 'finished'
    else:
        wm.focusbuffer.state = 'retrieve'

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'do'}}},
    'negations': {}, 'utility': 10,
    'action': do_unit_task, 'report': 'do unit task',
})

# Each of the four tasks takes one cycle to retrieve and one to report completion.
AllProductionSystems = {'ProceduralSystem': [ProceduralProductions, 1]}
DelayResetValues = {'ProceduralSystem': 1}

ps = ProductionCycle()
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=8, millisecpercycle=10)
