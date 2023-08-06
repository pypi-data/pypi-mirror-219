import numpy as np
import pandas as pd
import pytest

from float_table.fmt import pad_decimal, determine_eng_exponent, format_column, format_df


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ids=lambda x: f"seed={x}")
def num_column(request):
    n = 1000
    np.random.seed(request.param)

    def base_floats():
        # Generate floats spanning 12 orders of magnitude
        return np.random.rand(n) * 10.0 ** np.random.randint(-6, 6, n)

    positive_floats = base_floats()
    negative_floats = -base_floats()
    ints = base_floats().astype(int)

    nums = np.concatenate([positive_floats, negative_floats, ints])
    return pd.Series(nums)


@pytest.fixture
def str_column(num_column):
    strings = [f"{x:.{np.random.randint(0, 10)}f}" for x in num_column]
    return pd.Series(strings)


def test_pad_decimal(str_column):
    padded = pad_decimal(str_column)

    # All have same length
    assert padded.str.len().min() == padded.str.len().max()

    # Decimal points are aligned
    pos_decimals = []
    for x in padded:
        if "." in x:
            pos_decimals.append(x.index("."))
        else:
            # Find the last digit
            idx_last_digit = len(x.rstrip()) - 1
            int(x[idx_last_digit])  # Make sure it's a digit
            pos_decimals.append(idx_last_digit + 1)
    assert min(pos_decimals) == max(pos_decimals)


def test_exponent_is_eng(num_column):
    exponent = determine_eng_exponent(num_column)
    assert exponent % 3 == 0


def test_all_zeros():
    num_column = pd.Series([0, 0, 0])
    exponent = determine_eng_exponent(num_column)
    assert exponent == 0


@pytest.mark.parametrize("sig_figs", [1, 4, 8])
def test_numbers_correct(num_column, sig_figs):
    # The most obvious way to test this (using Python's 'g' formatter),
    # fails on edge cases: this is because round() applies "round half to even" whereas
    # 'g' format applies "round half away from zero".
    # This is a dumb hack to avoid integers that end in 5
    num_column = num_column.apply(lambda x: x + 0.0000001)

    actual = format_column(num_column, sig_figs)
    actual = actual.apply(lambda x: float(x.replace(" ", "")))

    g_rounder = "{:." + str(sig_figs) + "g}"
    expected = num_column.apply(lambda x: float(g_rounder.format(x)))

    for i in range(len(actual)):
        msg = f"For '{num_column.iloc[i]}', got '{actual.iloc[i]}', expected '{expected.iloc[i]}'"
        assert actual.iloc[i] == expected.iloc[i], msg


def test_format_df():
    df = pd.DataFrame(
        {
            "ints": [1, 2, 3],
            "floats": [1.0, 2.0, 3.0],
            "ints_and_floats": [1, 2.0, 3],
            "string": ["not a number", 1.23456789, 1.23456789e-10],
        }
    )
    formatted = format_df(df, 2)
    assert all(formatted["ints"] == ["1", "2", "3"])
    assert all(formatted["floats"] == ["1.0", "2.0", "3.0"])
    assert all(formatted["ints_and_floats"] == ["1.0", "2.0", "3.0"])
    assert all(formatted["string"] == df["string"])
