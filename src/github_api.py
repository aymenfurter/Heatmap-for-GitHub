import requests
from collections import defaultdict
from datetime import datetime

def fetch_all_commits(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers={"Accept": "application/vnd.github+json"})
    
    if response.status_code != 200:
        return []

    repos = response.json()
    all_commits = []

    for repo in repos:
        if not isinstance(repo, dict) or "name" not in repo:
            continue

        repo_name = repo["name"]
        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        commit_response = requests.get(commits_url, headers={"Accept": "application/vnd.github+json"})

        if commit_response.status_code == 200:
            all_commits.extend(commit_response.json())

    return all_commits

def fetch_hourly_commits(username):
    all_commits = fetch_all_commits(username)
    hourly_commits = defaultdict(int)

    for commit in all_commits:
        if not isinstance(commit, dict) or "commit" not in commit or "author" not in commit["commit"]:
            continue

        dt = commit["commit"]["author"]["date"]
        dt_obj = datetime.fromisoformat(dt)
        hourly_commits[dt_obj.hour] += 1

    return dict(hourly_commits)
