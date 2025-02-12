class MealPlan:
    # generates and updates a user's meal plan
    def __init__(self, plan_id, user_id, recipes, schedule):
        self.plan_id = plan_id
        self.user_id = user_id
        self.recipes = recipes
        self.schedule = schedule

    def generate_meal_plan(self, preferences):
        # pretend this picks meals based on user preferences
        return [recipe for recipe in self.recipes if preferences in recipe]

    def update_meal_plan(self, plan_id, changes):
        # fake update function
        return f"Meal plan {plan_id} updated with changes: {changes}"
