import requests
from datetime import datetime
from dateutil.parser import parse

def fetch_all_commits(username):
    repos_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(repos_url)
    if response.status_code != 200:
        return []

    repos = response.json()
    commit_data = []

    for repo in repos:
        repo_name = repo["name"]
        commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        response = requests.get(commit_url)
        if response.status_code != 200:
            continue

        commits = response.json()
        commit_data.extend(commits)

    print(commit_data)

    return commit_data

def fetch_hourly_commits(username):
    commit_data = fetch_all_commits(username)
    hourly_commits = {}

    for commit in commit_data:
        try:
            dt = commit["commit"]["author"]["date"]
            dt_obj = parse(dt)
            hour = dt_obj.hour
            hourly_commits[hour] = hourly_commits.get(hour, 0) + 1
        except KeyError:
            pass

    return hourly_commits
