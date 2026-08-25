# BORN-256 v0.1 Specification

## Status

Experimental cryptographic research prototype.

## Overview

BORN-256 is an open-source research project exploring
Boolean-gate-based symmetric cryptographic constructions.

The design investigates the use of AND, OR, and NOT
operations within a multi-round 256-bit transformation.

## Design Parameters

- Block size: 256 bits
- Key size: 256 bits
- Encryption rounds: To be finalized
- Boolean operations: AND, OR, NOT
- Cipher type: Symmetric
- Status: Experimental

## Encryption Architecture

Plaintext
    ↓
256-bit block
    ↓
Key schedule
    ↓
Boolean transformation
    ↓
Permutation
    ↓
Multiple rounds
    ↓
Ciphertext

## Security Status

BORN-256 v0.1 is a research prototype.

No claim of cryptographic security or post-quantum
security is made at this stage.

The construction requires further cryptanalysis,
testing, and independent review.
