"""
BORN-256 Full Cipher Test

Tests the complete 16-round encryption/decryption structure.
"""

import sys

sys.path.insert(0, "src")

from born256 import (
    key_schedule,
    born_round,
    inverse_born_round,
    ROUNDS,
)


def main():

    plaintext = bytes(range(32))

    key = bytes(
        [
            0xAA if i % 2 == 0 else 0x55
            for i in range(32)
        ]
    )

    print()
    print("BORN-256 Full 16-Round Cipher Test")
    print("=" * 45)

    # --------------------------------------------------------
    # Generate round keys
    # --------------------------------------------------------

    round_keys = key_schedule(
        key,
        ROUNDS
    )

    print(
        f"Rounds                : {ROUNDS}"
    )

    print(
        f"Plaintext size        : "
        f"{len(plaintext) * 8} bits"
    )

    print(
        f"Round keys generated  : "
        f"{len(round_keys)}"
    )

    # --------------------------------------------------------
    # Encryption
    # --------------------------------------------------------

    state = plaintext

    for round_number, round_key in enumerate(
        round_keys,
        start=1
    ):

        state = born_round(
            state,
            round_key
        )

        print(
            f"Round {round_number:02d} completed"
        )

    ciphertext = state

    print()
    print(
        "Plaintext :",
        plaintext.hex()
    )

    print(
        "Ciphertext:",
        ciphertext.hex()
    )

    # --------------------------------------------------------
    # Decryption
    # --------------------------------------------------------

    state = ciphertext

    for round_number, round_key in reversed(
        list(enumerate(round_keys, start=1))
    ):

        state = inverse_born_round(
            state,
            round_key
        )

    recovered = state

    print(
        "Recovered :",
        recovered.hex()
    )

    # --------------------------------------------------------
    # Reversibility check
    # --------------------------------------------------------

    if recovered != plaintext:

        raise AssertionError(
            "Full 16-round reversibility FAILED."
        )

    print()
    print(
        "Full 16-round reversibility: PASS"
    )

    # --------------------------------------------------------
    # Ciphertext must differ from plaintext
    # --------------------------------------------------------

    if ciphertext == plaintext:

        raise AssertionError(
            "Ciphertext is identical to plaintext."
        )

    print(
        "Ciphertext differs from plaintext: PASS"
    )

    print("=" * 45)
    print(
        "BORN-256 full cipher test passed."
    )


if __name__ == "__main__":
    main()