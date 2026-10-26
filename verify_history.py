import sqlite3

conn = sqlite3.connect("factory_v2.db")
cursor = conn.cursor()

print("\n=== INCIDENTS ===")
cursor.execute("""
SELECT *
FROM OperationalIncidents
""")

for row in cursor.fetchall():
    print(row)

print("\n=== CNC101 HEALTH ===")

cursor.execute("""
SELECT ReadingTime,
       Temperature,
       Vibration
FROM MachineHealthHistory
WHERE MachineID='CNC101'
ORDER BY ReadingTime DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

print("\n=== HYD-LINE-A QUALITY ===")

cursor.execute("""
SELECT InspectionDate,
       DefectRate,
       ScrapRate
FROM QualityHistory
WHERE LineID='HYD-LINE-A'
ORDER BY InspectionDate DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()