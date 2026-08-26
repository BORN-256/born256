"""
BORN-256 Cross-Group Mixing Test

Experimental reversible mixing layer.

This test verifies:
1. Reversibility.
2. Cross-group bit propagation.
"""

# ============================================================
# BOOLEAN GATES
# ============================================================

def and_gate(a, b):
    return a & b


def or_gate(a, b):
    return a | b


def not_gate(a):
    return 1 - a


def xor_gate(a, b):
    return and_gate(
        or_gate(a, b),
        not_gate(and_gate(a, b))
    )


# ============================================================
# REVERSIBLE CROSS-GROUP MIX
# ============================================================

def cross_mix(groups):
    """
    Reversible cross-group mixing.

    Each group contains 3 bits.

    The operation is a sequence of reversible
    XOR-based controlled transformations.
    """

    groups = [list(group) for group in groups]

    # Mix group 0 -> group 1
    for i in range(3):
        groups[1][i] = xor_gate(
            groups[1][i],
            groups[0][i]
        )

    # Mix group 1 -> group 2
    for i in range(3):
        groups[2][i] = xor_gate(
            groups[2][i],
            groups[1][i]
        )

    # Mix group 2 -> group 0
    for i in range(3):
        groups[0][i] = xor_gate(
            groups[0][i],
            groups[2][i]
        )

    return tuple(tuple(group) for group in groups)


# ============================================================
# INVERSE
# ============================================================

def inverse_cross_mix(groups):
    """
    Reverse the cross-group mixing.

    Operations are undone in reverse order.
    """

    groups = [list(group) for group in groups]

    # Undo group 2 -> group 0
    for i in range(3):
        groups[0][i] = xor_gate(
            groups[0][i],
            groups[2][i]
        )

    # Undo group 1 -> group 2
    for i in range(3):
        groups[2][i] = xor_gate(
            groups[2][i],
            groups[1][i]
        )

    # Undo group 0 -> group 1
    for i in range(3):
        groups[1][i] = xor_gate(
            groups[1][i],
            groups[0][i]
        )

    return tuple(tuple(group) for group in groups)


# ============================================================
# REVERSIBILITY TEST
# ============================================================

def test_reversibility():

    test_cases = [
        (
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ),
        (
            (1, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ),
        (
            (0, 1, 0),
            (0, 0, 0),
            (0, 0, 0),
        ),
        (
            (0, 0, 1),
            (0, 0, 0),
            (0, 0, 0),
        ),
        (
            (1, 1, 1),
            (0, 1, 0),
            (1, 0, 1),
        ),
    ]

    for original in test_cases:

        transformed = cross_mix(original)

        recovered = inverse_cross_mix(
            transformed
        )

        if recovered != original:
            raise AssertionError(
                f"FAILED: "
                f"{original} -> "
                f"{transformed} -> "
                f"{recovered}"
            )

    print(
        "Cross-group reversibility test: PASS"
    )


# ============================================================
# DIFFUSION TEST
# ============================================================

def count_changed_bits(a, b):

    changed = 0

    for group_a, group_b in zip(a, b):

        for bit_a, bit_b in zip(
            group_a,
            group_b
        ):
            if bit_a != bit_b:
                changed += 1

    return changed


def test_cross_group_diffusion():

    original = (
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    )

    modified = (
        (1, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    )

    output_a = cross_mix(original)
    output_b = cross_mix(modified)

    changed = count_changed_bits(
        output_a,
        output_b
    )

    print(
        f"Cross-group diffusion: "
        f"{changed} / 9 bits changed"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_reversibility()

    test_cross_group_diffusion()