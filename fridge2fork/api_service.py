import re

class APIService:
    # handles API calls to external services like OpenAI and OpenFoodFacts
    def __init__(self, api_name, api_key):
        self.api_name = api_name
        self.api_key = api_key

    def fetch_recipes(self, query):
        # pretend this makes an API call to get recipe data
        return f"Fetching recipes for {query} from {self.api_name}"

    def process_nlp(self, user_input):
        # extract potential ingredients by removing common words
        common_words = {"what", "can", "i", "cook", "with", "and"}
        words = re.findall(r'\b\w+\b', user_input.lower())  # extract words
        filtered_words = [word for word in words if word not in common_words]
        return filtered_words
