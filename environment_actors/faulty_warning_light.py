"""Independent environmental actor for the faulty warning light."""

import random


faulty_warning_light_productions = []


def maybe_turn_on_warning_light(memories):
    """Turn the light on with the probability stored in the actor's memory."""
    actor_state = memories["warning_light_memory"]["state"]
    actor_state["checks"] += 1
    if random.random() < actor_state["probability"]:
        memories["environment"]["warning_light"]["state"] = "on"
        print("ENVIRONMENT ACTOR: warning-light check done; faulty warning light turned on")
    else:
        print("ENVIRONMENT ACTOR: warning-light check done; warning light stayed off")


faulty_warning_light_productions.append({
    "matches": {
        "environment": {"warning_light": {"state": "off"}},
        "warning_light_memory": {
            "state": {"probability": "*", "checks": "*"}
        },
    },
    "negations": {},
    "utility": 10,
    "action": maybe_turn_on_warning_light,
    "report": "faulty warning light check",
})


REQUIRES = {
    "memories_keys": ["environment", "warning_light_memory"],
    "environment_objects": ["warning_light"],
}
