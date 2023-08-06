from transformers import pipeline

sentiment_model = pipeline(
    task="sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english"
)