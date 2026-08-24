"""
utils.py
-------------------------------------------------------
Study Buddy AI Agent

Common Utility Functions

Compatible with:
- Python 3.14.7
"""

import os
import json
import re
from datetime import datetime


# -------------------------------------------------------
# Create Folder
# -------------------------------------------------------

def ensure_folder(folder_path):

    os.makedirs(folder_path, exist_ok=True)


# -------------------------------------------------------
# Load JSON
# -------------------------------------------------------

def load_json(file_path, default=None):

    if default is None:
        default = {}

    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return default


# -------------------------------------------------------
# Save JSON
# -------------------------------------------------------

def save_json(file_path, data):

    folder = os.path.dirname(file_path)

    if folder:
        ensure_folder(folder)

    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# -------------------------------------------------------
# Save Text File
# -------------------------------------------------------

def save_text(file_path, text):

    folder = os.path.dirname(file_path)

    if folder:
        ensure_folder(folder)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


# -------------------------------------------------------
# Read Text File
# -------------------------------------------------------

def load_text(file_path):

    if not os.path.exists(file_path):
        return ""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# -------------------------------------------------------
# Clean Text
# -------------------------------------------------------

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------------------------------------------------------
# Count Words
# -------------------------------------------------------

def word_count(text):

    return len(text.split())


# -------------------------------------------------------
# Count Characters
# -------------------------------------------------------

def character_count(text):

    return len(text)


# -------------------------------------------------------
# Current Time
# -------------------------------------------------------

def current_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# -------------------------------------------------------
# File Size
# -------------------------------------------------------

def file_size(file_path):

    if not os.path.exists(file_path):
        return 0

    return round(
        os.path.getsize(file_path) / 1024,
        2
    )


# -------------------------------------------------------
# Supported File Check
# -------------------------------------------------------

def is_supported(filename):

    supported = [

        ".pdf",

        ".txt",

        ".csv",

        ".ppt",

        ".pptx"

    ]

    extension = os.path.splitext(filename)[1].lower()

    return extension in supported


# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

def text_statistics(text):

    return {

        "Words":
            word_count(text),

        "Characters":
            character_count(text),

        "Lines":
            len(text.splitlines())

    }


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    sample = """
Artificial Intelligence is changing the world.

Machine Learning is a branch of AI.
"""

    print(clean_text(sample))

    print()

    print(text_statistics(sample))

    print()

    print(current_time())