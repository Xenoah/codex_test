from __future__ import annotations

import math

from solar_sim.engine import SimulationEngine
from solar_sim.scenario import AU, build_solar_system


def test_earth_stays_near_one_au_after_one_year() -> None:
    engine = SimulationEngine(build_solar_system())
    for _ in range(365):
        engine.step(86400.0)

    earth = next(b for b in engine.bodies if b.name == "Earth")
    r = math.sqrt(sum(c * c for c in earth.position))
    assert 0.95 * AU <= r <= 1.05 * AU


def test_snapshot_restore_round_trip() -> None:
    engine = SimulationEngine(build_solar_system())
    snap = engine.snapshot()
    engine.step(86400.0)
    engine.restore(snap)
    earth = next(b for b in engine.bodies if b.name == "Earth")
    assert earth.position == snap.positions["Earth"]
