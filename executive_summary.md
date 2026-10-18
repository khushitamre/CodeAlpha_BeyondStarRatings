# Executive Summary

## Decision context

A 4- or 5-star average can conceal a smaller but actionable set of negative experiences. This project screens review text alongside ratings to identify where the two signals diverge and to surface recurring language for follow-up.

## Evidence from the analyzed dataset

The Stanford SNAP Gourmet Foods subset produced **154,502 usable reviews** after transparent cleaning. The mean rating was **4.24/5**, indicating a strongly positive rating distribution. The simple lexicon baseline marked **5.52%** of records as rating–text mismatches. This is a screening rate, not a fraud rate.

A chi-square test of rating-derived polarity against lexicon polarity found a statistically significant association, with an association magnitude of **0.457** on **154,502** reviews. Because the sample is large, the p-value is below 0.001; the effect size is more informative than significance alone. Reviews with positive lexicon scores had a mean rating of **4.54** across **115,101** reviews, while negative-score reviews averaged **2.15** across **6,997** reviews. The gap is descriptive and does not prove that the text caused the rating.

The most frequent terms in screened negative reviews included **bad, taste, product, tea, flavor, stale, money,** and **terrible**. These terms are candidate investigation areas. They are not validated root causes because simple counts ignore context, negation, product mix, and exposure.

A text-only TF-IDF/logistic regression benchmark, trained to reproduce rating-aligned positive/negative labels, achieved negative F1 **0.819** and positive F1 **0.965** on a stratified holdout. This is a model agreement benchmark, not an externally valid sentiment score.

## Recommended business use

Use the dashboard to filter for low ratings, negative text, and mismatch records. Then sample reviews manually by product and theme. If a business wants to operationalize this, the next step is an independently labeled evaluation set with a taxonomy such as taste, freshness, packaging, delivery, value, and preparation experience. Prioritize themes only after considering review volume, negative share, product concentration, and actionability together.

## Limitations

The source is historical and observational. Reviewers are self-selected, ratings may be inflated, and the lexicon can miss sarcasm, negation, and domain language. The project has no verified ground-truth sentiment labels, business costs, customer lifetime value, or experimental intervention. Therefore, findings support prioritization for investigation, not causal claims or automated customer decisions.
