"""
BORN-256 Key Schedule Test

Experimental key expansion for 256-bit keys.

This is NOT a cryptographic security proof.
"""

import sys

sys.path.insert(0, "src")

from born256 import (
    key_schedule,
    inverse_key_schedule,
)


KEY_SIZE = 32
ROUNDS = 16


def changed_bits(a, b):
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(a, b)
    )


def main():

    key = bytes(
        range(KEY_SIZE)
    )

    print()
    print("BORN-256 Key Schedule Test")
    print("=" * 45)

    # --------------------------------------------------------
    # Generate round keys
    # --------------------------------------------------------

    round_keys = key_schedule(
        key,
        ROUNDS
    )

    print(
        f"Master key size       : {len(key) * 8} bits"
    )

    print(
        f"Round keys generated  : {len(round_keys)}"
    )

    # --------------------------------------------------------
    # Validate sizes
    # --------------------------------------------------------

    for i, round_key in enumerate(round_keys):

        if len(round_key) != KEY_SIZE:

            raise AssertionError(
                f"Round key {i} has invalid size."
            )

    print(
        "Round-key size test   : PASS"
    )

    # --------------------------------------------------------
    # Check uniqueness
    # --------------------------------------------------------

    unique_keys = len(
        set(round_keys)
    )

    print(
        f"Unique round keys     : "
        f"{unique_keys} / {ROUNDS}"
    )

    if unique_keys != ROUNDS:

        raise AssertionError(
            "Duplicate round keys detected."
        )

    print(
        "Round-key uniqueness  : PASS"
    )

    # --------------------------------------------------------
    # Key avalanche
    # --------------------------------------------------------

    modified_key = bytearray(key)

    modified_key[0] ^= 0x01

    modified_key = bytes(
        modified_key
    )

    modified_round_keys = key_schedule(
        modified_key,
        ROUNDS
    )

    differences = []

    for original, modified in zip(
        round_keys,
        modified_round_keys
    ):

        differences.append(
            changed_bits(
                original,
                modified
            )
        )

    average = (
        sum(differences)
        / len(differences)
    )

    print()
    print(
        "Key avalanche"
    )

    print(
        f"Minimum changed bits : "
        f"{min(differences)}"
    )

    print(
        f"Maximum changed bits : "
        f"{max(differences)}"
    )

    print(
        f"Average changed bits : "
        f"{average:.2f} / 256"
    )

    print(
        f"Average percentage  : "
        f"{average / 256 * 100:.2f}%"
    )

    print("=" * 45)

    print()
    print(
        "This is an experimental key-schedule "
        "diffusion measurement."
    )

    print(
        "It does NOT establish cryptographic security."
    )


if __name__ == "__main__":
    main()