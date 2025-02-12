class Recipe:
    # represents a recipe with ingredients and instructions
    def __init__(self, recipe_id, name, ingredients, instructions):
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def get_ingredients(self):
        # returns the list of ingredients
        return self.ingredients

    def get_recipe_details(self):
        # returns a dictionary of recipe info
        return {
            "id": self.recipe_id,
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

    def is_vegetarian(self):
        # checks if recipe is vegetarian (no meat items)
        non_veg_items = ["chicken", "beef", "pork", "fish"]
        return not any(item.lower() in non_veg_items for item in self.ingredients)
