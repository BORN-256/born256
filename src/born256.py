"""
BORN-256 v0.1
Experimental Cryptographic Research Construction

Reference implementation under development.

This implementation is experimental and must not be used
to protect real-world sensitive information.
"""


BLOCK_SIZE = 32       # 256 bits = 32 bytes
KEY_SIZE = 32         # 256 bits = 32 bytes
ROUNDS = 16


def validate_block(block: bytes) -> None:
    """Validate that the input block is exactly 256 bits."""
    if len(block) != BLOCK_SIZE:
        raise ValueError("BORN-256 requires a 256-bit (32-byte) block.")


def validate_key(key: bytes) -> None:
    """Validate that the key is exactly 256 bits."""
    if len(key) != KEY_SIZE:
        raise ValueError("BORN-256 requires a 256-bit (32-byte) key.")


def encrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Encrypt one 256-bit block.

    Implementation will be added after the individual
    reversible components are tested.
    """
    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "BORN-256 encryption is not implemented yet."
    )


def decrypt_block(block: bytes, key: bytes) -> bytes:
    """
    Decrypt one 256-bit block.

    Implementation will be added after the individual
    reversible components are tested.
    """
    validate_block(block)
    validate_key(key)

    raise NotImplementedError(
        "BORN-256 decryption is not implemented yet."
    )
