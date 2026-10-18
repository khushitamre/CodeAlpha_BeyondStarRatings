from __future__ import annotations

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

POSITIVE = {"excellent", "great", "good", "love", "loved", "best", "perfect", "amazing", "delicious", "fresh", "recommend"}
NEGATIVE = {"bad", "worst", "hate", "hated", "poor", "awful", "terrible", "stale", "broken", "disappoint", "refund", "waste", "bland"}


def lexicon_score(text: str) -> float:
    tokens = re.findall(r"[a-z]+", text.lower())
    if not tokens:
        return 0.0
    pos = sum(token in POSITIVE for token in tokens)
    neg = sum(token in NEGATIVE for token in tokens)
    return (pos - neg) / max(len(tokens) ** 0.5, 1.0)


def add_lexicon_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["lexicon_score"] = out["review_text"].map(lexicon_score)
    out["lexicon_sentiment"] = out["lexicon_score"].map(lambda x: "positive" if x > 0.05 else "negative" if x < -0.05 else "neutral")
    out["rating_sentiment_mismatch"] = ((out["score"] >= 4) & (out["lexicon_sentiment"] == "negative")) | ((out["score"] <= 2) & (out["lexicon_sentiment"] == "positive"))
    return out


def train_rating_aligned_model(df: pd.DataFrame):
    """Train a text-only model on a deterministic split for a transparent benchmark."""
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    labels = df["rating_label"].where(df["rating_label"].isin(["positive", "negative"]), pd.NA)
    work = df.loc[labels.notna()].copy()
    y = work["rating_label"]
    x_train, x_test, y_train, y_test = train_test_split(work["review_text"], y, test_size=0.2, random_state=42, stratify=y)
    model = Pipeline([("tfidf", TfidfVectorizer(min_df=3, max_features=60000, ngram_range=(1, 2), sublinear_tf=True)), ("clf", LogisticRegression(max_iter=300, class_weight="balanced"))])
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return model, classification_report(y_test, pred, output_dict=True), (y_test, pred)
