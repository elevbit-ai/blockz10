import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blockz10 import (  # noqa: E402
    Block155,
    DEFAULT_RULES,
    EXAMPLE_RULES,
    decode,
    encode,
    generate_key,
    key_entropy_bits,
)


def test_original_example():
    # The canonical example from the 2021 post: eee11 -> 311
    assert encode("eee11") == "311"
    assert decode("311") == "eee11"


def test_roundtrip_random():
    rng = random.Random(155)
    for _ in range(500):
        s = "".join(rng.choice("e1") for _ in range(rng.randint(1, 128)))
        assert decode(encode(s)) == s


def test_long_e_runs_split():
    assert encode("e" * 13) == "94"
    assert decode("94") == "e" * 13


def test_single_e_is_unambiguous():
    assert encode("e") == "e"
    assert encode("1") == "1"
    assert decode(encode("e1e")) == "e1e"


def test_published_key_roundtrips():
    key = "111e1ee1e1eeeee11111ee1111e11e11111e11e1e111e11ee11e1111ee1e1eee"
    assert len(key) == 64
    assert decode(encode(key)) == key
    assert len(encode(key)) < len(key)  # it actually compresses


def test_generated_key_is_valid_hex():
    key = generate_key()
    assert len(key) == 64
    int(key, 16)  # must parse as hexadecimal (ETH private key syntax)


def test_entropy_is_64_bits():
    assert key_entropy_bits(64, 2) == 64.0
    assert key_entropy_bits(64, 16) == 256.0


def test_system_total_is_150():
    b = Block155()
    assert sum(b.level_total(lv) for lv in range(6)) == 150.0


def test_conservation_with_truncation():
    # The original hand-worked round loses only rounding dust:
    # 149.86 recovered out of 150.
    for rules in (DEFAULT_RULES, EXAMPLE_RULES):
        r = Block155(rules=dict(rules)).distribute()
        assert r.total_in == 150.0
        assert r.conserved
        assert r.dust < 0.2  # dust stays in the same order as 150-149.86


def test_conservation_exact_without_truncation():
    r = Block155(rules=dict(EXAMPLE_RULES), precision=None).distribute()
    assert math.isclose(r.total_out, 150.0, abs_tol=1e-9)


def test_example_rule_matches_blog():
    # "Block 2 = 20 -> 20/3 = 6.66 to receptor blocks 3, 4, 5"
    b = Block155(rules=dict(EXAMPLE_RULES))
    assert b.quota(2) == 6.66
    assert EXAMPLE_RULES[2].receptors == (3, 4, 5)


def test_incentive_table():
    b = Block155()
    assert b.incentive(1) == (16.66, +0.15)
    assert b.incentive(5) == (11.16, +0.10)
    assert b.incentive(0) is None


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)} tests passed.")
