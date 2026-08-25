"""
BORN-256 v0.1
Experimental Cryptographic Research Construction

Reference implementation under development.

This implementation is experimental and must NOT be used
to protect real-world sensitive information.
"""


# ============================================================
# BORN-256 PARAMETERS
# ============================================================

BLOCK_SIZE = 32       # 256 bits = 32 bytes
KEY_SIZE = 32         # 256 bits = 32 bytes
ROUNDS = 16           # Initial research parameter


# ============================================================
# VALIDATION
# ============================================================

def validate_block(block: bytes) -> None:
    """
    Validate that the input block is exactly 256 bits.
    """
    if not isinstance(block, bytes):
        raise TypeError("Block must be a bytes object.")

    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) block."
        )


def validate_key(key: bytes) -> None:
    """
    Validate that the key is exactly 256 bits.
    """
    if not isinstance(key, bytes):
        raise TypeError("Key must be a bytes object.")

    if len(key) != KEY_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) key."
        )


def validate_bit(value: int) -> None:
    """
    Validate that a value represents a single bit.
    """
    if value not in (0, 1):
        raise ValueError("Boolean values must be 0 or 1.")


# ============================================================
# BOOLEAN GATES
# ============================================================

def and_gate(a: int, b: int) -> int:
    """
    AND gate.
    """
    validate_bit(a)
    validate_bit(b)

    return a & b


def or_gate(a: int, b: int) -> int:
    """
    OR gate.
    """
    validate_bit(a)
    validate_bit(b)

    return a | b


def not_gate(a: int) -> int:
    """
    NOT gate.

    The result is restricted to a single bit.
    """
    validate_bit(a)

    return 1 - a


# ============================================================
# XOR CONSTRUCTED FROM AND / OR / NOT
# ============================================================

def xor_gate(a: int, b: int) -> int:
    """
    XOR constructed entirely from AND, OR, and NOT.

    XOR(A, B) =
        (A OR B) AND NOT(A AND B)

    XOR is NOT used as a primitive gate here.
    """
    validate_bit(a)
    validate_bit(b)

    a_or_b = or_gate(a, b)
    a_and_b = and_gate(a, b)
    not_a_and_b = not_gate(a_and_b)

    return and_gate(a_or_b, not_a_and_b)


# ============================================================
# BORN-T REVERSIBLE BOOLEAN TRANSFORMATION
# ============================================================

def born_t(a: int, b: int, c: int) -> tuple[int, int, int]:
    """
    BORN-T reversible Boolean transformation.

    Input:
        (a, b, c)

    Transformation:

        a' = a
        b' = b
        c' = c XOR (a AND b)

    XOR itself is implemented using only:
        AND
        OR
        NOT

    BORN-T is self-inverse:

        BORN-T(BORN-T(a, b, c)) = (a, b, c)
    """

    validate_bit(a)
    validate_bit(b)
    validate_bit(c)

    # AND operation
    product = and_gate(a, b)

    # XOR(c, product)
    new_c = xor_gate(c, product)

    return a, b, new_c


# ============================================================
# BORN-T INVERSE
# ============================================================

def inverse_born_t(a: int, b: int, c: int) -> tuple[int, int, int]:
    """
    Inverse of BORN-T.

    BORN-T is self-inverse, so the same operation
    performs the inverse transformation.
    """
    return born_t(a, b, c)


# ============================================================
# BLOCK / KEY PLACEHOLDERS
# ============================================================

def encrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Encrypt one 256-bit block.

    The complete BORN-256 encryption function will be
    implemented after the following components are
    individually tested:

        1. BORN-T transformation
        2. 256-bit state representation
        3. Key mixing
        4. Key schedule
        5. Permutation
        6. Complete round function
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 encryption is not implemented yet."
    )


def decrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Decrypt one 256-bit block.

    The complete decryption function will be implemented
    after the reversible encryption components are tested.
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 decryption is not implemented yet."
    )


# ============================================================
# BASIC SELF-TEST
# ============================================================

def test_born_t() -> None:
    """
    Verify that BORN-T is reversible for all possible
    three-bit input combinations.
    """

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):

                original = (a, b, c)

                transformed = born_t(a, b, c)

                recovered = inverse_born_t(*transformed)

                if recovered != original:
                    raise AssertionError(
                        f"BORN-T failed: "
                        f"{original} -> "
                        f"{transformed} -> "
                        f"{recovered}"
                    )

    print("BORN-T reversibility test: PASS")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    test_born_t()
