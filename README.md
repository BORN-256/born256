# BORN-256

> An experimental 256-bit reversible block cipher exploring diffusion, permutation, key mixing, and multi-round cryptographic transformations.

**BORN-256** is an experimental 256-bit cryptographic block cipher research project.

It explores a custom reversible transformation design combining BORN-T transformations, state-wide mixing, permutation, key mixing, and a multi-round key schedule.

> ⚠️ **SECURITY WARNING**
>
> BORN-256 is an experimental cryptographic construction.
> It has not undergone independent cryptanalysis, formal security analysis, or professional security review.
>
> **BORN-256 must not be used to protect production systems or sensitive real-world data.**

---

## Current Status

**Experimental / Research**

The current implementation includes:

- 256-bit block size
- 256-bit key size
- 16-round cipher
- BORN-T reversible transformation
- 256-bit state-wide mixing
- 256-bit permutation layer
- 256-bit key mixing
- 256-bit round-key schedule
- Encryption and decryption
- Full-round reversibility
- Key-schedule reversibility
- Deterministic encryption
- Avalanche analysis
- Differential analysis
- Differential distribution experiment
- Collision experiment
- Full consistency testing

---

## Features

- 🔐 256-bit block size
- 🔑 256-bit key size
- 🔄 16-round reversible design
- 🧩 BORN-T transformation
- 🌐 State-wide diffusion
- 🔀 Permutation layer
- 🔑 Multi-round key schedule
- 📊 Avalanche analysis
- 📈 Differential experiments
- 🧪 Automated test suite
- 🔁 Full encryption/decryption reversibility

---

## BORN-256 Structure

The current experimental cipher uses a 16-round structure.

Each round applies the core transformation and mixing operations together with a round key.

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

The experimental key schedule expands a 256-bit master key into one 256-bit round key for each of the 16 rounds.

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

The key schedule is designed to be reversible in the current experimental implementation.

| Parameter        |                     Value |
| ---------------- | ------------------------: |
| Block size       |                  256 bits |
| Key size         |                  256 bits |
| State size       |                  256 bits |
| Number of rounds |                        16 |
| Round key size   |                  256 bits |
| Cipher type      | Experimental block cipher |
| Implementation   |                    Python |

Experimental Results

The following results come from the current experimental test suite.

Full Cipher Avalanche
Samples               : 1000
Minimum changed bits  : 104
Maximum changed bits  : 148
Average changed bits  : 127.91 / 256
Average changed       : 49.97%

The measured average is close to the approximately 50% reference commonly used when evaluating avalanche behavior.

Key Avalanche
Samples               : 1000
Minimum changed bits  : 109
Maximum changed bits  : 147
Average changed bits  : 128.62 / 256
Average changed       : 50.24%

This experiment measures the effect of changing a single key bit on the resulting ciphertext.

Differential Analysis
Samples               : 1000
Minimum output diff   : 105 bits
Maximum output diff   : 149 bits
Average output diff   : 128.59 / 256
Average percentage    : 50.23%

This measures diffusion of arbitrary input differences.

Differential Distribution
Samples                  : 1000
Unique output differences: 1000
Maximum frequency        : 1
Maximum probability      : 0.1000%

Every tested input difference produced a unique output difference in this particular 1000-sample experiment.

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

Identical plaintext and key inputs consistently produced identical ciphertexts.

Full Consistency
Samples     : 1000
Failures    : 0
Result      : PASS

Encryption followed by decryption successfully recovered the original plaintext for all tested samples.

| Experiment                       |             Result |
| -------------------------------- | -----------------: |
| Full cipher avalanche            |       127.91 / 256 |
| Full cipher avalanche percentage |             49.97% |
| Key avalanche                    |       128.62 / 256 |
| Key avalanche percentage         |             50.24% |
| Differential diffusion           |       128.59 / 256 |
| Differential percentage          |             50.23% |
| Differential distribution        | 1000 / 1000 unique |
| Collision experiment             |           0 / 1000 |
| Deterministic encryption         |        1000 / 1000 |
| Full consistency                 |        1000 / 1000 |
| Full cipher reversibility        |               PASS |
| Key schedule reversibility       |               PASS |

These are experimental measurements only. They do not constitute a cryptographic security proof.

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

Expected result:

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
Full Cipher Test
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
│   ├── test_differential.py
│   ├── test_differential_distribution.py
│   ├── test_key_schedule.py
│   ├── test_key_schedule_avalanche.py
│   ├── test_full_cipher.py
│   ├── test_full_cipher_avalanche.py
│   ├── test_key_avalanche.py
│   ├── test_collision.py
│   ├── test_deterministic.py
│   └── test_full_consistency.py
│
└── README.md



What the Tests Demonstrate

The current test suite demonstrates several implementation properties.

Reversibility

Encryption and decryption can recover the original plaintext in the tested cases.

Diffusion

Small changes to inputs can produce significant changes in the resulting state or ciphertext.

Avalanche Behavior

The current experiments show approximately 50% output-bit changes on average for tested single-bit changes.

Key Sensitivity

Changing a single key bit resulted in substantial ciphertext differences in the tested experiments.

Determinism

Identical inputs produce identical outputs.

Consistency

Repeated encryption/decryption operations behave consistently across the tested samples.

What the Tests Do NOT Demonstrate

Passing these tests does not prove that BORN-256 is cryptographically secure.

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

Approximately 50% avalanche does not by itself demonstrate cryptographic security.

The current results should therefore be interpreted as experimental measurements of the implementation and its observed behavior.

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

Each stage is tested before moving toward the next stage.

Project Goals

The main goals of BORN-256 are to explore:

Reversible cryptographic transformations
256-bit state diffusion
Multi-round state mixing
Key sensitivity
Avalanche behavior
Experimental differential properties
Key-schedule behavior
Implementation correctness
Cryptographic research and learning
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

BORN-256 should currently be treated as a research and educational construction.

It has not undergone:

Independent cryptanalysis
Formal security analysis
Peer review
Professional cryptographic audit
Large-scale cryptanalytic evaluation

Therefore, BORN-256 should not be used as a replacement for established cryptographic algorithms.

For real-world applications, use mature, independently reviewed cryptographic standards and libraries.

License

Add the project's selected license here.

If a license has not yet been selected, this section should remain unchanged until one is chosen.

Project

BORN-256

Experimental cryptography research project.

Repository:

https://github.com/BORN-256/born256
Disclaimer

BORN-256 is an experimental cryptographic research project.

The experimental results presented in this repository demonstrate implementation behavior under the tested conditions. They do not constitute a proof of cryptographic security.

Use BORN-256 for research, education, experimentation, and development purposes only.

Do not use BORN-256 to protect sensitive or production data.


### After replacing `README.md`

Run:

```fish
cd ~/born256
git diff -- README.md

If everything looks correct:

git add README.md
git commit -m "Improve BORN-256 documentation"
git push origin main
git status

You should finish with:

Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean

