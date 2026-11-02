from datetime import datetime, timezone

def get_datetime() -> dict[str, str]:
    """get the current date and time in UTC"""

    now = datetime.now(timezone.utc)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": "UTC",
        "datetime": now.isoformat()
    }