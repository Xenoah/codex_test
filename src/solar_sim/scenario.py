from __future__ import annotations

from .bodies import Body

AU = 149_597_870_700.0


def build_solar_system() -> list[Body]:
    """Solar-centric starter scenario.

    This is intentionally compact for MVP: Sun + 8 planets in near-circular initial orbits.
    """

    return [
        Body("Sun", 1.9885e30, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        Body("Mercury", 3.3011e23, (0.387 * AU, 0.0, 0.0), (0.0, 47_870.0, 0.0)),
        Body("Venus", 4.8675e24, (0.723 * AU, 0.0, 0.0), (0.0, 35_020.0, 0.0)),
        Body("Earth", 5.97237e24, (1.0 * AU, 0.0, 0.0), (0.0, 29_780.0, 0.0)),
        Body("Mars", 6.4171e23, (1.524 * AU, 0.0, 0.0), (0.0, 24_077.0, 0.0)),
        Body("Jupiter", 1.8982e27, (5.203 * AU, 0.0, 0.0), (0.0, 13_070.0, 0.0)),
        Body("Saturn", 5.6834e26, (9.537 * AU, 0.0, 0.0), (0.0, 9_680.0, 0.0)),
        Body("Uranus", 8.6810e25, (19.191 * AU, 0.0, 0.0), (0.0, 6_800.0, 0.0)),
        Body("Neptune", 1.02413e26, (30.07 * AU, 0.0, 0.0), (0.0, 5_430.0, 0.0)),
    ]
