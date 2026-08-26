import sys

sys.path.insert(0, "src")

from born256 import encrypt_block


SAMPLES = 1000

KEY = bytes([0xAA] * 32)


def main():

    seen = set()
    collisions = 0

    for i in range(SAMPLES):

        plaintext = (
            i.to_bytes(4, "big")
            + bytes(28)
        )

        ciphertext = encrypt_block(
            plaintext,
            KEY
        )

        if ciphertext in seen:
            collisions += 1
        else:
            seen.add(ciphertext)

    print()
    print("BORN-256 Collision Experiment")
    print("=" * 40)

    print(
        f"Samples              : {SAMPLES}"
    )

    print(
        f"Unique ciphertexts   : {len(seen)}"
    )

    print(
        f"Collisions           : {collisions}"
    )

    print("=" * 40)

    if collisions == 0:
        print("Collision result: PASS")
    else:
        print("Collision result: REVIEW")

    print()
    print(
        "NOTE: This experiment does NOT prove "
        "collision resistance."
    )


if __name__ == "__main__":
    main()