from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, List, Sequence, Tuple

from .bodies import Body, Vector3

BASE_GRAVITATIONAL_CONSTANT = 6.67430e-11


@dataclass
class Snapshot:
    positions: Dict[str, Vector3]
    velocities: Dict[str, Vector3]


class SimulationEngine:
    """Simple N-body engine using leapfrog integration."""

    def __init__(
        self,
        bodies: Iterable[Body],
        g: float = BASE_GRAVITATIONAL_CONSTANT,
        softening: float = 1e3,
    ):
        body_list = list(bodies)
        if len(body_list) < 2:
            raise ValueError("Simulation requires at least two bodies.")

        names = [body.name for body in body_list]
        if len(names) != len(set(names)):
            raise ValueError("Body names must be unique.")

        if g <= 0:
            raise ValueError("Gravitational constant must be positive.")
        if softening < 0:
            raise ValueError("Softening length must be non-negative.")

        self.bodies: List[Body] = body_list
        self.g = g
        self.softening = softening

    def set_gravity_scale(self, scale: float) -> None:
        if scale <= 0:
            raise ValueError("Gravity scale must be positive.")
        self.g = BASE_GRAVITATIONAL_CONSTANT * scale

    def snapshot(self) -> Snapshot:
        return Snapshot(
            positions={b.name: b.position for b in self.bodies},
            velocities={b.name: b.velocity for b in self.bodies},
        )

    def restore(self, snapshot: Snapshot) -> None:
        for body in self.bodies:
            if body.name not in snapshot.positions or body.name not in snapshot.velocities:
                raise KeyError(f"Body {body.name!r} missing in snapshot.")
            body.position = snapshot.positions[body.name]
            body.velocity = snapshot.velocities[body.name]

    def run(self, steps: int, dt_seconds: float) -> None:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        for _ in range(steps):
            self.step(dt_seconds)

    def center_of_mass(self) -> Vector3:
        total_mass = sum(body.mass for body in self.bodies)
        x = sum(body.mass * body.position[0] for body in self.bodies) / total_mass
        y = sum(body.mass * body.position[1] for body in self.bodies) / total_mass
        z = sum(body.mass * body.position[2] for body in self.bodies) / total_mass
        return (x, y, z)

    def total_momentum(self) -> Vector3:
        px = sum(body.mass * body.velocity[0] for body in self.bodies)
        py = sum(body.mass * body.velocity[1] for body in self.bodies)
        pz = sum(body.mass * body.velocity[2] for body in self.bodies)
        return (px, py, pz)

    def total_energy(self) -> float:
        kinetic = sum(b.kinetic_energy() for b in self.bodies)
        potential = 0.0
        for i, bi in enumerate(self.bodies):
            for bj in self.bodies[i + 1 :]:
                dx = bj.position[0] - bi.position[0]
                dy = bj.position[1] - bi.position[1]
                dz = bj.position[2] - bi.position[2]
                r = sqrt(dx * dx + dy * dy + dz * dz + self.softening * self.softening)
                potential -= self.g * bi.mass * bj.mass / r
        return kinetic + potential

    def step(self, dt_seconds: float) -> None:
        if dt_seconds <= 0:
            raise ValueError("dt_seconds must be positive")

        # Velocity half step
        accelerations = self._compute_accelerations(self.bodies)
        for i, body in enumerate(self.bodies):
            ax, ay, az = accelerations[i]
            vx, vy, vz = body.velocity
            body.velocity = (
                vx + ax * dt_seconds * 0.5,
                vy + ay * dt_seconds * 0.5,
                vz + az * dt_seconds * 0.5,
            )

        # Position full step
        for body in self.bodies:
            px, py, pz = body.position
            vx, vy, vz = body.velocity
            body.position = (
                px + vx * dt_seconds,
                py + vy * dt_seconds,
                pz + vz * dt_seconds,
            )

        # Velocity second half step
        accelerations = self._compute_accelerations(self.bodies)
        for i, body in enumerate(self.bodies):
            ax, ay, az = accelerations[i]
            vx, vy, vz = body.velocity
            body.velocity = (
                vx + ax * dt_seconds * 0.5,
                vy + ay * dt_seconds * 0.5,
                vz + az * dt_seconds * 0.5,
            )

    def _compute_accelerations(self, bodies: Sequence[Body]) -> List[Vector3]:
        accels: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0) for _ in bodies]
        for i, bi in enumerate(bodies):
            ax, ay, az = accels[i]
            for j, bj in enumerate(bodies):
                if i == j:
                    continue
                dx = bj.position[0] - bi.position[0]
                dy = bj.position[1] - bi.position[1]
                dz = bj.position[2] - bi.position[2]
                r2 = dx * dx + dy * dy + dz * dz + self.softening * self.softening
                inv_r3 = 1.0 / (r2 * sqrt(r2))
                scale = self.g * bj.mass * inv_r3
                ax += dx * scale
                ay += dy * scale
                az += dz * scale
            accels[i] = (ax, ay, az)
        return accels
