from openai import OpenAI
import requests

# Set your API keys
OPENAI_API_KEY = "KEY"
OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product/"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_recipes_from_ingredients(ingredients, dietary_preferences=None):
    """
    Use OpenAI's API to generate recipes based on ingredients and dietary preferences.
    """
    prompt = f"What can I cook with {', '.join(ingredients)}? Provide detailed recipes."
    if dietary_preferences:
        prompt += f" The recipes should be {', '.join(dietary_preferences)}."

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides recipes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def get_nutritional_info(food_item):
    """
    Fetch nutritional information using OpenFoodFacts API.
    """
    response = requests.get(f"{OPENFOODFACTS_API_URL}{food_item}.json")
    if response.status_code == 200:
        data = response.json()
        if data.get("product"):
            return data["product"].get("nutriments", {})
    return None

def filter_recipes_by_diet(recipes, dietary_preferences):
    """
    Filter recipes based on dietary preferences (e.g., vegan, gluten-free).
    """
    filtered_recipes = []
    for recipe in recipes:
        if all(preference.lower() in recipe.lower() for preference in dietary_preferences):
            filtered_recipes.append(recipe)
    return filtered_recipes

def food_planning(recipes, days):
    """
    Basic food planning tool to suggest recipes for a given number of days.
    """
    plan = {}
    for day in range(1, days + 1):
        plan[f"Day {day}"] = recipes[(day - 1) % len(recipes)]
    return plan

def main():
    # User input for ingredients
    user_input = input("What ingredients do you have? (e.g., chicken, spinach, rice) or type 'none': ")
    ingredients = [ingredient.strip() for ingredient in user_input.split(",")] if user_input.lower() != "none" else []

    # User input for dietary preferences
    dietary_preferences = input("Any dietary preferences? (e.g., vegan, gluten-free, low-carb) or type 'none': ")
    dietary_preferences = [preference.strip() for preference in dietary_preferences.split(",")] if dietary_preferences.lower() != "none" else None

    # Get recipes
    if ingredients:
        recipes = get_recipes_from_ingredients(ingredients, dietary_preferences)
        print("\nGenerated Recipes:\n", recipes)

        # Filter recipes if dietary preferences are provided
        if dietary_preferences:
            recipes_list = recipes.split("\n")
            filtered_recipes = filter_recipes_by_diet(recipes_list, dietary_preferences)
            print("\nFiltered Recipes:\n", "\n".join(filtered_recipes))
    else:
        print("No ingredients provided. Exiting recipe generation.")

    # Get nutritional info for a specific food item
    food_item = input("\nEnter a food item to get nutritional info (e.g., rice) or type 'none': ")
    if food_item.lower() != "none":
        nutritional_info = get_nutritional_info(food_item)
        if nutritional_info:
            print(f"\nNutritional Info for {food_item}:\n", nutritional_info)
        else:
            print("No nutritional information found.")
    else:
        print("Skipping nutritional info.")

    # Food planning
    days_input = input("\nHow many days do you want to plan meals for? (Enter a number or type 'none'): ")
    if days_input.lower() != "none":
        days = int(days_input)
        meal_plan = food_planning(recipes.split("\n"), days)
        print("\nMeal Plan:")
        for day, recipe in meal_plan.items():
            print(f"{day}: {recipe}")
    else:
        print("Skipping meal planning.")

if __name__ == "__main__":
    main()
