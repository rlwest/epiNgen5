"""ACT-R Emotion combines ACT-R-ish memory with amygdala productions.

CAPABILITIES
    Imports VisualProductions, MotorProductions, DM_Symbolic_Productions,
    DM_Subsymbolic_Productions, and AmygdalaProductions. Provides
    setup_production_systems, ProductionCycle, and make_model_runner. Models define
    their own ProceduralProductions and explicitly register all production
    systems they intend to run. Import alone does NOT start subsymbolic updates.
    This is an epiNgen teaching architecture, not a full ACT-R implementation.

MEMORY ORGANIZATION
    Exposes connected memories, working_memory, and environment MemoryView
    objects, with an initially empty working_memory.focusbuffer. Models
    initialize required motor/visual buffers and the declarative interface:
        DM_command_buffer              normal / retrieve / retrieve_partial
        DM_retieval_buffer             retrieval matches and negations
        DM_output_buffer               returned chunk or no_match result
        memories.declarative_memory    persistent chunks and their utility
    DM_retieval_buffer is the existing spelling in dm_symbolic.py and must
    remain unchanged until the whole interface is migrated together.
    At depth 2, whole-chunk assignment deep-copies; slot edits do not copy.
    Both bracket and dot access reach the same underlying memory.

SUBSYMBOLIC PROCESSING
    This template supplies an ACT-R-ish-specific subsymbolic production action
    that applies noise, decay, and cue-based spreading activation to
    declarative_memory (not working_memory). The focusbuffer provides the cue
    for spreading activation. Configure ACTRISH_SUBSYMBOLIC_PARAMETERS:
        noise_scalar         Gaussian utility noise per subsymbolic firing
        decay_amount         utility subtracted per subsymbolic firing
        spreading_boost      utility increase for shared cue values
    All three controls default to 0 (inactive). The model must register
    DM_Subsymbolic_Productions for these updates to occur. The underlying
    utility operations clamp noise/decay at zero. Retrieval is separately
    handled by DM_Symbolic_Productions; changing a subsymbolic parameter does
    not change retrieval thresholds or automatically request retrieval.

IMPORT BEHAVIOUR
    Importing assembles the architecture but runs no cycles, has no startup
    printout, and does not reset shared state. Run independent simulations in
    fresh processes.
"""

from modules.amygdala2 import (
    AmygdalaProductions, CalmProduction, CALM, FEAR, calm_down, feel_fear,
    REQUIRES as AMYGDALA_REQUIRES,
)

from modules.visual_productions import VisualProductions, REQUIRES as VISUAL_REQUIRES

from modules.motor_productions import MotorProductions, REQUIRES as MOTOR_REQUIRES

from modules.dm_symbolic import DM_Symbolic_Productions
from modules.dm_subsymbolic import DM_Subsymbolic_Productions as _BASE_DM_SUBSYMBOLIC_PRODUCTIONS
from cognitive_functions.chunk_noise import add_noise_to_utility
from cognitive_functions.decay import decay_all_memory_chunks
from cognitive_functions.spreading_activation import spreading_activation_boost

# Architecture-local settings. Subsymbolic processes work on declarative
# memory; working memory (focusbuffer) supplies the spreading-activation cue.
# Keeping this override in the ACT-R-ish template leaves shared modules and
# the GOMS architecture unchanged.
ACTRISH_SUBSYMBOLIC_PARAMETERS = {
    'noise_scalar': 0.0,
    'decay_amount': 0.0,
    'spreading_boost': 0.0,
}


def _adjust_actrish_DM(memories):
    settings = ACTRISH_SUBSYMBOLIC_PARAMETERS
    if settings['noise_scalar']:
        add_noise_to_utility(
            memories['declarative_memory'], scalar=settings['noise_scalar'])
    if settings['decay_amount']:
        decay_all_memory_chunks(
            memories, 'declarative_memory', decay_amount=settings['decay_amount'])
    if settings['spreading_boost']:
        spreading_activation_boost(
            memories, 'declarative_memory',
            memories['working_memory']['focusbuffer'],
            boost_factor=settings['spreading_boost'])


# Clone the module's production definitions instead of modifying the shared
# list: this architecture alone uses the corrected subsymbolic action.
DM_Subsymbolic_Productions = [
    {**production, 'action': _adjust_actrish_DM}
    if production.get('report') == 'adjust_DM' else production.copy()
    for production in _BASE_DM_SUBSYMBOLIC_PRODUCTIONS
]

from computational_architecture.production_cycle import ProductionCycle
from computational_architecture.setup_production_systems import setup_production_systems
from computational_architecture.model_runner import make_model_runner

from computational_architecture.memory_view import MemoryView as _MemoryView
from computational_architecture.memory_view import register_buffer as _register_buffer




# Import the architecture's connected memory views; models fill their buffers.
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

