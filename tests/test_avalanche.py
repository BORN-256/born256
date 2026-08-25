"""
BORN-256 Avalanche Analysis

Experimental analysis of the one-round BORN-256 construction.

This test measures how many output bits change when exactly
one input bit is flipped.

This is NOT a cryptographic security proof.
"""

import os
import sys


# ============================================================
# IMPORT BORN-256
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    PROJECT_ROOT,
    "src"
)

sys.path.insert(0, SRC_DIR)

from born256 import born_round


# ============================================================
# PARAMETERS
# ============================================================

BLOCK_SIZE = 32
STATE_BITS = 256

SAMPLES = 1000


# ============================================================
# BIT UTILITIES
# ============================================================

def flip_bit(data: bytes, bit_index: int) -> bytes:
    """
    Return a copy of data with exactly one bit flipped.

    Bit index:
        0 -> first bit
        255 -> last bit
    """

    if not 0 <= bit_index < STATE_BITS:
        raise ValueError(
            "Bit index must be between 0 and 255."
        )

    result = bytearray(data)

    byte_index = bit_index // 8

    bit_position = 7 - (bit_index % 8)

    result[byte_index] ^= (
        1 << bit_position
    )

    return bytes(result)


def count_changed_bits(
    a: bytes,
    b: bytes
) -> int:
    """
    Count the number of differing bits between
    two 256-bit values.
    """

    if len(a) != len(b):
        raise ValueError(
            "Inputs must have the same length."
        )

    changed = 0

    for byte_a, byte_b in zip(a, b):

        difference = byte_a ^ byte_b

        changed += difference.bit_count()

    return changed


# ============================================================
# AVALANCHE TEST
# ============================================================

def run_avalanche_test() -> None:
    """
    Run the avalanche analysis.

    For every sample:

        1. Generate random 256-bit state.
        2. Generate random 256-bit round key.
        3. Select one random input bit.
        4. Flip exactly that bit.
        5. Run both states through one BORN round.
        6. Count changed output bits.
    """

    results = []

    for _ in range(SAMPLES):

        # ----------------------------------------------------
        # Random 256-bit state
        # ----------------------------------------------------

        state = os.urandom(
            BLOCK_SIZE
        )

        # ----------------------------------------------------
        # Random 256-bit round key
        # ----------------------------------------------------

        round_key = os.urandom(
            BLOCK_SIZE
        )

        # ----------------------------------------------------
        # Select exactly one input bit
        # ----------------------------------------------------

        bit_index = int.from_bytes(
            os.urandom(2),
            "big"
        ) % STATE_BITS

        modified_state = flip_bit(
            state,
            bit_index
        )

        # ----------------------------------------------------
        # Process both states
        # ----------------------------------------------------

        output_a = born_round(
            state,
            round_key
        )

        output_b = born_round(
            modified_state,
            round_key
        )

        # ----------------------------------------------------
        # Count changed output bits
        # ----------------------------------------------------

        changed_bits = count_changed_bits(
            output_a,
            output_b
        )

        results.append(
            changed_bits
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    minimum = min(results)

    maximum = max(results)

    average = sum(results) / len(results)

    percentage = (
        average / STATE_BITS
    ) * 100

    # ========================================================
    # OUTPUT
    # ========================================================

    print()
    print("BORN-256 Avalanche Analysis")
    print("=" * 35)

    print(
        f"Samples               : {SAMPLES}"
    )

    print(
        f"State size             : {STATE_BITS} bits"
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
        f"Average changed        : {percentage:.2f}%"
    )

    print("=" * 35)

    print()
    print(
        "Ideal reference:"
    )

    print(
        "Approximately 128 / 256 bits "
        "changed on average (~50%)."
    )

    print()
    print(
        "This result is an experimental "
        "diffusion measurement, not a "
        "cryptographic security proof."
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_avalanche_test()
    