class Feedback:
    # stores and processes user feedback on recipes
    def __init__(self, feedback_id, user_id, recipe_id, rating, comments):
        self.feedback_id = feedback_id
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.rating = rating
        self.comments = comments

    def analyze_feedback(self):
        # basic sentiment analysis (just checks rating)
        return "Positive" if self.rating >= 4 else "Negative"

    def adjust_suggestions(self):
        # pretend this adjusts future recipe recommendations
        return f"Adjusting suggestions based on feedback: {self.comments}"
