from src.utils import parametersCalculation


def calc_rho(l_ratings):
    return parametersCalculation.calc_rho(l_ratings)


def calc_rho_positive(l_ratings):
    return parametersCalculation.calc_rho_positive(l_ratings)


def good_items_calculation(l_ratings):
    return parametersCalculation.good_items_calculation(l_ratings)


def items_difference_calculation(items_user, items_u):
    return parametersCalculation.items_difference_calculation(items_user, items_u)


def from_string_to_int_list(s):
    return parametersCalculation.from_string_to_int_list(s)


def from_string_to_float_list(s):
    return parametersCalculation.from_string_to_float_list(s)


def find_indices(lis, x):
    return parametersCalculation.find_indices(lis, x)
