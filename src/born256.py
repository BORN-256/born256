"""
BORN-256 v0.1
Experimental Cryptographic Research Construction

This implementation is experimental.
It must NOT be used to protect real-world sensitive information.
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
    if not isinstance(block, bytes):
        raise TypeError("Block must be a bytes object.")

    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) block."
        )


def validate_key(key: bytes) -> None:
    if not isinstance(key, bytes):
        raise TypeError("Key must be a bytes object.")

    if len(key) != KEY_SIZE:
        raise ValueError(
            "BORN-256 requires a 256-bit (32-byte) key."
        )


def validate_bit(value: int) -> None:
    if value not in (0, 1):
        raise ValueError(
            "Boolean values must be 0 or 1."
        )


# ============================================================
# BOOLEAN GATES
# ============================================================

def and_gate(a: int, b: int) -> int:
    validate_bit(a)
    validate_bit(b)
    return a & b


def or_gate(a: int, b: int) -> int:
    validate_bit(a)
    validate_bit(b)
    return a | b


def not_gate(a: int) -> int:
    validate_bit(a)
    return 1 - a


def xor_gate(a: int, b: int) -> int:
    validate_bit(a)
    validate_bit(b)

    a_or_b = or_gate(a, b)
    a_and_b = and_gate(a, b)

    return and_gate(
        a_or_b,
        not_gate(a_and_b)
    )


# ============================================================
# BORN-T
# ============================================================

def born_t(
    a: int,
    b: int,
    c: int
) -> tuple[int, int, int]:

    validate_bit(a)
    validate_bit(b)
    validate_bit(c)

    product = and_gate(a, b)

    new_c = xor_gate(
        c,
        product
    )

    return a, b, new_c


def inverse_born_t(
    a: int,
    b: int,
    c: int
) -> tuple[int, int, int]:

    return born_t(a, b, c)


# ============================================================
# BYTE / BIT CONVERSION
# ============================================================

def bytes_to_bits(data: bytes) -> list[int]:

    bits = []

    for byte in data:

        for bit_position in range(8):

            bit = (
                byte >> (7 - bit_position)
            ) & 1

            bits.append(bit)

    return bits


def bits_to_bytes(
    bits: list[int]
) -> bytes:

    if len(bits) != STATE_BITS:
        raise ValueError(
            "BORN-256 state must contain exactly 256 bits."
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

def born_t_layer(
    state: bytes
) -> bytes:

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
# INVERSE BORN-T LAYER
# ============================================================

def inverse_born_t_layer(
    state: bytes
) -> bytes:

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
# KEY MIXING
# ============================================================

def key_mix(
    state: bytes,
    key: bytes
) -> bytes:

    validate_block(state)
    validate_key(key)

    state_bits = bytes_to_bits(state)
    key_bits = bytes_to_bits(key)

    mixed_bits = []

    for state_bit, key_bit in zip(
        state_bits,
        key_bits
    ):

        mixed_bits.append(
            xor_gate(
                state_bit,
                key_bit
            )
        )

    return bits_to_bytes(
        mixed_bits
    )


# ============================================================
# STATE-WIDE MIXING
# ============================================================

def mix_bit(
    state: list[int],
    destination: int,
    source: int
) -> None:

    state[destination] = xor_gate(
        state[destination],
        state[source]
    )


def state_mix(
    state: bytes
) -> bytes:

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
# PERMUTATION
# ============================================================

def permute_state(
    state: bytes
) -> bytes:

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
# INVERSE PERMUTATION
# ============================================================

def inverse_permute_state(
    state: bytes
) -> bytes:

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
# BORN-256 KEY SCHEDULE
# ============================================================

def key_schedule(
    master_key: bytes,
    rounds: int = ROUNDS
) -> list[bytes]:

    validate_key(master_key)

    if rounds <= 0:
        raise ValueError(
            "Number of rounds must be positive."
        )

    keys = []

    current = master_key

    for round_number in range(rounds):

        rotation = (
            (round_number + 1) * 7
        ) % STATE_BITS

        bits = bytes_to_bits(
            current
        )

        rotated = (
            bits[rotation:]
            + bits[:rotation]
        )

        current = bits_to_bytes(
            rotated
        )

        current = born_t_layer(
            current
        )

        constant = (
            (round_number + 1)
            * 0x9E3779B1
        ) & 0xFFFFFFFF

        constant_bytes = (
            constant.to_bytes(
                4,
                "big"
            ) * 8
        )

        current = key_mix(
            current,
            constant_bytes
        )

        keys.append(current)

    return keys


# ============================================================
# INVERSE KEY SCHEDULE
# ============================================================

def inverse_key_schedule(
    round_keys: list[bytes]
) -> bytes:

    if not round_keys:
        raise ValueError(
            "Round-key list cannot be empty."
        )

    current = round_keys[-1]

    for round_number in reversed(
        range(len(round_keys))
    ):

        constant = (
            (round_number + 1)
            * 0x9E3779B1
        ) & 0xFFFFFFFF

        constant_bytes = (
            constant.to_bytes(
                4,
                "big"
            ) * 8
        )

        current = key_mix(
            current,
            constant_bytes
        )

        current = inverse_born_t_layer(
            current
        )

        rotation = (
            (round_number + 1) * 7
        ) % STATE_BITS

        bits = bytes_to_bits(
            current
        )

        if rotation:

            bits = (
                bits[-rotation:]
                + bits[:-rotation]
            )

        current = bits_to_bytes(
            bits
        )

    return current


# ============================================================
# ONE BORN-256 ROUND
# ============================================================

def born_round(
    state: bytes,
    round_key: bytes
) -> bytes:

    validate_block(state)
    validate_key(round_key)

    state = key_mix(
        state,
        round_key
    )

    state = born_t_layer(
        state
    )

    state = state_mix(
        state
    )

    state = permute_state(
        state
    )

    return state


# ============================================================
# INVERSE ONE BORN-256 ROUND
# ============================================================

def inverse_born_round(
    state: bytes,
    round_key: bytes
) -> bytes:

    validate_block(state)
    validate_key(round_key)

    state = inverse_permute_state(
        state
    )

    state = inverse_state_mix(
        state
    )

    state = inverse_born_t_layer(
        state
    )

    state = key_mix(
        state,
        round_key
    )

    return state


# ============================================================
# FULL 16-ROUND ENCRYPTION
# ============================================================

def encrypt_block(
    block: bytes,
    key: bytes
) -> bytes:

    validate_block(block)
    validate_key(key)

    round_keys = key_schedule(
        key,
        ROUNDS
    )

    state = block

    for round_key in round_keys:

        state = born_round(
            state,
            round_key
        )

    return state


# ============================================================
# FULL 16-ROUND DECRYPTION
# ============================================================

def decrypt_block(
    block: bytes,
    key: bytes
) -> bytes:

    validate_block(block)
    validate_key(key)

    round_keys = key_schedule(
        key,
        ROUNDS
    )

    state = block

    for round_key in reversed(
        round_keys
    ):

        state = inverse_born_round(
            state,
            round_key
        )

    return state


# ============================================================
# SELF-TEST: BORN-T
# ============================================================

def test_born_t() -> None:

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
                        "BORN-T reversibility failed."
                    )

    print(
        "BORN-T reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: 256-BIT BORN-T
# ============================================================

def test_born_t_layer() -> None:

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

        recovered = inverse_born_t_layer(
            transformed
        )

        if recovered != original:

            raise AssertionError(
                "256-bit BORN-T reversibility failed."
            )

    print(
        "256-bit BORN-T reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: KEY MIXING
# ============================================================

def test_key_mix() -> None:

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
                "256-bit key mixing reversibility failed."
            )

    print(
        "256-bit key mixing reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: STATE-WIDE MIXING
# ============================================================

def test_state_mix() -> None:

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
                "256-bit state-wide mixing reversibility failed."
            )

    print(
        "256-bit state-wide mixing reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: PERMUTATION
# ============================================================

def test_permutation() -> None:

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

        recovered = inverse_permute_state(
            permuted
        )

        if recovered != original:

            raise AssertionError(
                "256-bit permutation reversibility failed."
            )

    print(
        "256-bit permutation reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: KEY SCHEDULE
# ============================================================

def test_key_schedule() -> None:

    master_key = bytes(
        range(KEY_SIZE)
    )

    round_keys = key_schedule(
        master_key,
        ROUNDS
    )

    if len(round_keys) != ROUNDS:

        raise AssertionError(
            "Incorrect number of round keys."
        )

    for round_key in round_keys:

        if len(round_key) != KEY_SIZE:

            raise AssertionError(
                "Invalid round-key size."
            )

    if len(set(round_keys)) != ROUNDS:

        raise AssertionError(
            "Duplicate round keys detected."
        )

    recovered_key = inverse_key_schedule(
        round_keys
    )

    if recovered_key != master_key:

        raise AssertionError(
            "Key schedule reversibility failed."
        )

    print(
        "BORN-256 key schedule test: PASS"
    )


# ============================================================
# SELF-TEST: ONE ROUND
# ============================================================

def test_born_round() -> None:

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

        output = born_round(
            original_state,
            round_key
        )

        recovered = inverse_born_round(
            output,
            round_key
        )

        if recovered != original_state:

            raise AssertionError(
                "BORN-256 one-round reversibility failed."
            )

    print(
        "BORN-256 one-round reversibility test: PASS"
    )


# ============================================================
# SELF-TEST: FULL CIPHER
# ============================================================

def test_full_cipher() -> None:

    plaintext = bytes(range(32))

    key = bytes(
        [
            0xAA
            if i % 2 == 0
            else 0x55
            for i in range(32)
        ]
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

        raise AssertionError(
            "Full BORN-256 reversibility failed."
        )

    if ciphertext == plaintext:

        raise AssertionError(
            "Ciphertext is identical to plaintext."
        )

    print(
        "BORN-256 full cipher reversibility test: PASS"
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

    test_key_schedule()

    test_born_round()

    test_full_cipher()

    print()

    print(
        "All current BORN-256 tests passed."
    )