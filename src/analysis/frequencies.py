import pandas as pd
from sqlalchemy import create_engine, text

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db"))
from schema import DB_URL


def compute_relative_frequencies(db_url: str = DB_URL) -> pd.DataFrame:
    engine = create_engine(db_url)

    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT sample_id, population, count FROM cell_counts"), conn)

    df["total_count"] = df.groupby("sample_id")["count"].transform("sum")
    df["pct"] = (df["count"] / df["total_count"] * 100).round(2)

    return df[["sample_id", "population", "count", "total_count", "pct"]]


OUTPUT_PATH = "output/frequencies.csv"


def save(df: pd.DataFrame, path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def overview(df: pd.DataFrame) -> None:
    summary = (
        df.groupby("population")["pct"]
        .agg(mean="mean", min="min", max="max")
        .round(2)
    )
    print(f"\nSamples : {df['sample_id'].nunique()}")
    print(f"Populations : {df['population'].nunique()}")
    print(f"\nMean % per population across all samples:\n")
    print(summary.to_string())


if __name__ == "__main__":
    df = compute_relative_frequencies()
    save(df)
    overview(df)
