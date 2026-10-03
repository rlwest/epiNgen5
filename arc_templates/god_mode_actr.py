"""God Mode with dot access and independent copies for every whole chunk.

Start a student model with:
    from arc_templates.god_mode_actr import *

Set one slot, leaving the other slots alone:
    working_memory.focusbuffer.state = 'bread1'

Replace a buffer's entire chunk with an independent deep copy:
    working_memory.focusbuffer = {'state': 'bread1', 'goal': 'sandwich'}

The same rule applies to environmental objects and new memory sources:
    environment.bread1 = {'location': 'counter'}
    environment.bread2 = environment.bread1  # independent contents
    memories.emotional_memory = {'mood': {'state': 'calm'}}

No registration is needed for new buffers, objects, or chunks. For example:
    working_memory.retrievalbuffer = {'state': 'empty'}
The older register_buffer(name, chunk) shorthand also remains available.

The filename is retained for existing student models. This is not full ACT-R:
there is no automatic merging, activation change, or buffer-only restriction.
Dot access and copying are reusable computational mechanisms, implemented and
explained in computational_architecture/memory_view.py. This architecture template chooses
which memories exist and selects copying for all chunks at depth 2.

Dictionary conditions, wildcard matching, bracket access, and update() remain
available. Populate the supplied views in place; rebinding a local variable
will not reconnect it to memories. Imports share state within one Python
process, so run each model in a fresh process.
"""

from computational_architecture.production_cycle import ProductionCycle
from computational_architecture.memory_view import MemoryView as _MemoryView
from computational_architecture.memory_view import register_buffer as _register_buffer

# This list controls the names supplied by the student's single star import.
# The reusable implementation stays out of the student's model namespace.
__all__ = ['ProductionCycle', 'working_memory', 'environment', 'memories',
           'register_buffer']


# ASSEMBLING THIS ARCHITECTURE
# MemoryView supplies the access mechanism; this template supplies its policy.
# God Mode exposes both working memory and the environment for direct access.
# Depth 1 is a memory source; depth 2 is a buffer, object, or stored chunk.
# Selecting this depth gives ALL such locations the same copying rule, even
# in memory sources added later by students. Slot edits remain ordinary edits.
memories = _MemoryView({'working_memory': {}, 'environment': {}}, copy_chunk_depth=2)
working_memory = memories.working_memory
environment = memories.environment

# These names view the same dictionaries held inside memories, not copies.
# Create an empty starting buffer; the policy already applies automatically.
# Editing one slot changes the existing chunk rather than replacing it.
working_memory.focusbuffer = {}


def register_buffer(name, chunk=None):
    """Add a working-memory buffer using this template's student shorthand.

    name is the buffer key; chunk is its optional starting dictionary or view.
    With no chunk, preserve existing contents or start empty. Return the buffer
    view. The reusable function performs copying and validates the arguments.
    Registration is optional here because depth 2 already has a copying rule.

    This convenience function chooses working_memory for students. Another
    architecture template can call the reusable function with its own containing location,
    including a nested view; the mechanism has no working-memory assumption.
    """
    return _register_buffer(working_memory, name, chunk)


# TEACHING FEEDBACK
# Importing assembles the configuration and explains it; it does not run a
# model. Python normally imports a module once per process, so another import
# neither resets the memories nor repeats this introduction.
print("""God Mode with dot access and whole-chunk copying loaded.
You have ProductionCycle, working_memory, environment, and memories.
  working_memory.focusbuffer starts empty.
  environment is empty and remains directly accessible in God Mode.
  memories connects working_memory and environment to the engine.

Set a slot: working_memory.focusbuffer.state = 'bread1'
Replace a chunk: working_memory.focusbuffer = {'state': 'bread1'}
Whole-chunk assignments copy equally in working memory, the environment,
and any new memory source. Slot edits preserve the other slots.
New buffers and objects need no registration:
  working_memory.retrievalbuffer = {'state': 'empty'}
  environment.bread2 = environment.bread1  # independent copy (create bread1 first)
Dictionary conditions, wildcard matching, bracket access, and update() still work.
There is no automatic merging, activation change, or buffer-only restriction.
The reusable access mechanism is in computational_architecture/memory_view.py.
Fill your memories, define productions, then create and run ProductionCycle.
""")
