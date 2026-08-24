"""
text_reader.py
-------------------------------------
Reads plain text (.txt) files.

Compatible with:
- Python 3.14.7
"""

from pathlib import Path


# Try these encodings in order
ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "utf-16",
    "latin-1",
    "cp1252",
]


def read_text(file_path: str) -> str:
    """
    Read a text file and return its contents.

    Parameters
    ----------
    file_path : str
        Path to the text file.

    Returns
    -------
    str
        File contents.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    for encoding in ENCODINGS:

        try:

            with open(
                path,
                "r",
                encoding=encoding
            ) as file:

                text = file.read()

                if text.strip():
                    return text

        except UnicodeDecodeError:
            continue

        except Exception as e:
            raise RuntimeError(
                f"Unable to read text file.\n{e}"
            )

    raise ValueError(
        "Unable to decode the text file using supported encodings."
    )


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    sample = "sample_notes/sample.txt"

    try:

        content = read_text(sample)

        print(content)

    except Exception as error:

        print(error)