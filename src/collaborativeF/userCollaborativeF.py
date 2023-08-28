# - The idea of a user related collaborative filtering is to suggest items basing on most similar users to us
# - Before give the idea to the user relevance we make a change in how to define rho
# - Since for this type of analysis we don't care to distinguish how the user rated the items,
#   our new rho is defined as: rho_new(k) = basel_series(k)

# - This because in this scenario we just want to give importance to how many items he rated
# - Now we can define how much a user u is relevant for our reference user u*
# - The idea is the following:
#       Given:
#           #good_items(u) = 0.75 (!!!) * #items_rated_4(u) + #items_rated_5(u)
#           #items_different(u,u*) = #items rated by u but not by u*
#           utility(u,u*) = #good_items(u) / #items_different(u,u*)
#       The relevance score is defined as following:
#           Relevance_score(u,u*) = 0, if cos_similarity(u,u*) == 1
#           Relevance_score(u,u*) = cos_similarity(u,u*) * utility(u,u*) * rho_new(u)
# - we pick the P (!!!) most relevant users according to the relevance_score and for each we take M (!!!) most rated
#   items (according to the item relevance score computed like this:
# #   item_relevance_score =
# #       rho_new(u*) * rating(item) + (1 - rho_new(u*)) * popularity_score (Normalized between 1 and 5))
#
#   In case the recommended items end up being less than M (unlikely in our use case),
#   we pick the remaining items from the Item Popularity Model.
#
#   We also have to check that all M items recommended are items not already rated by u*.
#
#
# - NB: when I wrote (!!!) I provided alternatives of different models that we can evaluate in the validation set


import os
import pandas as pd
from src.collaborativeF.UserCollaborativeModel import UserCollaborativeModel

# path statement necessary to let the project work in different environments with respect to PyCharm
here = os.path.dirname(os.path.abspath(__file__))


class UserCollaborativeHelper:

    def __init__(self, topu=5, topn=10):
        """
        Helper class for User Collaborative Model.
        Args:
            topu: defaults to 5. Defines amount of relevant users from which to recommend recipes
            topn: the number of most relevant items to be recommended to the user
        """

        self.topu = topu
        self.topn = topn

        # loading the users dataframe
        users_df = pd.read_csv(os.path.join(here, "../../dataset/users.csv"))
        # loading the popularity_scores dataframe
        popularity_scores_df = pd.read_csv(os.path.join(here, "../../dataset/popularity_scores.csv"))
        # loading the recipes dataframe
        recipes_df = pd.read_csv(os.path.join(here, "../../dataset/recipes.csv"))
        # loading the interactions dataframe
        interactions_df = pd.read_csv(os.path.join(here, "../../dataset/interactions.csv"))

        self.user_collaborative_model = UserCollaborativeModel(users_df, interactions_df,
                                                               popularity_scores_df, recipes_df)  # ignoring 50% items

    def recommend_items(self, user_id, prnt=False, verbose=False):
        """
            Utilises the ItemCollaborative Model to recommend a set of items to a specified user.

            Args:
                user_id: the id of the user in question
                prnt: defaults to False
                verbose: defaults to False
        """

        recommended_items_df = self.user_collaborative_model.recommend_items(user_id, self.topu, self.topn, verbose)

        if prnt:
            print("\nHere we have the", self.topn, "recipes that we recommend to the user_id:", user_id, "\n")
            print(recommended_items_df)
            print("\nDescription of recommended_items_df: \n")
            print(recommended_items_df.describe())

        return recommended_items_df
