"""
csv_reader.py
----------------------------------------
Reads CSV files and converts them into
AI-readable text.

Compatible with:
- Python 3.14.7
- pandas
"""

from pathlib import Path
import pandas as pd


def read_csv(file_path: str) -> str:
    """
    Read a CSV file and convert it into
    human-readable text.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    str
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    try:
        df = pd.read_csv(path)

    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding="latin-1")
        except Exception as e:
            raise RuntimeError(
                f"Unable to read CSV file.\n{e}"
            )

    except Exception as e:
        raise RuntimeError(
            f"Unable to open CSV file.\n{e}"
        )

    if df.empty:
        raise ValueError("CSV file is empty.")

    # Replace missing values
    df = df.fillna("N/A")

    lines = []

    # File information
    lines.append("CSV DATASET INFORMATION")
    lines.append("-" * 40)
    lines.append(f"Rows: {len(df)}")
    lines.append(f"Columns: {len(df.columns)}")
    lines.append("")

    lines.append("COLUMN NAMES")
    lines.append("-" * 40)

    for column in df.columns:
        lines.append(f"- {column}")

    lines.append("")
    lines.append("DATA")
    lines.append("-" * 40)

    # Convert every row into readable text
    for index, row in df.iterrows():

        lines.append(f"\nRecord {index + 1}")

        for column in df.columns:
            value = row[column]
            lines.append(f"{column}: {value}")

    return "\n".join(lines)


# ----------------------------------------
# Testing
# ----------------------------------------

if __name__ == "__main__":

    sample = "sample_notes/sample.csv"

    try:

        content = read_csv(sample)

        print(content)

    except Exception as error:

        print(error)