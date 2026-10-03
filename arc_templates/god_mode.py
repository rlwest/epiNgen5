"""Minimal architecture with working memory and direct environmental access.

Start a model with:
    from arc_templates.god_mode import ProductionCycle, working_memory, environment, memories

Then supply the model's initial contents, for example:
    working_memory['focusbuffer']['state'] = 'bread1'
    environment.update({'bread1': {'location': 'counter'}})

Update these dictionaries in place so that memories keeps referring to them.
Define productions and run ProductionCycle in the model's own file.
Python imports this module once per process; repeated imports share its state
and do not repeat the introductory message. Run each model in a fresh process.
"""

from computational_architecture.production_cycle import ProductionCycle

__all__ = ['ProductionCycle', 'working_memory', 'environment', 'memories']

working_memory = {'focusbuffer': {}}
environment = {}

memories = {
    'working_memory': working_memory,
    'environment': environment,
}

print("""God Mode architectural template loaded.
You have imported the following structures:
  - ProductionCycle: the computational architecture's production-cycle class.
  - working_memory: a dictionary with an empty 'focusbuffer' for task state.
  - environment: an empty dictionary for objects in the external world.
  - memories: a dictionary connecting 'working_memory' and 'environment' to the engine.

God Mode productions can directly inspect and change the environment.
There are no separate vision or motor modules; delayed actions are available.
Next: fill the focusbuffer, add environmental objects, and define your productions.
Update working_memory and environment in place to keep them connected to memories.
Create a ProductionCycle instance and run it when your model is ready.
""")
