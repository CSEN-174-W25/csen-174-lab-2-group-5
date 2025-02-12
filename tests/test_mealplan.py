import pytest
from fridge2fork.mealplan import MealPlan

def test_generate_meal_plan():
    mealplan = MealPlan(1, 1, ["Pasta", "Salad"], "Weekly")
    assert mealplan.generate_meal_plan("Pasta") == ["Pasta"]

def test_update_meal_plan():
    mealplan = MealPlan(2, 2, ["Soup"], "Daily")
    assert "updated" in mealplan.update_meal_plan(2, "Add Sandwich")

def test_generate_meal_plan_with_multiple_recipes():
    mealplan = MealPlan(201, 1, ["Salad", "Pasta", "Rice Bowl"], "Weekly")
    assert mealplan.generate_meal_plan("Pasta") == ["Pasta"]

def test_update_meal_plan_with_changes():
    mealplan = MealPlan(202, 2, ["Burger", "Soup"], "Daily")
    assert mealplan.update_meal_plan(202, "Add Pizza") == "Meal plan 202 updated with changes: Add Pizza"

def test_mealplan_schedule():
    mealplan = MealPlan(203, 3, ["Oatmeal", "Smoothie"], "Morning")
    assert mealplan.schedule == "Morning"