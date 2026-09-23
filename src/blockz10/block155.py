"""
Block 15/5 — conservative value-distribution pyramid.

Structure (blockz10.blogspot.com / block155.blogspot.com, 2020-2022):

  * Level 0: 1 block holding value 0 (the origin block).
  * Levels 1..5: level n holds n blocks of value 10 each.
  * 15 value blocks across 5 levels ("15/5"); system total = 150.

Each level divides its total among a set of *receptor* levels. The
division is conservative: the sum over all receptors always returns
the system total, minus explicit rounding dust which the simulator
tracks instead of silently losing (149.86 vs 150 in the original
hand-worked example, when quotas are truncated to 2 decimals).

The rule table is configurable. Two tables documented by the author
are shipped:

  * ``DEFAULT_RULES``  - the manuscript table
        (0: /2, 1: /3, 2: /2, 3: /4, 4: /2, 5: /3)
  * ``EXAMPLE_RULES``  - the worked example on block155.blogspot.com
        (level 2 = 20 -> /3 -> 6.66 to receptor levels 3, 4, 5)

Threshold incentives from the manuscript are exposed via
``Block155.incentive`` :

    quota 16.66 at level 1 -> +15%
    quota 13.34 at level 4 -> +10%
    quota 11.16 at level 5 -> +10%
    quota  6.66 at level 3 -> -10%
    quota  3.75 at level 2 -> -10%
"""

from __future__ import annotations

from dataclasses import dataclass, field


BLOCK_VALUE = 10.0
LEVELS = (0, 1, 2, 3, 4, 5)


@dataclass(frozen=True)
class DistributionRule:
    """How one level splits its total: divisor and receptor levels."""

    divisor: int
    receptors: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.divisor < 1:
            raise ValueError("divisor must be >= 1")
        if len(self.receptors) != self.divisor:
            raise ValueError(
                f"rule declares divisor {self.divisor} but {len(self.receptors)} receptors"
            )
        for r in self.receptors:
            if r not in LEVELS:
                raise ValueError(f"receptor level out of range: {r}")


# Manuscript table: 0/2, 10/3, 20/2, 30/4, 40/2, 50/3.
# Receptors follow the hand-drawn arrows (downward/lateral flow).
DEFAULT_RULES: dict[int, DistributionRule] = {
    0: DistributionRule(2, (1, 2)),
    1: DistributionRule(3, (2, 3, 4)),
    2: DistributionRule(2, (4, 5)),
    3: DistributionRule(4, (1, 2, 4, 5)),
    4: DistributionRule(2, (3, 5)),
    5: DistributionRule(3, (0, 1, 2)),
}

# Worked example published on block155.blogspot.com:
# "Block 2 (blue) = 20 < Block 2 in Block 3, 4, and 5 = 20/3 = 6.66"
EXAMPLE_RULES: dict[int, DistributionRule] = {
    **DEFAULT_RULES,
    2: DistributionRule(3, (3, 4, 5)),
}

# Manuscript threshold incentives: (level, quota) -> earn/loss rate.
INCENTIVES: dict[int, tuple[float, float]] = {
    1: (16.66, +0.15),
    2: (3.75, -0.10),
    3: (6.66, -0.10),
    4: (13.34, +0.10),
    5: (11.16, +0.10),
}


@dataclass
class Block155:
    """Simulator for one distribution round of the 15/5 pyramid."""

    rules: dict[int, DistributionRule] = field(default_factory=lambda: dict(DEFAULT_RULES))
    precision: int | None = 2  # None = exact fractions (no dust)

    def level_total(self, level: int) -> float:
        """Initial total held by a level (level n holds n * 10)."""
        if level not in LEVELS:
            raise ValueError(f"level out of range: {level}")
        return level * BLOCK_VALUE

    def quota(self, level: int) -> float:
        """Per-receptor quota a level sends out (total / divisor)."""
        q = self.level_total(level) / self.rules[level].divisor
        if self.precision is not None:
            q = _truncate(q, self.precision)
        return q

    def distribute(self) -> "RoundResult":
        """Run one full round: every level splits into its receptors."""
        received = {lv: 0.0 for lv in LEVELS}
        sent = {lv: 0.0 for lv in LEVELS}
        for lv in LEVELS:
            rule = self.rules[lv]
            q = self.quota(lv)
            for r in rule.receptors:
                received[r] += q
                sent[lv] += q
        total_in = sum(self.level_total(lv) for lv in LEVELS)
        total_out = sum(received.values())
        return RoundResult(
            received=received,
            sent=sent,
            total_in=total_in,
            total_out=round(total_out, 10),
            dust=round(total_in - total_out, 10),
        )

    def incentive(self, level: int) -> tuple[float, float] | None:
        """Manuscript threshold and earn/loss rate for a level, if any."""
        return INCENTIVES.get(level)


@dataclass(frozen=True)
class RoundResult:
    received: dict[int, float]
    sent: dict[int, float]
    total_in: float
    total_out: float
    dust: float

    @property
    def conserved(self) -> bool:
        """Value is conserved up to rounding dust (dust >= 0, < 1)."""
        return 0.0 <= self.dust < 1.0


def _truncate(x: float, digits: int) -> float:
    scale = 10**digits
    return int(x * scale) / scale
