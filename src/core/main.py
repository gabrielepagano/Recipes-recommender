import os
import sys

from src.popularityF import popularityF
from src.collaborativeF import itemCollaborativeF

sys.path.append(os.getcwd())


def main():
    u_id = 180  # our reference user ID
    topn = 10  # number of recipes we recommend to u_id
    recommended_with_popularity_model = popularityF.recommend_items(u_id, topn, prnt=True, verbose=False)

    recommended_with_item_collaborative_model = itemCollaborativeF.recommend_items(u_id, topn, prnt=True, verbose=True)


if __name__ == "__main__":
    main()
