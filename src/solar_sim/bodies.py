from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Vector3 = Tuple[float, float, float]


@dataclass
class Body:
    """Single celestial body for N-body simulation."""

    name: str
    mass: float
    position: Vector3
    velocity: Vector3

    def kinetic_energy(self) -> float:
        vx, vy, vz = self.velocity
        return 0.5 * self.mass * (vx * vx + vy * vy + vz * vz)
