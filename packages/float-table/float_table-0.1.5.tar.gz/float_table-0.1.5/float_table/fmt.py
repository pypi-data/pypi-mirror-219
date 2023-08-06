import math


def determine_eng_exponent(column):
    """
    Determine the common engineering notation exponent for a numeric column.
    """
    max_abs_val = max(abs(column))
    if max_abs_val == 0:
        return 0
    exponent = 3 * math.floor(
        math.log10(max_abs_val) / 3
    )  # Choose the exponent based on the maximum absolute value
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


def format_column(column, sig_figs):
    column = column.copy()

    exponent = determine_eng_exponent(column)

    formatted = round_sigfig(column / 10**exponent, sig_figs)

    formatted = pad_decimal(formatted)

    if exponent != 0:
        formatted = formatted + "e" + str(exponent)

    return formatted


def format_df(df, sig_figs):
    formatted = df.copy()
    numeric_columns = df.select_dtypes("number").columns
    formatted[numeric_columns] = formatted[numeric_columns].apply(
        lambda x: format_column(x, sig_figs)
    )
    return formatted
