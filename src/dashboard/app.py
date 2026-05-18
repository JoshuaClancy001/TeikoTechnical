import os
import sys

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analysis"))

from schema import DB_URL
from frequencies import compute_relative_frequencies
from dataset import build_analysis_dataset
from stats import run_mannwhitney
from subset_analysis import (
    BASELINE_FILTER,
    _load_baseline,
    avg_bcell_count,
    samples_by_project,
    subjects_by_response,
    subjects_by_sex,
)

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
BOXPLOT_PATH = os.path.join(ROOT, "output", "responder_boxplot.png")


@st.cache_data
def get_overview():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        subjects = conn.execute(text("SELECT COUNT(*) FROM subjects")).scalar()
        samples = conn.execute(text("SELECT COUNT(*) FROM samples")).scalar()
        populations = conn.execute(text("SELECT COUNT(DISTINCT population) FROM cell_counts")).scalar()
        projects = conn.execute(text("SELECT COUNT(DISTINCT project) FROM subjects")).scalar()
    return subjects, samples, populations, projects


@st.cache_data
def get_frequencies():
    return compute_relative_frequencies()


@st.cache_data
def get_responder_stats():
    df = build_analysis_dataset()
    return run_mannwhitney(df)


@st.cache_data
def get_subset():
    engine = create_engine(DB_URL)
    baseline = _load_baseline(engine)
    return (
        samples_by_project(baseline),
        subjects_by_response(baseline),
        subjects_by_sex(baseline),
        avg_bcell_count(engine),
    )


st.set_page_config(page_title="Clinical Trial Analytics", layout="wide")
st.title("Clinical Trial Analytics Dashboard")

# ── Section 1: Overview ──────────────────────────────────────────────────────
st.header("Dataset Overview")
subjects, samples, populations, projects = get_overview()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Subjects", subjects)
c2.metric("Samples", samples)
c3.metric("Populations", populations)
c4.metric("Projects", projects)

st.divider()

# ── Section 2: Frequencies Table ─────────────────────────────────────────────
st.header("Relative Frequencies")
freq = get_frequencies()

col1, col2 = st.columns(2)
population_filter = col1.multiselect(
    "Filter by population",
    options=sorted(freq["population"].unique()),
    default=[],
)
sample_search = col2.text_input("Search sample ID")

filtered = freq.copy()
if population_filter:
    filtered = filtered[filtered["population"].isin(population_filter)]
if sample_search:
    filtered = filtered[filtered["sample_id"].str.contains(sample_search, case=False)]

st.dataframe(filtered, use_container_width=True, hide_index=True)

st.divider()

# ── Section 3: Responder Analysis ────────────────────────────────────────────
st.header("Responder Analysis — Melanoma / Miraclib / PBMC")

if os.path.exists(BOXPLOT_PATH):
    st.image(BOXPLOT_PATH, caption="Cell Population Frequencies by Response")
else:
    st.warning("Boxplot not found. Run `make pipeline` to generate it.")

st.subheader("Mann–Whitney U Results")
stats = get_responder_stats()
display = stats.copy()
display["significant"] = display["significant"].map({True: "Yes", False: "No"})
st.dataframe(display, use_container_width=True, hide_index=True)

st.divider()

# ── Section 4: Subset Analysis ───────────────────────────────────────────────
st.header("Baseline Subset Analysis (Melanoma / Miraclib / PBMC / Day 0)")

by_project, by_response, by_sex, avg_b = get_subset()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Samples by Project")
    st.dataframe(by_project, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Subjects by Response")
    st.dataframe(by_response, use_container_width=True, hide_index=True)

with col3:
    st.subheader("Subjects by Sex")
    st.dataframe(by_sex, use_container_width=True, hide_index=True)

st.metric("Avg B Cell Count (male responders, day 0)", avg_b)
