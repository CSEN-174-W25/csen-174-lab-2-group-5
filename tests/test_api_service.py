import pytest
from fridge2fork.api_service import APIService

def test_fetch_recipes():
    api = APIService("OpenAI", "fake_key")
    result = api.fetch_recipes("pasta")
    assert "pasta" in result

def test_process_nlp():
    api = APIService("OpenAI", "fake_key")
    result = api.process_nlp("What can I cook with eggs and spinach?")
    assert "eggs" in result
    assert "spinach" in result

def test_fetch_recipes_with_chicken():
    api = APIService("OpenAI", "fake_key")
    assert api.fetch_recipes("chicken") == "Fetching recipes for chicken from OpenAI"

def test_process_nlp_handles_empty_string():
    api = APIService("OpenAI", "fake_key")
    assert api.process_nlp("") == []

def test_process_nlp_parses_input():
    api = APIService("OpenAI", "fake_key")
    result = api.process_nlp("How do I make a sandwich?")
    assert "sandwich" in result