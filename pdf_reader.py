"""
pdf_reader.py
-------------------------------------
Reads PDF files and extracts text.

Compatible with:
- Python 3.14.7
- pypdf
"""

from pathlib import Path
from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    """
    Read a PDF file and return all extracted text.

    Parameters
    ----------
    file_path : str
        Path to the PDF file.

    Returns
    -------
    str
        Extracted text from all pages.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    try:
        reader = PdfReader(str(path))

    except Exception as e:
        raise RuntimeError(
            f"Unable to open PDF.\n{e}"
        )

    text = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:

            page_text = page.extract_text()

            if page_text:
                text.append(
                    f"\n\n========== PAGE {page_number} ==========\n\n"
                )

                text.append(page_text)

        except Exception:
            continue

    extracted_text = "".join(text).strip()

    if not extracted_text:

        raise ValueError(
            "No readable text found in the PDF.\n"
            "This PDF may contain only scanned images."
        )

    return extracted_text


# -----------------------------------------------------
# Test
# -----------------------------------------------------

if __name__ == "__main__":

    sample = "sample_notes/AI_Notes.pdf"

    try:

        content = read_pdf(sample)

        print(content[:1000])

    except Exception as error:

        print(error)