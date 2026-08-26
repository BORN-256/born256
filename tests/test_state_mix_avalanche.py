"""
BORN-256 State-Wide Avalanche Test

Measures avalanche behavior over many random 256-bit states.

Experimental research only.
This is NOT a cryptographic security proof.
"""

import random

from test_state_mix import state_mix


# ============================================================
# CONSTANTS
# ============================================================

STATE_SIZE = 256
SAMPLES = 1000


# ============================================================
# HELPERS
# ============================================================

def changed_bits(a, b):
    return sum(
        x != y
        for x, y in zip(a, b)
    )


def random_state():
    return tuple(
        random.getrandbits(1)
        for _ in range(STATE_SIZE)
    )


# ============================================================
# AVALANCHE TEST
# ============================================================

def main():

    results = []

    for _ in range(SAMPLES):

        original = random_state()

        # Flip one random input bit.
        position = random.randrange(STATE_SIZE)

        modified = list(original)
        modified[position] ^= 1
        modified = tuple(modified)

        output_a = state_mix(original)
        output_b = state_mix(modified)

        changed = changed_bits(
            output_a,
            output_b
        )

        results.append(changed)

    minimum = min(results)
    maximum = max(results)
    average = sum(results) / len(results)

    print()
    print("BORN-256 State-Wide Avalanche Analysis")
    print("=" * 45)

    print(
        f"Samples               : {SAMPLES}"
    )

    print(
        f"State size             : {STATE_SIZE} bits"
    )

    print(
        f"Minimum changed bits   : {minimum}"
    )

    print(
        f"Maximum changed bits   : {maximum}"
    )

    print(
        f"Average changed bits   : "
        f"{average:.2f}"
    )

    print(
        f"Average changed       : "
        f"{average / STATE_SIZE * 100:.2f}%"
    )

    print("=" * 45)

    print()
    print("Ideal reference:")
    print(
        "Approximately 128 / 256 bits "
        "changed on average (~50%)."
    )

    print()
    print(
        "This result is an experimental diffusion "
        "measurement, not a cryptographic security proof."
    )


if __name__ == "__main__":
    main()