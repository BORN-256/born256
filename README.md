# BORN-256

> An experimental 256-bit reversible block cipher exploring custom transformations, diffusion, permutation, and multi-round key mixing.

BORN-256 is an experimental cryptographic block cipher research project.

The project explores a custom reversible design combining:

- BORN-T transformations
- State-wide mixing
- Permutation
- Key mixing
- Multi-round key scheduling
- 256-bit state processing

> ⚠️ **SECURITY WARNING**
>
> BORN-256 is an experimental research and educational construction.
> It has not been independently cryptanalyzed, formally proven secure,
> or professionally audited.
>
> **Do not use BORN-256 to protect production systems or sensitive data.**

---

## Current Status

**Experimental / Research**

The current implementation provides:

- 256-bit block size
- 256-bit key size
- 256-bit internal state
- 16-round cipher
- BORN-T transformation
- State-wide diffusion layer
- Permutation layer
- Key mixing
- 256-bit round-key schedule
- Encryption
- Decryption
- Reversible round transformations
- Full cipher reversibility
- Avalanche analysis
- Key avalanche analysis
- Differential analysis
- Differential distribution experiments
- Collision experiments
- Deterministic encryption testing
- Full consistency testing

---

## BORN-256 Structure

BORN-256 uses a 16-round experimental structure.

Each round applies several reversible transformations to the
256-bit state.

```text
                    256-bit Plaintext
                           │
                           ▼
                  ┌─────────────────┐
                  │    16 Rounds    │
                  └────────┬────────┘
                           │
             ┌─────────────▼─────────────┐
             │         Each Round        │
             │                           │
             │  ┌─────────────────────┐  │
             │  │    Key Mixing       │  │
             │  └──────────┬──────────┘  │
             │             ▼             │
             │  ┌─────────────────────┐  │
             │  │     BORN-T Layer    │  │
             │  └──────────┬──────────┘  │
             │             ▼             │
             │  ┌─────────────────────┐  │
             │  │  State-Wide Mixing  │  │
             │  └──────────┬──────────┘  │
             │             ▼             │
             │  ┌─────────────────────┐  │
             │  │  Permutation Layer  │  │
             │  └─────────────────────┘  │
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  256-bit Ciphertext

Key Schedule

The master key is 256 bits.

The experimental key schedule generates one 256-bit round key for
each of the 16 rounds.
                  256-bit Master Key
                          │
                          ▼
                  ┌───────────────┐
                  │ Key Schedule  │
                  └───────┬───────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
         Round 1       Round 2       ... Round 16
        256-bit key   256-bit key       256-bit key

The key schedule also includes diffusion, permutation, nonlinear
transformation, rotation, and round-dependent constants.


Parameters
| Parameter        |        Value |
| ---------------- | -----------: |
| Block size       |     256 bits |
| Key size         |     256 bits |
| Internal state   |     256 bits |
| Number of rounds |           16 |
| Round key size   |     256 bits |
| Implementation   |       Python |
| Project status   | Experimental |


Experimental Results

The following results were obtained from the current test suite.

Full Cipher Avalanche

A single-bit plaintext change was tested across 1000 samples.

Samples               : 1000
Minimum changed bits  : 104
Maximum changed bits  : 148
Average changed bits  : 127.91 / 256
Average changed       : 49.97%

The measured average is close to the approximately 50% reference
used for avalanche measurements.


Key Avalanche

A single key-bit change was tested across 1000 samples.

Samples               : 1000
Minimum changed bits  : 109
Maximum changed bits  : 147
Average changed bits  : 128.62 / 256
Average changed       : 50.24%

This indicates strong experimental sensitivity to single-bit
key changes under the tested conditions.


Differential Analysis

Samples               : 1000
Minimum output diff   : 105 bits
Maximum output diff   : 149 bits
Average output diff   : 128.59 / 256
Average percentage    : 50.23%

This experiment measures the diffusion of arbitrary input
differences.


Differential Distribution

Samples                  : 1000
Unique output differences: 1000
Maximum frequency        : 1
Maximum probability      : 0.1000%

Every tested input difference produced a unique output difference
in this particular 1000-sample experiment.


Collision Experiment

Samples              : 1000
Unique ciphertexts   : 1000
Collisions           : 0

No collisions were observed in the tested sample.

This experiment does not prove collision resistance.


Deterministic Encryption

Samples     : 1000
Failures    : 0
Result      : PASS

The same plaintext and key consistently produced the same
ciphertext.


Full Consistency

Samples     : 1000
Failures    : 0
Result      : PASS

Encryption followed by decryption successfully recovered the
original plaintext for all tested samples.


Experimental Summary

| Experiment                 |             Result |
| -------------------------- | -----------------: |
| Full cipher avalanche      |       127.91 / 256 |
| Full cipher avalanche      |             49.97% |
| Key avalanche              |       128.62 / 256 |
| Key avalanche              |             50.24% |
| Differential diffusion     |       128.59 / 256 |
| Differential diffusion     |             50.23% |
| Differential distribution  | 1000 / 1000 unique |
| Collision experiment       |           0 / 1000 |
| Deterministic encryption   |        1000 / 1000 |
| Full consistency           |        1000 / 1000 |
| Full cipher reversibility  |               PASS |
| Key schedule reversibility |               PASS |

These results are experimental measurements only. They do not
constitute a cryptographic security proof.


Core Self-Tests

The implementation currently passes:

BORN-T reversibility test: PASS
256-bit BORN-T reversibility test: PASS
256-bit key mixing reversibility test: PASS
256-bit state-wide mixing reversibility test: PASS
256-bit permutation reversibility test: PASS
BORN-256 key schedule test: PASS
BORN-256 one-round reversibility test: PASS
BORN-256 full cipher reversibility test: PASS


Quick Start

Clone the repository:

git clone https://github.com/BORN-256/born256.git
cd born256

Run the built-in self-tests:

python src/born256.py

Expected output:

Running BORN-256 self-tests...

BORN-T reversibility test: PASS
256-bit BORN-T reversibility test: PASS
256-bit key mixing reversibility test: PASS
256-bit state-wide mixing reversibility test: PASS
256-bit permutation reversibility test: PASS
BORN-256 key schedule test: PASS
BORN-256 one-round reversibility test: PASS
BORN-256 full cipher reversibility test: PASS

All current BORN-256 tests passed.


Running the Tests

Full Cipher

python tests/test_full_cipher.py

Full Cipher Avalanche

python tests/test_full_cipher_avalanche.py

Key Avalanche

python tests/test_key_avalanche.py

Key Schedule Avalanche

python tests/test_key_schedule_avalanche.py

Differential Analysis

python tests/test_differential.py

Differential Distribution

python tests/test_differential_distribution.py

Collision Experiment

python tests/test_collision.py

Deterministic Encryption

python tests/test_deterministic.py

Full Consistency

python tests/test_full_consistency.py


Project Structure

born256/
│
├── src/
│   └── born256.py
│
├── tests/
│   ├── test_diffusion_layer.py
│   ├── test_diffusion_avalanche.py
│   ├── test_256_diffusion.py
│   ├── test_cross_mix.py
│   ├── test_cross_mix_v2.py
│   ├── test_full_diffusion.py
│   ├── test_state_mix.py
│   ├── test_state_mix_avalanche.py
│   ├── test_round_avalanche.py
│   ├── test_key_schedule.py
│   ├── test_key_schedule_avalanche.py
│   ├── test_full_cipher.py
│   ├── test_full_cipher_avalanche.py
│   ├── test_key_avalanche.py
│   ├── test_differential.py
│   ├── test_differential_distribution.py
│   ├── test_collision.py
│   ├── test_deterministic.py
│   └── test_full_consistency.py
│
└── README.md


What the Tests Demonstrate

The current test suite demonstrates several implementation
properties.

Reversibility

Encryption and decryption can recover the original plaintext in
the tested cases.

Diffusion

Small changes to inputs can produce significant changes in the
resulting state or ciphertext.

Avalanche Behavior

The current experiments show approximately 50% output-bit changes
on average for tested single-bit changes.

Key Sensitivity

Changing a single key bit produced substantial ciphertext
differences in the tested experiments.

Determinism

Identical plaintext and key inputs produce identical ciphertexts.

Consistency

Repeated encryption and decryption operations behave consistently
across the tested samples.


What the Tests Do NOT Demonstrate

Passing these tests does not prove that BORN-256 is
cryptographically secure.

The current experiments do not establish resistance against:

Differential cryptanalysis
Linear cryptanalysis
Integral attacks
Algebraic attacks
Related-key attacks
Meet-in-the-middle attacks
Impossible differential attacks
Statistical distinguishers
Side-channel attacks
Fault attacks
Structural weaknesses
Other cryptanalytic attacks

In particular:

Approximately 50% avalanche does not by itself demonstrate
cryptographic security.

The results should be interpreted as experimental measurements of
the current implementation and its observed behavior.


Development Approach

BORN-256 has been developed incrementally.

The general development process is:

Design
  │
  ▼
Implementation
  │
  ▼
Reversibility Testing
  │
  ▼
Component Diffusion Testing
  │
  ▼
State-Wide Mixing
  │
  ▼
Avalanche Testing
  │
  ▼
Key Schedule
  │
  ▼
Full Cipher
  │
  ▼
Differential Experiments
  │
  ▼
Collision / Consistency Testing
  │
  ▼
Further Cryptanalysis

Each major component is tested before being integrated into the
complete construction.


Project Goals

The main goals of BORN-256 are to explore:

1. Reversible cryptographic transformations
2. 256-bit state diffusion
3. Multi-round state mixing
4. Key sensitivity
5. Avalanche behavior
6. Experimental differential properties
7. Key-schedule behavior
8. Implementation correctness
9. Cryptographic research and learnin


Future Work

Potential future research includes:

Differential cryptanalysis
Linear cryptanalysis
Related-key analysis
Integral analysis
Algebraic analysis
Statistical distinguishers
Larger-scale testing
Performance optimization
Formal specification
Test-vector generation
Independent cryptanalysis
Independent security review
Comparison with established block cipher designs


Security Considerations

BORN-256 should currently be treated as a research and
educational construction.

It has not undergone:

Independent cryptanalysis
Formal security analysis
Peer review
Professional cryptographic audit
Large-scale cryptanalytic evaluation

Therefore, BORN-256 should not be used as a replacement for
established cryptographic algorithms.

For real-world applications, use mature, independently reviewed


License

Add the project's selected license here.

If a license has not yet been selected, this section should remain
unchanged until one is chosen.


Project

BORN-256

Experimental cryptography research project.

Repository:
https://github.com/BORN-256/born256


Disclaimer

BORN-256 is an experimental cryptographic research project.

The experimental results presented in this repository demonstrate
implementation behavior under the tested conditions. They do not
constitute a proof of cryptographic security.

Use BORN-256 for research, education, experimentation, and
development purposes only.

Do not use BORN-256 to protect sensitive or production data.


After replacing it:

```fish
cd ~/born256
git add README.md
git commit -m "Improve BORN-256 README"
git push origin main
git status

