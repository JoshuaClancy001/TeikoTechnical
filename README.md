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

| Command          | Description                        |
|------------------|------------------------------------|
| `make setup`     | Install dependencies               |
| `make pipeline`  | Run the data pipeline              |
| `make dashboard` | Launch the Streamlit dashboard     |

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
