import os
import sys

from src.popularityF import popularityF
from src.collaborativeF import itemCollaborativeF

sys.path.append(os.getcwd())


def main():
    u_id = 180  # our reference user ID
    topn = 10  # number of recipes we recommend to u_id

    popularity_helper = popularityF.PopularityHelper(topn)
    recommended_with_popularity_model = (
        popularity_helper.recommend_items(u_id, prnt=True, verbose=False))

    item_collaborative_helper = itemCollaborativeF.ItemCollaborativeHelper(topn)
    recommended_with_item_collaborative_model = (
        item_collaborative_helper.recommend_items(u_id, prnt=True, verbose=True))


if __name__ == "__main__":
    main()
