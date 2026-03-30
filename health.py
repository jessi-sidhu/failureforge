import requests
import time
import datetime

def poll_health(url: str, duration_seconds: int) -> list:
    """
    Polls a health endpoint every 2 seconds for a given duration.

    Args: 
        url: the health check URL to poll
        duration_seconds: how long to poll in seconds

    Returns:
        a list of results, each containing timestamp, status code, and response time
    """

    results = []
    end_time = time.time() + duration_seconds

    while time.time() < end_time:
        timestamp = datetime.datetime.now()
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            response_time_ms = (time.time() - start) * 1000
            status_code= response.status_code
            is_healthy = response.status_code == 200
        except requests.exceptions.ConnectionError:
            response_time_ms = None
            status_code = None
            is_healthy = False

        results.append({
            "timestamp": timestamp,
            "status_code" : status_code,
            "response_time_ms" : response_time_ms,
            "is_healthy": is_healthy
        })

        print(f"[{timestamp}] status={status_code} | healthy={is_healthy} | response={response_time_ms}ms")
        time.sleep(2)

    return results