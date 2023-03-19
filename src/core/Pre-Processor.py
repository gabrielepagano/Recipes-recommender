import os
import pandas as pd
from src import utils

# path statement necessary to let the project work in different environments with respect to PyCharm
here = os.path.dirname(os.path.abspath(__file__))
# path statement for saving the final CSV data
save_path_users = os.path.join(here, "../../dataset/users_test.csv")


# loading the users dataframe
users_df = pd.read_csv(os.path.join(here, "../../dataset/users.csv"))

# the dataframe structure will be: u, items, ratings, rho, n_interactions
l_rho = []
for l_ratings in users_df['ratings']:
    l_rho.append(utils.calc_rho(l_ratings))

users_df['rho'] = l_rho
users_df.reindex(columns=['u', 'items', 'ratings', 'rho', 'n_interactions'])
print("\nCorrectly calculated and injected rho information to users dataframe.")
print("Saving to file...")
users_df.to_csv(save_path_users, index=False)
print("Finished saving users dataframe to csv file.")

print("Description of users_test_df: \n")
print(users_df.describe())
