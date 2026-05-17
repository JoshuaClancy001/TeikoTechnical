import os

import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_PATH = "output/responder_boxplot.png"


def plot_responder_boxplot(df, path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(
        data=df,
        x="population",
        y="percentage",
        hue="response",
        palette={"yes": "#2196F3", "no": "#F44336"},
        ax=ax,
    )

    ax.set_title("Cell Population Frequencies by Response (Melanoma / Miraclib / PBMC)")
    ax.set_xlabel("Population")
    ax.set_ylabel("Percentage of Total (%)")
    ax.legend(title="Response")

    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved boxplot to {path}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from dataset import build_analysis_dataset

    df = build_analysis_dataset()
    plot_responder_boxplot(df)
