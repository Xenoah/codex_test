from __future__ import annotations

import argparse

from .engine import SimulationEngine
from .scenario import AU, build_solar_system


def run() -> None:
    parser = argparse.ArgumentParser(description="Solar-centric simulation demo")
    parser.add_argument("--steps", type=int, default=365, help="integration steps")
    parser.add_argument("--dt", type=float, default=86400.0, help="seconds per step")
    parser.add_argument("--gravity-scale", type=float, default=1.0)
    args = parser.parse_args()

    engine = SimulationEngine(build_solar_system())
    engine.set_gravity_scale(args.gravity_scale)

    for _ in range(args.steps):
        engine.step(args.dt)

    print("Simulation completed")
    for body in engine.bodies:
        x_au = body.position[0] / AU
        y_au = body.position[1] / AU
        print(f"{body.name:8s} x={x_au:+.3f} AU y={y_au:+.3f} AU")


if __name__ == "__main__":
    run()
