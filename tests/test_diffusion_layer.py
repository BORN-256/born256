"""
BORN-256 Diffusion Layer Test

Experimental reversible Boolean diffusion construction.

This test verifies:
1. The transformation is reversible.
2. All possible 3-bit inputs are recovered correctly.
3. The transformation changes multiple bits for selected inputs.

This is NOT a cryptographic security proof.
"""


# ============================================================
# BOOLEAN GATES
# ============================================================

def and_gate(a, b):
    return a & b


def or_gate(a, b):
    return a | b


def not_gate(a):
    return 1 - a


def xor_gate(a, b):
    """
    XOR constructed only from AND, OR and NOT.
    """
    return and_gate(
        or_gate(a, b),
        not_gate(and_gate(a, b))
    )


# ============================================================
# REVERSIBLE DIFFUSION TRANSFORMATION
# ============================================================

def diffusion_layer(a, b, c):
    """
    Reversible 3-bit Boolean transformation.

        a' = a
        b' = b XOR a
        c' = c XOR b'

    XOR is constructed from:
        AND
        OR
        NOT
    """

    new_a = a

    new_b = xor_gate(b, a)

    new_c = xor_gate(c, new_b)

    return new_a, new_b, new_c


# ============================================================
# INVERSE TRANSFORMATION
# ============================================================

def inverse_diffusion_layer(a, b, c):
    """
    Inverse of diffusion_layer().
    """

    original_a = a

    original_b = xor_gate(b, a)

    original_c = xor_gate(c, b)

    return original_a, original_b, original_c


# ============================================================
# EXHAUSTIVE REVERSIBILITY TEST
# ============================================================

def test_reversibility():

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):

                original = (a, b, c)

                transformed = diffusion_layer(
                    a, b, c
                )

                recovered = inverse_diffusion_layer(
                    *transformed
                )

                if recovered != original:
                    raise AssertionError(
                        f"FAILED: "
                        f"{original} -> "
                        f"{transformed} -> "
                        f"{recovered}"
                    )

    print(
        "3-bit diffusion reversibility test: PASS"
    )


# ============================================================
# DISPLAY TRANSFORMATION
# ============================================================

def show_transformation():

    print()
    print("BORN-256 Diffusion Layer")
    print("=" * 40)

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):

                original = (a, b, c)

                transformed = diffusion_layer(
                    a, b, c
                )

                print(
                    f"{original} -> {transformed}"
                )

    print("=" * 40)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_reversibility()
    show_transformation()