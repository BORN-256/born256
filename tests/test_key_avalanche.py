import sys

sys.path.insert(0, "src")

from born256 import encrypt_block


SAMPLES = 1000
STATE_BITS = 256

PLAINTEXT = bytes(range(32))
KEY = bytes([0xAA] * 32)


def changed_bits(a, b):
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(a, b)
    )


def main():

    minimum = STATE_BITS
    maximum = 0
    total = 0

    ciphertext = encrypt_block(
        PLAINTEXT,
        KEY
    )

    for i in range(SAMPLES):

        modified_key = bytearray(KEY)

        # Change one key bit.
        bit_index = i % STATE_BITS

        byte_index = bit_index // 8
        bit_position = 7 - (bit_index % 8)

        modified_key[byte_index] ^= (
            1 << bit_position
        )

        modified_key = bytes(modified_key)

        modified_ciphertext = encrypt_block(
            PLAINTEXT,
            modified_key
        )

        difference = changed_bits(
            ciphertext,
            modified_ciphertext
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
    print("BORN-256 Key Avalanche Analysis")
    print("=" * 45)

    print(
        f"Samples               : {SAMPLES}"
    )

    print(
        f"State size             : {STATE_BITS} bits"
    )

    print(
        f"Minimum changed bits  : {minimum}"
    )

    print(
        f"Maximum changed bits  : {maximum}"
    )

    print(
        f"Average changed bits  : {average:.2f}"
    )

    print(
        f"Average changed       : "
        f"{average / STATE_BITS * 100:.2f}%"
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
        "This is an experimental diffusion measurement."
    )

    print(
        "It does NOT establish cryptographic security."
    )


if __name__ == "__main__":
    main()