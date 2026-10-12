import sqlite3

conn = sqlite3.connect("factory.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductionStatus (
    LineID TEXT,
    TargetProduction INTEGER,
    CurrentProduction INTEGER,
    HoursElapsed INTEGER,
    HoursRemaining INTEGER,
    ShiftHours INTEGER,
    MachineUtilization INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS QualityMetrics (
    LineID TEXT,
    DefectRate REAL,
    ScrapRate REAL,
    ReworkRate REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MachineHealth (
    MachineID TEXT,
    Temperature INTEGER,
    Vibration TEXT,
    RuntimeHours INTEGER,
    LastMaintenanceDate TEXT
)
""")

conn.commit()
conn.close()

print("Database created.")