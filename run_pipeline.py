from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

from src.preprocessing import load_reviews
from src.sentiment import add_lexicon_sentiment, train_rating_aligned_model
from src.analysis import mismatch_test, sentiment_rating_effect, top_ngrams
from src.visualization import save_charts

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data/raw/Gourmet_Foods.txt.gz"
PROCESSED = ROOT / "data/processed/reviews_processed.csv"
ASSETS = ROOT / "assets"
REPORTS = ROOT / "reports"


def main():
    REPORTS.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True); PROCESSED.parent.mkdir(exist_ok=True)
    df = load_reviews(RAW)
    df = add_lexicon_sentiment(df)
    df.to_csv(PROCESSED, index=False)
    themes = top_ngrams(df, "negative", 20)
    themes.to_csv(REPORTS / "negative_themes.csv", index=False)
    test = mismatch_test(df)
    effect = sentiment_rating_effect(df)
    model, model_report, _ = train_rating_aligned_model(df.sample(min(len(df), 100000), random_state=42))
    results = {"cleaning_log": df.attrs.get("cleaning_log", {}), "rows": int(len(df)), "date_min": str(df.review_date.min()), "date_max": str(df.review_date.max()), "avg_rating": float(df.score.mean()), "mismatch_rate": float(df.rating_sentiment_mismatch.mean()), "mismatch_test": {k: (v.to_dict() if hasattr(v, "to_dict") else v) for k, v in test.items()}, "sentiment_rating_effect": effect, "model_classification_report": model_report, "top_negative_terms": themes.to_dict(orient="records")}
    (REPORTS / "results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    save_charts(df, themes, ASSETS)
    print(json.dumps({"rows": len(df), "avg_rating": round(df.score.mean(), 3), "mismatch_rate": round(df.rating_sentiment_mismatch.mean(), 4), "negative_terms": themes.head(10).to_dict(orient="records"), "model_f1_negative": round(model_report["negative"]["f1-score"], 3), "model_f1_positive": round(model_report["positive"]["f1-score"], 3)}, indent=2))

if __name__ == "__main__":
    main()
