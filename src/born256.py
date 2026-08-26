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

BLOCK_SIZE = 32
KEY_SIZE = 32
STATE_BITS = 256
ROUNDS = 16

PERMUTATION_MULTIPLIER = 5


# ============================================================
# VALIDATION
# ============================================================

def validate_block(block: bytes) -> None:
    """Validate a 256-bit block/state."""

    if not isinstance(block, bytes):
        raise TypeError("Block must be a bytes object.")

    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) block."
        )


def validate_key(key: bytes) -> None:
    """Validate a 256-bit key."""

    if not isinstance(key, bytes):
        raise TypeError("Key must be a bytes object.")

    if len(key) != KEY_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) key."
        )


def validate_bit(value: int) -> None:
    """Validate a single bit."""

    if value not in (0, 1):
        raise ValueError(
            "Boolean values must be 0 or 1."
        )


# ============================================================
# BOOLEAN GATES
# ============================================================

def and_gate(a: int, b: int) -> int:
    """AND gate."""

    validate_bit(a)
    validate_bit(b)

    return a & b


def or_gate(a: int, b: int) -> int:
    """OR gate."""

    validate_bit(a)
    validate_bit(b)

    return a | b


def not_gate(a: int) -> int:
    """NOT gate restricted to one bit."""

    validate_bit(a)

    return 1 - a


# ============================================================
# XOR USING AND / OR / NOT
# ============================================================

def xor_gate(a: int, b: int) -> int:
    """
    XOR constructed using only:

        AND
        OR
        NOT

    Formula:

        XOR(A,B) =
            (A OR B) AND NOT(A AND B)
    """

    validate_bit(a)
    validate_bit(b)

    a_or_b = or_gate(a, b)
    a_and_b = and_gate(a, b)
    not_a_and_b = not_gate(a_and_b)

    return and_gate(
        a_or_b,
        not_a_and_b
    )


# ============================================================
# BORN-T
# ============================================================

def born_t(
    a: int,
    b: int,
    c: int
) -> tuple[int, int, int]:
    """
    BORN-T reversible Boolean transformation.

        a' = a
        b' = b
        c' = c XOR (a AND b)

    XOR is constructed using AND / OR / NOT.
    """

    validate_bit(a)
    validate_bit(b)
    validate_bit(c)

    product = and_gate(a, b)

    new_c = xor_gate(
        c,
        product
    )

    return a, b, new_c


# ============================================================
# BORN-T INVERSE
# ============================================================

def inverse_born_t(
    a: int,
    b: int,
    c: int
) -> tuple[int, int, int]:
    """BORN-T is self-inverse."""

    return born_t(a, b, c)


# ============================================================
# BYTE <-> BIT CONVERSION
# ============================================================

def bytes_to_bits(data: bytes) -> list[int]:
    """
    Convert bytes to individual bits.

    Bits are ordered MSB first.
    """

    bits = []

    for byte in data:
        for bit_position in range(8):
            bit = (
                byte >> (7 - bit_position)
            ) & 1

            bits.append(bit)

    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    """
    Convert exactly 256 bits into 32 bytes.
    """

    if len(bits) != STATE_BITS:
        raise ValueError(
            "BORN-256 state must contain exactly "
            "256 bits."
        )

    result = bytearray(BLOCK_SIZE)

    for i, bit in enumerate(bits):

        validate_bit(bit)

        byte_index = i // 8
        bit_position = 7 - (i % 8)

        result[byte_index] |= (
            bit << bit_position
        )

    return bytes(result)


# ============================================================
# 256-BIT BORN-T LAYER
# ============================================================

def born_t_layer(state: bytes) -> bytes:
    """
    Apply BORN-T across the 256-bit state.

    For every bit position i:

        a = (i + 1) mod 256
        b = (i + 33) mod 256

        S[i] = S[i] XOR
               (S[a] AND S[b])

    Operations are performed sequentially.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    for i in range(STATE_BITS):

        a_index = (
            i + 1
        ) % STATE_BITS

        b_index = (
            i + 33
        ) % STATE_BITS

        a = bits[a_index]
        b = bits[b_index]
        c = bits[i]

        _, _, new_c = born_t(
            a,
            b,
            c
        )

        bits[i] = new_c

    return bits_to_bytes(bits)


# ============================================================
# INVERSE 256-BIT BORN-T LAYER
# ============================================================

def inverse_born_t_layer(
    state: bytes
) -> bytes:
    """
    Reverse the 256-bit BORN-T layer.

    Operations are executed in reverse order.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    for i in range(
        STATE_BITS - 1,
        -1,
        -1
    ):

        a_index = (
            i + 1
        ) % STATE_BITS

        b_index = (
            i + 33
        ) % STATE_BITS

        a = bits[a_index]
        b = bits[b_index]
        c = bits[i]

        _, _, original_c = inverse_born_t(
            a,
            b,
            c
        )

        bits[i] = original_c

    return bits_to_bytes(bits)


# ============================================================
# 256-BIT KEY MIXING
# ============================================================

def key_mix(
    state: bytes,
    key: bytes
) -> bytes:
    """
    Mix a 256-bit state with a 256-bit key.

        M[i] = S[i] XOR K[i]

    XOR is constructed using AND / OR / NOT.
    """

    validate_block(state)
    validate_key(key)

    state_bits = bytes_to_bits(state)
    key_bits = bytes_to_bits(key)

    mixed_bits = []

    for state_bit, key_bit in zip(
        state_bits,
        key_bits
    ):

        mixed_bit = xor_gate(
            state_bit,
            key_bit
        )

        mixed_bits.append(
            mixed_bit
        )

    return bits_to_bytes(
        mixed_bits
    )


# ============================================================
# STATE-WIDE REVERSIBLE MIXING
# ============================================================

def mix_bit(
    state: list[int],
    destination: int,
    source: int
) -> None:
    """
    Reversible operation:

        state[destination] ^= state[source]

    XOR is constructed through AND / OR / NOT.
    """

    state[destination] = xor_gate(
        state[destination],
        state[source]
    )


def state_mix(state: bytes) -> bytes:
    """
    Experimental 256-bit state-wide reversible
    diffusion layer.

    The operation sequence was previously tested
    for reversibility and avalanche behavior.

    Distances:

        1
        3
        7
        15
        31
        63
        127

    Each operation is reversible.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    distances = (
        1,
        3,
        7,
        15,
        31,
        63,
        127
    )

    for distance in distances:

        for i in range(STATE_BITS):

            source = (
                i + distance
            ) % STATE_BITS

            mix_bit(
                bits,
                i,
                source
            )

    return bits_to_bytes(bits)


# ============================================================
# INVERSE STATE-WIDE MIXING
# ============================================================

def inverse_state_mix(
    state: bytes
) -> bytes:
    """
    Exact inverse of state_mix().

    The operations are performed in reverse order.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    distances = (
        1,
        3,
        7,
        15,
        31,
        63,
        127
    )

    for distance in reversed(distances):

        for i in reversed(
            range(STATE_BITS)
        ):

            source = (
                i + distance
            ) % STATE_BITS

            mix_bit(
                bits,
                i,
                source
            )

    return bits_to_bytes(bits)


# ============================================================
# 256-BIT PERMUTATION
# ============================================================

def permute_state(
    state: bytes
) -> bytes:
    """
    Reversibly permute the 256-bit state.

        output[i] =
            input[(i * 5) mod 256]

    gcd(5,256) = 1, so the mapping is bijective.
    """

    validate_block(state)

    bits = bytes_to_bits(state)

    permuted = [0] * STATE_BITS

    for i in range(STATE_BITS):

        source_index = (
            i * PERMUTATION_MULTIPLIER
        ) % STATE_BITS

        permuted[i] = bits[
            source_index
        ]

    return bits_to_bytes(
        permuted
    )


# ============================================================
# INVERSE 256-BIT PERMUTATION
# ============================================================

def inverse_permute_state(
    state: bytes
) -> bytes:
    """Reverse the 256-bit permutation."""

    validate_block(state)

    bits = bytes_to_bits(state)

    original = [0] * STATE_BITS

    for i in range(STATE_BITS):

        source_index = (
            i * PERMUTATION_MULTIPLIER
        ) % STATE_BITS

        original[
            source_index
        ] = bits[i]

    return bits_to_bytes(
        original
    )


# ============================================================
# BORN-256 ONE ROUND
# ============================================================

def born_round(
    state: bytes,
    round_key: bytes
) -> bytes:
    """
    Apply one experimental BORN-256 round.

    Round structure:

        1. Key Mixing
        2. BORN-T Layer
        3. State-Wide Mixing
        4. Permutation
    """

    validate_block(state)
    validate_key(round_key)

    # --------------------------------------------------------
    # Step 1: Key mixing
    # --------------------------------------------------------

    state = key_mix(
        state,
        round_key
    )

    # --------------------------------------------------------
    # Step 2: Boolean transformation
    # --------------------------------------------------------

    state = born_t_layer(
        state
    )

    # --------------------------------------------------------
    # Step 3: State-wide diffusion
    # --------------------------------------------------------

    state = state_mix(
        state
    )

    # --------------------------------------------------------
    # Step 4: Permutation
    # --------------------------------------------------------

    state = permute_state(
        state
    )

    return state


# ============================================================
# INVERSE BORN-256 ONE ROUND
# ============================================================

def inverse_born_round(
    state: bytes,
    round_key: bytes
) -> bytes:
    """
    Reverse one BORN-256 round.

    Forward:

        Key Mixing
            ↓
        BORN-T Layer
            ↓
        State-Wide Mixing
            ↓
        Permutation

    Inverse:

        Inverse Permutation
            ↓
        Inverse State-Wide Mixing
            ↓
        Inverse BORN-T Layer
            ↓
        Key Mixing
    """

    validate_block(state)
    validate_key(round_key)

    # --------------------------------------------------------
    # Step 1: Reverse permutation
    # --------------------------------------------------------

    state = inverse_permute_state(
        state
    )

    # --------------------------------------------------------
    # Step 2: Reverse state-wide mixing
    # --------------------------------------------------------

    state = inverse_state_mix(
        state
    )

    # --------------------------------------------------------
    # Step 3: Reverse BORN-T
    # --------------------------------------------------------

    state = inverse_born_t_layer(
        state
    )

    # --------------------------------------------------------
    # Step 4: Reverse key mixing
    # --------------------------------------------------------

    state = key_mix(
        state,
        round_key
    )

    return state


# ============================================================
# ENCRYPTION PLACEHOLDER
# ============================================================

def encrypt_block(
    block: bytes,
    key: bytes
) -> bytes:
    """
    Full 16-round encryption is not implemented yet.

    Current development stage:

        One reversible round
        has been implemented and tested.
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 encryption "
        "is not implemented yet."
    )


# ============================================================
# DECRYPTION PLACEHOLDER
# ============================================================

def decrypt_block(
    block: bytes,
    key: bytes
) -> bytes:
    """
    Full 16-round decryption is not implemented yet.
    """

    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "Full BORN-256 decryption "
        "is not implemented yet."
    )


# ============================================================
# TEST: BORN-T
# ============================================================

def test_born_t() -> None:
    """Test every possible 3-bit input."""

    for a in (0, 1):

        for b in (0, 1):

            for c in (0, 1):

                original = (
                    a,
                    b,
                    c
                )

                transformed = born_t(
                    a,
                    b,
                    c
                )

                recovered = inverse_born_t(
                    *transformed
                )

                if recovered != original:

                    raise AssertionError(
                        f"BORN-T failed: "
                        f"{original} -> "
                        f"{transformed} -> "
                        f"{recovered}"
                    )

    print(
        "BORN-T reversibility test: PASS"
    )


# ============================================================
# TEST: 256-BIT BORN-T LAYER
# ============================================================

def test_born_t_layer() -> None:
    """Test reversibility of the 256-bit BORN-T layer."""

    test_states = [

        bytes(32),

        bytes([0xFF] * 32),

        bytes(range(32)),

        bytes(
            [
                0xAA
                if i % 2 == 0
                else 0x55
                for i in range(32)
            ]
        ),
    ]

    for original in test_states:

        transformed = born_t_layer(
            original
        )

        recovered = (
            inverse_born_t_layer(
                transformed
            )
        )

        if recovered != original:

            raise AssertionError(
                "256-bit BORN-T layer "
                "failed reversibility test."
            )

    print(
        "256-bit BORN-T reversibility test: PASS"
    )


# ============================================================
# TEST: KEY MIXING
# ============================================================

def test_key_mix() -> None:
    """Test reversibility of 256-bit key mixing."""

    test_cases = [

        (
            bytes(32),
            bytes([0xFF] * 32)
        ),

        (
            bytes([0xFF] * 32),
            bytes(32)
        ),

        (
            bytes(range(32)),
            bytes([0xAA] * 32)
        ),

        (
            bytes([0x55] * 32),
            bytes([0xAA] * 32)
        ),
    ]

    for original_state, key in test_cases:

        mixed_state = key_mix(
            original_state,
            key
        )

        recovered_state = key_mix(
            mixed_state,
            key
        )

        if recovered_state != original_state:

            raise AssertionError(
                "256-bit key mixing "
                "failed reversibility test."
            )

    print(
        "256-bit key mixing reversibility test: PASS"
    )


# ============================================================
# TEST: STATE-WIDE MIXING
# ============================================================

def test_state_mix() -> None:
    """Test reversibility of state-wide mixing."""

    test_states = [

        bytes(32),

        bytes([0xFF] * 32),

        bytes(range(32)),

        bytes(
            [
                0xAA
                if i % 2 == 0
                else 0x55
                for i in range(32)
            ]
        ),

        bytes([0x01] + [0x00] * 31),

        bytes([0x00] * 31 + [0x01]),
    ]

    for original in test_states:

        transformed = state_mix(
            original
        )

        recovered = inverse_state_mix(
            transformed
        )

        if recovered != original:

            raise AssertionError(
                "256-bit state-wide mixing "
                "failed reversibility test."
            )

    print(
        "256-bit state-wide mixing reversibility test: PASS"
    )


# ============================================================
# TEST: PERMUTATION
# ============================================================

def test_permutation() -> None:
    """Test reversibility of the permutation."""

    test_states = [

        bytes(32),

        bytes([0xFF] * 32),

        bytes(range(32)),

        bytes(
            [
                0xAA
                if i % 2 == 0
                else 0x55
                for i in range(32)
            ]
        ),
    ]

    for original in test_states:

        permuted = permute_state(
            original
        )

        recovered = (
            inverse_permute_state(
                permuted
            )
        )

        if recovered != original:

            raise AssertionError(
                "256-bit permutation "
                "failed reversibility test."
            )

    print(
        "256-bit permutation reversibility test: PASS"
    )


# ============================================================
# TEST: ONE COMPLETE ROUND
# ============================================================

def test_born_round() -> None:
    """Test that one complete BORN-256 round is reversible."""

    test_cases = [

        # Zero state
        (
            bytes(32),
            bytes([0xFF] * 32)
        ),

        # All-one state
        (
            bytes([0xFF] * 32),
            bytes(32)
        ),

        # Incrementing state
        (
            bytes(range(32)),
            bytes([0xAA] * 32)
        ),

        # Alternating state and key
        (
            bytes(
                [
                    0xAA
                    if i % 2 == 0
                    else 0x55
                    for i in range(32)
                ]
            ),
            bytes(
                [
                    0x55
                    if i % 2 == 0
                    else 0xAA
                    for i in range(32)
                ]
            )
        ),
    ]

    for original_state, round_key in test_cases:

        round_output = born_round(
            original_state,
            round_key
        )

        recovered_state = inverse_born_round(
            round_output,
            round_key
        )

        if recovered_state != original_state:

            raise AssertionError(
                "BORN-256 one-round "
                "reversibility test failed."
            )

    print(
        "BORN-256 one-round reversibility test: PASS"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "Running BORN-256 self-tests..."
    )

    print()

    test_born_t()

    test_born_t_layer()

    test_key_mix()

    test_state_mix()

    test_permutation()

    test_born_round()

    print()

    print(
        "All current BORN-256 tests passed."
    )