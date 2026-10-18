# Beyond Star Ratings: Consumer Review Intelligence

A reproducible CodeAlpha Data Analytics internship project that combines exploratory data analysis, visualization, and sentiment screening to test whether star ratings fully describe customer experience.

## CodeAlpha alignment

This project completes three tasks from the official internship brief: **Task 2 — Exploratory Data Analysis**, **Task 3 — Data Visualization**, and **Task 4 — Sentiment Analysis**. The PDF requires completing at least two or three of the four listed tasks, uploading complete source code to a GitHub repository named `CodeAlpha_ProjectName`, posting a LinkedIn explanation video with the repository link, and submitting through the provided submission form. The PDF does not specify a deadline, dashboard hosting requirement, or required programming language.

## Business questions

1. How concentrated are ratings, and can a high average hide a meaningful negative minority?
2. How often does a simple text sentiment signal disagree with the numeric rating?
3. Which terms recur in negative reviews and can they suggest operational follow-up areas?
4. Do reviews with positive versus negative text differ in their ratings?
5. How does the mix change over time within the historical source data?

These are association questions. The project does not infer causation, fraud, or deceptive reviewing from a mismatch.

## Dataset and provenance

The project uses the **Gourmet Foods subset of the Stanford SNAP Amazon Reviews dataset**. Stanford documents the source, fields, historical coverage, and downloadable category files at <https://snap.stanford.edu/data/web-Amazon.html>. The dataset includes product ID, user ID, rating, helpfulness, timestamp, summary, and review text. The raw download is kept locally at `data/raw/Gourmet_Foods.txt.gz` and is not committed by default because the source file is large and the repository should retain a reproducible download instruction.

The source is historical and observational. Potential limitations include selection bias, merged/duplicate reviews in the broader SNAP data, changing review behavior over time, lack of an independent human sentiment label, and the absence of business cost or product quality outcomes.

## Verified run results

The pipeline parsed 154,635 raw records and retained 154,502 records after removing 122 duplicates/invalid rows and 11 non-positive timestamp placeholders. The final mean rating is 4.24/5. A simple lexicon screen marked 5.52% of reviews as rating–text mismatches. The contingency test between rating-derived polarity and lexicon polarity produced Cramer's/phi-style association magnitude 0.457 with p < 0.001; this confirms the variables are related, not that either method is ground truth. The text-only TF-IDF/logistic regression benchmark achieved negative-class F1 0.819 and positive-class F1 0.965 on a stratified holdout of rating-aligned labels. These metrics evaluate agreement with rating-derived labels, not human sentiment truth.

The most frequent terms in screened negative reviews include `like`, `bad`, `taste`, `product`, `just`, `tea`, `flavor`, and `stale`. Raw term counts are not causal complaint priorities; they need product-level review and context before action.

## Project structure

- `run_pipeline.py`: end-to-end parsing, cleaning, sentiment scoring, analysis, modeling, and chart generation.
- `app.py`: Streamlit dashboard.
- `src/`: reusable preprocessing, sentiment, analysis, and visualization modules.
- `data/raw/`: downloaded source file.
- `data/processed/`: generated clean analytical table.
- `reports/`: computed results, executive summary, methodology, and negative-term table.
- `assets/`: generated PNG charts.
- `tests/`: automated unit tests.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
python -m pytest -q
streamlit run app.py
```

If the raw file is missing, download it from the official Stanford page and place it at `data/raw/Gourmet_Foods.txt.gz`. Do not replace the source with a fabricated or randomly generated dataset.

## GitHub and LinkedIn checklist

Create a repository named `CodeAlpha_BeyondStarRatings` or another name following the required `CodeAlpha_ProjectName` pattern. Commit source code, reports, charts, tests, and the data README; do not commit secrets or unnecessary personal identifiers. Push the repository, verify that a fresh clone can run the commands above, record a 2–3 minute walkthrough of the business problem, source, pipeline, dashboard, one evidence-backed finding, and limitations, then post the video on LinkedIn tagging `@CodeAlpha` and include the GitHub link. Finally complete the CodeAlpha submission form shared in the internship WhatsApp group. The PDF says that the form is the required submission channel but does not provide the form URL in the attachment.

## Important limitation

The project is a strong reproducible internship submission, not a production sentiment system. Before claiming a complaint theme is a business priority, manually inspect representative reviews and validate the theme with an independently labeled sample or stakeholder-defined taxonomy.
