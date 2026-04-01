# FailureForge

> A YAML-driven resilience experiment runner for Docker Compose environments.

## What it does

FailureForge uses Pumba to inject failures into Docker Compose containers,
polls a health endpoint to measure healthy and unhealthy responses, stores
the results in a SQLite database, and generates a markdown resilience report.

## Why it exists

Most chaos engineering tools assume a Kubernetes cluster and a dedicated SRE team.
Solo developers and small teams have no way to stress-test their services before a
production incident does it for them. FailureForge makes resilience testing accessible
to anyone running Docker Compose.

## Quick start

### Prerequisites

- Docker Desktop
- Python 3.9+
- Pumba (`brew install pumba`)

### Installation

```bash
git clone https://github.com/jessi-sidhu/failureforge.git
cd failureforge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run an experiment

```bash
python3 cli.py run --config experiments/db-outage.yaml
```

### Generate a report

```bash
python3 cli.py report --experiment-name db-outage-sim
```

## Architecture

| Module         | Purpose                                           |
| -------------- | ------------------------------------------------- |
| `config.py`    | Parses YAML experiment configs                    |
| `health.py`    | Polls health endpoints and measures response time |
| `storage.py`   | Stores experiment results in SQLite               |
| `injectors.py` | Failure injection via Pumba                       |
| `runner.py`    | Orchestrates the full experiment lifecycle        |
| `report.py`    | Computes metrics and generates markdown reports   |
| `cli.py`       | CLI interface built with Typer                    |

## Sample Report

```
# FailureForge Resilience Report
## Experiment: db-outage-sim

- Total polls: 33
- Healthy polls: 30
- Unhealthy polls: 3
- Error rate: 9.09%
- Average response time: 10.73ms
```
