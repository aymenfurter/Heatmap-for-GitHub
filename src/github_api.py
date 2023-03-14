import requests
from typing import List, Dict
from utils import parse_commit_datetime

GITHUB_API_BASE_URL = "https://api.github.com"

def fetch_commit_data(username: str) -> Dict[str, List[int]]:
    repos = fetch_repositories(username)
    commit_data = {}

    for repo in repos:
        repo_commits = fetch_repository_commits(username, repo["name"])
        for commit in repo_commits:
            commit_datetime = parse_commit_datetime(commit["commit"]["committer"]["date"])
            hour = commit_datetime.hour
            commit_data[hour] = commit_data.get(hour, 0) + 1

    return commit_data

def fetch_repositories(username: str) -> List[Dict]:
    url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_repository_commits(username: str, repo_name: str) -> List[Dict]:
    url = f"{GITHUB_API_BASE_URL}/repos/{username}/{repo_name}/commits"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
