from src.popularityF import popularityF


def get_popularity(verbose=False):
    return popularityF.get_popularity(verbose)


def recommend_items(user_id, topn, prnt=False, verbose=False):
    return popularityF.recommend_items(user_id, topn, prnt, verbose)
