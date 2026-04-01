import sqlite3
import datetime

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