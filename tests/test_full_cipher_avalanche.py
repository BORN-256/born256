import sys

sys.path.insert(0, "src")

from born256 import (
    encrypt_block,
)


SAMPLES = 1000
BLOCK_SIZE = 32


def changed_bits(a, b):
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(a, b)
    )


def main():

    key = bytes([0xAA] * BLOCK_SIZE)

    minimum = BLOCK_SIZE * 8
    maximum = 0
    total = 0

    for sample in range(SAMPLES):

        plaintext = (
            sample.to_bytes(4, "big")
            + bytes(28)
        )

        modified = bytearray(plaintext)

        # Flip one input bit.
        modified[0] ^= 0x01

        modified = bytes(modified)

        ciphertext_a = encrypt_block(
            plaintext,
            key
        )

        ciphertext_b = encrypt_block(
            modified,
            key
        )

        difference = changed_bits(
            ciphertext_a,
            ciphertext_b
        )

        minimum = min(
            minimum,
            difference
        )

        maximum = max(
            maximum,
            difference
        )

        total += difference

    average = total / SAMPLES

    print()
    print("BORN-256 Full Cipher Avalanche Analysis")
    print("=" * 45)

    print(
        f"Samples               : {SAMPLES}"
    )

    print(
        f"State size             : "
        f"{BLOCK_SIZE * 8} bits"
    )

    print(
        f"Minimum changed bits  : "
        f"{minimum}"
    )

    print(
        f"Maximum changed bits  : "
        f"{maximum}"
    )

    print(
        f"Average changed bits  : "
        f"{average:.2f}"
    )

    print(
        f"Average changed       : "
        f"{average / (BLOCK_SIZE * 8) * 100:.2f}%"
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
        "This result is an experimental "
        "diffusion measurement."
    )

    print(
        "It does NOT establish cryptographic security."
    )


if __name__ == "__main__":
    main()