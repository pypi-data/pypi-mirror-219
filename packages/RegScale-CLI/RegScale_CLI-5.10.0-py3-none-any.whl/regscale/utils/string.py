"""Define commonly used methods for strings."""
import re


ANSI_ESCAPE_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def remove_ansi_escape_sequences(text: str) -> str:
    """Remove all ANSI escape sequences from a text
    :param str text: a string to remove ANSI escape sequences from
    :returns: a string with no ANSI escape sequences
    """
    return ANSI_ESCAPE_REGEX.sub("", text)
