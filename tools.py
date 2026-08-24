from summarizer import summarize
from topics import extract
from quiz import generate
from evaluator import evaluate
from flashcards import create_flashcards
from planner import create_plan
from explain import explain_topic
from progress_tracker import load_progress
from charts import analytics_report


def summarize_notes(text):
    return summarize(text)


def extract_topics(text):
    return extract(text)


def generate_quiz(text):
    return generate(text)


def evaluate_answer(text, user_answer):
    return evaluate(text, user_answer)


def generate_flashcards(text):
    return create_flashcards(text)


def explain_concept(text, concept):
    return explain_topic(text, concept)


def create_revision_plan(text):
    return create_plan(text)


def get_progress():
    return load_progress()


def get_analytics():
    return analytics_report()