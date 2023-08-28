import os
import sys

from src.popularityF import popularityF
from src.collaborativeF import itemCollaborativeF, userCollaborativeF

sys.path.append(os.getcwd())


def main():
    user_id = 180  # our reference user ID
    topu = 5  # number of relative users to be considered by the user-collaborative model
    topn = 10  # number of recipes we recommend to user_id

    # POPULARITY MODEL DEBUG
    popularity_helper = popularityF.PopularityHelper(topn)
    recommended_with_popularity_model = (
        popularity_helper.recommend_items(user_id, prnt=True, verbose=False))

    # USER COLLABORATIVE MODEL DEBUG
    user_collaborative_helper = userCollaborativeF.UserCollaborativeHelper(topu, topn)
    recommended_with_user_collaborative_model = (
        user_collaborative_helper.recommend_items(user_id, prnt=True, verbose=True))

    # ITEM COLLABORATIVE MODEL DEBUG
    item_collaborative_helper = itemCollaborativeF.ItemCollaborativeHelper(topn)
    recommended_with_item_collaborative_model = (
        item_collaborative_helper.recommend_items(user_id, prnt=True, verbose=True))


if __name__ == "__main__":
    main()
