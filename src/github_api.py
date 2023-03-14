import requests
from typing import Dict

def fetch_hourly_commits(username: str) -> Dict[str, int]:
    commit_data = fetch_all_commits(username)
    hourly_commits = {}

    for commit in commit_data:
        hour = commit["hour"]
        if hour not in hourly_commits:
            hourly_commits[hour] = 0
        hourly_commits[hour] += 1

    print("Hourly commits:", hourly_commits)  # Debugging line
    return hourly_commits

def fetch_all_commits(username: str) -> list:
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching repos for {username}: {response.status_code}")
        return []

    repos = response.json()
    commits = []

    for repo in repos:
        repo_name = repo["name"]
        commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        commit_response = requests.get(commit_url)

        if commit_response.status_code != 200:
            print(f"Error fetching commits for {repo_name}: {commit_response.status_code}")
            continue

        repo_commits = commit_response.json()
        for commit in repo_commits:
            commit_date = commit["commit"]["committer"]["date"]
            commit_hour = int(commit_date[11:13])
            commits.append({"hour": commit_hour})

    print("Fetched hourly commits:", commits)  # Debugging line
    return commits
