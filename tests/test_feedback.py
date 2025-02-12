import pytest
from fridge2fork.feedback import Feedback

def test_positive_feedback():
    feedback = Feedback(1, 1, 1, 5, "Great recipe!")
    assert feedback.analyze_feedback() == "Positive"

def test_negative_feedback():
    feedback = Feedback(2, 2, 2, 2, "Not good")
    assert feedback.analyze_feedback() == "Negative"

def test_adjust_suggestions():
    feedback = Feedback(3, 3, 3, 4, "Loved it!")
    assert "Adjusting suggestions" in feedback.adjust_suggestions()

def test_sentiment_analysis_positive():
    feedback = Feedback(4, 4, 4, 5, "Amazing!")
    assert feedback.analyze_feedback() == "Positive"

def test_sentiment_analysis_negative():
    feedback = Feedback(5, 5, 5, 3, "Could be better")
    assert feedback.analyze_feedback() == "Negative"