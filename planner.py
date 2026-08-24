"""
planner.py
-------------------------------------------------------
Study Buddy AI Agent

Revision Planner

Compatible with:
- Python 3.14.7
"""

import json
import math
import os
from datetime import datetime, timedelta

from topics import extract_topics

DATA_FOLDER = "data"

SCHEDULE_FILE = os.path.join(
    DATA_FOLDER,
    "study_schedule.json"
)

os.makedirs(DATA_FOLDER, exist_ok=True)


# ----------------------------------------------------
# Load Schedule
# ----------------------------------------------------

def load_schedule():

    if not os.path.exists(SCHEDULE_FILE):

        save_schedule([])

        return []

    with open(
        SCHEDULE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ----------------------------------------------------
# Save Schedule
# ----------------------------------------------------

def save_schedule(schedule):

    with open(
        SCHEDULE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schedule,
            file,
            indent=4,
            ensure_ascii=False
        )


# ----------------------------------------------------
# Create Revision Plan
# ----------------------------------------------------

def create_plan(
        text,
        days=7,
        file_name="Uploaded File"
):

    topics = extract_topics(text)

    if not topics:

        return "No topics found."

    topics_per_day = math.ceil(
        len(topics) / days
    )

    today = datetime.today()

    schedule = []

    index = 0

    for day in range(days):

        daily_topics = topics[
            index:index+topics_per_day
        ]

        if not daily_topics:
            break

        schedule.append({

            "day": day + 1,

            "date": (
                today +
                timedelta(days=day)
            ).strftime("%Y-%m-%d"),

            "topics": daily_topics,

            "status": "Pending"

        })

        index += topics_per_day

    history = load_schedule()

    history.append({

        "created_on":
            today.strftime("%Y-%m-%d"),

        "file_name":
            file_name,

        "duration_days":
            days,

        "schedule":
            schedule

    })

    save_schedule(history)

    return format_schedule(schedule)


# ----------------------------------------------------
# Format Schedule
# ----------------------------------------------------

def format_schedule(schedule):

    output = []

    output.append("=" * 60)

    output.append("REVISION PLAN")

    output.append("=" * 60)

    for day in schedule:

        output.append(
            f"\nDay {day['day']} "
            f"({day['date']})"
        )

        output.append("-" * 30)

        for topic in day["topics"]:

            output.append(
                f"• {topic}"
            )

        output.append(
            f"Status : {day['status']}"
        )

    return "\n".join(output)


# ----------------------------------------------------
# Mark Completed
# ----------------------------------------------------

def complete_day(day_number):

    history = load_schedule()

    if not history:
        return

    latest = history[-1]

    for day in latest["schedule"]:

        if day["day"] == day_number:

            day["status"] = "Completed"

    save_schedule(history)


# ----------------------------------------------------
# Statistics
# ----------------------------------------------------

def planner_statistics():

    history = load_schedule()

    if not history:

        return {

            "Plans": 0,

            "Completed": 0,

            "Pending": 0

        }

    latest = history[-1]

    completed = sum(

        d["status"] == "Completed"

        for d in latest["schedule"]

    )

    pending = sum(

        d["status"] == "Pending"

        for d in latest["schedule"]

    )

    return {

        "Plans": len(history),

        "Completed": completed,

        "Pending": pending

    }


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    sample = """

Artificial Intelligence

Machine Learning

Deep Learning

Neural Networks

Backpropagation

Computer Vision

Natural Language Processing

"""

    print(

        create_plan(
            sample,
            days=5,
            file_name="AI Notes.pdf"
        )

    )

    print()

    print(

        planner_statistics()

    )