# Exploratory Analysis Guide

This repository keeps the reusable work in `src/` and `run_pipeline.py` so the analysis is not trapped in a monolithic notebook. To reproduce the exploratory analysis:

```python
from pathlib import Path
from src.preprocessing import load_reviews
from src.sentiment import add_lexicon_sentiment
from src.analysis import mismatch_test, sentiment_rating_effect, top_ngrams

reviews = load_reviews(Path('../data/raw/Gourmet_Foods.txt.gz'))
reviews = add_lexicon_sentiment(reviews)
print(reviews.info())
print(reviews.isna().mean().sort_values(ascending=False).head())
print(reviews['score'].value_counts(normalize=True).sort_index())
print(mismatch_test(reviews))
print(sentiment_rating_effect(reviews))
print(top_ngrams(reviews, 'negative', 20))
```

Questions addressed: schema and data quality, rating concentration, rating/text disagreement, recurring negative language, and time variation. All values in the final reports come from the executed pipeline rather than illustrative notebook numbers.
