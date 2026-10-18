from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parent
DATA = ROOT / "data/processed/reviews_processed.csv"
THEMES = ROOT / "reports/negative_themes.csv"

st.set_page_config(
    page_title="Beyond Star Ratings | Review Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Design system
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
      --ink: #e9f1ff;
      --muted: #91a3c1;
      --line: rgba(148, 163, 184, .16);
      --panel: rgba(17, 28, 51, .76);
      --panel-2: rgba(22, 36, 66, .88);
      --cyan: #62e6e2;
      --violet: #9b8cff;
      --coral: #ff7f8a;
      --gold: #f8cc72;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
      background: radial-gradient(circle at 82% 0%, rgba(91, 78, 180, .22), transparent 30%),
                  radial-gradient(circle at 8% 4%, rgba(40, 188, 189, .13), transparent 27%),
                  #07101f;
      color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, rgba(8, 18, 36, .98), rgba(11, 22, 43, .96));
      border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--ink); }
    .block-container { max-width: 1480px; padding: 2.2rem 3.4rem 4rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -.035em; color: var(--ink); }
    h1 { font-size: clamp(2.8rem, 5vw, 5.4rem); line-height: .98; margin: 0; }
    h2 { font-size: 1.7rem; margin-top: 1.8rem; }
    h3 { font-size: 1.2rem; }
    p, li { color: var(--muted); }
    .brand-mark { color: var(--cyan); font-size: 1.05rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
    .eyebrow { color: var(--cyan); font-size: .76rem; text-transform: uppercase; letter-spacing: .19em; font-weight: 700; margin-bottom: 1rem; }
    .hero { padding: 1rem 0 2.4rem; }
    .hero-copy { max-width: 780px; color: var(--muted); font-size: 1.07rem; line-height: 1.7; margin-top: 1.35rem; }
    .hero-rule { height: 1px; background: linear-gradient(90deg, var(--cyan), rgba(98,230,226,0)); margin: 2rem 0 1.3rem; }
    .hero-note { color: var(--muted); font-size: .86rem; }
    .metric-card { background: linear-gradient(145deg, rgba(20, 38, 68, .95), rgba(13, 24, 46, .85)); border: 1px solid var(--line); border-radius: 20px; padding: 1.25rem 1.3rem; min-height: 128px; box-shadow: 0 18px 55px rgba(0,0,0,.18); }
    .metric-label { color: var(--muted); text-transform: uppercase; letter-spacing: .12em; font-size: .68rem; font-weight: 700; }
    .metric-value { font-family: 'Space Grotesk'; color: var(--ink); font-size: 2.35rem; font-weight: 700; margin-top: .55rem; }
    .metric-accent { color: var(--cyan); }
    .metric-sub { color: var(--muted); font-size: .78rem; margin-top: .3rem; }
    .section-kicker { display: flex; align-items: center; gap: .7rem; margin: 2.2rem 0 .6rem; color: var(--cyan); text-transform: uppercase; letter-spacing: .15em; font-size: .72rem; font-weight: 700; }
    .section-kicker:before { content: ''; display: inline-block; width: 27px; height: 2px; background: var(--cyan); }
    .story-card { background: linear-gradient(145deg, rgba(19, 34, 63, .9), rgba(11, 21, 40, .92)); border: 1px solid var(--line); border-radius: 22px; padding: 1.4rem 1.5rem; height: 100%; }
    .story-number { font-family: 'Space Grotesk'; color: var(--violet); font-size: 2.2rem; font-weight: 700; }
    .story-title { color: var(--ink); font-size: 1.02rem; font-weight: 700; margin: .45rem 0 .55rem; }
    .story-text { color: var(--muted); font-size: .88rem; line-height: 1.6; }
    .callout { border-left: 3px solid var(--cyan); background: rgba(98, 230, 226, .06); padding: 1.05rem 1.25rem; border-radius: 0 14px 14px 0; color: var(--ink); line-height: 1.6; }
    .method-card { border: 1px solid var(--line); border-radius: 18px; background: rgba(15, 29, 53, .66); padding: 1.2rem; }
    .method-card strong { color: var(--ink); }
    .footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .8rem; }
    [data-testid="stMetric"] { background: transparent; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    div[data-baseweb="select"] > div { background: rgba(20, 34, 60, .9); border-color: var(--line); }
    .stTabs [data-baseweb="tab-list"] { gap: 1.4rem; border-bottom: 1px solid var(--line); }
    .stTabs [data-baseweb="tab"] { color: var(--muted); padding: .8rem .2rem; }
    .stTabs [aria-selected="true"] { color: var(--cyan); }
    </style>
    """,
    unsafe_allow_html=True,
)

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_LAYOUT = dict(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#91a3c1"),
    title_font=dict(family="Space Grotesk", color="#e9f1ff", size=18),
    margin=dict(l=12, r=12, t=58, b=15),
    hoverlabel=dict(bgcolor="#142443", font_color="#e9f1ff"),
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA, parse_dates=["review_date"])

@st.cache_data
def load_themes():
    return pd.read_csv(THEMES)


def card(label, value, sub, accent=False):
    color = "metric-accent" if accent else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value {color}">{value}</div><div class="metric-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def style_fig(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,.10)", zeroline=False)
    return fig


df = load_data()
themes = load_themes()

# Sidebar controls
with st.sidebar:
    st.markdown('<div class="brand-mark">✦ Review Intelligence</div>', unsafe_allow_html=True)
    st.markdown("### Explore the evidence")
    st.caption("Use filters to move from the portfolio-level signal to the supporting review records.")
    scores = st.multiselect("Star ratings", sorted(df.score.dropna().unique()), default=sorted(df.score.dropna().unique()))
    years = st.multiselect("Review years", sorted(df.year.dropna().unique()), default=sorted(df.year.dropna().unique()))
    sentiments = st.multiselect("Text sentiment", ["negative", "neutral", "positive"], default=["negative", "neutral", "positive"])
    st.markdown("---")
    st.caption("Source")
    st.markdown("**Stanford SNAP · Amazon Reviews**")
    st.caption("Gourmet Foods subset · historical observational data")

filtered = df[df.score.isin(scores) & df.year.isin(years) & df.lexicon_sentiment.isin(sentiments)].copy()

# Hero
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">Consumer experience analytics · CodeAlpha portfolio project</div>', unsafe_allow_html=True)
st.markdown("# Beyond<br>Star Ratings", unsafe_allow_html=True)
st.markdown('<p class="hero-copy">A premium review intelligence workspace for discovering what average ratings leave unsaid — combining structured ratings, language signals, recurring themes and supporting records.</p>', unsafe_allow_html=True)
st.markdown('<div class="hero-rule"></div><div class="hero-note">The interface is designed around one principle: every visual should lead to a question, and every question should lead back to evidence.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# KPI row
k1, k2, k3, k4 = st.columns(4)
with k1: card("Reviews in view", f"{len(filtered):,}", "after current filters", True)
with k2: card("Average rating", f"{filtered.score.mean():.2f}/5", "numeric experience signal")
with k3: card("Negative text", f"{(filtered.lexicon_sentiment == 'negative').mean():.1%}", "lexicon screening baseline")
with k4: card("Mismatch signal", f"{filtered.rating_sentiment_mismatch.mean():.1%}", "rating and text disagree")

st.markdown('<div class="section-kicker">The story in three signals</div>', unsafe_allow_html=True)
st.markdown("## What the data is telling us", unsafe_allow_html=True)

story1, story2, story3 = st.columns(3)
with story1:
    st.markdown('<div class="story-card"><div class="story-number">01</div><div class="story-title">The average is optimistic</div><div class="story-text">Star ratings lean strongly positive. That makes the smaller negative minority easy to overlook — and potentially valuable for product improvement.</div></div>', unsafe_allow_html=True)
with story2:
    st.markdown('<div class="story-card"><div class="story-number">02</div><div class="story-title">Language adds texture</div><div class="story-text">Text sentiment gives a second lens. It can reveal emotional language that a single star value cannot explain on its own.</div></div>', unsafe_allow_html=True)
with story3:
    st.markdown('<div class="story-card"><div class="story-number">03</div><div class="story-title">Themes create a route to action</div><div class="story-text">Repeated terms such as taste, flavor and stale are investigation leads — not causal conclusions — for a business team to validate.</div></div>', unsafe_allow_html=True)

# Tabs for guided experience
st.markdown('<div class="section-kicker">Evidence lab</div>', unsafe_allow_html=True)
tab_overview, tab_mismatch, tab_themes, tab_records = st.tabs(["Overview", "Mismatch explorer", "Theme intelligence", "Supporting records"])

with tab_overview:
    left, right = st.columns(2)
    with left:
        counts = filtered.score.value_counts().sort_index().rename_axis("score").reset_index(name="reviews")
        fig = px.bar(counts, x="score", y="reviews", color="score", color_continuous_scale=["#ff7f8a", "#f8cc72", "#62e6e2"], title="How ratings are distributed")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with right:
        sc = filtered.lexicon_sentiment.value_counts().reindex(["negative", "neutral", "positive"]).fillna(0).rename_axis("sentiment").reset_index(name="reviews")
        fig = px.bar(sc, x="sentiment", y="reviews", color="sentiment", color_discrete_map={"negative":"#ff7f8a", "neutral":"#91a3c1", "positive":"#62e6e2"}, title="What the text signal detects")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    yearly = filtered.groupby("year").agg(reviews=("score", "size"), negative_rate=("rating_label", lambda s: (s == "negative").mean())).reset_index()
    fig = px.line(yearly, x="year", y="negative_rate", markers=True, title="Does the negative share change over time?", color_discrete_sequence=["#ff7f8a"])
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(style_fig(fig, 340), use_container_width=True)

with tab_mismatch:
    st.markdown("### Where do the two signals disagree?")
    st.markdown('<div class="callout">A mismatch is a screening signal, not evidence of a fake or deceptive review. It flags extreme ratings whose text polarity points the other way.</div>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered.score, filtered.lexicon_sentiment).reindex(columns=["negative", "neutral", "positive"], fill_value=0).reset_index().melt(id_vars="score", var_name="sentiment", value_name="reviews")
    fig = px.bar(cross, x="score", y="reviews", color="sentiment", barmode="group", title="Rating × text sentiment", color_discrete_map={"negative":"#ff7f8a", "neutral":"#91a3c1", "positive":"#62e6e2"})
    st.plotly_chart(style_fig(fig, 410), use_container_width=True)
    mm = filtered[filtered.rating_sentiment_mismatch]
    a, b = st.columns(2)
    with a: card("Mismatch records", f"{len(mm):,}", "current filter scope", True)
    with b: card("Share of view", f"{len(mm) / max(len(filtered), 1):.1%}", "screening rate")

with tab_themes:
    st.markdown("### What keeps appearing in negative reviews?")
    st.caption("Frequency is a discovery tool. Validate context and product concentration before recommending action.")
    plot_themes = themes.sort_values("count").tail(15)
    fig = px.bar(plot_themes, x="count", y="term", orientation="h", title="Recurring terms in negative-text reviews", color="count", color_continuous_scale=["#3a315f", "#9b8cff", "#62e6e2"])
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(style_fig(fig, 520), use_container_width=True)
    st.dataframe(themes.head(20), use_container_width=True, hide_index=True)

with tab_records:
    st.markdown("### Trace every headline back to evidence")
    record_type = st.radio("Show", ["Potential mismatches", "Negative text with low ratings", "Most helpful negative records"], horizontal=True)
    if record_type == "Potential mismatches":
        records = filtered[filtered.rating_sentiment_mismatch]
    elif record_type == "Negative text with low ratings":
        records = filtered[(filtered.lexicon_sentiment == "negative") & (filtered.score <= 2)]
    else:
        records = filtered[filtered.lexicon_sentiment == "negative"].sort_values("helpfulness_rate", ascending=False)
    st.dataframe(records[["product_id", "score", "lexicon_score", "helpfulness_rate", "summary", "review_text", "review_date"]].head(100), use_container_width=True, hide_index=True)

# Methodology section
st.markdown('<div class="section-kicker">How it works</div>', unsafe_allow_html=True)
st.markdown("## Transparent by design", unsafe_allow_html=True)
mc1, mc2, mc3 = st.columns(3)
with mc1:
    st.markdown('<div class="method-card"><strong>01 · Prepare</strong><br><span>Parse the official SNAP format, remove duplicates and invalid timestamps, preserve raw and processed data separately.</span></div>', unsafe_allow_html=True)
with mc2:
    st.markdown('<div class="method-card"><strong>02 · Compare</strong><br><span>Use rating bands and a transparent lexicon baseline, then benchmark a TF-IDF logistic regression model without test leakage.</span></div>', unsafe_allow_html=True)
with mc3:
    st.markdown('<div class="method-card"><strong>03 · Validate</strong><br><span>Use the dashboard for prioritization, then manually inspect records before treating themes as business actions.</span></div>', unsafe_allow_html=True)

with st.expander("Read the limitations before drawing conclusions"):
    st.markdown("""
    This is historical, observational review data. The lexicon can miss negation, sarcasm and domain-specific meaning. The machine-learning benchmark predicts rating-aligned labels rather than independently human-labeled sentiment. Reviewers are self-selected, and association does not establish causation. A mismatch must not be interpreted as fraud or deception.
    """)

st.markdown('<div class="footer">Built for CodeAlpha Data Analytics · Tasks 2, 3 and 4 · Source: Stanford SNAP Amazon Reviews · Evidence first, claims second.</div>', unsafe_allow_html=True)
