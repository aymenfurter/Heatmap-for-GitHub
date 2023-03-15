import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_heatmap(hourly_commits: list) -> plt.Figure:
    # Initialize an empty 7x24 numpy array
    data = np.zeros((7, 24))

    # Fill the data array with hourly commit counts
    for weekday, hour, count in hourly_commits:
        data[weekday][hour] = count

    # Create the heatmap using seaborn
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)

    # Set the labels and title
    ax.set_xticklabels([f"{i:02d}:00" for i in range(24)], rotation=45)
    ax.set_yticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=0)
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Day of the Week")
    ax.set_title("GitHub Commit Heatmap")

    return fig
