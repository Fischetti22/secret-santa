import random

from secret_santa import (
    PARTICIPANTS,
    RESTRICTED_GROUP,
    create_assignments,
    is_valid_assignment,
    load_state,
    save_state,
)


def test_generated_assignments_are_valid_and_unique():
    assignments = create_assignments(random.Random(42))

    assert set(assignments) == set(PARTICIPANTS)
    assert len(set(assignments.values())) == len(PARTICIPANTS)
    assert is_valid_assignment(assignments)


def test_restricted_group_members_are_not_paired_together():
    for seed in range(100):
        assignments = create_assignments(random.Random(seed))
        for giver in RESTRICTED_GROUP:
            assert assignments[giver] not in RESTRICTED_GROUP


def test_load_state_adds_wishlists_to_existing_draw(tmp_path):
    state_path = tmp_path / "assignments.json"
    save_state({"assignments": create_assignments(random.Random(1)), "revealed": []}, state_path)

    state = load_state(state_path)

    assert state["wishlists"] == {}
