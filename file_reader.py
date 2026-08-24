"""
file_reader.py
-----------------------------------
Automatically reads uploaded study files.

Supported Formats:
- PDF
- TXT
- CSV
- PPT
- PPTX

Python 3.14.7 Compatible
"""

from pathlib import Path

from pdf_reader import read_pdf
from text_reader import read_text
from csv_reader import read_csv
from ppt_reader import read_ppt


SUPPORTED_EXTENSIONS = {
    ".pdf": read_pdf,
    ".txt": read_text,
    ".csv": read_csv,
    ".ppt": read_ppt,
    ".pptx": read_ppt,
}


def read_uploaded_file(file_path: str) -> str:
    """
    Detect the uploaded file type and
    return extracted text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    reader = SUPPORTED_EXTENSIONS[extension]

    try:
        text = reader(str(path))

        if not text.strip():
            raise ValueError(
                "No readable content found."
            )

        return text

    except Exception as e:
        raise RuntimeError(
            f"Failed to read {path.name}\n\n{e}"
        )