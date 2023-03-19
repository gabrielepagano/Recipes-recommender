import math


# Telescop_series(n) = 1 / [n * (n+1)] (Telescop_series(3) = 1/2 + 1/6 + 1/12)
# Basel_series(n) = 6/pi^2 * 1/n^2
# n = N_4 + N_5
# rho(n) = (N_4 * Telescop_series(n) + N_5 * Telescop_series(n)) / (N_4 + N_5)

def telescop_series(n):
    ret = 0
    for i in range(1, n + 1):
        ret += 1 / (n * (n + 1))

    return ret


def basel_series(n):
    ret = 0
    for i in range(1, n + 1):
        ret += 6 / math.pow(math.pi, 2) * 1 / math.pow(n, 2)

    return ret


def translate(value, from_, to_):
    # Figure out how 'wide' each range is
    from_Span = from_[1] - from_[0]
    to_Span = to_[1] - to_[0]

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - from_[0]) / float(from_Span)

    # Convert the 0-1 range into a value in the right range.
    return to_[0] + (valueScaled * to_Span)


def rho(a, b):
    """
    Return the rho value calculated for a particular user.

    Args:
        a: the number of 4* (four star) ratings of a particular user.
        b: the number of 5* (five star) ratings of a particular user.
    """
    n = a + b
    return (a * telescop_series(n) + b * telescop_series(n)) / n


def calc_rho(ratings):
    """
    Parse the interactions of a particular user and calculate the rho value.

    Args:
        ratings: a list containing all ratings the user has assigned to items.
    """
    a = 0  # a counts the number of 4* (four star) ratings
    b = 0  # b counts the number of 5* (five star) ratings
    for r in ratings:
        if r == '4':
            a += 1
        elif r == '5':
            b += 1
    if a > 0 and b > 0:
        return rho(a, b)

    return 0
