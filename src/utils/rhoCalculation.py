import math


def telescop_series(n):
    """
    Telescop_series(n) = 1 / n * (n+1) + Telescop_series(n - 1)
    eg. (Telescop_series(3) = 1/12 + 1/6 + 1/2)

    Args:
        n: the n-th element of the series
    """
    ret = 0
    for i in range(1, n + 1):
        ret += 1 / (i * (i + 1))

    return ret


def basel_series(n):
    """
    Basel_series(n) = 6/pi^2 * 1/n^2 + Basel_series(n - 1)

    Args:
        n: the n-th element of the series
    """
    ret = 0
    for i in range(1, n + 1):
        ret += 6 / math.pow(math.pi, 2) * 1 / math.pow(i, 2)

    return ret


# (!) UNUSED - Subject to removal
def translate(value, from_, to_):
    """
    Translates a value from the original range to a new range.

    Args:
        value: the value for translation.
        from_: the original range [a, b].
        to_: the new range [c, d].
    """
    # Figure out how 'wide' each range is
    from_Span = from_[1] - from_[0]
    to_Span = to_[1] - to_[0]

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - from_[0]) / float(from_Span)

    # Convert the 0-1 range into a value in the right range.
    return to_[0] + (valueScaled * to_Span)


def rho_positive(a, b):
    """
    Return the rho value calculated for a particular user in respect to their 4* and 5* ratings.
    Specifically: rho_positive(a + b) = (a * Telescop_series(a + b) + b * Basel_series(a + b)) / (a + b)

    Args:
        a: the number of 4* (four star) ratings of a particular user.
        b: the number of 5* (five star) ratings of a particular user.
    """
    n = a + b
    if n > 0:
        return (a * telescop_series(n) + b * basel_series(n)) / n
    else:
        return 0


def calc_rho_positive(ratings):
    """
    Parse the interactions of a particular user and calculate the rho_positive value.

    Args:
        ratings: a list (or list-like string) containing all ratings the user has assigned to items.
    """
    a = 0  # a counts the number of 4* (four star) ratings
    b = 0  # b counts the number of 5* (five star) ratings
    for r in ratings:
        if r == '4':
            a += 1
        elif r == '5':
            b += 1
    return rho_positive(a, b)


# (!) Subject to change
def rho(n):
    """
    Return the rho value calculated for a particular user in respect to all their ratings.
    Specifically: rho(n) = Basel_series(n)
    Args:
        n: the number of ratings of a particular user.
    """
    if n > 0:
        return basel_series(n)
    else:
        return 0


# (!) Subject to change
def calc_rho(ratings):
    """
    Parse the interactions of a particular user and calculate the rho value.

    Args:
        ratings: a list (or list-like string) containing all ratings the user has assigned to items.
    """
    n = 0  # counts the total number of ratings (possibly fair to retrieve this information from n_interactions)
    for r in ratings:
        if r in ['1', '2', '3', '4', '5']:
            n += 1
    return rho(n)
