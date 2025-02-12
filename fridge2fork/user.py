class User:
    # represents a user with preferences and saved recipes
    def __init__(self, user_id, name, email, preferences):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.preferences = preferences
        self.saved_recipes = []

    def update_preferences(self, new_preferences):
        # updates user dietary preferences
        self.preferences = new_preferences
        return f"Preferences updated to {new_preferences}"

    def save_recipe(self, recipe):
        # saves a recipe to user's list
        self.saved_recipes.append(recipe)
        return f"Recipe {recipe.name} saved!"
