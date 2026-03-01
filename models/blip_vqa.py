import torch
import torch.nn.functional as F
from transformers import BlipProcessor, BlipForQuestionAnswering


class BLIPVQA:
    def __init__(self, model_name="Salesforce/blip-vqa-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForQuestionAnswering.from_pretrained(model_name)

        self.model.to(self.device)
        self.model.eval()

    def predict(self, image, question):
        inputs = self.processor(
            images=image,
            text=question,
            return_tensors="pt"
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                return_dict_in_generate=True,
                output_scores=True
            )

        generated_ids = outputs.sequences[0]
        scores = outputs.scores

        answer = self.processor.decode(
            generated_ids,
            skip_special_tokens=True
        )

        token_probs = []
        for step_logits, token_id in zip(scores, generated_ids[1:]):
            probs = F.softmax(step_logits, dim=-1)
            token_prob = probs[0, token_id]
            token_probs.append(token_prob.item())

        confidence = round(
            (sum(token_probs) / len(token_probs)) * 100, 2
        ) if token_probs else 0.0

        return answer, confidence