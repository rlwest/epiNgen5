
# import productions for modules
from modules.visual_productions import VisualProductions, REQUIRES as VISUAL_REQUIRES
print("Motor Module REQUIRES:", VISUAL_REQUIRES)

from modules.motor_productions import MotorProductions, REQUIRES as MOTOR_REQUIRES
print("Motor Module REQUIRES:", MOTOR_REQUIRES)

#### from modules.dm_symbolic import DM_Symbolic_Productions
#### from modules.dm_subsymbolic import DM_Subsymbolic_Productions

from computational_architecture.production_cycle import ProductionCycle

from computational_architecture.memory_view import MemoryView as _MemoryView
from computational_architecture.memory_view import register_buffer as _register_buffer




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
