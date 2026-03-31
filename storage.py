import sqlite3
import datetime

def init_db(db_path: str = "results.db"):
    """
    Creates the database and results table if they don't exist.

    Args:
        db_path: path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_name TEXT,
            timestamp TEXT,
            status_code INTEGER,
            response_time_ms REAL,
            is_healthy INTEGER
        )
    """)
    conn.commit()
    print(f"Database initialized at {db_path}")
    conn.close()
    
def save_results(experiment_name: str, results: list, db_path: str = "results.db"): 
    """
    Saves poll results to the database
    
    Args:
        experiment_name: the name of the experiment these results belong to
        results: list of poll results from poll_health
        db_path: path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for result in results:
        cursor.execute("""
            INSERT INTO results (experiment_name, timestamp, status_code, response_time_ms, is_healthy)
            VALUES(?, ?, ?, ?, ?)
        """, (
            experiment_name,
            str(result["timestamp"]),
            result["status_code"],
            result["response_time_ms"],
            1 if result["is_healthy"] else 0
        ))
    conn.commit()
    print(f"Saved {len(results)} results for experiment '{experiment_name}'")
    conn.close()
