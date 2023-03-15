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

    return commit_data

def fetch_hourly_commits_per_weekday(username):
    commit_data = fetch_all_commits(username)
    hourly_commits_per_weekday = {}

    for i in range(7):  # Initialize the structure
        hourly_commits_per_weekday[i] = {}
        for j in range(24):
            hourly_commits_per_weekday[i][j] = 0

    for commit in commit_data:
        try:
            dt = commit["commit"]["author"]["date"]
            dt_obj = parse(dt)
            hour = dt_obj.hour
            weekday = dt_obj.weekday()
            hourly_commits_per_weekday[weekday][hour] += 1
        except KeyError:
            pass

    # Flatten the dictionary to a list of tuples
    flattened_data = [(weekday, hour, count) for weekday, hours in hourly_commits_per_weekday.items() for hour, count in hours.items()]

    return flattened_data
