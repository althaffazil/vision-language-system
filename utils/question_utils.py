import re


def normalize_question(question: str):
    question = question.strip()

    if not question.endswith("?"):
        question += "?"

    return question


def is_valid_question(question: str):
    if not re.search(r"[a-zA-Z]", question):
        return False

    if len(question.split()) < 3:
        return False

    return True