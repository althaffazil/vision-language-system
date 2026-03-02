FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download BLIP model during build
RUN python -c "from transformers import BlipProcessor, BlipForQuestionAnswering; \
BlipProcessor.from_pretrained('Salesforce/blip-vqa-base'); \
BlipForQuestionAnswering.from_pretrained('Salesforce/blip-vqa-base')"

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]