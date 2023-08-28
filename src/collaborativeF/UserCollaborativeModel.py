import numpy as np
import pandas as pd

from src import utils
from numpy.linalg import norm

from src.popularityF import popularityF


class UserCollaborativeModel:
    MODEL_NAME = 'UserCollaborative'

    def __init__(self, users_df, interactions_test_df, popularity_df, recipes_df=None):
        """
            This class is an Item Collaborative Recommendation Model.
             It recommends based on the similarity between items.

            Args:
                users_df: a complete dataframe of all the users
                interactions_test_df: the test sub-set of interactions_df
                popularity_df: the global item popularity dataframe
                recipes_df: a complete dataframe of recipes
        """

        self.users_df = users_df
        self.interactions_test_df = interactions_test_df
        self.popularity_df = popularity_df
        self.recipes_df = recipes_df

    def get_model_name(self):
        """
            Returns:
                model_name: the name of the model
        """

        return self.MODEL_NAME

    def setup(self, user_id):
        """
            Args:
                user_id: the id of the user that the model is recommending recipes to
            Returns:
                ratings_full: a complete df of #USERS x #ITEMS containing all the ratings (including null ones)
        """

        # ids of the items rated by the reference user_id and their ratings
        reference_user_items = utils.from_string_to_int_list(self.users_df.iloc[user_id]['items'])
        reference_user_ratings = utils.from_string_to_float_list(self.users_df.iloc[user_id]['ratings'])

        # ratings of the reference user_id, but also considering non-rated items
        reference_user_ratings_full = np.zeros(len(self.recipes_df.index))

        # submitting the correct values (ratings) in reference_user_ratings_full
        for i in range(len(reference_user_items)):
            index = reference_user_items[i]
            reference_user_ratings_full[index] = reference_user_ratings[i]

        relevance_scores = []  # the relevance score of each user in respects to the reference user_id

        for u in range(len(self.users_df.index)):
            if u % 1000 == 0:
                print("Currently the user {} is being processed...".format(u))
            couple = [u]
            if u != user_id:  # case of the reference user_id's relevance to every other user "u"

                ratings_different = []
                rho = self.users_df.iloc[u]['rho']

                # ids of the items rated by each u and their ratings
                u_items = utils.from_string_to_int_list(self.users_df.iloc[u]['items'])
                u_ratings = utils.from_string_to_float_list(self.users_df.iloc[u]['ratings'])

                # ratings of u, but also considering non-rated items
                u_ratings_full = np.zeros(len(self.recipes_df.index))

                # submitting the correct values (ratings) in u_ratings_full
                for i in range(len(u_items)):
                    index = u_items[i]
                    u_ratings_full[index] = u_ratings[i]

                # retrieving the number of different items and their ids (between each user and the reference user_id)
                n_different, items_different = utils.items_difference_calculation(u_items, reference_user_items)

                # retrieving the ratings of each item in items_different
                for item in items_different:
                    ratings_different.append(u_ratings_full[item])

                # calculating the "n_good" score
                n_items4, n_items5 = utils.good_items_calculation(ratings_different)
                n_good = 0.75 * n_items4 + n_items5  # we can eventually try different models and change that 0.75

                # calculating the utility of user u
                if n_different == 0:
                    utility = 0
                else:
                    utility = n_good / n_different

                # calculating the relevance score of user u in respect to the reference user_id
                norm_prod = norm(u_ratings_full) * norm(reference_user_ratings_full)
                if norm_prod == 0:
                    cos_similarity = 0.0
                else:
                    cos_similarity = np.dot(u_ratings_full, reference_user_ratings_full) / norm_prod
                if cos_similarity == 1:
                    relevance_score = 0.0
                else:
                    relevance_score = cos_similarity * utility * rho

                # connecting (coupling) the relevance score to the respective user id
                couple.append(relevance_score)

            else:  # case of the reference user_id's relevance to itself

                # We are connecting a relevance_score of 1.0 in this case as a placeholder to recognise that
                # this current array cell (in the relevance_scores array) is referring to the reference user_id itself.
                relevance_score = 1.0

                # connecting (coupling) the relevance score to the respective user id (in this case, the reference user)
                couple.append(relevance_score)

            # appending to the relevance_scores array
            relevance_scores.append(couple)
            # relevance_scores will be a list of lists containing both the relevance_score
            # of each user (in respects to the reference user_id) and their respective user id

        relevance_scores.sort(reverse=True, key=lambda x: x[1])  # reverse ordering by rating

        return relevance_scores

    def recommend_items(self, user_id, topu=5, topn=10, verbose=False):
        """
            Args:
                user_id: the id of the user that the model is recommending recipes to
                topu: defaults to 5. Defines amount of relevant users from which to recommend recipes
                topn: defaults to 10. Defines amount of recipes to be recommended
                verbose: defaults to False
            Returns:
                recommendations_df: the topn recommended recipes
        """

        recommended_indices = []
        recommended_scores = []

        print("Calculating relevance scores in respect to our reference user.. .")

        relevance_scores = self.setup(user_id)

        # ids of the items rated by the reference user_id and their ratings
        reference_user_items = utils.from_string_to_int_list(self.users_df.iloc[user_id]['items'])
        reference_user_ratings = utils.from_string_to_float_list(self.users_df.iloc[user_id]['ratings'])
        reference_user_rho = self.users_df.iloc[user_id]['rho']

        print("Calculating the recommendations.. .")

        # Loading the popularity model and scores (for supplementing the item-recommender model)
        popularity_df = popularityF.get_popularity()
        popularity_scores = popularity_df['popularity_score'].to_numpy()

        popularity_helper = popularityF.PopularityHelper(topn)

        # Excluding items the User has already interacted with
        recipes_to_ignore = utils.get_interacted(user_id=user_id, interactions_df=self.interactions_test_df)

        relevant_users_ids = []  # the topu most relevant users
        recommended_items = []  # all the item-ids of the relevant users
        recommended_ratings = []  # the corresponding ratings

        # a list that will contain as elements an item ID (taken from recommended_items)
        # and its corresponding ratings in recommended_ratings
        recommended_item_ratings_list = []

        items_checked = []  # item IDs for which we already checked duplicates

        if len(relevance_scores) == 0:
            popular_recommended_items = popularity_helper.recommend_items(user_id, topn)
            recommended_indices = popular_recommended_items.index
            recommended_scores = popular_recommended_items.iloc['popularity_score']

        else:
            # adjusting topu based on relevant users acquired
            if len(relevance_scores) - 1 < topu:
                topu = len(relevance_scores) - 1

            for i in range(topu):
                # we skip the first one because it is the reference user
                relevant_users_ids.append(relevance_scores[i + 1][0])

            for user in relevant_users_ids:
                u_items = utils.from_string_to_int_list(self.users_df.iloc[user]['items'])
                u_ratings = utils.from_string_to_float_list(self.users_df.iloc[user]['ratings'])
                recommended_items.extend(u_items)
                recommended_ratings.extend(u_ratings)

            for item_id in recommended_items:
                # if the item has been rated multiple times we take as rating the average value of the ratings
                s, count, avg = 0, 0, 0
                if item_id not in items_checked:
                    indices = utils.find_indices(recommended_items, item_id)
                    for idx in indices:
                        if recommended_ratings[idx] != 0.0:  # we do not want to count '0.0' as rating
                            s += recommended_ratings[idx]
                            count += 1
                    if count != 0:
                        avg = s / count
                        recommended_item_ratings_list.append([item_id, avg])
                    items_checked.append(item_id)

            for item in recommended_item_ratings_list:
                if item[0] not in reference_user_items:
                    popularity_score = popularity_scores[item[0]]
                    item_score = reference_user_rho * item[1] + (1 - reference_user_rho) * popularity_score
                    recommended_indices.append(item[0])
                    recommended_scores.append(item_score)

        # Supplement recommendations from the popularity model if needed
        if len(recommended_indices) < topn:
            # Supplementing from the popularity model does not ignore the skipped items**
            popularity_helper.topn = topn - len(recommended_indices)
            items = popularity_helper.recommend_items(user_id, recommended_indices)

            recommended_indices.extend(items.index.to_list())  # recommend some items from popularity model
            recommended_scores.extend(items['popularity_score'].to_list())

        print("Items recommended: ", recommended_indices)

        recommendations_df = pd.DataFrame(data=np.array([recommended_indices, recommended_scores]).transpose(),
                                          columns=['i', 'relevance_score'])
        # turning the item ids to type int64 (they change to float in the step above -> due to numpy.array())
        recommendations_df['i'] = recommendations_df['i'].astype('int64')

        if verbose:
            recommendations_df = recommendations_df[~recommendations_df['i'].isin(recipes_to_ignore)] \
                .sort_values('relevance_score', ascending=True)

            if self.recipes_df is None:
                raise Exception('"recipes_df" is required in verbose mode')

            recommendations_df = (recommendations_df.merge(self.recipes_df, how='left',
                                                           left_on=recommendations_df['i'],
                                                           right_on='i')[
                                      ['relevance_score', 'i', 'name', 'tags', 'contributor_id', 'minutes', 'n_steps',
                                       'n_ingredients']]
                                  .sort_values('relevance_score', ascending=False)).head(topn)
        else:
            recommendations_df = recommendations_df[~recommendations_df['i'].isin(recipes_to_ignore)] \
                .sort_values('relevance_score', ascending=False) \
                .head(topn)

        return recommendations_df
