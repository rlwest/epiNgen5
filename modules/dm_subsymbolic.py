"""Configure noise, decay, and spreading activation for one model's productions."""

from functools import partial

from cognitive_functions.chunk_noise import add_noise_to_utility
from cognitive_functions.decay import decay_all_memory_chunks
from cognitive_functions.spreading_activation import spreading_activation_boost


def adjust_DM(memories, *, noise_scalar=0.0, decay_amount=0.0, spreading_boost=0.0):
    """Apply noise to declarative memory and decay and spreading to working memory."""
    if noise_scalar:
        add_noise_to_utility(memories['declarative_memory'], scalar=noise_scalar)
    if decay_amount:
        decay_all_memory_chunks(memories, 'working_memory', decay_amount=decay_amount)
    if spreading_boost:
        spreading_activation_boost(memories, 'working_memory',
                                   memories['working_memory']['focusbuffer'],
                                   boost_factor=spreading_boost)


def make_dm_subsymbolic_productions(*, noise_scalar=0.0, decay_amount=0.0, spreading_boost=0.0):
    """Return productions with settings local to this model. Zero disables an effect."""
    action = partial(adjust_DM, noise_scalar=noise_scalar, decay_amount=decay_amount,
                     spreading_boost=spreading_boost)
    return [{
        'matches': {'working_memory': {'DM_command_buffer': {'state': '*'}}},
        'negations': {},
        'utility': 10,
        'action': action,
        'report': 'adjust_DM',
    }]


DM_Subsymbolic_Productions = make_dm_subsymbolic_productions()


REQUIRES = {
    "working_memory_buffers": ["DM_command_buffer", "focusbuffer"],
    "memories_keys": ["declarative_memory", "working_memory"],
}
