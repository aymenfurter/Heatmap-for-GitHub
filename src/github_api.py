import requests
from typing import Dict, List
from datetime import datetime, timezone

def fetch_hourly_commits(username: str) -> Dict[str, int]:
    commit_data = fetch_all_commits(username)

    hourly_commits = {}
    for commit in commit_data:
        commit_hour = commit["commit"]["committer"]["date"].hour
        if str(commit_hour) not in hourly_commits:
            hourly_commits[str(commit_hour)] = 1
        else:
            hourly_commits[str(commit_hour)] += 1

    print("Fetched hourly commits: ", hourly_commits)
    return hourly_commits

def fetch_all_commits(username: str) -> List[Dict]:
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    repos = response.json()

    if not isinstance(repos, list):
        return []

    commit_data = []
    for repo in repos:
        repo_name = repo["name"]
        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        commit_response = requests.get(commits_url)
        commit_data.extend(commit_response.json())
    return commit_data

def process_commit_data(commit_data: List[Dict]) -> Dict[str, int]:
    hourly_commits = {}
    for commit in commit_data:
        try:
            commit_date = commit["commit"]["committer"]["date"]
            dt = datetime.fromisoformat(commit_date[:-1])
            dt_utc = dt.replace(tzinfo=timezone.utc)
            hour = dt_utc.hour
            if hour not in hourly_commits:
                hourly_commits[str(hour)] = 0
            hourly_commits[str(hour)] += 1
        except KeyError:
            pass
    return hourly_commits
