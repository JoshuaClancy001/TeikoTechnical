import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db"))
from schema import DB_URL

from frequencies import compute_relative_frequencies

CONDITION = "melanoma"
TREATMENT = "miraclib"
SAMPLE_TYPE = "PBMC"


def build_analysis_dataset(db_url: str = DB_URL) -> pd.DataFrame:
    engine = create_engine(db_url)

    query = text("""
        SELECT
            sa.sample_id,
            su.subject_id,
            su.response
        FROM samples sa
        JOIN subjects su ON sa.subject_id = su.subject_id
        WHERE
            su.condition   = :condition
            AND su.treatment   = :treatment
            AND sa.sample_type = :sample_type
    """)

    with engine.connect() as conn:
        cohort = pd.read_sql(query, conn, params={
            "condition": CONDITION,
            "treatment": TREATMENT,
            "sample_type": SAMPLE_TYPE,
        })

    freq = compute_relative_frequencies(db_url)[["sample_id", "population", "pct"]]

    df = cohort.merge(freq, on="sample_id", how="inner")
    df = df.rename(columns={"pct": "percentage"})

    return df[["sample_id", "subject_id", "response", "population", "percentage"]]


def split_by_response(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    responders = df[df["response"] == "yes"].copy()
    non_responders = df[df["response"] == "no"].copy()
    return responders, non_responders


if __name__ == "__main__":
    df = build_analysis_dataset()
    responders, non_responders = split_by_response(df)

    print(f"Subjects    : {df['subject_id'].nunique()}")
    print(f"Samples     : {df['sample_id'].nunique()}")
    print(f"Responders  : {responders['subject_id'].nunique()} subjects")
    print(f"Non-resp.   : {non_responders['subject_id'].nunique()} subjects")
    print()
    print(df.head(10).to_string(index=False))
