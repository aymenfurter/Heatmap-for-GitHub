import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

def generate_heatmap(commit_data: Dict[str, List[int]]):
    hours = list(range(24))
    commit_counts = [commit_data.get(hour, 0) for hour in hours]

    data = np.array(commit_counts).reshape(1, 24)

    fig, ax = plt.subplots(figsize=(12, 2))
    heatmap = ax.imshow(data, cmap='hot', aspect='auto', interpolation='nearest')
    ax.set_yticks([])
    ax.set_xticks(hours)
    ax.set_xticklabels(hours)

    plt.colorbar(heatmap, ax=ax, orientation='vertical', pad=0.1)

    return fig
