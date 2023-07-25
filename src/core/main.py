import os
import sys

sys.path.append(os.getcwd())
from src.popularityF import popularityF


def main():
    u_id = 180  # our reference user ID
    topn = 20  # number of recipes we recommend to u_id

    recommended_with_popularity_df = popularityF.recommend_items(u_id, topn, prnt=True, verbose=False)


if __name__ == "__main__":
    main()
