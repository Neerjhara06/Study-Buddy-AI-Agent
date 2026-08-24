"""
charts.py
-------------------------------------------------------
Study Buddy AI Agent

Progress Analytics Charts

Compatible with:
- Python 3.14.7
- matplotlib
"""

import json
import os
import matplotlib.pyplot as plt

DATA_FOLDER = "data"

PROGRESS_FILE = os.path.join(
    DATA_FOLDER,
    "progress.json"
)

QUIZ_HISTORY = os.path.join(
    DATA_FOLDER,
    "quiz_history.json"
)


# --------------------------------------------------
# Load JSON
# --------------------------------------------------

def load_json(path, default):

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return default


# --------------------------------------------------
# Quiz Scores
# --------------------------------------------------

def get_scores():

    progress = load_json(PROGRESS_FILE, {})

    return progress.get(
        "quiz_scores",
        []
    )


# --------------------------------------------------
# Analytics Report
# --------------------------------------------------

def analytics_report():

    progress = load_json(PROGRESS_FILE, {})

    scores = progress.get("quiz_scores", [])

    if scores:

        average = round(
            sum(scores) / len(scores),
            2
        )

        best = max(scores)

    else:

        average = 0

        best = 0

    report = f"""

=============================
STUDY ANALYTICS
=============================

Study Days :
{progress.get("study_days",0)}

Uploaded Files :
{progress.get("total_files_uploaded",0)}

Completed Topics :
{len(progress.get("completed_topics",[]))}

Total Quizzes :
{progress.get("total_quizzes",0)}

Average Score :
{average} %

Best Score :
{best} %

Study Time :
{progress.get("study_time_minutes",0)} minutes

"""

    return report


# --------------------------------------------------
# Score Trend
# --------------------------------------------------

def plot_score_history():

    scores = get_scores()

    if not scores:

        return None

    plt.figure(figsize=(8,4))

    plt.plot(
        range(1, len(scores)+1),
        scores,
        marker="o"
    )

    plt.title("Quiz Score History")

    plt.xlabel("Quiz Number")

    plt.ylabel("Score (%)")

    plt.grid(True)

    return plt.gcf()


# --------------------------------------------------
# Pie Chart
# --------------------------------------------------

def plot_progress_pie():

    progress = load_json(PROGRESS_FILE, {})

    completed = len(
        progress.get(
            "completed_topics",
            []
        )
    )

    remaining = max(
        1,
        20 - completed
    )

    plt.figure(figsize=(6,6))

    plt.pie(

        [completed, remaining],

        labels=[
            "Completed",
            "Remaining"
        ],

        autopct="%1.1f%%"

    )

    plt.title("Study Progress")

    return plt.gcf()


# --------------------------------------------------
# Bar Chart
# --------------------------------------------------

def plot_dashboard():

    progress = load_json(PROGRESS_FILE, {})

    labels = [

        "Study Days",

        "Files",

        "Topics",

        "Quizzes"

    ]

    values = [

        progress.get("study_days",0),

        progress.get("total_files_uploaded",0),

        len(
            progress.get(
                "completed_topics",
                []
            )
        ),

        progress.get("total_quizzes",0)

    ]

    plt.figure(figsize=(8,4))

    plt.bar(labels, values)

    plt.title("Study Dashboard")

    return plt.gcf()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print(
        analytics_report()
    )

    fig = plot_score_history()

    if fig:
        plt.show()