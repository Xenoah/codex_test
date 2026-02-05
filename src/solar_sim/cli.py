from __future__ import annotations

import argparse
from math import sqrt

from .engine import SimulationEngine
from .scenario import AU, build_solar_system


def _norm(v: tuple[float, float, float]) -> float:
    return sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def run() -> None:
    parser = argparse.ArgumentParser(description="Solar-centric simulation demo")
    parser.add_argument("--steps", type=int, default=365, help="integration steps")
    parser.add_argument("--dt", type=float, default=86400.0, help="seconds per step")
    parser.add_argument("--gravity-scale", type=float, default=1.0, help="multiplier for physical G")
    args = parser.parse_args()

    engine = SimulationEngine(build_solar_system())
    engine.set_gravity_scale(args.gravity_scale)

    energy_before = engine.total_energy()
    momentum_before = _norm(engine.total_momentum())
    engine.run(args.steps, args.dt)
    energy_after = engine.total_energy()
    momentum_after = _norm(engine.total_momentum())

    print("Simulation completed")
    print(f"Energy drift ratio: {(energy_after - energy_before) / abs(energy_before):+.3e}")
    print(f"Momentum norm: {momentum_before:.3e} -> {momentum_after:.3e}")

    com = engine.center_of_mass()
    print(f"Center of mass (AU): x={com[0] / AU:+.6f}, y={com[1] / AU:+.6f}, z={com[2] / AU:+.6f}")

    for body in engine.bodies:
        x_au = body.position[0] / AU
        y_au = body.position[1] / AU
        print(f"{body.name:8s} x={x_au:+.3f} AU y={y_au:+.3f} AU")


if __name__ == "__main__":
    run()
