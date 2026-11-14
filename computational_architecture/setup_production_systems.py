"""Assemble production systems with one timing setting per system. for use by production_cycle.py"""


def setup_production_systems(groups, default_countdown=1, countdowns=None):
    """Return (systems, reset_values) for ProductionCycle.run_cycles.

    groups maps system names to their production lists. default_countdown
    applies to every system unless countdowns supplies an override by name.
    For example, countdowns={'VisionSystem': 3} gives vision a three-cycle
    countdown while other systems use the default.

    Each timing is a positive whole number of cycles. The same value sets the
    starting countdown and the reset after firing. The engine changes the
    current countdown while reset_values retains the configured value.
    A countdown of 1 permits matching on the first cycle and the cycle after
    firing. Eligibility still requires a matching production.

    Preserve the supplied system order and production lists. Only the mutable
    countdown containers are new; this function neither runs nor copies a model.
    Motor action completion delays remain separate from these system timings.
    """
    if (not isinstance(default_countdown, int)
            or isinstance(default_countdown, bool) or default_countdown < 1):
        raise ValueError('default_countdown must be a positive whole number of cycles.')

    if countdowns is None:
        countdowns = {}
    for name, countdown in countdowns.items():
        if name not in groups:
            raise ValueError(f'Unknown production system in countdowns: {name!r}')
        if (not isinstance(countdown, int)
                or isinstance(countdown, bool) or countdown < 1):
            raise ValueError(f'Countdown for {name!r} must be a positive whole number of cycles.')

    systems = {}
    reset_values = {}
    for name, productions in groups.items():
        countdown = countdowns.get(name, default_countdown)
        systems[name] = [productions, countdown]
        reset_values[name] = countdown
    return systems, reset_values
