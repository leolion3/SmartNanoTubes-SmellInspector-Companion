#!/usr/bin/env python3
import sqlite3


db = sqlite3.connect('database.db')
db.row_factory = sqlite3.Row
cursor = db.cursor()

q = "SELECT * FROM Substance"
print([dict(x) for x in cursor.execute(q).fetchall()])

q = "SELECT HUMIDITY FROM Data WHERE SUBSTANCE_ID = 1";
results = cursor.execute(q).fetchall()
average_humidity = sum([float(dict(x)['HUMIDITY']) for x in results]) / len(results)
filter_humidity = average_humidity * 1.25 # 125%
