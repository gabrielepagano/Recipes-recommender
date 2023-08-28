from scipy.sparse import csr_matrix

from src import utils
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

from src.popularityF import popularityF


class ItemCollaborativeModel:
    MODEL_NAME = 'ItemCollaborative'

    def __init__(self, users_df, interactions_test_df, popularity_df, recipes_df=None, subset=0.3):
        """
            This class is an Item Collaborative Recommendation Model.
             It recommends based on the similarity between items.

            Args:
                users_df: a complete dataframe of all the users
                interactions_test_df: the test sub-set of interactions_df
                popularity_df: the global item popularity dataframe
                recipes_df: a complete dataframe of recipes
                subset: a fraction of items to be algorithmically ignored by the model for faster recommendations
        """

        # initializing a few lists (used for speed optimizations)
        self.selected_items_ids = None
        self.ignored_items_ids = None
        self.selected_items = None
        self.ignored_items = None

        self.users_df = users_df
        self.interactions_test_df = interactions_test_df
        self.popularity_df = popularity_df
        self.recipes_df = recipes_df
        self.subset = subset

        # Set up the complete Item-User-Ratings dataframe
        self.ratings_full = self.setup()

    def get_model_name(self):
        """
            Returns:
                model_name: the name of the model
        """

        return self.MODEL_NAME

    def setup(self):
        """
            Returns:
                ratings_full: a complete df of #USERS x #ITEMS containing all the ratings (including null ones)
        """

        # Take a (random) subset of the items based on the model's subset percentage
        # Different algorithms may be used for this filter, possibly even considering a mixed-approach
        # with a Content-Based Recommendation Model
        self.ignored_items = self.recipes_df.sample(frac=self.subset)
        self.selected_items = self.recipes_df.drop(self.ignored_items.index)
        self.ignored_items_ids = self.ignored_items['i'].to_list()
        self.selected_items_ids = self.selected_items['i'].to_list()

        item_map = [-1] * len(self.recipes_df.index)  # helper mapping list for faster computation (python bad at loops)
        for i in self.recipes_df['i']:
            try:
                item_map[int(i)] = self.selected_items_ids.index(int(i))  # avoiding to .index() search in the big loop*
            except ValueError:
                pass

            # A full matrix of item ratings for each user: #ITEMS x #USERS
        ratings_full = [np.zeros(len(self.selected_items_ids))] * len(self.users_df.index)

        for u in range(len(self.users_df.index)):
            if u % 1000 == 0:
                print("Filling Interactions Matrix, currently processing ratings for entry {}.".format(u))

            # The ids of the items rated by each user
            u_items = utils.from_string_to_int_list(
                self.users_df.iloc[u]['items'])

            # The ratings of each user
            u_ratings = utils.from_string_to_float_list(self.users_df.iloc[u]['ratings'])

            # Assign correct ratings to the ratings_full matrix
            for i in range(len(u_items)):
                index = u_items[i]  # get the index of the item in the full-items dataset

                if item_map[index] < 0:  # (directly accessing items from the mapping instead of searching in list)*
                    continue  # skip the items in the ignored list

                # map the index to the filtered list
                index = item_map[index]  # (directly accessing items from the mapping instead of searching in list)*
                ratings_full[u][index] = u_ratings[i]

        print("Matrix Size:", len(ratings_full[0]), "X", len(ratings_full))

        return np.transpose(ratings_full)

    def recommend_items(self, user_id, topn=10, verbose=False):
        """
            Args:
                user_id: the id of the user that the model is recommending recipes to
                topn: defaults to 10. Defines amount of recipes to be recommended.
                verbose: defaults to False
            Returns:
                recommendations_df: the topn recommended recipes
        """

        print("Optimizing the dataset.. .")

        # Loading the popularity model and scores (for supplementing the item-recommender model)
        popularity_df = popularityF.get_popularity()
        popularity_scores = popularity_df['popularity_score'].to_numpy()

        # Excluding items the User has already interacted with
        recipes_to_ignore = utils.get_interacted(user_id=user_id, interactions_df=self.interactions_test_df)

        # User's interaction data
        user_ratings = np.transpose(self.ratings_full)[user_id]

        # N rated items of the User in question
        top_rated_items = []

        # The relevance score of each of the N items
        relevance_scores = []

        rho = self.users_df.iloc[user_id]['rho_positive']

        # Retrieving the N rated-items of the user in question
        for u_rating_index in range(len(user_ratings)):
            if user_ratings[u_rating_index] > 0:
                top_rated_items.append(u_rating_index)
                relevance_scores.append(rho * user_ratings[u_rating_index] +
                                        (1 - rho) * popularity_scores[u_rating_index])

        top_rated_items, relevance_scores = (list(t) for t in zip(*sorted(zip(top_rated_items, relevance_scores))))

        top_rated_items = top_rated_items[:topn]

        csr_sample = csr_matrix(self.ratings_full)

        print("Preparing the KNN Model.. .")

        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
        knn.fit(csr_sample)

        print("Calculating items to recommend.. .")

        recommended_distances = []
        recommended_indices = []
        for i in top_rated_items:  # N items

            # similarity between N items and the rest (M)
            distances, indices = knn.kneighbors(csr_sample[i], n_neighbors=10)

            # Selecting the recommended indices
            indices = indices.flatten()
            indices = indices[1:]
            recommended_indices.extend([self.selected_items_ids[x] for x in indices])

            # Selecting the respective distances
            distances = distances.flatten()
            distances = distances[1:]
            recommended_distances.extend(distances)

        # removing duplicates and reformatting the lists
        _recommended_indices = []
        _recommended_distances = []

        for (i, j) in zip(recommended_indices, recommended_distances):
            if i not in _recommended_indices:
                _recommended_indices.append(i)
                _recommended_distances.append(j)

        recommended_indices = [int(x) for x in _recommended_indices]
        recommended_distances = [5 - x for x in _recommended_distances]  # reformatting distances (most relevant == 5)

        # Supplement recommendations from the popularity model if needed
        if len(recommended_indices) < topn:
            # Supplementing from the popularity model does not ignore the skipped items**
            popularity_helper = popularityF.PopularityHelper(topn - len(recommended_indices))
            items = popularity_helper.recommend_items(user_id, recommended_indices)

            recommended_indices.extend(items.index.to_list())  # recommend some items from popularity model
            recommended_distances.extend(items['popularity_score'].to_list())

        print("Items to be recommended: ", recommended_indices)

        recommendations_df = pd.DataFrame(data=np.array([recommended_indices, recommended_distances]).transpose(),
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
