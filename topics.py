"""
topics.py
-------------------------------------
Extract important study topics.

Compatible with:
- Python 3.14.7
"""

import re
from collections import Counter


# ---------------------------------------------
# Common English stop words
# ---------------------------------------------

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "of", "to", "and", "or", "for", "on", "in",
    "at", "by", "with", "as", "this", "that",
    "these", "those", "be", "been", "being",
    "it", "its", "from", "into", "than",
    "can", "could", "should", "would",
    "will", "may", "might", "using",
    "use", "used", "their", "there",
    "his", "her", "our", "your",
    "they", "them", "he", "she",
    "you", "we", "i"
}


# ---------------------------------------------
# Clean text
# ---------------------------------------------

def clean_text(text: str) -> str:

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------
# Extract Keywords
# ---------------------------------------------

def extract(text: str) -> str:
    """
    Main function used by LangChain Tool.
    """

    topics = extract_topics(text)

    return "\n".join(f"• {topic}" for topic in topics)


# ---------------------------------------------
# Extract Topic List
# ---------------------------------------------

def extract_topics(text: str, top_n: int = 15):

    cleaned = clean_text(text)

    words = cleaned.split()

    filtered = []

    for word in words:

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        if word.isdigit():
            continue

        filtered.append(word)

    counts = Counter(filtered)

    return [word.title() for word, _ in counts.most_common(top_n)]


# ---------------------------------------------
# Keyword Frequency
# ---------------------------------------------

def keyword_frequency(text: str):

    cleaned = clean_text(text)

    words = cleaned.split()

    filtered = [
        w
        for w in words
        if w not in STOP_WORDS
        and len(w) > 2
        and not w.isdigit()
    ]

    return Counter(filtered)


# ---------------------------------------------
# Statistics
# ---------------------------------------------

def topic_statistics(text: str):

    topics = extract_topics(text)

    return {
        "Total Topics": len(topics),
        "Topics": topics
    }


# ---------------------------------------------
# Testing
# ---------------------------------------------

if __name__ == "__main__":

    sample = """
    Artificial Intelligence is transforming healthcare.

    Machine Learning is a branch of Artificial Intelligence.

    Deep Learning uses Neural Networks.

    Neural Networks use Backpropagation.

    Artificial Intelligence is also used in Robotics.
    """

    print("=" * 60)

    print("TOPICS")

    print("=" * 60)

    print(extract(sample))

    print("\n")

    print(topic_statistics(sample))