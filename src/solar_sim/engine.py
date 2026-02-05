from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, List, Tuple

from .bodies import Body, Vector3


@dataclass
class Snapshot:
    positions: Dict[str, Vector3]
    velocities: Dict[str, Vector3]


class SimulationEngine:
    """Simple N-body engine using leapfrog integration."""

    def __init__(self, bodies: Iterable[Body], g: float = 6.67430e-11, softening: float = 1e3):
        self.bodies: List[Body] = list(bodies)
        self.g = g
        self.softening = softening

    def set_gravity_scale(self, scale: float) -> None:
        self.g = 6.67430e-11 * scale

    def snapshot(self) -> Snapshot:
        return Snapshot(
            positions={b.name: b.position for b in self.bodies},
            velocities={b.name: b.velocity for b in self.bodies},
        )

    def restore(self, snapshot: Snapshot) -> None:
        for body in self.bodies:
            body.position = snapshot.positions[body.name]
            body.velocity = snapshot.velocities[body.name]

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
        # Velocity half step
        accelerations = self._compute_accelerations()
        for i, body in enumerate(self.bodies):
            ax, ay, az = accelerations[i]
            vx, vy, vz = body.velocity
            body.velocity = (vx + ax * dt_seconds * 0.5, vy + ay * dt_seconds * 0.5, vz + az * dt_seconds * 0.5)

        # Position full step
        for body in self.bodies:
            px, py, pz = body.position
            vx, vy, vz = body.velocity
            body.position = (px + vx * dt_seconds, py + vy * dt_seconds, pz + vz * dt_seconds)

        # Velocity second half step
        accelerations = self._compute_accelerations()
        for i, body in enumerate(self.bodies):
            ax, ay, az = accelerations[i]
            vx, vy, vz = body.velocity
            body.velocity = (vx + ax * dt_seconds * 0.5, vy + ay * dt_seconds * 0.5, vz + az * dt_seconds * 0.5)

    def _compute_accelerations(self) -> List[Vector3]:
        accels: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0) for _ in self.bodies]
        for i, bi in enumerate(self.bodies):
            ax, ay, az = accels[i]
            for j, bj in enumerate(self.bodies):
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
