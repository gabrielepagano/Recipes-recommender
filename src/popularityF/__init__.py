from src.popularityF import popularityF


def recommend_items(user_id, topn, prnt=False, verbose=False):
    return popularityF.recommend_items(user_id, topn, prnt, verbose)
