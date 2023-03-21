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
#   (according to the item relevance score computed like this:
#   item_relevance_score =
#       rho_new(u*) * rating(item) + (1 - rho_new(u*)) * popularity_score (Normalized between 1 and 5))
#
#   In case the recommended items end up being less than M (unlikely in our use case),
#   we pick the remaining items from the Item Popularity Model.
#
#   We also have to check that all M items recommended are items not already rated by u*.
#
#
# - NB: when I wrote (!!!) I provided alternatives of different models that we can evaluate in the validation set
import numpy as np
import pandas as pd
from src import utils
from numpy.linalg import norm

u_id = 8903  # our reference user. I found out that the more items rated a user has, the lower will be the highest relevance
# scores for him; but at the same time the fewer items rated he has, the lower will be the number of non-zero
# relevance scores
users_df = pd.read_csv("../../dataset/users.csv")
recipes_df = pd.read_csv("../../dataset/recipes.csv")
relevance_scores = []
uid_items = utils.fromStringToIntList(users_df.iloc[u_id]['items'])  # ids of the items rated by u_id
uid_ratings = utils.fromStringToFloatList(users_df.iloc[u_id]['ratings'])
uid_ratings_full = np.zeros(len(recipes_df.index))  # ratings of uid, but also considering non-rated items
for i in range(len(uid_items)):
    index = uid_items[i]
    uid_ratings_full[index] = uid_ratings[i]
for u in range(len(users_df.index)):
    print("Currently the user {} is being processed...".format(u))
    couple = [u]
    if u != u_id:
        ratings_different = []
        rho = users_df.iloc[u]['rho']
        u_items = utils.fromStringToIntList(users_df.iloc[u]['items'])  # ids of the items rated by u
        u_ratings = utils.fromStringToFloatList(users_df.iloc[u]['ratings'])
        u_ratings_full = np.zeros(len(recipes_df.index))  # ratings of u, but also considering non-rated items
        for i in range(len(u_items)):
            index = u_items[i]
            u_ratings_full[index] = u_ratings[i]
        n_different, items_different = utils.itemsDifferenceCalculation(u_items, uid_items)
        for item in items_different:
            ratings_different.append(u_ratings_full[item])
        n_items5, n_items6 = utils.goodItemsCalculation(ratings_different)
        n_good = 0.75 * n_items5 + n_items6  # we can eventually try different models and change that 0.75
        if n_different == 0:
            utility = 0
        else:
            utility = n_good / n_different
        norm_prod = norm(u_ratings_full) * norm(uid_ratings_full)
        if norm_prod == 0:
            cos_similarity = 0.0
        else:
            cos_similarity = np.dot(u_ratings_full, uid_ratings_full) / norm_prod
        if cos_similarity == 1:
            relevance_score = 0.0
        else:
            relevance_score = cos_similarity * utility * rho
        couple.append(relevance_score)
    else:
        couple.append(1.0)  # A value that would be impossible to obtain. It's just a placeholder that we need
        # to understand that the current array cell we are considering in the relevance_scores
        # array is referred to the reference user itself.
    relevance_scores.append(couple)  # relevance_scores will be a list of lists containing both the relevance_score of
    # that specific user and its user ID

relevance_scores.sort(reverse=True, key=lambda x: x[1])  # reverse ordering by rating
