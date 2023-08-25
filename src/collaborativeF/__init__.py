from src.collaborativeF import itemCollaborativeF


def recommend_items(user_id, topn, prnt=False, verbose=False):
    return itemCollaborativeF.recommend_items(user_id, topn, prnt, verbose)
