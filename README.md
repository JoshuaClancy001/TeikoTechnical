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

## Database Schema and Design Rationale

The Database is normalized into 3 tables. subjects, samples, and cell_counts

- subjects: stores patient metadata such as condition, treatment, age, sex etc.
- samples: stores biological sample information and links each sample to a subject.
- cell_counts: stores immune population measurements in long format, where each row represents a single population measurement for a sample.

This design reflects the structure of the dataset. Subjects have multiple samples and samples contain mutliple immune cell populations

Cell populations were stored in long format (population, count) instead of separate columns because it scales more cleanly for analytics and future expansion. New immune populations can be added without changing the database schema or analytical code.
