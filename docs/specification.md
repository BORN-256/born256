# BORN-256 v0.1 Specification

## Status

**Experimental Cryptographic Research Construction**

BORN-256 is an open-source research project exploring the
use of Boolean-gate-based transformations in symmetric
cryptographic constructions.

This document defines the initial BORN-256 v0.1 architecture.
The construction is experimental and may change as security
analysis and cryptanalysis are performed.

---

# 1. Overview

BORN-256 is a proposed 256-bit symmetric cryptographic
construction based on Boolean logic operations.

The primary research focus is the use of:

- AND
- OR
- NOT

within a multi-round transformation network.

The design combines Boolean transformations with:

- Secret-key mixing
- Round-key derivation
- Permutation
- Diffusion
- Multiple encryption rounds

The purpose of the project is to investigate whether a
Boolean-gate-oriented construction can provide useful
cryptographic properties when combined with appropriate
key mixing and diffusion mechanisms.

BORN-256 is intended as an experimental research project
and is not currently intended for protecting real-world
sensitive information.

---

# 2. Design Parameters

| Parameter | BORN-256 v0.1 |
|---|---|
| Cipher type | Symmetric |
| Block size | 256 bits |
| Block size | 32 bytes |
| Master key size | 256 bits |
| Master key | 32 bytes |
| Number of rounds | 16 |
| Primary Boolean operations | AND, OR, NOT |
| Output representation | Hexadecimal |
| Current status | Experimental |
| Security status | Not formally established |

---

# 3. Encryption Architecture

BORN-256 operates on 256-bit blocks using a 256-bit
master key.

The encryption process is divided into multiple rounds.

Each round consists conceptually of:

1. Round-key derivation
2. Key mixing
3. Boolean transformation
4. Permutation and diffusion

The exact mathematical definition of each component is
subject to cryptographic analysis and may be refined in
future versions.

---

# 4. High-Level Encryption Flow

```text
                         ┌──────────────────────┐
                         │      PLAINTEXT       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   UTF-8 ENCODING     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   256-BIT BLOCK      │
                         │      (32 BYTES)      │
                         └──────────┬───────────┘
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │              ROUND 1                    │
              │                                         │
              │  Round-Key Derivation                   │
              │            ↓                            │
              │  Key Mixing                             │
              │            ↓                            │
              │  AND / OR / NOT Transformation          │
              │            ↓                            │
              │  Permutation / Diffusion                │
              └──────────────────┬──────────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────────┐
              │              ROUND 2                    │
              │                                         │
              │  Round-Key Derivation                   │
              │            ↓                            │
              │  Key Mixing                             │
              │            ↓                            │
              │  AND / OR / NOT Transformation          │
              │            ↓                            │
              │  Permutation / Diffusion                │
              └──────────────────┬──────────────────────┘
                                 │
                                 ▼
                                ...
                                 │
                                 ▼
              ┌─────────────────────────────────────────┐
              │             ROUND 16                    │
              │                                         │
              │  Round-Key Derivation                   │
              │            ↓                            │
              │  Key Mixing                             │
              │            ↓                            │
              │  AND / OR / NOT Transformation          │
              │            ↓                            │
              │  Permutation / Diffusion                │
              └──────────────────┬──────────────────────┘
                                 │
                                 ▼
                         ┌──────────────────────┐
                         │      CIPHERTEXT      │
                         │     256-BIT BLOCK    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  HEX ENCODED OUTPUT  │
                         └──────────────────────┘
