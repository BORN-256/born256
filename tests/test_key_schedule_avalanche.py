import sys

sys.path.insert(0, "src")

from born256 import key_schedule, ROUNDS


SAMPLES = 1000
KEY_SIZE = 32
STATE_BITS = 256


def changed_bits(a, b):
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(a, b)
    )


def main():

    minimum = STATE_BITS
    maximum = 0
    total = 0
    count = 0

    for sample in range(SAMPLES):

        key = (
            sample.to_bytes(4, "big")
            + bytes(28)
        )

        modified = bytearray(key)

        # Flip one bit of the master key.
        modified[0] ^= 0x01

        modified = bytes(modified)

        keys_a = key_schedule(
            key,
            ROUNDS
        )

        keys_b = key_schedule(
            modified,
            ROUNDS
        )

        for round_key_a, round_key_b in zip(
            keys_a,
            keys_b
        ):

            difference = changed_bits(
                round_key_a,
                round_key_b
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
            count += 1

    average = total / count

    print()
    print("BORN-256 Key Schedule Avalanche Analysis")
    print("=" * 45)

    print(
        f"Samples               : {SAMPLES}"
    )

    print(
        f"Rounds                : {ROUNDS}"
    )

    print(
        f"Key size               : {STATE_BITS} bits"
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