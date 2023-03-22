import os
import numpy as np
import pandas as pd
from src import utils

# path statement necessary to let the project work in different environments with respect to PyCharm
here = os.path.dirname(os.path.abspath(__file__))
# path statement for saving the final CSV data
save_path_users = os.path.join(here, "../../dataset/users.csv")


# loading the users dataframe
users_df = pd.read_csv(os.path.join(here, "../../dataset/users.csv"))

# the final dataframe structure will be: u, items, ratings, rho, rho_positive, n_interactions
l_rho = []
l_rho_positive = []
for l_ratings in users_df['ratings']:
    l_rho.append(utils.calc_rho(utils.fromStringToFloatList(l_ratings)))
    l_rho_positive.append(utils.calc_rho_positive(utils.fromStringToFloatList(l_ratings)))

users_df['rho'] = l_rho
users_df['rho_positive'] = l_rho_positive
users_df.reindex(columns=['u', 'items', 'ratings', 'rho', 'rho_positive', 'n_interactions'])
print("\nCorrectly calculated and injected rho information to users dataframe.")
print("Saving to file...")
users_df.to_csv(save_path_users, index=False)
print("Finished saving users dataframe to csv file.")
print("Here we have some elements of the newly created csv file:\n")
print(users_df.head(10))
print("\nDescription of users_test_df: \n")
print(users_df.describe())
