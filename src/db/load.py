import os

import pandas as pd
from sqlalchemy import create_engine

from schema import DB_URL

CSV_PATH = os.environ.get("CSV_PATH", "data/cell-count.csv")

SUBJECT_COLS = ["subject", "project", "condition", "age", "sex", "treatment", "response"]
SAMPLE_COLS = ["sample", "subject", "sample_type", "time_from_treatment_start"]
CELL_POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def load_csv(path: str = CSV_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def inspect(df: pd.DataFrame) -> None:
    print(f"Rows           : {len(df)}")
    print(f"Unique subjects: {df['subject'].nunique()}")
    print(f"Unique samples : {df['sample'].nunique()}")


def _extract_subjects(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[SUBJECT_COLS]
        .drop_duplicates(subset="subject")
        .rename(columns={"subject": "subject_id"})
    )


def _extract_samples(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[SAMPLE_COLS]
        .drop_duplicates(subset="sample")
        .rename(columns={"sample": "sample_id", "subject": "subject_id"})
    )


def _extract_cell_counts(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["sample"] + CELL_POPULATIONS]
        .rename(columns={"sample": "sample_id"})
        .melt(id_vars="sample_id", var_name="population", value_name="count")
    )


def _insert_ignore(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    conn.execute(table.table.insert().prefix_with("OR IGNORE"), data)


def insert(df: pd.DataFrame, db_url: str = DB_URL) -> None:
    engine = create_engine(db_url)

    subjects = _extract_subjects(df)
    samples = _extract_samples(df)
    cell_counts = _extract_cell_counts(df)

    subjects.to_sql("subjects", engine, if_exists="append", index=False, method=_insert_ignore)
    print(f"Inserted {len(subjects)} subjects")

    samples.to_sql("samples", engine, if_exists="append", index=False, method=_insert_ignore)
    print(f"Inserted {len(samples)} samples")

    cell_counts.to_sql("cell_counts", engine, if_exists="append", index=False, method=_insert_ignore)
    print(f"Inserted {len(cell_counts)} cell count rows")


if __name__ == "__main__":
    df = load_csv()
    inspect(df)
    insert(df)
