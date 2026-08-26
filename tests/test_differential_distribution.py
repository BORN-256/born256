import sys
from collections import Counter

sys.path.insert(0, "src")

from born256 import encrypt_block


SAMPLES = 1000

KEY = bytes([0xAA] * 32)


def xor_bytes(a, b):
    return bytes(
        x ^ y
        for x, y in zip(a, b)
    )


def main():

    plaintext_difference = bytes(
        [0x01] + [0x00] * 31
    )

    counter = Counter()

    for i in range(SAMPLES):

        plaintext = (
            i.to_bytes(4, "big")
            + bytes(28)
        )

        modified = xor_bytes(
            plaintext,
            plaintext_difference
        )

        ciphertext_a = encrypt_block(
            plaintext,
            KEY
        )

        ciphertext_b = encrypt_block(
            modified,
            KEY
        )

        output_difference = xor_bytes(
            ciphertext_a,
            ciphertext_b
        )

        counter[output_difference] += 1

    frequencies = list(
        counter.values()
    )

    maximum = max(frequencies)
    unique = len(counter)

    print()
    print(
        "BORN-256 Differential Distribution Experiment"
    )
    print("=" * 50)

    print(
        f"Samples                 : {SAMPLES}"
    )

    print(
        f"Unique output differences: {unique}"
    )

    print(
        f"Maximum frequency       : {maximum}"
    )

    print(
        f"Maximum probability     : "
        f"{maximum / SAMPLES * 100:.4f}%"
    )

    print("=" * 50)

    print()
    print(
        "This measures output-difference distribution."
    )

    print(
        "It does NOT establish resistance to "
        "differential cryptanalysis."
    )


if __name__ == "__main__":
    main()