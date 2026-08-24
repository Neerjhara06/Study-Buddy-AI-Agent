"""
evaluator.py
-------------------------------------------------------
Study Buddy AI Agent

Evaluates quiz answers.

Compatible with:
- Python 3.14.7
"""

import json
import os
from datetime import datetime

from quiz import load_quiz

# ------------------------------------------------------
# File Paths
# ------------------------------------------------------

DATA_DIR = "data"

QUIZ_HISTORY = os.path.join(
    DATA_DIR,
    "quiz_history.json"
)

PROGRESS_FILE = os.path.join(
    DATA_DIR,
    "progress.json"
)

os.makedirs(DATA_DIR, exist_ok=True)


# ------------------------------------------------------
# Load JSON
# ------------------------------------------------------

def load_json(path, default):

    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------------------
# Save JSON
# ------------------------------------------------------

def save_json(path, data):

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ------------------------------------------------------
# Main Evaluation Function
# ------------------------------------------------------

def evaluate(text, user_answers):
    """
    Parameters
    ----------
    text : str
        (Unused, kept for compatibility.)

    user_answers : list[str]
        User answers in quiz order.

    Returns
    -------
    dict
    """

    quiz = load_quiz()

    if not quiz:

        return {
            "status": "error",
            "message": "No quiz found. Generate a quiz first."
        }

    if not isinstance(user_answers, list):

        return {
            "status": "error",
            "message": "Answers must be provided as a list."
        }

    total = len(quiz)

    correct = 0

    wrong = 0

    results = []

    for i, question in enumerate(quiz):

        correct_answer = str(
            question["answer"]
        ).strip().lower()

        if i < len(user_answers):

            user = str(
                user_answers[i]
            ).strip().lower()

        else:

            user = ""

        is_correct = user == correct_answer

        if is_correct:
            correct += 1
        else:
            wrong += 1

        results.append({

            "question_no": i + 1,

            "question": question["question"],

            "correct_answer": question["answer"],

            "user_answer": user_answers[i] if i < len(user_answers) else "",

            "result": "Correct" if is_correct else "Incorrect"

        })

    score = round(
        (correct / total) * 100,
        2
    )

    save_history(score)

    update_progress(score)

    feedback = create_feedback(score)

    return {

        "status": "success",

        "score": score,

        "correct": correct,

        "wrong": wrong,

        "total": total,

        "feedback": feedback,

        "results": results

    }


# ------------------------------------------------------
# Quiz History
# ------------------------------------------------------

def save_history(score):

    history = load_json(
        QUIZ_HISTORY,
        []
    )

    history.append({

        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "score": score

    })

    save_json(
        QUIZ_HISTORY,
        history
    )


# ------------------------------------------------------
# Progress Tracker
# ------------------------------------------------------

def update_progress(score):

    progress = load_json(
        PROGRESS_FILE,
        {

            "completed_topics": [],

            "quiz_scores": [],

            "study_days": 0

        }

    )

    progress["quiz_scores"].append(score)

    progress["study_days"] += 1

    progress["average_score"] = round(

        sum(progress["quiz_scores"])
        / len(progress["quiz_scores"]),

        2

    )

    save_json(
        PROGRESS_FILE,
        progress
    )


# ------------------------------------------------------
# Feedback
# ------------------------------------------------------

def create_feedback(score):

    if score >= 90:
        return "Excellent! Outstanding performance."

    elif score >= 75:
        return "Very Good! Keep practicing."

    elif score >= 60:
        return "Good. Revise weak topics."

    elif score >= 40:
        return "Average. Spend more time revising."

    return "Needs Improvement. Review the study material."


# ------------------------------------------------------
# Pretty Print
# ------------------------------------------------------

def format_result(result):

    if result["status"] == "error":
        return result["message"]

    output = []

    output.append("=" * 60)

    output.append("QUIZ RESULT")

    output.append("=" * 60)

    output.append(f"Score : {result['score']} %")

    output.append(f"Correct : {result['correct']}")

    output.append(f"Wrong : {result['wrong']}")

    output.append(f"Total : {result['total']}")

    output.append("")

    output.append("Feedback")

    output.append(result["feedback"])

    output.append("")

    output.append("=" * 60)

    output.append("QUESTION REVIEW")

    output.append("=" * 60)

    for item in result["results"]:

        output.append(f"\nQ{item['question_no']}")

        output.append(item["question"])

        output.append(
            f"Your Answer : {item['user_answer']}"
        )

        output.append(
            f"Correct Answer : {item['correct_answer']}"
        )

        output.append(
            f"Result : {item['result']}"
        )

    return "\n".join(output)


# ------------------------------------------------------
# Testing
# ------------------------------------------------------

if __name__ == "__main__":

    answers = [

        "Artificial",

        "True",

        "Networks",

        "AI is useful.",

    ]

    result = evaluate(
        "",
        answers
    )

    print(
        format_result(result)
    )