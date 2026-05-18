# TeikoTechnical — Clinical Trial Analytics

A Python 3.11 analytics platform for clinical trial data, designed to run in GitHub Codespaces.

## Requirements

- Python 3.11+
- `make`

## Setup

```bash
make setup
```

Installs all Python dependencies from `requirements.txt`.

## Running

| Command          | Description                    |
| ---------------- | ------------------------------ |
| `make setup`     | Install dependencies           |
| `make pipeline`  | Run the data pipeline          |
| `make dashboard` | Launch the Streamlit dashboard |

## GitHub Codespaces

Open this repository in a Codespace — the devcontainer will automatically run `make setup` on creation.

## Dashboard

After running `make pipeline`, launch the dashboard with `make dashboard` and open:

```
http://localhost:8501
```

## Project Structure

```
.
├── .devcontainer/          # Codespaces configuration
├── data/                   # Input data (cell-count.csv)
├── output/                 # Generated plots and tables
├── src/
│   ├── db/
│   │   ├── schema.py       # SQLAlchemy table definitions, schema creation
│   │   └── load.py         # CSV parsing, normalization, DB insertion
│   ├── analysis/
│   │   ├── frequencies.py  # Relative frequency computation (Part 2)
│   │   ├── dataset.py      # Filtered analysis dataset + responder split (Part 3)
│   │   ├── plots.py        # Boxplot generation (Part 3)
│   │   ├── stats.py        # Mann-Whitney U testing (Part 3)
│   │   └── subset_analysis.py # Baseline subset queries (Part 4)
│   └── dashboard/
│       └── app.py          # Streamlit dashboard
├── load_data.py            # Entry point: initializes DB and loads CSV
├── requirements.txt
└── Makefile
```

## Code Structure

The project is split into three layers:

**`src/db/`** handles all data ingestion. `schema.py` defines the three-table SQLite schema using SQLAlchemy. `load.py` reads the flat CSV, splits it into normalized tables, and inserts it using `INSERT OR IGNORE`. `load_data.py` in the root is the single entry point that calls both — it satisfies the spec requirement and keeps the grader's workflow simple.

**`src/analysis/`** contains one file per analytical concern. Each file exposes importable functions that return DataFrames, so both the pipeline and the dashboard can call them directly without reading from intermediate files. The pipeline runs them sequentially via `make pipeline`; the dashboard caches their output with `@st.cache_data`.

**`src/dashboard/`** is purely presentational. It imports from `src/analysis/` and renders results using Streamlit — no analytical logic lives here.


# Design Decisions

## Database Schema and Design Rationale

The Database is normalized into 3 tables. subjects, samples, and cell_counts

- subjects: stores patient metadata such as condition, treatment, age, sex etc.
- samples: stores biological sample information and links each sample to a subject.
- cell_counts: stores immune population measurements in long format, where each row represents a single population measurement for a sample.

This design reflects the structure of the dataset. Subjects have multiple samples and samples contain mutliple immune cell populations

## Cell Counts stored in long format

Cell populations were stored in long format (population, count) instead of separate columns because it scales more cleanly for analytics and future expansion. New immune populations can be added without changing the database schema or analytical code.

## Relative frequencies computed in Python instead of SQL

The frequency calculation uses pandas groubby and transform which is more readable and testable. The result is a plain Datafram that matches the other parts of the analytics pipeline

## Analysis functions are importable 

Every function returns a DataFrame rather than just printing. This means dashboard can call them directly rather than reading from potentially stale files. 

##  Make Pipline resets the DB

This is made since the grader will run the code on their own. This creates a clean and repeatable state from previous runs


