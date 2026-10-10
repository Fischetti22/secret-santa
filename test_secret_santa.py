import random

from secret_santa import PARTICIPANTS, RESTRICTED_GROUP, create_assignments, is_valid_assignment


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
