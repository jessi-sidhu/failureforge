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

## Metrics

| Metric | Description |
|---|---|
| Availability | % of polls that returned a healthy response |
| Error rate | % of polls that failed during the fault window |
| Avg response time | Mean response time across all healthy polls |
| P95 response time | 95th percentile response time — captures worst-case latency |
| First failure detected | Timestamp of the first unhealthy poll |
| Recovery time | Seconds between first failure and first successful recovery |

## Sample Report

```
# FailureForge Resilience Report
## Experiment: db-outage-sim

**Generated:** 2026-04-02 23:34:09

**Fault type:** container_kill

- Total polls: 93
- Healthy polls: 90
- Unhealthy polls: 3
- Error rate: 3.23%
- Average response time: 9.95ms
- P95 response time: 16.93ms
- Availability:  96.77%
- First failure detected: 2026-03-30 19:56:57.031592
- Recovered: True
- Recovery time: 1091.105836s

The service maintained  96.77% availability during the fault window.
```
