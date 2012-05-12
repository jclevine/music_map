import unicodedata


def sanitize_string(s, remove_the=False, remove_and=False):
    s = s.lower()
    s = s.replace("_", " ")
    s = s.replace(".", "")
    s = s.replace("-", " ")
    s = s.replace("(", "")
    s = s.replace(")", "")
    if remove_the:
        s = s.replace(" the", "")
        s = s.replace("the ", "")

    if remove_and:
        s = s.replace("& ", "")
        s = s.replace(" &", "")
        s = s.replace("and ", "")
        s = s.replace(" and", "")
    # Change special characters into their somewhat normal equivalent
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    s = s.rstrip()
    return s
