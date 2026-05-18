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

## Project Structure

```
.
├── .devcontainer/      # Codespaces configuration
├── data/               # Raw and processed data (gitignored)
├── output/             # Pipeline outputs (gitignored)
├── src/                # Source code
├── requirements.txt
└── Makefile
```


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


