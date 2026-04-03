import sqlite3
import datetime
import numpy as np

def load_results(experiment_name: str, db_path: str = "results.db"):
    """
    Loads results from the database for given experiment name.
    
    Args:
        experiment_name: Name of the specific experiment
        
    Returns:
        a list of rows from the database for the given experiment
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
                   "SELECT * FROM results WHERE experiment_name = ?", 
                   (experiment_name, )
                   )
    rows = cursor.fetchall()
    conn.close()
    return rows

def compute_metrics(rows: list):
    """
    Computes metrics for a given row
    
    Returns:
        A dictionary of all metrics computed
    """
    total_polls = len(rows)
    healthy_polls = sum(1 for row in rows if row[5] == 1)
    unhealthy_polls = total_polls - healthy_polls
    error_rate = (unhealthy_polls/total_polls * 100 if total_polls > 0 else 0)
    response_time_list = [row [4] for row in rows if row[4] is not None]
    average_response_time = (sum(response_time_list) / len(response_time_list) if response_time_list else 0)
    p95_response_time = np.percentile(response_time_list, 95) if response_time_list else 0
    availability = (healthy_polls / total_polls * 100 if total_polls > 0 else 0)

    return {
        "total_polls": total_polls,
        "healthy_polls": healthy_polls,
        "unhealthy_polls": unhealthy_polls,
        "error_rate": error_rate,
        "average_response_time": average_response_time,
        "p95_response_time": p95_response_time,
        "availability": availability
    }
    
def generate_report(experiment_name: str):
    """
    Generates markdown file with metrics for given experiment
    """
    results = load_results(experiment_name, "results.db")
    metrics = compute_metrics(results)
    
    with open(f"{experiment_name}_report.md", "w") as f:
        f.write(f"# FailureForge Resilience Report\n")
        f.write(f"## Experiment: {experiment_name}\n\n")
        f.write(f"- Total polls: {metrics['total_polls']}\n")
        f.write(f"- Healthy polls: {metrics['healthy_polls']}\n")
        f.write(f"- Unhealthy polls: {metrics['unhealthy_polls']}\n")
        f.write(f"- Error rate: {metrics['error_rate']:.2f}%\n")
        f.write(f"- Average response time: {metrics['average_response_time']:.2f}ms\n")
        f.write(f"- P95 response time: {metrics['p95_response_time']:.2f}ms\n")
        f.write(f"- Availability: {metrics['availability']: .2f}%\n")
        f.write(f"\nThe service maintained {metrics['availability']: .2f}% availability during the fault window.\n")
        print(f"Report saved to {experiment_name}_report.md")