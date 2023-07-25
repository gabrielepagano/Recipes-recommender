import os
import numpy as np
import pandas as pd
import sys
sys.path.append(os.getcwd())
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
    l_rho.append(utils.calc_rho(utils.from_string_to_float_list(l_ratings)))
    l_rho_positive.append(utils.calc_rho_positive(utils.from_string_to_float_list(l_ratings)))

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
print("\n\nProcessing interactions dataset.. .\n")



# # path statement for saving the final CSV data
save_path_popularity_scores = os.path.join(here, "../../dataset/popularity_scores.csv")

# loading the interactions dataframe
interactions_df = pd.read_csv(os.path.join(here, "../../dataset/interactions.csv"))
# loading the recipes dataframe
recipes_df = pd.read_csv(os.path.join(here, "../../dataset/recipes.csv"))

# the final dataframe structure will be: i, popularity_score, total_ratings, total_ratings_4, total_ratings_5
total_ratings = np.zeros(len(recipes_df.index))
total_stars = np.zeros(len(recipes_df.index))
popularity_score = np.zeros(len(recipes_df.index))
bias = 0.7  # the importance given to the "total ratings" bias. The larger the number, the lower the score of items with few ratings.

# iterating through pandas has low performance (disclaimer from pandas documentation)
recipe_ids = interactions_df[['i']].values
recipe_scores = interactions_df[['rating']].values

for (r_id, r_rating) in zip(recipe_ids, recipe_scores):
    if r_rating > 0:
        total_ratings[r_id] += 1
    if r_rating == 1.0:
        total_stars[r_id] += 1
    if r_rating == 2.0:
        total_stars[r_id] += 2
    if r_rating == 3.0:
        total_stars[r_id] += 3
    if r_rating == 4.0:
        total_stars[r_id] += 4
    elif r_rating == 5.0:
        total_stars[r_id] += 5

# the popularity score is 
for (i, tot_stars, tot_rat) in zip(range(len(popularity_score)), total_stars, total_ratings):
    if tot_rat > 0 and tot_stars > 0:
        popularity_score[i] = tot_stars / tot_rat + utils.normalize(tot_rat, [np.min(total_ratings), np.max(total_ratings)], [0, bias])
    else:
        popularity_score[i] = 0
for i in range(len(popularity_score)):
    if popularity_score[i] > 0:
        popularity_score[i] = utils.normalize(popularity_score[i], [1, 5 + bias], [1, 5])

print("The minimum popularity score:")
print(np.min(popularity_score), "\n")
print("The maximum popularity score:")
print(np.max(popularity_score), "\n")

# TODO: implement a method to return the minimum value that's greater than number 'a' (eg. 0)
# and apply it to popularity model

# creating the popularity_scores DataFrame
popularity_scores_data = {
    'popularity_score': popularity_score.flatten(),
    'total_ratings': total_ratings.flatten(),
    'total_stars': total_stars.flatten(),
}
popularity_scores_df = pd.DataFrame(popularity_scores_data)

# saving the popylarity_scores_df to a csv file
popularity_scores_df.to_csv(save_path_popularity_scores, index=True)
popularity_scores_df.index.name = "i"
print("Finished saving popularity_scores dataframe to csv file.")
print("Here we have some elements of the newly created csv file:\n")
print(popularity_scores_df.head(10))
print("\nDescription of popularity_scores_df: \n")
print(popularity_scores_df.describe())


