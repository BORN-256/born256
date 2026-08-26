## BORN-256 Structure

The current experimental cipher uses a 16-round structure.
Each round applies the core transformation and mixing operations
together with a round key.

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




### Key Schedule

The 256-bit master key is expanded into one 256-bit round key
for each of the 16 rounds.

```text
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




### One more recommendation

Keep this line exactly as you have it:

> **has not been independently cryptanalyzed or formally proven secure**

That's very important. Your **49.97% / 50.24% avalanche results are promising experimental measurements**, but they shouldn't be presented as proof of security.

So overall: **yes, your README is good**, but I'd use the revised structure above because it explains the architecture much more clearly.
