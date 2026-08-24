"""
flashcards.py
-------------------------------------------------------
Study Buddy AI Agent

Flashcard Generator

Compatible with:
- Python 3.14.7
"""

import json
import os
import re

DATA_FOLDER = "data"

FLASHCARD_FILE = os.path.join(
    DATA_FOLDER,
    "flashcards.json"
)

os.makedirs(DATA_FOLDER, exist_ok=True)


# -------------------------------------------------------
# Clean Text
# -------------------------------------------------------

def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [

        sentence.strip()

        for sentence in sentences

        if len(sentence.split()) >= 5

    ]


# -------------------------------------------------------
# Generate Flashcards
# -------------------------------------------------------

def create_flashcards(text):

    sentences = split_sentences(text)

    if not sentences:

        return "No flashcards generated."

    flashcards = []

    for sentence in sentences:

        words = sentence.split()

        if len(words) < 6:
            continue

        question = f"What is:\n\n{words[0]} ?"

        answer = sentence

        flashcards.append({

            "question": question,

            "answer": answer

        })

    save_flashcards(flashcards)

    return format_flashcards(flashcards)


# -------------------------------------------------------
# Save Flashcards
# -------------------------------------------------------

def save_flashcards(cards):

    with open(

        FLASHCARD_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            cards,

            file,

            indent=4,

            ensure_ascii=False

        )


# -------------------------------------------------------
# Load Flashcards
# -------------------------------------------------------

def load_flashcards():

    if not os.path.exists(FLASHCARD_FILE):

        return []

    with open(

        FLASHCARD_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)


# -------------------------------------------------------
# Format
# -------------------------------------------------------

def format_flashcards(cards):

    output = []

    output.append("=" * 60)

    output.append("FLASHCARDS")

    output.append("=" * 60)

    for i, card in enumerate(cards, start=1):

        output.append(f"\nFlashcard {i}")

        output.append("-" * 30)

        output.append(card["question"])

        output.append("")

        output.append("Answer:")

        output.append(card["answer"])

    return "\n".join(output)


# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

def flashcard_statistics():

    cards = load_flashcards()

    return {

        "Total Flashcards":

            len(cards)

    }


# -------------------------------------------------------
# Search Flashcards
# -------------------------------------------------------

def search_flashcards(keyword):

    cards = load_flashcards()

    results = []

    keyword = keyword.lower()

    for card in cards:

        if keyword in card["answer"].lower():

            results.append(card)

    return results


# -------------------------------------------------------
# Testing
# -------------------------------------------------------

if __name__ == "__main__":

    sample = """

Artificial Intelligence is the simulation of human intelligence.

Machine Learning is a subset of Artificial Intelligence.

Deep Learning uses Neural Networks.

Backpropagation is used to train neural networks.

"""

    print(

        create_flashcards(sample)

    )

    print()

    print(

        flashcard_statistics()

    )