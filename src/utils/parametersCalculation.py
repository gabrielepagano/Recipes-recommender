import math


def telescope_series(n):
    """
    Telescope_series(n) = 1 / n * (n+1) + Telescope_series(n - 1) + ... + Telescope_series(1)
    e.g. (Telescope_series(3) = 1/12 + 1/6 + 1/2)

    Args:
        n: the n-th element of the series
    """
    ret = 0
    for i in range(1, n + 1):
        ret += 1 / (i * (i + 1))

    return ret


def basel_series(n):
    """
    Basel_series(n) = 6/pi^2 * 1/n^2 + Basel_series(n - 1) + ... + Basel_series(1)

    Args:
        n: the n-th element of the series
    """
    ret = 0
    for i in range(1, n + 1):
        ret += (6 / math.pow(math.pi, 2)) * 1 / math.pow(i, 2)

    return ret


# (!) UNUSED - Subject to removal
# TODO: if we want to use this method we should modify it taking into account also how much big the value was in the old
#      span. For example if I want to translate '0.5' from a [0,1] interval to a [2,8] interval the result should be 5,
#      but if we call the function below with these parameters it outputs 5/2.
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


def fromStringToIntList(s):
    """
    Parses the input parameter to a list of integers and returns it.

    Args:
        s: the input string
    """
    cut_str = s[1:-1]
    list_of_items = cut_str.split(',')
    return [int(x) for x in list_of_items]


def fromStringToFloatList(s):
    """
        Parses the input parameter to a list of floating point numbers and returns it.

        Args:
            s: the input string
        """
    cut_str = s[1:-1]
    list_of_ratings = cut_str.split(',')
    return [float(x) for x in list_of_ratings]


def goodItemsCalculation(ratings):
    """
    Returns the number of good rated items (i.e., the number of items rated either 4* or 5*) for a specific user.

    Args:
        ratings: a list (or list-like string) containing all ratings the user has assigned to items.
    """
    a = 0  # a counts the number of 4* (four star) ratings
    b = 0  # b counts the number of 5* (five star) ratings
    for r in ratings:
        if r == 4.0:
            a += 1
        elif r == 5.0:
            b += 1
    return a, b


def itemsDifferenceCalculation(items_user, items_u):
    """
    Returns the number of items rated by the current user that have not been rated by the reference user and a list
    containing them.

    Args:
        items_u: a list (or list-like string) containing all the ids corresponding to the items that the reference user
                 has rated.
        items_user: a list (or list-like string) containing all the ids corresponding to the items that the current user
                    has rated.
    """
    n = 0
    dim = len(items_user)
    items_different = []
    for i in range(dim):
        if not items_user[i] in items_u:
            n += 1
            items_different.append(items_user[i])
    return n, items_different


def rho_positive(a, b):
    """
    Returns the rho value calculated for a particular user in respect to their 4* and 5* ratings.
    Specifically: rho_positive(a, b) = (a * Telescope_series(a) + b * Basel_series(b)) / (a + b)

    Args:
        a: the number of 4* (four star) ratings of a particular user.
        b: the number of 5* (five star) ratings of a particular user.
    """
    n = a + b
    if n > 0:
        return (a * telescope_series(a) + b * basel_series(b)) / n
    else:
        return 0


def calc_rho_positive(ratings):
    """
    Parses the interactions of a particular user and calculate the rho_positive value.

    Args:
        ratings: a list (or list-like string) containing all ratings the user has assigned to items.
    """
    a, b = goodItemsCalculation(ratings)
    return rho_positive(a, b)


# (!) Subject to change
def rho(n):
    """
    Returns the rho value calculated for a particular user in respect to all their ratings.
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
    Parses the interactions of a particular user and calculate the rho value.

    Args:
        ratings: a list (or list-like string) containing all ratings the user has assigned to items.
    """
    n = 0  # counts the total number of ratings (possibly fair to retrieve this information from n_interactions)
    for r in ratings:
        if r in [1.0, 2.0, 3.0, 4.0, 5.0]:
            n += 1
    return rho(n)
