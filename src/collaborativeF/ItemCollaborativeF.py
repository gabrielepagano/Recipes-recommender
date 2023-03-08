# The main idea of this algorithm is to recommend to a user an item basing on its 'relevance score'. But what is
# a relevance score? It is a score assigned to each item (once the user is fixed) that takes into account both how much
# the single item is popular and how the same item is relevant for the user. Here is the algorithm procedure:


# - We have a personalization coefficient 0 <= rho <= 1
# - This coefficient indicates how much we have to take into account the "personalized" recommendation with respect to
#   the popular one (which will have (1 - rho) as coefficient)
# - The rho is different from each user, and it increases basing on how many high rated reviews he made
#   (we avoid to consider both the comments and the low rated reviews because the first ones are useless in the
#   recommendation decision and the second ones because we do not want to recommend something to a user basing on some
#   poorly rated items).
# - TODO: we have to decide the formula to increase the rho. I was thinking about a slighter increase for the 4.0 ratings
#           and a faster one for the 5.0 ones but for sure if the user has no ratings >= 4.0 he will have rho = 0.
# - This because we want to give a more personalized recommendation to a user that "knows what he wants".
# - After have assigned the rho, we compute the similarity (TODO: we have to decide which type of similarity)
#   between the M items he didn't rate and the N ones with the highest relevance score, computed
#   using a weighted sum between the normalized popularity score (from 1 to 5) and the score he assigned to them
#   (TODO: we have to decide N, we can also try different ones and compare in some histograms)
# - We will have a NxM matrix and from this we will take P items (TODO: decide P and the criterion to choose them)
#   to recommend to the user
