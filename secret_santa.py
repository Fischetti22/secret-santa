"""Constrained Secret Santa matching and local assignment storage."""

from __future__ import annotations

import json
import random
from pathlib import Path

PARTICIPANTS = (
    "Pedro",
    "Sydney",
    "Selena",
    "Amelia",
    "Thiago",
    "Alitza",
    "Maura",
    "Ken",
    "Yuta",
    "Matheus",
    "Rosie",
    "Alessandro",
    "Samantha",
    "Marina",
    "Anayah",
    "Maria",
)
RESTRICTED_GROUP = frozenset({"Pedro", "Sydney", "Selena", "Amelia"})
STATE_FILE = Path(__file__).with_name("assignments.json")


def is_valid_assignment(assignments: dict[str, str]) -> bool:
    """Return whether assignments obey every Secret Santa rule."""
    if set(assignments) != set(PARTICIPANTS):
        return False
    if set(assignments.values()) != set(PARTICIPANTS):
        return False
    return all(
        giver != recipient
        and not ({giver, recipient} <= RESTRICTED_GROUP)
        for giver, recipient in assignments.items()
    )


def create_assignments(rng: random.Random | None = None) -> dict[str, str]:
    """Create a random, valid complete assignment."""
    rng = rng or random.SystemRandom()
    recipients = list(PARTICIPANTS)

    for _ in range(10_000):
        rng.shuffle(recipients)
        assignments = dict(zip(PARTICIPANTS, recipients, strict=True))
        if is_valid_assignment(assignments):
            return assignments

    raise RuntimeError("Could not create a valid Secret Santa assignment.")


def load_state(path: Path = STATE_FILE) -> dict[str, object]:
    """Load saved assignments and revealed participants, creating them if needed."""
    if path.exists():
        with path.open(encoding="utf-8") as state_file:
            state = json.load(state_file)
        if is_valid_assignment(state.get("assignments", {})):
            state.setdefault("revealed", [])
            state.setdefault("wishlists", {})
            return state

    state = {"assignments": create_assignments(), "revealed": [], "wishlists": {}}
    save_state(state, path)
    return state


def save_state(state: dict[str, object], path: Path = STATE_FILE) -> None:
    """Write state atomically to avoid a partial file during a rerun."""
    temporary_path = path.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, indent=2)
    temporary_path.replace(path)
