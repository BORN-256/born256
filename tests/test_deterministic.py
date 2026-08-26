import sys

sys.path.insert(0, "src")

from born256 import encrypt_block


SAMPLES = 1000

KEY = bytes([0xAA] * 32)


def main():

    failures = 0

    for i in range(SAMPLES):

        plaintext = (
            i.to_bytes(4, "big")
            + bytes(28)
        )

        ciphertext_a = encrypt_block(
            plaintext,
            KEY
        )

        ciphertext_b = encrypt_block(
            plaintext,
            KEY
        )

        if ciphertext_a != ciphertext_b:
            failures += 1

    print()
    print("BORN-256 Deterministic Encryption Test")
    print("=" * 45)

    print(
        f"Samples              : {SAMPLES}"
    )

    print(
        f"Failures             : {failures}"
    )

    print("=" * 45)

    if failures == 0:
        print("Deterministic result: PASS")
    else:
        print("Deterministic result: FAIL")


if __name__ == "__main__":
    main()