from unidecode import unidecode
import re

THE_WORD_REGEX = re.compile(r"\bthe\b")
AND_WORD_REGEX = re.compile(r"\band\b")
AMPERSAND_WORD_REGEX = re.compile(r"\s&\s")


def sanitize_string(s, remove_the=False, remove_and=False):
    s = s.lower()
    s = s.replace("_", " ")
    s = s.replace(".", "")
    s = s.replace("-", " ")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("[", "")
    s = s.replace("]", "")

    if remove_the:
        s = re.sub(THE_WORD_REGEX, "", s)

    if remove_and:
        s = re.sub(AMPERSAND_WORD_REGEX, " ", s)
        s = re.sub(AND_WORD_REGEX, "", s)

    # Change special characters into their somewhat normal equivalent
    s = unidecode(s)
    s = s.strip()

    # Get rid of double-spaces when an and or & is removed.
    s = s.replace("  ", " ")

    return s
