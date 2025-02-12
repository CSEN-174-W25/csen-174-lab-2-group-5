import pytest
from fridge2fork.recipe import Recipe

def test_get_ingredients():
    recipe = Recipe(101, "Salad", ["Lettuce", "Tomato"], "Mix together.")
    assert "Lettuce" in recipe.get_ingredients()

def test_get_recipe_details():
    recipe = Recipe(102, "Soup", ["Broth", "Carrots"], "Heat and serve.")
    assert recipe.get_recipe_details()["name"] == "Soup"

def test_is_vegetarian_true():
    recipe = Recipe(103, "Veggie Stir Fry", ["Broccoli", "Carrots"], "Stir-fry.")
    assert recipe.is_vegetarian() is True

def test_is_vegetarian_false():
    recipe = Recipe(104, "Chicken Curry", ["Chicken", "Spices"], "Cook and serve.")
    assert recipe.is_vegetarian() is False

def test_recipe_get_details():
    recipe = Recipe(106, "Avocado Toast", ["Avocado", "Bread"], "Toast bread, add avocado.")
    details = recipe.get_recipe_details()
    assert details["id"] == 106
    assert details["name"] == "Avocado Toast"
    assert details["instructions"] == "Toast bread, add avocado."