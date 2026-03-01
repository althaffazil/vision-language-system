def detect_question_type(question: str):
    q = question.lower()

    if any(word in q for word in ["how many", "number of", "count"]):
        return "Counting"

    if any(word in q for word in ["what color", "which color", "colour"]):
        return "Color"

    if any(word in q for word in ["where", "position", "left", "right", "top", "bottom"]):
        return "Spatial"

    if q.startswith(("is", "are", "does", "do", "was", "were")):
        return "Yes/No"

    if any(word in q for word in ["what", "which", "who"]):
        return "Object Identification"

    return "General"