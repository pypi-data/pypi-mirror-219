import numpy as np
import pandas as pd
import pytest
import sigfig

from float_table.fmt import pad_decimal, determine_eng_exponent, format_column


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ids=lambda x: f"seed={x}")
def num_column(request):
    n = 3
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


def test_exponent(num_column):
    exponent = determine_eng_exponent(num_column)
    assert exponent % 3 == 0


@pytest.mark.parametrize("sig_figs", [1, 4, 8])
def test_numbers_correct(num_column, sig_figs):
    actual = format_column(num_column, sig_figs)

    # Use the sigfig library to check (our code does not use sigfig)
    expected = num_column.apply(lambda x: sigfig.round(x, sig_figs, output_type=str))
    actual = actual.apply(lambda x: x.replace(" ", ""))

    expected = expected.astype(float)
    actual = actual.astype(float)
    assert (actual == expected).all()
