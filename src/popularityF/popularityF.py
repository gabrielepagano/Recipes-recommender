import os
import pandas as pd
from src.popularityF.popularityModel import PopularityModel


# path statement necessary to let the project work in different environments with respect to PyCharm
here = os.path.dirname(os.path.abspath(__file__))

def recommend_items(user_id, topn, prnt=False, verbose=False):
    """
    Utilises the Popularity Model to recommend a set of items to a specified user.

    Args:
        user_id: the id of the user in question
        topn: the number of most popular items to be recommended to the user
        prnt: defaults to False
        verbose: defaults to False
    """

    # loading the popularity_scores dataframe
    popularity_scores_df = pd.read_csv(os.path.join(here, "../../dataset/popularity_scores.csv"))
    # loading the recipes dataframe
    recipes_df = pd.read_csv(os.path.join(here, "../../dataset/recipes.csv"))
    # loading the interactions dataframe
    interactions_df = pd.read_csv(os.path.join(here, "../../dataset/interactions.csv"))

    popularity_model = PopularityModel(interactions_df, popularity_scores_df, recipes_df)

    if prnt:
        print("\nHere we have the", topn, "recipes that we recommend to the user_id:", user_id, "\n")
        recommended_items_df = popularity_model.recommend_items(user_id, topn, verbose)
        print(recommended_items_df)
        print("\nDescription of recommended_items_df: \n")
        print(recommended_items_df.describe())

    return recommended_items_df