import os
import pandas as pd

# path statement necessary to let the project work in different environments with respect to PyCharm
here = os.path.dirname(os.path.abspath(__file__))

# saving paths of my final CSV data
save_path_interactions = os.path.join(here, "../../dataset/interactions.csv")
save_path_users = os.path.join(here, "../../dataset/users.csv")
save_path_recipes = os.path.join(here, "../../dataset/recipes.csv")

# CSV files readings (some dataframes created here are just temporary)
temp_df_train = pd.read_csv(os.path.join(here, "../../files/interactions_train.csv"))
temp_df_valid = pd.read_csv(os.path.join(here, "../../files/interactions_validation.csv"))
temp_df_test = pd.read_csv(os.path.join(here, "../../files/interactions_test.csv"))
temp_df_RAW_interactions = pd.read_csv(os.path.join(here, "../../files/RAW_interactions.csv"))
temp_df_RAW_recipes = pd.read_csv(os.path.join(here, "../../files/RAW_recipes.csv"))
users_df = pd.read_csv(os.path.join(here, "../../files/PP_users.csv"))
recipes_df = pd.read_csv(os.path.join(here, "../../files/PP_recipes.csv"))

# the final dataframe structure will be: u, i, date, rating, review
interactions_df = pd.concat([temp_df_train, temp_df_valid, temp_df_test], ignore_index=True)
interactions_df['review'] = ""
for i in interactions_df.index:
    print("Interactions file creation in progress: " + str(i) + "/" + str(len(interactions_df.index)))
    interactions_df.at[i, 'review'] = temp_df_RAW_interactions[(temp_df_RAW_interactions['user_id'] ==
                                                                interactions_df.at[i, 'user_id']) &
                                                               (temp_df_RAW_interactions['recipe_id'] ==
                                                                interactions_df.at[i, 'recipe_id'])]['review'].values[0]
interactions_df = interactions_df.drop(['user_id', 'recipe_id'], axis=1)
print("Interactions file correctly created.")
print("Saving interactions file...")
interactions_df = interactions_df.iloc[:, [2, 3, 0, 1, 4]]
interactions_df = interactions_df.reset_index(drop=True)
interactions_df.to_csv(save_path_interactions, index=False)

# the final dataframe structure will be: u, items, ratings, n_interactions
users_df = users_df.drop(['techniques', 'n_items'], axis=1)
users_df.columns = ['u', 'items', 'ratings', 'n_interactions']
print("\nUsers file correctly created.")
print("Saving user file...")
users_df.to_csv(save_path_users, index=False)

# the final dataframe structure will be: i, name, contributor_id, tags, minutes (,submitted, nutrition, n_steps,
#                                        steps, description, ingredients, n_ingredients)
recipes_df = recipes_df.drop(['name_tokens', 'ingredient_tokens', 'steps_tokens', 'techniques', 'calorie_level',
                              'ingredient_ids'], axis=1)
recipes_df['name'] = ""
recipes_df['contributor_id'] = ""
recipes_df['tags'] = ""
recipes_df['minutes'] = ""
recipes_df['submitted'] = ""
recipes_df['nutrition'] = ""
recipes_df['n_steps'] = ""
recipes_df['steps'] = ""
recipes_df['description'] = ""
recipes_df['ingredients'] = ""
recipes_df['n_ingredients'] = ""
for i in recipes_df.index:
    print("\nRecipes file creation in progress: " + str(i) + "/" + str(len(recipes_df.index)))
    recipes_df.at[i, 'name'] = \
        temp_df_RAW_recipes[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['name'].values[0]
    recipes_df.at[i, 'contributor_id'] = \
        temp_df_RAW_recipes[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['contributor_id'].values[0]
    recipes_df.at[i, 'tags'] = \
        temp_df_RAW_recipes[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['tags'].values[0]
    recipes_df.at[i, 'minutes'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['minutes'].values[0]
    recipes_df.at[i, 'submitted'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['submitted'].values[0]
    recipes_df.at[i, 'nutrition'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['nutrition'].values[0]
    recipes_df.at[i, 'n_steps'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['n_steps'].values[0]
    recipes_df.at[i, 'steps'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['steps'].values[0]
    recipes_df.at[i, 'description'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['description'].values[0]
    recipes_df.at[i, 'ingredients'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['ingredients'].values[0]
    recipes_df.at[i, 'n_ingredients'] = \
        temp_df_RAW_recipes.loc[temp_df_RAW_recipes['id'] == recipes_df.at[i, 'id']]['n_ingredients'].values[0]
recipes_df = recipes_df.drop(['id'], axis=1)
print("Recipes file correctly created.")
print("Saving recipes file...")
recipes_df.to_csv(save_path_recipes, index=False)

