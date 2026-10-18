from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")


def save_charts(df, themes, out_dir: str | Path):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=df, x="score", color="#2563eb", ax=ax)
    ax.set(title="Review volume by star rating", xlabel="Star rating", ylabel="Reviews")
    fig.tight_layout(); fig.savefig(out / "rating_distribution.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    order = ["negative", "neutral", "positive"]
    sns.countplot(data=df, x="lexicon_sentiment", order=order, palette={"negative":"#dc2626", "neutral":"#64748b", "positive":"#16a34a"}, ax=ax)
    ax.set(title="Lexicon sentiment distribution", xlabel="Sentiment", ylabel="Reviews")
    fig.tight_layout(); fig.savefig(out / "sentiment_distribution.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot = themes.sort_values("count").tail(15)
    sns.barplot(data=plot, x="count", y="term", color="#dc2626", ax=ax)
    ax.set(title="Most frequent terms in negative reviews", xlabel="Occurrences", ylabel="Term")
    fig.tight_layout(); fig.savefig(out / "negative_themes.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    monthly = df.groupby("year").agg(avg_rating=("score", "mean"), negative_rate=("rating_label", lambda s: (s == "negative").mean()), reviews=("score", "size")).reset_index()
    sns.lineplot(data=monthly, x="year", y="negative_rate", marker="o", color="#dc2626", ax=ax)
    ax.set(title="Negative review rate by year", xlabel="Year", ylabel="Share of reviews")
    fig.tight_layout(); fig.savefig(out / "negative_rate_by_year.png", dpi=160); plt.close(fig)
