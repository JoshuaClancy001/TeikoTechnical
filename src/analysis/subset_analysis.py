import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db"))
from schema import DB_URL

OUTPUT_PATH = "output/subset_analysis.csv"

BASELINE_FILTER = {
    "condition": "melanoma",
    "treatment": "miraclib",
    "sample_type": "PBMC",
    "time_from_treatment_start": 0,
}


def _load_baseline(engine) -> pd.DataFrame:
    query = text("""
        SELECT
            su.subject_id,
            su.project,
            su.response,
            su.sex,
            sa.sample_id
        FROM subjects su
        JOIN samples sa ON su.subject_id = sa.subject_id
        WHERE su.condition              = :condition
          AND su.treatment              = :treatment
          AND sa.sample_type            = :sample_type
          AND sa.time_from_treatment_start = :time_from_treatment_start
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params=BASELINE_FILTER)


def samples_by_project(baseline: pd.DataFrame) -> pd.DataFrame:
    return (
        baseline.groupby("project")["sample_id"]
        .nunique()
        .reset_index()
        .rename(columns={"sample_id": "sample_count"})
        .sort_values("sample_count", ascending=False)
    )


def subjects_by_response(baseline: pd.DataFrame) -> pd.DataFrame:
    return (
        baseline.drop_duplicates("subject_id")
        .groupby("response")["subject_id"]
        .nunique()
        .reset_index()
        .rename(columns={"subject_id": "subject_count"})
    )


def subjects_by_sex(baseline: pd.DataFrame) -> pd.DataFrame:
    return (
        baseline.drop_duplicates("subject_id")
        .groupby("sex")["subject_id"]
        .nunique()
        .reset_index()
        .rename(columns={"subject_id": "subject_count"})
    )


def avg_bcell_count(engine) -> float:
    query = text("""
        SELECT ROUND(AVG(cc.count), 2) AS avg_b_cell
        FROM subjects su
        JOIN samples sa  ON su.subject_id = sa.subject_id
        JOIN cell_counts cc ON sa.sample_id = cc.sample_id
        WHERE su.condition                  = :condition
          AND su.treatment                  = :treatment
          AND sa.sample_type                = :sample_type
          AND sa.time_from_treatment_start  = :time_from_treatment_start
          AND su.sex                        = 'M'
          AND su.response                   = 'yes'
          AND cc.population                 = 'b_cell'
    """)
    with engine.connect() as conn:
        result = conn.execute(query, BASELINE_FILTER).scalar()
    return result


def save(results: dict[str, pd.DataFrame], path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sections = []
    for label, df in results.items():
        df = df.copy()
        df.insert(0, "metric", label)
        sections.append(df)
    pd.concat(sections, ignore_index=True).to_csv(path, index=False)
    print(f"Saved results to {path}")


def run(db_url: str = DB_URL) -> None:
    engine = create_engine(db_url)
    baseline = _load_baseline(engine)

    by_project = samples_by_project(baseline)
    by_response = subjects_by_response(baseline)
    by_sex = subjects_by_sex(baseline)
    avg_b = avg_bcell_count(engine)

    print(f"Baseline cohort: {baseline['sample_id'].nunique()} samples, "
          f"{baseline['subject_id'].nunique()} subjects\n")

    print("Samples by project:")
    print(by_project.to_string(index=False))

    print("\nSubjects by response:")
    print(by_response.to_string(index=False))

    print("\nSubjects by sex:")
    print(by_sex.to_string(index=False))

    print(f"\nAverage B cell count (male, responders, baseline): {avg_b}")

    save({
        "samples_by_project": by_project,
        "subjects_by_response": by_response,
        "subjects_by_sex": by_sex,
    })


if __name__ == "__main__":
    run()
