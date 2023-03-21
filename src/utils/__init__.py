from src.utils import parametersCalculation


def calc_rho(l_ratings):
    return parametersCalculation.calc_rho(l_ratings)


def calc_rho_positive(l_ratings):
    return parametersCalculation.calc_rho_positive(l_ratings)


def goodItemsCalculation(l_ratings):
    return parametersCalculation.goodItemsCalculation(l_ratings)


def itemsDifferenceCalculation(items_user, items_u):
    return parametersCalculation.itemsDifferenceCalculation(items_user, items_u)


def fromStringToIntList(s):
    return parametersCalculation.fromStringToIntList(s)


def fromStringToFloatList(s):
    return parametersCalculation.fromStringToFloatList(s)
