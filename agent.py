"""
agent.py
---------
Main AI Agent for Study Buddy AI Agent
Compatible with Python 3.14.7
"""

from tools import (
    summarize_notes,
    extract_topics,
    generate_quiz,
    evaluate_answer,
    generate_flashcards,
    explain_concept,
    create_revision_plan,
    get_progress,
    get_analytics,
)


def process_user_request(text: str, task: str):
    """
    Routes the user's request to the correct tool.
    """

    if not text or not text.strip():
        return "No study material found."

    try:

        # -----------------------------
        # Summary
        # -----------------------------
        if task == "summary":
            return summarize_notes(text)

        # -----------------------------
        # Topics
        # -----------------------------
        elif task == "topics":
            return extract_topics(text)

        # -----------------------------
        # Quiz
        # -----------------------------
        elif task == "quiz":
            return generate_quiz(text)

        # -----------------------------
        # Evaluate Quiz
        # -----------------------------
        elif task.startswith("evaluate:"):

            answer = task.replace("evaluate:", "", 1)

            return evaluate_answer(
                text=text,
                user_answer=answer
            )

        # -----------------------------
        # Flashcards
        # -----------------------------
        elif task == "flashcards":
            return generate_flashcards(text)

        # -----------------------------
        # Explain Concept
        # -----------------------------
        elif task.startswith("explain:"):

            concept = task.replace("explain:", "", 1)

            return explain_concept(
                text=text,
                concept=concept
            )

        # -----------------------------
        # Revision Planner
        # -----------------------------
        elif task == "planner":
            return create_revision_plan(text)

        # -----------------------------
        # Progress Tracker
        # -----------------------------
        elif task == "progress":
            return get_progress()

        # -----------------------------
        # Analytics
        # -----------------------------
        elif task == "analytics":
            return get_analytics()

        else:
            return "Invalid request."

    except Exception as e:
        return f"Error: {str(e)}"