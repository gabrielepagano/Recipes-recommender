from src import utils


class PopularityModel:
    MODEL_NAME = 'Popularity'

    def __init__(self, interactions_test_df, popularity_df, recipes_df=None):
        """
            This class is a Popularity Recommendation Model. It recommends based on the global popularity of items

            Args:
                interactions_test_df: the test sub-set of interactions_df
                popularity_df: the global item popularity dataframe
                recipes_df: a complete dataframe of recipes
        """

        self.interactions_test_df = interactions_test_df
        self.popularity_df = popularity_df
        self.recipes_df = recipes_df

    def get_model_name(self):
        """
            Returns:
                model_name: the name of the model
        """

        return self.MODEL_NAME

    #TODO: implement an overloading method in case we need a popularity model without necessarily considering a specific user
    def recommend_items(self, user_id, topn=10, verbose=False):
        """
            Args:
                user_id: the id of the user that the model is recommending recipes to
                topn: defaults to 10. Defines amount of recipes to be recommended. If '-1' it returns the full
                      popularity model
                verbose: defaults to False
            Returns:
                recommendations_df: the topn recommended recipes
        """

        # Recommend the more popular recipes that the user hasn't seen yet.
        recipes_to_ignore = utils.get_interacted(user_id=user_id, interactions_df=self.interactions_test_df)
        if topn != -1:
            recommendations_df = self.popularity_df[~self.popularity_df.index.isin(recipes_to_ignore)] \
                .sort_values('popularity_score', ascending=False) \
                .head(topn)
        # consider to add the recipes to ignore instead of doing the check in the UserCollaborative filtering file
        else:
            recommendations_df = self.popularity_df.sort_values('popularity_score', ascending=False)

        if verbose:
            if self.recipes_df is None:
                raise Exception('"recipes_df" is required in verbose mode')

            recommendations_df = recommendations_df.merge(self.recipes_df, how='left',
                                                          left_on=recommendations_df.index,
                                                          right_on='i')[
                ['popularity_score', 'i', 'name', 'tags', 'contributor_id', 'minutes', 'n_steps', 'n_ingredients']]

        return recommendations_df
