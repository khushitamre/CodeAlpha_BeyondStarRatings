from __future__ import annotations

import gzip
import re
from pathlib import Path
from typing import Iterator

import pandas as pd

FIELDS = {
    "product/productId": "product_id",
    "product/title": "product_title",
    "product/price": "product_price",
    "review/userId": "user_id",
    "review/profileName": "profile_name",
    "review/helpfulness": "helpfulness_raw",
    "review/score": "score",
    "review/time": "review_time",
    "review/summary": "summary",
    "review/text": "text",
}


def parse_records(path: str | Path) -> Iterator[dict]:
    """Parse Stanford SNAP's key:value review format without loading raw data in memory."""
    current: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                if current:
                    yield current
                    current = {}
                continue
            key, sep, value = line.partition(": ")
            if sep:
                current[key] = value
        if current:
            yield current


def load_reviews(path: str | Path) -> pd.DataFrame:
    rows = []
    for record in parse_records(path):
        row = {FIELDS.get(k, k): v for k, v in record.items()}
        rows.append(row)
    df = pd.DataFrame(rows)
    numeric = ["score", "review_time"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["review_date"] = pd.to_datetime(df["review_time"], unit="s", errors="coerce", utc=True).dt.tz_localize(None)
    helpful = df["helpfulness_raw"].fillna("0/0").str.extract(r"(?P<helpful_num>\d+)/(?:\s*)(?P<helpful_den>\d+)").astype(float)
    df["helpful_num"] = helpful["helpful_num"]
    df["helpful_den"] = helpful["helpful_den"]
    df["helpfulness_rate"] = (df["helpful_num"] / df["helpful_den"].replace(0, pd.NA)).fillna(0.0)
    df["text"] = df["text"].fillna("").astype(str).str.strip()
    df["summary"] = df["summary"].fillna("").astype(str).str.strip()
    df["review_text"] = (df["summary"] + ". " + df["text"]).str.strip(" .")
    before = len(df)
    df = df.drop_duplicates(subset=["user_id", "product_id", "review_time", "review_text"])
    # The source uses Unix timestamps; non-positive values are invalid placeholders.
    df = df[df["score"].between(1, 5) & df["review_text"].str.len().gt(0) & df["review_time"].gt(0)].copy()
    df["year"] = df["review_date"].dt.year
    df["rating_label"] = df["score"].map(lambda x: "negative" if x <= 2 else "neutral" if x == 3 else "positive")
    df.attrs["cleaning_log"] = {"raw_rows": before, "final_rows": len(df), "removed_rows": before - len(df)}
    return df.reset_index(drop=True)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
