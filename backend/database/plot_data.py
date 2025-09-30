#!/usr/bin/env python3
import sqlite3
from typing import List
import matplotlib.pyplot as plt
import numpy as np

db = sqlite3.connect('database.db')
db.row_factory = sqlite3.Row
cursor = db.cursor()

q = "SELECT * FROM Substance"
results = [dict(x) for x in cursor.execute(q).fetchall()]
print([
    {
        (x['SUBSTANCE_NAME'] + ' ' + x['QUANTITY']).strip(): x['ID']
    } for x in results
])

LABELS = [f'DATA_{i}' for i in range(64)]
DATA_LABELS = ', '.join(LABELS)

q = f"SELECT ID, {DATA_LABELS} FROM data WHERE SUBSTANCE_ID = 4"
data = [dict(x) for x in cursor.execute(q).fetchall()]
data = [
    {
        'label': x['ID'],
        'data': [x[y] for y in LABELS]
    } for x in data
]

datasets = []
last_index = -1

groups = []
group = []
for d in data:
    if d['label'] != last_index + 1 and len(group) > 0:
        groups.append(group)
        group = []
    last_index = d['label']
    group.append([d['label']] + [float(x) for x in d['data']])

# air: 65-67
# domol:
# octeniderm: 6-8

i = 4
first_group = groups[i] + groups[i+1] + groups[i+2]
last_group = groups[len(groups) - 3] + groups[len(groups) - 2] + groups[len(groups) - 1]

if len(first_group) > len(last_group):
    first_group = first_group[:len(last_group)]
elif len(first_group) < len(last_group):
    last_group = last_group[:len(first_group)]

print('First group time range start (Minutes):', first_group[0][0] * 2 / 3600)
print('Last group time range start (Minutes):', last_group[0][0] * 2 / 3600)

first_group = [x[1:] for x in first_group]
last_group = [x[1:] for x in last_group]

first_group = np.array(first_group)
last_group = np.array(last_group)

print(first_group.shape)
print(last_group.shape)

fontsize = 32

fig, ax = plt.subplots(figsize=(20, 10))
ax.tick_params(axis="y", labelsize=fontsize - 4)
ax.tick_params(axis="x", labelsize=fontsize - 4)

for i in range(first_group.shape[1]):
    plt.plot(first_group[:, i], label=f"Sensor {i+1}", linewidth=4.0)
plt.title("Domol (after 3 hours)", fontsize=fontsize + 4, pad=20)
plt.xlabel("Time (1 data point per 2 seconds)", fontsize=fontsize, labelpad=20)
plt.grid(True)
plt.ylabel("Resistance (Ω)", fontsize=fontsize, labelpad=20)
plt.ylim(0, 60000)
plt.tight_layout()
plt.show()
fig.savefig('first.png')


# Plot last_group
fig, ax = plt.subplots(figsize=(20, 10))
ax.tick_params(axis="y", labelsize=fontsize - 4)
ax.tick_params(axis="x", labelsize=fontsize - 4)

for i in range(last_group.shape[1]):
    plt.plot(last_group[:, i], label=f"Sensor {i+1}", linewidth=4.0)
plt.title("Domol (after 7 hours)", fontsize=fontsize + 4, pad=20)
plt.xlabel("Time (1 data point per 2 seconds)", fontsize=fontsize, labelpad=20)
plt.grid(True)
plt.ylabel("Resistance (Ω)", fontsize=fontsize, labelpad=20)
plt.ylim(0, 60000)
plt.tight_layout()
plt.show()
fig.savefig('second.png')

# q = "SELECT HUMIDITY FROM Data WHERE SUBSTANCE_ID = 1";
# results = cursor.execute(q).fetchall()
# average_humidity = sum([float(dict(x)['HUMIDITY']) for x in results]) / len(results)
# filter_humidity = average_humidity * 1.25 # 125%
