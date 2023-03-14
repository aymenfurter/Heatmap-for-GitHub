from datetime import datetime

def parse_commit_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
