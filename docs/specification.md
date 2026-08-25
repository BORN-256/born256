## Encryption Architecture

BORN-256 operates on 256-bit (32-byte) blocks using a
256-bit master key.

The encryption process consists of 16 rounds.

Each round contains:

1. Round-key generation
2. Key mixing
3. Boolean transformation
4. Permutation/diffusion

### High-Level Flow

Plaintext
    ↓
UTF-8 Encoding
    ↓
256-bit Block
    ↓
Round 1
    ├── Key Mixing
    ├── Boolean Transformation
    └── Permutation
    ↓
Round 2
    ├── Key Mixing
    ├── Boolean Transformation
    └── Permutation
    ↓
...
    ↓
Round 16
    ├── Key Mixing
    ├── Boolean Transformation
    └── Permutation
    ↓
Ciphertext
    ↓
Hexadecimal Output

## Boolean Operations

The core design investigates the use of:

- AND
- OR
- NOT

XOR may be constructed from these operations:

XOR(A,B) = (A OR B) AND NOT(A AND B)

The project will evaluate whether these Boolean
transformations provide sufficient confusion and
diffusion when combined with key mixing and permutation.

## Design Goals

The construction will be evaluated for:

- Avalanche effect
- Diffusion
- Confusion
- Key sensitivity
- Plaintext sensitivity
- Statistical properties
- Differential characteristics
- Resistance to known cryptanalytic techniques

## Security Status

BORN-256 is an experimental research construction.

No claim of cryptographic security or post-quantum
security is made at this stage.
