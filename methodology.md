# Methodology and Limitations

## Dataset choice

The proposed review-intelligence idea was compared with two alternatives. Yelp Open Dataset offers richer business attributes and reviews, but the official download is 4.35 GB compressed and intended for educational use, making it less reproducible on a normal laptop. The UCI Online Shoppers dataset is small and CC BY 4.0, but it has browsing-session behavior rather than review text and ratings, so it cannot answer the proposed mismatch and complaint-theme questions. The Stanford SNAP Amazon category subset is the strongest fit because it has review text, numeric ratings, helpfulness, product/user identifiers, and timestamps in a manageable category file.

## Preparation

The parser reads Stanford's `key: value` blocks from gzip without using a synthetic dataset. Numeric fields are coerced with errors becoming missing. Review timestamps are converted from Unix seconds. Helpfulness is split into numerator, denominator, and a zero-safe rate. Empty review text, invalid ratings outside 1–5, duplicate records on user/product/time/text, and non-positive timestamps are removed. The cleaning log is stored in `reports/results.json`.

The source reports historical coverage. Invalid placeholder timestamp rows are excluded rather than silently retained. The raw download remains separate from `data/processed/reviews_processed.csv`.

## Labels and sentiment

Rating-derived polarity is defined as 1–2 negative, 3 neutral, and 4–5 positive. The baseline sentiment method is a transparent small lexicon of positive and negative terms. Its score is net matched terms divided by the square root of token count. Scores above 0.05 are positive, below -0.05 negative, and otherwise neutral.

A mismatch is flagged only when a 4–5 star review receives a negative lexicon label or a 1–2 star review receives a positive lexicon label. This is an analytical screening rule. It does not identify fake, deceptive, or fraudulent reviews.

The second approach is a TF-IDF word/phrase model with logistic regression. It uses a deterministic stratified holdout and class weighting. The target is rating-aligned polarity because no independent sentiment labels are supplied. This prevents overstating model validity.

## Statistical analysis

The rating/sentiment relationship is tested with a chi-square test of independence and an association magnitude calculated as sqrt(chi-square / N). The rating distributions for positive versus negative lexicon groups are compared with a two-sided Mann–Whitney U test because ratings are ordinal and heavily skewed. A standardized mean difference is reported as a descriptive effect size. With a large sample, p-values are expected to be tiny; effect sizes and sample sizes are therefore reported alongside them.

## Visual analysis

The pipeline saves rating distribution, sentiment distribution, negative-term frequency, and negative-rate-by-year charts. The Streamlit dashboard adds filters and supporting records. Charts are intended to answer specific questions rather than decorate the report.

## Limitations and next tests

The lexicon is not a language model and does not reliably understand negation, sarcasm, or food-specific context. The model's labels are derived from ratings, so its performance is not independent human sentiment accuracy. The sample is historical, self-selected, and not necessarily representative of all customers. Product-level confounding and review duplication can affect apparent themes. Before deployment, manually label a stratified sample, compare a stronger model, inspect calibration, test sensitivity to mismatch thresholds, and validate themes with business owners.
