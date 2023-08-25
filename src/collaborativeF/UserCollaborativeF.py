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
import numpy as np
import pandas as pd

from src import utils
from src import popularityF
from numpy.linalg import norm

u_id = 180  # our reference user ID
users_df = pd.read_csv("../../dataset/users.csv")
recipes_df = pd.read_csv("../../dataset/recipes.csv")
relevance_scores = []
uid_items = utils.from_string_to_int_list(users_df.iloc[u_id]['items'])  # ids of the items rated by u_id
uid_ratings = utils.from_string_to_float_list(users_df.iloc[u_id]['ratings'])
uid_rho = users_df.iloc[u_id]['rho']
uid_ratings_full = np.zeros(len(recipes_df.index))  # ratings of uid, but also considering non-rated items
for i in range(len(uid_items)):
    index = uid_items[i]
    uid_ratings_full[index] = uid_ratings[i]
for u in range(len(users_df.index)):
    if u % 1000 == 0:
        print("Currently the user {} is being processed...".format(u))
    couple = [u]
    if u != u_id:
        ratings_different = []
        rho = users_df.iloc[u]['rho']
        u_items = utils.from_string_to_int_list(users_df.iloc[u]['items'])  # ids of the items rated by u
        u_ratings = utils.from_string_to_float_list(users_df.iloc[u]['ratings'])
        u_ratings_full = np.zeros(len(recipes_df.index))  # ratings of u, but also considering non-rated items
        for i in range(len(u_items)):
            index = u_items[i]
            u_ratings_full[index] = u_ratings[i]
        n_different, items_different = utils.items_difference_calculation(u_items, uid_items)
        for item in items_different:
            ratings_different.append(u_ratings_full[item])
        n_items4, n_items5 = utils.good_items_calculation(ratings_different)
        n_good = 0.75 * n_items4 + n_items5  # we can eventually try different models and change that 0.75
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

# for the moment let's suppose P = 5, M = 10 and that the popularity score is always 2.5 (We need the popularity model
# that hasn't been implemented yet)
P = 5  # (!!!)
M = 10  # (!!!)
full_popularity_model = popularityF.get_popularity()
relevant_users_ids = []
total_items = []  # all the items ids of the relevant users
total_ratings = []  # the corresponding ratings
item_ratings_list = []  # a list that will contain as elements an item ID (taken from total_items)
# and its corresponding ratings in total_ratings
items_checked = []  # item IDs for which we already checked duplicates
count = 0  # number of times that the current item ID is present in total_items
if len(relevance_scores) == 0:
    print("\nHere there are the suggested items for user n° {}:\n".format(u_id))
    popular_recommended_items = popularityF.recommend_items(u_id, M)
    ids = popular_recommended_items.index
    for i in ids:
        print("Item n° {}   --->   Score: {}".format(i, popular_recommended_items.iloc[i]['popularity_score']))
else:
    if len(relevance_scores) - 1 < P:
        P = len(relevance_scores) - 1
    for i in range(P):
        relevant_users_ids.append(relevance_scores[i + 1][0])  # we skip the first one because it is the reference user
    for user in relevant_users_ids:
        u_items = utils.from_string_to_int_list(users_df.iloc[user]['items'])
        u_ratings = utils.from_string_to_float_list(users_df.iloc[user]['ratings'])
        total_items = total_items + u_items
        total_ratings = total_ratings + u_ratings
    for item in total_items:
        item_ratings = []  # the single item appended in item_ratings_list
        s = 0
        count = 0
        avg = 0
        if item not in items_checked:
            indices = utils.find_indices(total_items,
                                         item)  # if the item has been rated multiple times we take as rating
            # the average of its ratings
            for idx in indices:
                if total_ratings[idx] != 0.0:  # we do not want to count '0.0' as rating
                    s += total_ratings[idx]
                    count += 1
            if count != 0:
                avg = s / count
                item_ratings.append(item)
                item_ratings.append(avg)
                item_ratings_list.append(item_ratings)
            items_checked.append(item)

    item_relevance_scores = []  # the single element of this list is a couple <item, relevance_score>
    for elem in item_ratings_list:
        if elem[0] not in uid_items:
            popularity_score = full_popularity_model.iloc[elem[0]]['popularity_score']
            item_relevance_score = [elem[0]]
            item_score = uid_rho * elem[1] + (1 - uid_rho) * popularity_score
            item_relevance_score.append(item_score)
            item_relevance_scores.append(item_relevance_score)

item_relevance_scores.sort(reverse=True, key=lambda x: x[1])  # reverse ordering by item_relevance_score
if len(item_relevance_scores) < M:
    n_items = M - len(item_relevance_scores)
    items_to_be_picked = []
    recommended_items = []
    relevant_items = []
    for ele in item_relevance_scores:
        relevant_items.append(ele[0])
    count = 0
    # we assume that never happens that the user has already interacted with all the existing items in the database
    for ind in full_popularity_model.index:
        if ind not in relevant_items and ind not in uid_items:
            items_to_be_picked.append(ind)
            count += 1
            if count == n_items:
                break
    for i in items_to_be_picked:
        recommended_item = [i, full_popularity_model.iloc[i]['popularity_score']]
        recommended_items.append(recommended_item)
    print("\nHere there are the suggested items for user n° {}:\n".format(u_id))
    for item in item_relevance_scores:
        print("Item n° {}   --->   Score: {}".format(item[0], item[1]))
    for item in recommended_items:
        print("Item n° {}   --->   Score: {} (chosen from popularity model)".format(item[0], item[1]))
else:
    item_relevance_scores = item_relevance_scores[0:M]
    print("\nHere there are the suggested items for user n° {}:\n".format(u_id))
    for item in item_relevance_scores:
        print("Item n° {}   --->   Score: {}".format(item[0], item[1]))
