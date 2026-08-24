"""
progress_tracker.py
-------------------------------------------------------
Study Buddy AI Agent

Tracks study progress and statistics.

Compatible with:
- Python 3.14.7
"""

import json
import os
from datetime import datetime

DATA_FOLDER = "data"
PROGRESS_FILE = os.path.join(DATA_FOLDER, "progress.json")


DEFAULT_PROGRESS = {
    "study_days": 0,
    "total_files_uploaded": 0,
    "completed_topics": [],
    "quiz_scores": [],
    "average_score": 0,
    "best_score": 0,
    "last_score": 0,
    "total_quizzes": 0,
    "study_time_minutes": 0,
    "files": [],
    "last_study_date": ""
}


# -------------------------------------------------
# Create data folder
# -------------------------------------------------

os.makedirs(DATA_FOLDER, exist_ok=True)


# -------------------------------------------------
# Save Progress
# -------------------------------------------------

def save_progress(progress):

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            progress,
            file,
            indent=4,
            ensure_ascii=False
        )


# -------------------------------------------------
# Load Progress
# -------------------------------------------------

def load_progress():

    if not os.path.exists(PROGRESS_FILE):

        save_progress(DEFAULT_PROGRESS)

        return DEFAULT_PROGRESS.copy()

    try:

        with open(
            PROGRESS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            progress = json.load(file)

    except Exception:

        save_progress(DEFAULT_PROGRESS)

        return DEFAULT_PROGRESS.copy()

    # Add missing keys automatically
    for key, value in DEFAULT_PROGRESS.items():

        if key not in progress:
            progress[key] = value

    return progress


# -------------------------------------------------
# Record File Upload
# -------------------------------------------------

def add_uploaded_file(filename):

    progress = load_progress()

    if filename not in progress["files"]:

        progress["files"].append(filename)

        progress["total_files_uploaded"] = len(
            progress["files"]
        )

    save_progress(progress)


# -------------------------------------------------
# Record Completed Topic
# -------------------------------------------------

def complete_topic(topic):

    progress = load_progress()

    if topic not in progress["completed_topics"]:

        progress["completed_topics"].append(topic)

    save_progress(progress)


# -------------------------------------------------
# Record Study Time
# -------------------------------------------------

def add_study_time(minutes):

    progress = load_progress()

    progress["study_time_minutes"] += minutes

    save_progress(progress)


# -------------------------------------------------
# Record Quiz Result
# -------------------------------------------------

def update_quiz(score):

    progress = load_progress()

    progress["quiz_scores"].append(score)

    progress["last_score"] = score

    progress["total_quizzes"] += 1

    progress["average_score"] = round(

        sum(progress["quiz_scores"]) /
        len(progress["quiz_scores"]),

        2

    )

    progress["best_score"] = max(
        progress["quiz_scores"]
    )

    today = datetime.now().strftime("%Y-%m-%d")

    if progress["last_study_date"] != today:

        progress["study_days"] += 1

        progress["last_study_date"] = today

    save_progress(progress)


# -------------------------------------------------
# Dashboard Statistics
# -------------------------------------------------

def get_dashboard():

    progress = load_progress()

    dashboard = {

        "Study Days":
            progress["study_days"],

        "Uploaded Files":
            progress["total_files_uploaded"],

        "Completed Topics":
            len(progress["completed_topics"]),

        "Total Quizzes":
            progress["total_quizzes"],

        "Average Score":
            progress["average_score"],

        "Best Score":
            progress["best_score"],

        "Last Score":
            progress["last_score"],

        "Study Time":
            progress["study_time_minutes"]

    }

    return dashboard


# -------------------------------------------------
# Pretty Dashboard
# -------------------------------------------------

def dashboard_text():

    d = get_dashboard()

    return f"""
========================================

        STUDY DASHBOARD

========================================

Study Days           : {d['Study Days']}

Uploaded Files       : {d['Uploaded Files']}

Completed Topics     : {d['Completed Topics']}

Total Quizzes        : {d['Total Quizzes']}

Average Score        : {d['Average Score']} %

Best Score           : {d['Best Score']} %

Last Score           : {d['Last Score']} %

Study Time           : {d['Study Time']} minutes

========================================
"""


# -------------------------------------------------
# Reset Progress
# -------------------------------------------------

def reset_progress():

    save_progress(DEFAULT_PROGRESS.copy())


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    add_uploaded_file("AI_Notes.pdf")

    add_uploaded_file("Statistics.pdf")

    complete_topic("Machine Learning")

    complete_topic("Deep Learning")

    add_study_time(40)

    update_quiz(88)

    update_quiz(94)

    print(dashboard_text())