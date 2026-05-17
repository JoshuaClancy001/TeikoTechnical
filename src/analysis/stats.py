import os

import pandas as pd
from scipy.stats import mannwhitneyu

OUTPUT_PATH = "output/statistical_results.csv"


def run_mannwhitney(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for population, group in df.groupby("population"):
        responders = group[group["response"] == "yes"]["percentage"]
        non_responders = group[group["response"] == "no"]["percentage"]

        _, p_value = mannwhitneyu(responders, non_responders, alternative="two-sided")

        results.append({
            "population": population,
            "responder_median": round(responders.median(), 2),
            "non_responder_median": round(non_responders.median(), 2),
            "p_value": round(p_value, 4),
            "significant": p_value < 0.05,
        })

    return pd.DataFrame(results).sort_values("p_value")


def print_summary(results: pd.DataFrame) -> None:
    significant = results[results["significant"]]

    if significant.empty:
        print("No populations reached statistical significance (p < 0.05).")
    else:
        print("Significant populations (p < 0.05):")
        for _, row in significant.iterrows():
            print(f"  - {row['population']} (p={row['p_value']})")


def save(results: pd.DataFrame, path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    results.to_csv(path, index=False)
    print(f"Saved results to {path}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from dataset import build_analysis_dataset

    df = build_analysis_dataset()
    results = run_mannwhitney(df)
    save(results)
    print()
    print_summary(results)
