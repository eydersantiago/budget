from transformers import pipeline
from functools import lru_cache

@lru_cache(maxsize=1)
def _get_classifier():
    return pipeline(
        task="text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

def classify(text: str):
    clf = _get_classifier()
    result = clf(text)[0]  # {'label': 'POSITIVE'|'NEGATIVE', 'score': float}
    return {"label": result["label"], "score": float(result["score"])}
