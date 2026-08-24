"""
quiz.py
Study Buddy AI Agent - Quiz Generator
Compatible with Python 3.14.7
"""

import json
import os
import random
import re


DATA_FOLDER = "data"

CURRENT_QUIZ_FILE = os.path.join(
    DATA_FOLDER,
    "current_quiz.json"
)

QUIZ_HISTORY_FILE = os.path.join(
    DATA_FOLDER,
    "quiz_history.json"
)

os.makedirs(DATA_FOLDER, exist_ok=True)


def load_json(file_path, default=None):
    if default is None:
        default = []

    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    text = clean_text(text)

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 6
    ]


def get_study_sentences(text, limit=50):
    sentences = split_sentences(text)

    if not sentences:
        return []

    sentences = list(dict.fromkeys(sentences))

    suitable = [
        sentence
        for sentence in sentences
        if 6 <= len(sentence.split()) <= 40
    ]

    if not suitable:
        suitable = sentences

    random.shuffle(suitable)

    return suitable[:limit]


def create_mcq(sentence, all_sentences):
    words = sentence.split()

    if len(words) < 6:
        return None

    candidates = []

    for word in words:
        clean_word = word.strip(
            ".,!?;:()[]{}\"'"
        )

        if len(clean_word) >= 5:
            candidates.append(clean_word)

    if not candidates:
        return None

    answer = random.choice(candidates)

    pattern = re.compile(
        re.escape(answer),
        re.IGNORECASE
    )

    question_text = pattern.sub(
        "_____",
        sentence,
        count=1
    )

    distractors = []

    for other_sentence in all_sentences:

        if other_sentence == sentence:
            continue

        for word in other_sentence.split():

            clean_word = word.strip(
                ".,!?;:()[]{}\"'"
            )

            if len(clean_word) < 5:
                continue

            if clean_word.lower() == answer.lower():
                continue

            if clean_word in distractors:
                continue

            distractors.append(clean_word)

            if len(distractors) == 3:
                break

        if len(distractors) == 3:
            break

    if len(distractors) < 3:
        return None

    options = [
        answer,
        distractors[0],
        distractors[1],
        distractors[2]
    ]

    random.shuffle(options)

    return {
        "type": "MCQ",
        "question": (
            "Fill in the blank:\n\n"
            + question_text
        ),
        "options": options,
        "answer": answer
    }


def create_true_false(sentence):
    if not sentence:
        return None

    return {
        "type": "True/False",
        "question": (
            "True or False?\n\n"
            + sentence
        ),
        "options": [
            "True",
            "False"
        ],
        "answer": "True"
    }


def generate(text, number_of_questions=10):
    text = clean_text(text)

    if not text:
        raise ValueError(
            "No study material was provided."
        )

    try:
        number_of_questions = int(
            number_of_questions
        )
    except (ValueError, TypeError):
        number_of_questions = 10

    number_of_questions = max(
        1,
        min(number_of_questions, 50)
    )

    sentences = get_study_sentences(
        text,
        limit=max(
            number_of_questions * 3,
            30
        )
    )

    if not sentences:
        raise ValueError(
            "Not enough study material to generate a quiz."
        )

    quiz = []

    for sentence in sentences:

        if len(quiz) >= number_of_questions:
            break

        question = create_mcq(
            sentence,
            sentences
        )

        if question:
            quiz.append(question)

    if len(quiz) < number_of_questions:

        for sentence in sentences:

            if len(quiz) >= number_of_questions:
                break

            question = create_true_false(
                sentence
            )

            if question:
                quiz.append(question)

    if not quiz:
        raise ValueError(
            "Unable to generate quiz questions."
        )

    for number, question in enumerate(
        quiz,
        start=1
    ):
        question["question_no"] = number

    save_json(
        CURRENT_QUIZ_FILE,
        quiz
    )

    return quiz


def load_quiz():
    return load_json(
        CURRENT_QUIZ_FILE,
        []
    )


def clear_quiz():
    save_json(
        CURRENT_QUIZ_FILE,
        []
    )


def save_quiz_history(
    score,
    total,
    correct,
    wrong
):
    history = load_json(
        QUIZ_HISTORY_FILE,
        []
    )

    record = {
        "quiz_number": len(history) + 1,
        "score": score,
        "total_questions": total,
        "correct": correct,
        "wrong": wrong
    }

    history.append(record)

    save_json(
        QUIZ_HISTORY_FILE,
        history
    )

    return record


def quiz_statistics():
    history = load_json(
        QUIZ_HISTORY_FILE,
        []
    )

    if not history:
        return {
            "total_quizzes": 0,
            "average_score": 0,
            "best_score": 0,
            "last_score": 0
        }

    scores = [
        item.get("score", 0)
        for item in history
    ]

    return {
        "total_quizzes": len(scores),
        "average_score": round(
            sum(scores) / len(scores),
            2
        ),
        "best_score": max(scores),
        "last_score": scores[-1]
    }


def format_quiz(quiz):
    if not quiz:
        return "No quiz available."

    output = []

    output.append("=" * 60)
    output.append("STUDY BUDDY QUIZ")
    output.append("=" * 60)

    for question in quiz:

        number = question.get(
            "question_no",
            "?"
        )

        output.append(
            f"\nQuestion {number}"
        )

        output.append("-" * 30)

        output.append(
            question.get(
                "question",
                ""
            )
        )

        options = question.get(
            "options",
            []
        )

        for index, option in enumerate(
            options
        ):
            letter = chr(65 + index)

            output.append(
                f"{letter}. {option}"
            )

    return "\n".join(output)


if __name__ == "__main__":

    sample_text = """
    Artificial Intelligence is a branch of computer science
    that focuses on creating intelligent machines.

    Machine Learning is a subset of Artificial Intelligence
    that allows computers to learn from data.

    Deep Learning uses artificial neural networks
    with multiple layers.

    Neural networks are inspired by the structure
    of the human brain.

    Python is widely used in Artificial Intelligence
    and Machine Learning applications.
    """

    quiz = generate(
        sample_text,
        5
    )

    print(
        format_quiz(quiz)
    )

    print("\nQuiz Statistics:")

    print(
        quiz_statistics()
    )