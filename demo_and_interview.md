# 2–3 minute demonstration script

1. Introduce the problem: star averages can hide negative experiences, so this dashboard compares ratings with review text.
2. Show the source and explain why Stanford SNAP Gourmet Foods was selected over Yelp's much larger educational download and UCI's non-review dataset.
3. Run the pipeline or show the generated results: 154,502 usable reviews, 4.24/5 average rating, 5.52% mismatch screening rate.
4. Open the dashboard, filter negative text, and show the rating/text comparison and supporting records.
5. Explain the leading negative terms and explicitly say they are candidate themes, not causal root causes.
6. Close with limitations: historical observational data, simple lexicon, no independent human labels, and no fraud claim.

# Likely interview questions

1. Why this dataset? — It contains both ratings and review text in a manageable official category file.
2. Why not use the average rating alone? — Averages can conceal a minority of negative experiences.
3. What is a mismatch? — A transparent rule comparing extreme rating bands with lexicon polarity; it is not fraud detection.
4. Why use Mann–Whitney U? — Ratings are ordinal and skewed, so a non-parametric comparison is safer than assuming normality.
5. Why report effect size? — Large samples make p-values tiny; effect size describes practical association magnitude.
6. What is the model target? — Rating-aligned polarity, not independently labeled human sentiment.
7. How did you avoid leakage? — The TF-IDF model is fit only on the training split before test prediction.
8. What would you improve first? — Create a stratified human-labeled evaluation sample and validate a domain-specific taxonomy.
9. Why not infer causation? — Reviews are observational and confounded by product, customer, and time effects.
10. What should a business do next? — Sample themes by product, validate them with owners, and prioritize by volume, severity, and actionability.
