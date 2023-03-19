# - The idea of a user related collaborative filtering is to suggest items basing on most similar users to us
# - Before give the idea to the user relevance we make a change in how to define rho
# - Since for this type of analysis we don't care to distinguish how the user rated the items,
#   our new rho is defined as: rho_new(k) = basel_series(k)

# - This because in this scenario we just want to give importance to how many items he rated
# - Now we can define how much a user u is relevant for our reference user u*
# - The idea is the following:
#       Given:
#           #good_items(u) = 0.75 (!!!) * #items_rated_4(u) + #items_rated_5(u)
#           #items_different(u,u*) = #items rated by u but not by u*
#           utility(u,u*) = #good_items(u) / #items_different(u,u*)
#           rating_rate(u) = #items_rated(u) / #items (!!!)
#       The relevance score is defined as following:
#           Relevance_score(u,u*) = 0, if cos_similarity(u,u*) == 1
#           Relevance_score(u,u*) = cos_similarity(u,u*) * utility(u,u*) * rho_new(u) (rating_rate(u) -> !!!), otherwise
#           (At beginning I thought about the rating rate, but the problem is that it grows too slowly compared to the
#            other two factors, so I preferred to choose something that grows with the same rate,
#            but we can still try also the other alternative)
# - we pick the P (!!!) most relevant users according to the relevance_score and for each we take M (!!!) most rated
#   (according to the item relevance score computed like this:
#   item_relevance_score =
#       rho_new(u*) * rating(item) + (1 - rho_new(u*)) * popularity_score (Normalized between 1 and 5))
#
#   In case the recommended items end up being less than M (unlikely in our use case),
#   we pick the remaining items from the Item Popularity Model.
#
#   We also have to check that all M items recommended are items not already rated by u*.
#
#
# - NB: when I wrote (!!!) I provided alternatives of different models that we can evaluate in the validation set
