"""
explain.py
-------------------------------------------------------
Study Buddy AI Agent

Concept Explanation Module

Compatible with:
- Python 3.14.7
"""

import re


# ----------------------------------------------------
# Clean Text
# ----------------------------------------------------

def clean_text(text):

    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# ----------------------------------------------------
# Split into Sentences
# ----------------------------------------------------

def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [

        sentence.strip()

        for sentence in sentences

        if sentence.strip()

    ]


# ----------------------------------------------------
# Explain Topic
# ----------------------------------------------------

def explain_topic(text, concept):

    if not text.strip():

        return "No study material available."

    if not concept.strip():

        return "Please enter a topic."

    text = clean_text(text)

    concept = concept.lower()

    sentences = split_sentences(text)

    matched = []

    for sentence in sentences:

        if concept in sentence.lower():

            matched.append(sentence)

    if matched:

        output = []

        output.append("=" * 60)

        output.append(f"EXPLANATION : {concept.title()}")

        output.append("=" * 60)

        output.append("")

        for sentence in matched:

            output.append(f"• {sentence}")

        return "\n".join(output)

    return (
        f"No explanation found for '{concept}'.\n"
        "Try another keyword."
    )


# ----------------------------------------------------
# Related Topics
# ----------------------------------------------------

def related_topics(text, concept):

    concept = concept.lower()

    words = set()

    for sentence in split_sentences(text):

        if concept in sentence.lower():

            for word in sentence.split():

                word = word.strip(".,!?()[]{}")

                if len(word) > 3:

                    words.add(word)

    return sorted(words)


# ----------------------------------------------------
# Summary Explanation
# ----------------------------------------------------

def short_explanation(text, concept):

    result = explain_topic(text, concept)

    if result.startswith("No explanation"):

        return result

    lines = result.split("\n")

    return "\n".join(lines[:8])


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    sample = """
Artificial Intelligence is the simulation of human intelligence by machines.

Machine Learning is a subset of Artificial Intelligence.

Deep Learning uses Neural Networks.

Backpropagation is used to train Neural Networks.

Artificial Intelligence is widely used in healthcare.
"""

    print(

        explain_topic(

            sample,

            "Artificial Intelligence"

        )

    )

    print()

    print(

        related_topics(

            sample,

            "Artificial Intelligence"

        )

    )