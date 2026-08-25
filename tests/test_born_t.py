import sys
from pathlib import Path

# Allow importing born256.py from the src directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from born256 import born_t, inverse_born_t


def test_all_born_t_inputs():
    """
    Test all possible 3-bit inputs and verify
    that BORN-T is reversible.
    """

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):

                original = (a, b, c)

                transformed = born_t(a, b, c)

                recovered = inverse_born_t(*transformed)

                assert recovered == original, (
                    f"Reversibility failure: "
                    f"{original} -> "
                    f"{transformed} -> "
                    f"{recovered}"
                )


if __name__ == "__main__":
    test_all_born_t_inputs()
    print("BORN-T exhaustive reversibility test: PASS")
