import math

import numpy as np
import pandas as pd
import tabulate


def floor_toward_zero(x):
    """
    Floor a number toward zero.
    """
    if x >= 0:
        return math.floor(x)
    else:
        return math.ceil(x)


def determine_eng_exponent(column):
    """
    Determine the common engineering notation exponent for a numeric column.
    """
    # Choose the exponent based on ``exponent_for``.
    column_abs = column.abs()
    if max(column_abs) == 0:
        exponent_for = 0
    else:
        exponent_for = np.quantile(column_abs, 0.85)

    if exponent_for == 0:
        return 0
    exponent = 3 * floor_toward_zero(math.log10(exponent_for) / 3)
    return exponent


def find_decimal(x):
    if "." not in x:
        x += "."  # Add a decimal point at the end if it's an integer
    return x.index(".")


def find_left_padding(column):
    """
    Find the left padding spaces for each number in the column to align decimal places.
    """
    # Find the decimal location for each number in the column
    decimal_locations = column.apply(find_decimal)

    # Find the maximum number of digits before the decimal
    max_digits_before_decimal = decimal_locations.max()

    # Calculate the left padding needed by each number
    left_padding = max_digits_before_decimal - decimal_locations

    return left_padding


def find_right_padding(column):
    """
    Find the right padding spaces for each number in the column to align decimal places.
    """
    # Find the number of digits after the decimal for each number in the column
    digits_after_decimal = column.apply(lambda x: len(x) - find_decimal(x))

    # Find the maximum number of digits after the decimal
    max_digits_after_decimal = digits_after_decimal.max()

    # Calculate the right padding needed by each number
    right_padding = max_digits_after_decimal - digits_after_decimal

    return right_padding


def pad_decimal(column):
    """Add padding spaces to align decimal points."""
    left_padding = find_left_padding(column)
    right_padding = find_right_padding(column)
    column_copy = column.copy()
    for i in range(len(column)):
        column_copy.iloc[i] = (
            " " * left_padding.iloc[i] + column.iloc[i] + " " * right_padding.iloc[i]
        )
    return column_copy


def round_sigfig(column, sig_figs):
    return column.apply(lambda x: _round_sigfig(x, sig_figs))


def _round_sigfig(x, sig_figs):
    if x == 0:
        return "0." + "0" * (sig_figs - 1)
    magnitude = math.floor(math.log10(abs(x)))
    decimal_shift = sig_figs - 1 - magnitude
    result = round(x, decimal_shift)
    return f"{result:.{max(0, decimal_shift)}f}"


def format_column(column, sig_figs, percent=False):
    """
    TODO: test for percent=True
    """
    column = column.copy()

    exponent = determine_eng_exponent(column)
    if percent:
        exponent = 0
        column = column * 100

    # If column is all integer data types, align, but don't round or use engineering notation
    if pd.api.types.is_integer_dtype(column):
        exponent = 0
        formatted = column.apply(lambda x: str(x))
    else:
        formatted = round_sigfig(column / 10**exponent, sig_figs)

    formatted = pad_decimal(formatted)

    if percent:
        formatted = formatted + "%"
    if exponent != 0:
        formatted = formatted + "e" + str(exponent)

    return formatted


def format_df(df: pd.DataFrame, sig_figs: int) -> pd.DataFrame:
    formatted = df.copy()
    float_cols = df.select_dtypes("number").columns
    formatted[float_cols] = formatted[float_cols].apply(lambda x: format_column(x, sig_figs))
    return formatted


def tabulate_df(df: pd.DataFrame, sig_figs: int, header: bool = True, index: bool = True) -> str:
    """
    Uses tabulate to format a dataframe as a github-flavored markdown table.
    :param df: The dataframe to format
    :param sig_figs: The number of significant figures to use
    :param header: Whether to include the header row
    :param index: Whether to include the index column
    """
    formatted = format_df(df, sig_figs)

    # Unfortunately, they made tabulate.PRESERVE_WHITESPACE a global variable
    # so we have to set it here and then reset it at the end of the function
    preserve_whitespace_prev = tabulate.PRESERVE_WHITESPACE
    tabulate.PRESERVE_WHITESPACE = True

    kwargs = {}
    if header:
        kwargs["headers"] = "keys"
    kwargs["showindex"] = index
    table = tabulate.tabulate(
        formatted,
        disable_numparse=True,
        tablefmt="github",
        **kwargs,
    )
    tabulate.PRESERVE_WHITESPACE = preserve_whitespace_prev
    return table
