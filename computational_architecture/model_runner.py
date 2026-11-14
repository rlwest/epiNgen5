"""Set up a model once and let it choose how many cycles to run."""

from computational_architecture.production_cycle import ProductionCycle
from computational_architecture.setup_production_systems import setup_production_systems as assemble_systems


def make_model_runner(memories, groups):
    """Return a run_cycles function for this model's memories and systems."""
    systems, reset_values = assemble_systems(groups)
    engine = ProductionCycle()

    def run_cycles(cycles):
        engine.run_cycles(memories, systems, reset_values, cycles=cycles)

    return run_cycles
