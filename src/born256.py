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
STATE_BITS = 256
ROUNDS = 16


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

    XOR is not used as a primitive gate here.
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

    XOR is implemented using:
        AND
        OR
        NOT

    BORN-T is self-inverse.
    """

    validate_bit(a)
    validate_bit(b)
    validate_bit(c)

    product = and_gate(a, b)
    new_c = xor_gate(c, product)

    return a, b, new_c


# ============================================================
# BORN-T INVERSE
# ============================================================

def inverse_born_t(
    a: int,
    b: int,
    c: int
) -> tuple[int, int, int]:
    """
    Inverse of BORN-T.

    BORN-T is self-inverse, so the same operation
    performs the inverse transformation.
    """
    return born_t(a, b, c)


# ============================================================
# BYTE <-> BIT CONVERSION
# ============================================================

def bytes_to_bits(data: bytes) -> list[int]:
    """
    Convert bytes into a list of individual bits.

    Example:

        0b10100001

    becomes:

        [1, 0, 1, 0, 0, 0, 0, 1]
    """

    bits = []

    for byte in data:
        for bit_position in range(8):
            bit = (byte >> (7 - bit_position)) & 1
            bits.append(bit)

    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    """
    Convert a list of 256 bits back into 32 bytes.
    """

    if len(bits) != STATE_BITS:
        raise ValueError(
            "BORN-256 state must contain exactly 256 bits."
        )

    result = bytearray(BLOCK_SIZE)

    for i, bit in enumerate(bits):
        validate_bit(bit)

        byte_index = i // 8
        bit_position = 7 - (i % 8)

        result[byte_index] |= bit << bit_position

    return bytes(result)


# ============================================================
# 256-BIT BORN-T LAYER
# ============================================================

def born_t_layer(state: bytes) -> bytes:
    """
    Apply the BORN-T transformation to a 256-bit state.

    The state contains exactly 32 bytes (256 bits).

    For each bit position i:

        a = (i + 1) mod 256
        b = (i + 33) mod 256
        target = i

        S[i] = S[i] XOR (S[a] AND S[b])

    The transformation is performed sequentially.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    for i in range(STATE_BITS):
        a_index = (i + 1) % STATE_BITS
        b_index = (i + 33) % STATE_BITS

        a = bits[a_index]
        b = bits[b_index]
        c = bits[i]

        _, _, new_c = born_t(a, b, c)

        bits[i] = new_c

    return bits_to_bytes(bits)


# ============================================================
# INVERSE 256-BIT BORN-T LAYER
# ============================================================

def inverse_born_t_layer(state: bytes) -> bytes:
    """
    Inverse of the 256-bit BORN-T layer.

    Because individual BORN-T operations are self-inverse,
    the complete sequential layer is reversed by applying
    the operations in reverse order.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    for i in range(STATE_BITS - 1, -1, -1):
        a_index = (i + 1) % STATE_BITS
        b_index = (i + 33) % STATE_BITS

        a = bits[a_index]
        b = bits[b_index]
        c = bits[i]

        _, _, original_c = inverse_born_t(a, b, c)

        bits[i] = original_c

    return bits_to_bytes(bits)


# ============================================================
# ENCRYPTION PLACEHOLDER
# ============================================================

def encrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Encrypt one 256-bit block.

    Full encryption will be implemented only after
    the individual reversible components are tested.

    Planned components:

        1. Key mixing
        2. BORN-T layer
        3. Permutation
        4. 16 rounds
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 encryption is not implemented yet."
    )


# ============================================================
# DECRYPTION PLACEHOLDER
# ============================================================

def decrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Decrypt one 256-bit block.

    Full decryption will be implemented after the
    encryption components are verified.
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 decryption is not implemented yet."
    )


# ============================================================
# TEST: BORN-T
# ============================================================

def test_born_t() -> None:
    """
    Test all possible 3-bit inputs.
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
# TEST: 256-BIT BORN-T LAYER
# ============================================================

def test_born_t_layer() -> None:
    """
    Test that the complete 256-bit BORN-T layer
    is reversible.
    """

    test_states = [
        bytes(32),

        bytes([0xFF] * 32),

        bytes(range(32)),

        bytes(
            [
                0xAA if i % 2 == 0 else 0x55
                for i in range(32)
            ]
        ),
    ]

    for original in test_states:

        transformed = born_t_layer(original)

        recovered = inverse_born_t_layer(transformed)

        if recovered != original:
            raise AssertionError(
                "256-bit BORN-T layer failed "
                "reversibility test."
            )

    print("256-bit BORN-T reversibility test: PASS")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("Running BORN-256 self-tests...")
    print()

    test_born_t()
    test_born_t_layer()

    print()
    print("All current BORN-256 tests passed.")
