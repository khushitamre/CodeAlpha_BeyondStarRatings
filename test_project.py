import pandas as pd
from src.preprocessing import normalize_text
from src.sentiment import lexicon_score, add_lexicon_sentiment


def test_normalize_text_removes_markup_and_punctuation():
    assert normalize_text("<b>Great!</b> tea") == "great tea"


def test_lexicon_score_direction():
    assert lexicon_score("excellent amazing product") > 0
    assert lexicon_score("terrible stale product") < 0


def test_mismatch_rule():
    df = pd.DataFrame({"score": [5, 1, 3], "review_text": ["terrible taste", "excellent product", "good enough"]})
    out = add_lexicon_sentiment(df)
    assert out["rating_sentiment_mismatch"].tolist() == [True, True, False]
