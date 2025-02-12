import pytest
from fridge2fork.user import User

def test_update_preferences_change():
    user = User(1, "Fernando", "f@example.com", "vegan")
    assert "updated" in user.update_preferences("gluten-free")

def test_save_recipe_1():
    user = User(2, "Kian", "k@example.com", "vegetarian")
    recipe = type("Recipe", (), {"name": "Pasta"})  # mock recipe object
    assert "saved" in user.save_recipe(recipe)

def test_update_preferences_correct_return():
    user = User(1, "Fernando", "fernando@example.com", "vegan")
    assert user.update_preferences("gluten-free") == "Preferences updated to gluten-free"

def test_save_recipe_2():
    user = User(2, "Kian", "kian@example.com", "vegetarian")
    
    class MockRecipe:  # creating a fake recipe object
        def __init__(self, name):
            self.name = name

    recipe = MockRecipe("Vegan Tacos")
    assert user.save_recipe(recipe) == "Recipe Vegan Tacos saved!"

def test_initial_saved_recipes_empty():
    user = User(3, "Sofia", "sofia@example.com", "paleo")
    assert user.saved_recipes == []