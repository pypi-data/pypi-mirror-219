from datetime import datetime
from typing import Any
from pathlib import Path
import numpy as np

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import yaml


def read_yaml(path: Path | str) -> Any:
    """
    Reads a yaml file and returns the data as a dictionary.
    """
    with open(path, "r") as stream:
        return yaml.safe_load(stream)


def convert_pdf_to_txt(path, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(path, "rb")
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


from pathlib import Path
import numpy as np
from datetime import datetime


def find_nearest_filepath(
    dir: Path, wildcard_filename: str, date_location_in_filename: int, date: datetime
) -> Path:
    """Finds the nearest file path in the specified directory based on a wildcard filename pattern and a target date.

    Args:
        dir (Path): The directory to search for files.
        wildcard_filename (str): The wildcard filename pattern to match files.
        date_location_in_filename (int): The index of the date in the filename split by underscores.
        date (datetime): The target date to find the nearest file.

    Returns:
        Path: The path to the nearest file.

    Raises:
        ValueError: If no file is found in the directory.

    """
    # Get all candidate file paths
    candidates = [*dir.rglob(wildcard_filename)]

    # Raise an error if no candidate files are found
    if not candidates:
        raise ValueError("No file found.")

    # Extract the dates from candidate file names
    candidate_dates = np.array(
        [
            np.datetime64(p.name.split(".")[0].split("_")[date_location_in_filename])
            for p in candidates
        ]
    )

    # Calculate the differences between target date and candidate dates
    date_diffs = np.abs(candidate_dates - np.datetime64(date))

    # Find the index of the minimum date difference
    idx = np.argmin(date_diffs)

    # Get the path of the nearest file
    path = candidates[idx]

    # Raise an error if the path does not exist
    if not path.exists():
        raise ValueError("No file found.")

    return path
