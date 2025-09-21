#!/usr/bin/env python3
import sqlite3
import matplotlib.pyplot as plt
import os
import shutil
import numpy as np


DB_PATH = 'database.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get substances
q = "SELECT * FROM Substance"
substances = [dict(row) for row in cursor.execute(q).fetchall()]

# Get data
substances = {
    3: 'DM Denk Mit (Ethanol 74/100)',
    4: 'domol Hygiene Spray (2-Propanol: 21g, Ethanol: 22g, 1-Propanol: 8g, Duftstoff CITRAL, LIMONENE)',
    5: 'octeni-derm (0.1g Octenidindilhydrochlorid, 30g 1-Propanol, 45g 2-Propanol)'
}
q = "SELECT * FROM Data WHERE SUBSTANCE_ID = 5" #ORDER BY ID DESC LIMIT 100 "
data = [dict(row) for row in cursor.execute(q).fetchall()]
test_id = 'test'
data = [item for item in data if item['TEST_ID'] == test_id]

substance_colors = {'2': 'yellow', '3': 'green'}
substance_markers = {'1': 'o', '2': 's', '3': 'D'}

# Render charts (NOTE SINGLE TEST HERE)
chart_names = [f'DATA_{i}' for i in range(64)]
x_axis = list(range(len(data)))


def render_tight():
    fig, axes = plt.subplots(8, 8, figsize=(20, 20))  # Adjust size for readability

    for i, ax in enumerate(axes.flatten()):
        chart_name = chart_names[i]
        y_axis = [item[chart_name] for item in data]

        # Plot the full time series in gray
        ax.plot(x_axis, y_axis, color='black', linestyle='-', alpha=0.5)

        for substance_id, color in substance_colors.items():
            # Get all indices where the SUBSTANCE_ID matches
            indices = [idx for idx, item in enumerate(data) if item["SUBSTANCE_ID"] == substance_id]

            # Draw vertical spans to highlight these regions
            for idx in indices:
                ax.axvspan(idx - 0.5, idx + 0.5, color=color, alpha=0.2)  # Transparent highlight


        ax.set_title(f"Channel {chart_name}", fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()


def export():
    output_dir = "output_charts"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print('Deleted old charts dir.')
    os.makedirs(output_dir, exist_ok=True)

    for i, chart_name in enumerate(chart_names):
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjust size as needed
        y_axis = [float(item[chart_name]) for item in data]

        # Plot the full time series in gray
        ax.plot(x_axis, y_axis, color='black', linestyle='-', alpha=0.5)

        for substance_id, color in substance_colors.items():
            indices = [idx for idx, item in enumerate(data) if item["SUBSTANCE_ID"] == substance_id]
            
            # Draw vertical highlights
            for idx in indices:
                ax.axvspan(idx - 0.5, idx + 0.5, color=color, alpha=0.2)  

        ax.set_title(f"Channel {chart_name}", fontsize=10)
        ax.set_xlabel("Timepoint (2-Second intervals)")
        ax.set_ylabel("Resistance (Ohm)")

        # 🔹 Reduce Y-ticks dynamically
        min_y, max_y = min(y_axis), max(y_axis)
        y_ticks = np.linspace(min_y, max_y, num=5)  # Adjust `num` to control spacing
        ax.set_yticks(y_ticks)
        
        # Save the plot
        filename = os.path.join(output_dir, f"{chart_name}.png")
        plt.savefig(filename, dpi=300)
        plt.close(fig)  # Close figure to free memory
        print(f'Saved chart {chart_name}' + ' ' * 30, end='\r')

    print()
    print(f"Saved {len(chart_names)} plots in '{output_dir}'")


render_tight()