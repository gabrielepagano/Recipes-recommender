# The main idea of this algorithm is to recommend to a user an item basing on its 'relevance score'. But what is
# a relevance score? It is a score assigned to each item (once the user is fixed) that takes into account both how much
# the single item is popular and how the same item is relevant for the user. The formula of the
# relevance score is the following: relevance_score = rho * personal_score + (1 - rho) * popularity_score.
# Here is the algorithm procedure:
#
# - We have a personalization coefficient 0 <= rho <= 1
# - This coefficient indicates how much we have to take into account the "personalized" recommendation with respect to
#   the popular one (which will have (1 - rho) as coefficient)
# - The rho is different from each user, and it increases basing on how many high rated reviews he made
#   (we avoid to consider both the comments and the low rated reviews because the first ones are useless in the
#   recommendation decision and the second ones because we do not want to recommend something to a user basing on some
#   poorly rated items).
# - This because we want to give a more personalized recommendation to a user that "knows what he wants".
# - A possible way to increase rho can be to exploit the telescoping mathematical series 1 / [n * (n+1)] and
#   6/pi^2 * 1/n^2 which both converge to 1. The idea is to update the rho, after k ratings of the user which are either
#   4 or 5, by considering the weighted sum of the k-th term of the telescoping series and the k-th term of the other one
#   where the weights are, respectively, the number of 4-rated items and the number of 5-rated items.

# Telescop_series(n) = 1 / [n * (n+1)] (Telescop_series(3) = 1/2 + 1/6 + 1/12)
# Basel_series(n) = 6/pi^2 * 1/n^2
# n = N_4 + N_5
# rho(n) = (N_4 * Telescop_series(n) + N_5 * Telescop_series(n)) / (N_4 + N_5)

# - After have assigned the rho, we compute the cosine similarity between the M items he didn't rate and the N ones
#   with the highest relevance score, computed using a weighted sum between the normalized popularity score
#   (from 1 to 5) and the score he assigned to them (we can also try different values of N and compare in some histograms)
# - We will have a NxM matrix and from this we will take the P items with the highest similarity to recommend
#   to the user (we will try different P in order to compute metrics Recall@P and NDCG@P with different values)
