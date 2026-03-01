import re


VALID_COLORS = {
    "red", "blue", "green", "yellow", "black", "white",
    "brown", "gray", "grey", "orange", "pink", "purple"
}


def validate_answer(question_type: str, answer: str):
    answer_lower = answer.lower()

    is_valid = True
    warning = None

    if question_type == "Counting":
        if not re.search(r"\d+", answer_lower):
            is_valid = False
            warning = "Counting question detected, but answer is not numeric."

    elif question_type == "Yes/No":
        if answer_lower not in ["yes", "no"]:
            is_valid = False
            warning = "Yes/No question detected, but answer is not 'yes' or 'no'."

    elif question_type == "Color":
        if not any(color in answer_lower for color in VALID_COLORS):
            is_valid = False
            warning = "Color question detected, but answer does not match common colors."

    return is_valid, warning