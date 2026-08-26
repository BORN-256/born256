"""
BORN-256 Differential Analysis

Experimental research test.

Measures how input differences propagate through
the current state-wide reversible mixing layer.

This is NOT a cryptographic security proof.
"""

import random

from test_state_mix import state_mix


# ============================================================
# PARAMETERS
# ============================================================

STATE_SIZE = 256
SAMPLES = 1000


# ============================================================
# HELPERS
# ============================================================

def random_state():
    return tuple(
        random.getrandbits(1)
        for _ in range(STATE_SIZE)
    )


def xor_states(a, b):
    return tuple(
        x ^ y
        for x, y in zip(a, b)
    )


def changed_bits(a, b):
    return sum(
        x != y
        for x, y in zip(a, b)
    )


# ============================================================
# DIFFERENTIAL TEST
# ============================================================

def main():

    results = []

    for _ in range(SAMPLES):

        original = random_state()

        # Create a random second state.
        modified = random_state()

        # Input difference.
        input_difference = xor_states(
            original,
            modified
        )

        # Ignore identical pairs.
        if not any(input_difference):
            continue

        output_a = state_mix(original)
        output_b = state_mix(modified)

        output_difference = xor_states(
            output_a,
            output_b
        )

        changed = sum(
            bit != 0
            for bit in output_difference
        )

        results.append(changed)

    minimum = min(results)
    maximum = max(results)
    average = sum(results) / len(results)

    print()
    print("BORN-256 Differential Analysis")
    print("=" * 45)

    print(
        f"Samples               : {len(results)}"
    )

    print(
        f"State size             : {STATE_SIZE} bits"
    )

    print(
        f"Minimum output diff    : {minimum} bits"
    )

    print(
        f"Maximum output diff    : {maximum} bits"
    )

    print(
        f"Average output diff    : "
        f"{average:.2f} bits"
    )

    print(
        f"Average percentage     : "
        f"{average / STATE_SIZE * 100:.2f}%"
    )

    print("=" * 45)

    print()
    print(
        "This measures diffusion of arbitrary "
        "input differences."
    )

    print(
        "It does NOT establish resistance to "
        "differential cryptanalysis."
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    main()