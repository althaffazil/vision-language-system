from models.blip_vqa import BLIPVQA
from utils.question_type import detect_question_type
from utils.answer_validation import validate_answer


class VQAService:
    def __init__(self):
        self.model = BLIPVQA()

    def answer(self, image, question):
        question_type = detect_question_type(question)

        answer, confidence = self.model.predict(image, question)

        is_valid, warning = validate_answer(question_type, answer)

        # Reduce confidence if validation fails
        if not is_valid:
            confidence = max(confidence - 25, 0)

        return {
            "answer": answer,
            "confidence": confidence,
            "question_type": question_type,
            "is_valid": is_valid,
            "warning": warning
        }