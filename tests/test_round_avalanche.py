"""
BORN-256 Full Round Avalanche Test

Experimental research test.
Measures how one changed input bit propagates
through the complete BORN-256 round.

NOT a cryptographic security proof.
"""

import random
import sys

sys.path.insert(0, "src")

from born256 import born_round


# ============================================================
# PARAMETERS
# ============================================================

BLOCK_SIZE = 32
SAMPLES = 1000


# ============================================================
# HELPERS
# ============================================================

def changed_bits(a, b):
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(a, b)
    )


def random_block():
    return bytes(
        random.getrandbits(8)
        for _ in range(BLOCK_SIZE)
    )


# ============================================================
# TEST
# ============================================================

def main():

    results = []

    key = bytes([0xAA] * BLOCK_SIZE)

    for _ in range(SAMPLES):

        original = random_block()

        position = random.randrange(256)

        modified = bytearray(original)

        byte_index = position // 8
        bit_index = 7 - (position % 8)

        modified[byte_index] ^= (1 << bit_index)

        modified = bytes(modified)

        output_a = born_round(
            original,
            key
        )

        output_b = born_round(
            modified,
            key
        )

        changed = changed_bits(
            output_a,
            output_b
        )

        results.append(changed)

    minimum = min(results)
    maximum = max(results)
    average = sum(results) / len(results)

    print()
    print("BORN-256 Full Round Avalanche Analysis")
    print("=" * 45)

    print(
        f"Samples               : {len(results)}"
    )

    print(
        f"State size             : 256 bits"
    )

    print(
        f"Minimum changed bits   : {minimum}"
    )

    print(
        f"Maximum changed bits   : {maximum}"
    )

    print(
        f"Average changed bits   : {average:.2f}"
    )

    print(
        f"Average changed       : "
        f"{average / 256 * 100:.2f}%"
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