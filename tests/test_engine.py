from __future__ import annotations

import math

import pytest

from solar_sim.engine import SimulationEngine
from solar_sim.scenario import AU, build_solar_system


def _norm(v: tuple[float, float, float]) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def test_earth_stays_near_one_au_after_one_year() -> None:
    engine = SimulationEngine(build_solar_system())
    engine.run(365, 86400.0)

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


def test_energy_is_reasonably_stable_for_one_year() -> None:
    engine = SimulationEngine(build_solar_system())
    e0 = engine.total_energy()
    engine.run(365, 86400.0)
    e1 = engine.total_energy()

    drift_ratio = abs((e1 - e0) / e0)
    assert drift_ratio < 1e-3


def test_total_momentum_is_conserved() -> None:
    engine = SimulationEngine(build_solar_system())
    p0 = _norm(engine.total_momentum())
    engine.run(30, 86400.0)
    p1 = _norm(engine.total_momentum())

    # Numerical error should stay tiny for this short horizon.
    assert abs(p1 - p0) / p0 < 1e-12


def test_validation_errors() -> None:
    bodies = build_solar_system()

    with pytest.raises(ValueError):
        SimulationEngine([bodies[0]])
    with pytest.raises(ValueError):
        SimulationEngine(bodies, g=0)
    with pytest.raises(ValueError):
        SimulationEngine(bodies, softening=-1)

    engine = SimulationEngine(bodies)
    with pytest.raises(ValueError):
        engine.run(-1, 1.0)
    with pytest.raises(ValueError):
        engine.step(0)
    with pytest.raises(ValueError):
        engine.set_gravity_scale(0)
