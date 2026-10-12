import sqlite3

conn = sqlite3.connect("factory.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM ProductionStatus")
cursor.execute("DELETE FROM QualityMetrics")
cursor.execute("DELETE FROM MachineHealth")

cursor.execute("""
INSERT INTO ProductionStatus
VALUES (
'Line3',
15000,
8500,
16,
8,
24,
79
)
""")

cursor.execute("""
INSERT INTO QualityMetrics
VALUES (
'Line3',
4.2,
1.8,
2.6
)
""")

cursor.execute("""
INSERT INTO MachineHealth
VALUES (
'CNC101',
92,
'HIGH',
460,
'2026-09-20'
)
""")

conn.commit()
conn.close()

print("Data loaded.")