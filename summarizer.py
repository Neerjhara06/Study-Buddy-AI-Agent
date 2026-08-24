"""
summarizer.py
----------------------------------------
Study Buddy AI Agent

Simple extractive summarizer.

Compatible with:
- Python 3.14.7
"""

import re


def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """

    if text is None:
        return ""

    text = text.replace("\r", "\n")

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    text = clean_text(text)

    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [s.strip() for s in sentences if s.strip()]


def summarize(text: str) -> str:
    """
    Generate a simple extractive summary.
    """

    text = clean_text(text)

    if not text:
        return "No readable text found."

    sentences = split_into_sentences(text)

    if not sentences:
        return "No readable sentences found."

    if len(sentences) <= 6:
        return "\n\n".join(sentences)

    summary = []

    # First three sentences
    summary.extend(sentences[:3])

    # Middle sentence
    middle = len(sentences) // 2
    summary.append(sentences[middle])

    # Last two sentences
    summary.extend(sentences[-2:])

    # Remove duplicates while preserving order
    unique_summary = []

    for sentence in summary:
        if sentence not in unique_summary:
            unique_summary.append(sentence)

    return "\n\n".join(unique_summary)


def bullet_summary(text: str) -> str:
    """
    Generate bullet point summary.
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return "No summary available."

    bullets = []

    for sentence in sentences[:10]:
        bullets.append(f"• {sentence}")

    return "\n".join(bullets)


def detailed_summary(text: str) -> str:
    """
    Return first 15 sentences.
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return "No detailed summary available."

    return "\n\n".join(sentences[:15])


def summary_statistics(text: str) -> dict:
    """
    Return statistics of the extracted text.
    """

    cleaned = clean_text(text)

    return {
        "Words": len(cleaned.split()),
        "Characters": len(cleaned),
        "Sentences": len(split_into_sentences(cleaned)),
    }


if __name__ == "__main__":

    sample = """
    Artificial Intelligence is the simulation of human intelligence by machines.
    Machine Learning is a subset of AI.
    Deep Learning uses neural networks.
    AI is used in healthcare.
    AI is used in finance.
    AI is used in robotics.
    AI is transforming education.
    """

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(summarize(sample))

    print("\n")

    print("=" * 60)
    print("BULLET SUMMARY")
    print("=" * 60)
    print(bullet_summary(sample))

    print("\n")

    print("=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(summary_statistics(sample))