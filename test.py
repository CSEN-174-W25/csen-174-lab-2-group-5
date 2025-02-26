from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__)

# Replace with environment variable for security
API_KEY = os.getenv("OPENAI_API_KEY", "Open_API_key")
client = OpenAI(api_key=API_KEY)


def get_recipes_from_ingredients(ingredients, dietary_preferences=None, feedback=None):
    """Generate formatted recipes with structured output."""
    prompt = f"""Create exactly 2 recipes using the following ingredients: {', '.join(ingredients)}.
    The format must strictly be:

    **Recipe 1: [NAME]**
    Ingredients:
    - Item 1
    - Item 2
    Instructions:
    1. Step 1
    2. Step 2

    **Recipe 2: [NAME]**
    Ingredients:
    - Item 1
    - Item 2
    Instructions:
    1. Step 1
    2. Step 2
    """

    if dietary_preferences:
        prompt += f"\nDietary Requirements: {', '.join(dietary_preferences)}"
    if feedback:
        prompt += f"\nUser Feedback for Recipe Improvement: {feedback}"

    prompt += "\n\nStrict Formatting Rules:\n- Wrap recipe names in ** **\n- Use 'Ingredients:' header\n- Use 'Instructions:' header"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a recipe formatting expert. Follow formatting rules strictly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        app.logger.error(f"API Error: {str(e)}")
        return None


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/generate-recipes", methods=["POST"])
def generate_recipes():
    try:
        data = request.json
        ingredients = [i.strip() for i in data.get("ingredients", "").split(",") if i.strip()]
        dietary_preferences = [dp.strip() for dp in data.get("dietary_preferences", "").split(",") if dp.strip()]

        if not ingredients:
            return jsonify({"error": "Please enter at least one ingredient."}), 400

        recipes = get_recipes_from_ingredients(ingredients, dietary_preferences)
        if not recipes:
            return jsonify({"error": "Failed to generate recipes. Try again later."}), 500

        return jsonify({"recipes": recipes})

    except Exception as e:
        app.logger.error(f"Error in generate_recipes: {str(e)}")
        return jsonify({"error": "An error occurred while generating recipes."}), 500


@app.route("/regenerate-recipes", methods=["POST"])
def regenerate_recipes():
    try:
        data = request.json
        ingredients = [i.strip() for i in data.get("ingredients", "").split(",") if i.strip()]
        dietary_preferences = [dp.strip() for dp in data.get("dietary_preferences", "").split(",") if dp.strip()]
        feedback = data.get("feedback", "").strip()

        if not ingredients or not feedback:
            return jsonify({"error": "Missing ingredients or feedback for regeneration."}), 400

        recipes = get_recipes_from_ingredients(ingredients, dietary_preferences, feedback)
        if not recipes:
            return jsonify({"error": "Failed to regenerate recipes. Try again later."}), 500

        return jsonify({"recipes": recipes})

    except Exception as e:
        app.logger.error(f"Error in regenerate_recipes: {str(e)}")
        return jsonify({"error": "An error occurred while regenerating recipes."}), 500


if __name__ == "__main__":
    app.run(debug=True)
