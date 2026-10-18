from __future__ import annotations

import re
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, mannwhitneyu
from sklearn.feature_extraction.text import CountVectorizer


def rating_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("score").agg(reviews=("score", "size"), mean_lexicon=("lexicon_score", "mean"), mismatch_rate=("rating_sentiment_mismatch", "mean")).reset_index()


def mismatch_test(df: pd.DataFrame) -> dict:
    table = pd.crosstab(df["rating_label"], df["lexicon_sentiment"])
    chi2, p, dof, expected = chi2_contingency(table)
    n = table.to_numpy().sum()
    phi = float(np.sqrt(chi2 / n)) if n else np.nan
    return {"table": table, "chi2": float(chi2), "p_value": float(p), "dof": int(dof), "phi": phi}


def sentiment_rating_effect(df: pd.DataFrame) -> dict:
    positive = df.loc[df["lexicon_sentiment"] == "positive", "score"]
    negative = df.loc[df["lexicon_sentiment"] == "negative", "score"]
    stat, p = mannwhitneyu(positive, negative, alternative="two-sided")
    pooled = np.sqrt((positive.var() + negative.var()) / 2)
    effect = float((positive.mean() - negative.mean()) / pooled) if pooled else np.nan
    return {"positive_n": int(len(positive)), "negative_n": int(len(negative)), "positive_mean_rating": float(positive.mean()), "negative_mean_rating": float(negative.mean()), "u_stat": float(stat), "p_value": float(p), "standardized_effect": effect}


def top_ngrams(df: pd.DataFrame, sentiment: str = "negative", n: int = 20) -> pd.DataFrame:
    texts = df.loc[df["lexicon_sentiment"] == sentiment, "review_text"]
    vectorizer = CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=max(5, int(len(texts) * 0.0002)), max_features=5000)
    matrix = vectorizer.fit_transform(texts)
    counts = np.asarray(matrix.sum(axis=0)).ravel()
    terms = vectorizer.get_feature_names_out()
    result = pd.DataFrame({"term": terms, "count": counts}).sort_values("count", ascending=False).head(n)
    return result.reset_index(drop=True)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    return df.set_index("review_date").groupby(pd.Grouper(freq="MS")).agg(reviews=("score", "size"), avg_rating=("score", "mean"), negative_rate=("rating_label", lambda s: (s == "negative").mean())).reset_index()
