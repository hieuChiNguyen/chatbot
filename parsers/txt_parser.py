import os

from logger import logger


def parse_txt_file(file_path: str) -> list:
    """
    Parse a .txt file and return its content as a list of strings.
    Args:
        file_path (str): Path to the .txt file.
    Returns:
        list: List containing the text content of the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        print(f"Successfully parsed text file: {os.path.basename(file_path)}")
        return [text]  # Return as a list to match other parsers' output format
    except Exception as e:
        logger.error(f"Error parsing text file {os.path.basename(file_path)}: {str(e)}")
        return []