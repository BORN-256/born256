"""
BORN-256 State-Wide Mixing Experiment

Experimental reversible bit-mixing network.

This is a research experiment, not a cryptographic security proof.
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
# STATE MIXING
# ============================================================

def mix_bit(state, destination, source):
    """
    Reversible operation:

        state[destination] ^= state[source]

    XOR is implemented through AND/OR/NOT.
    """

    state[destination] = xor_gate(
        state[destination],
        state[source]
    )


def state_mix(state):
    """
    Experimental state-wide reversible mixing.

    Uses a sequence of XOR-controlled operations.
    """

    state = list(state)

    # Forward mixing.
    for distance in (1, 3, 7, 15, 31, 63, 127):

        for i in range(256):
            source = (i + distance) % 256

            mix_bit(
                state,
                i,
                source
            )

    return tuple(state)


# ============================================================
# INVERSE
# ============================================================

def inverse_state_mix(state):
    """
    Exact inverse of state_mix().

    Since every XOR mixing operation is self-inverse,
    the operations are simply performed in reverse order.
    """

    state = list(state)

    for distance in reversed(
        (1, 3, 7, 15, 31, 63, 127)
    ):

        for i in reversed(range(256)):
            source = (i + distance) % 256

            mix_bit(
                state,
                i,
                source
            )

    return tuple(state)


# ============================================================
# BIT DIFFERENCE
# ============================================================

def changed_bits(a, b):
    return sum(
        x != y
        for x, y in zip(a, b)
    )


# ============================================================
# REVERSIBILITY TEST
# ============================================================

def test_reversibility():

    test_states = []

    # All-zero state.
    test_states.append(
        tuple([0] * 256)
    )

    # One-bit state.
    state = [0] * 256
    state[0] = 1
    test_states.append(tuple(state))

    # Middle-bit state.
    state = [0] * 256
    state[127] = 1
    test_states.append(tuple(state))

    # Last-bit state.
    state = [0] * 256
    state[255] = 1
    test_states.append(tuple(state))

    # Alternating state.
    test_states.append(
        tuple(i % 2 for i in range(256))
    )

    # All-one state.
    test_states.append(
        tuple([1] * 256)
    )

    for original in test_states:

        transformed = state_mix(original)

        recovered = inverse_state_mix(
            transformed
        )

        if recovered != original:
            raise AssertionError(
                "State-wide mixing reversibility FAILED"
            )

    print(
        "256-bit state mixing reversibility test: PASS"
    )


# ============================================================
# SINGLE-BIT DIFFUSION TEST
# ============================================================

def test_diffusion():

    original = [0] * 256

    modified = [0] * 256
    modified[0] = 1

    output_a = state_mix(original)
    output_b = state_mix(modified)

    changed = changed_bits(
        output_a,
        output_b
    )

    print(
        f"Single-bit diffusion: "
        f"{changed} / 256 bits changed"
    )

    print(
        f"Diffusion percentage: "
        f"{changed / 256 * 100:.2f}%"
    )


# ============================================================
# MULTIPLE INPUT BITS
# ============================================================

def test_multiple_positions():

    positions = (
        0,
        1,
        31,
        63,
        127,
        128,
        191,
        255,
    )

    print()
    print("Position diffusion")
    print("=" * 40)

    for position in positions:

        original = [0] * 256

        modified = [0] * 256
        modified[position] = 1

        output_a = state_mix(original)
        output_b = state_mix(modified)

        changed = changed_bits(
            output_a,
            output_b
        )

        print(
            f"Input bit {position:3d}: "
            f"{changed:3d} / 256"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("BORN-256 State-Wide Mixing Experiment")
    print("=" * 45)

    test_reversibility()
    test_diffusion()
    test_multiple_positions()

    print("=" * 45)
    print()
    print(
        "NOTE: This experiment does not establish "
        "cryptographic security."
    )