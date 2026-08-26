import sys

sys.path.insert(0, "src")

from born256 import encrypt_block, decrypt_block


SAMPLES = 1000


def main():

    failures = 0

    for i in range(SAMPLES):

        plaintext = (
            i.to_bytes(4, "big")
            + bytes(28)
        )

        key = (
            ((i * 0x9E3779B1) & 0xFFFFFFFF)
            .to_bytes(4, "big")
            + bytes(28)
        )

        ciphertext = encrypt_block(
            plaintext,
            key
        )

        recovered = decrypt_block(
            ciphertext,
            key
        )

        if recovered != plaintext:
            failures += 1

    print()
    print("BORN-256 Full Consistency Test")
    print("=" * 45)

    print(
        f"Samples              : {SAMPLES}"
    )

    print(
        f"Failures             : {failures}"
    )

    print("=" * 45)

    if failures == 0:
        print("Full consistency result: PASS")
    else:
        print("Full consistency result: FAIL")


if __name__ == "__main__":
    main()