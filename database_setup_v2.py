import sqlite3

conn = sqlite3.connect("factory_v2.db")

cursor = conn.cursor()

# ==========================================
# Plants
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Plants (
    PlantID TEXT PRIMARY KEY,
    PlantName TEXT,
    Location TEXT
)
""")

# ==========================================
# Production Lines
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductionLines (
    LineID TEXT PRIMARY KEY,
    PlantID TEXT,
    LineName TEXT,
    ProductType TEXT
)
""")

# ==========================================
# Machines
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Machines (
    MachineID TEXT PRIMARY KEY,
    LineID TEXT,
    MachineType TEXT,
    Manufacturer TEXT,
    InstallDate TEXT
)
""")

# ==========================================
# Production History
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductionHistory (
    ProductionID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductionDate TEXT,
    PlantID TEXT,
    LineID TEXT,
    Shift TEXT,
    TargetProduction INTEGER,
    ActualProduction INTEGER,
    DowntimeMinutes INTEGER,
    MachineUtilization REAL
)
""")

# ==========================================
# Quality History
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS QualityHistory (
    QualityID INTEGER PRIMARY KEY AUTOINCREMENT,
    InspectionDate TEXT,
    PlantID TEXT,
    LineID TEXT,
    DefectRate REAL,
    ScrapRate REAL,
    ReworkRate REAL,
    TotalDefects INTEGER
)
""")

# ==========================================
# Machine Health History
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS MachineHealthHistory (
    HealthID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReadingTime TEXT,
    MachineID TEXT,
    Temperature REAL,
    Vibration REAL,
    RuntimeHours INTEGER,
    LoadPercentage REAL
)
""")

# ==========================================
# Maintenance History
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS MaintenanceHistory (
    MaintenanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    MachineID TEXT,
    MaintenanceType TEXT,
    MaintenanceDate TEXT,
    Technician TEXT,
    Cost REAL,
    DowntimeHours REAL,
    Notes TEXT
)
""")

# ==========================================
# Operational Incidents
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS OperationalIncidents (
    IncidentID INTEGER PRIMARY KEY AUTOINCREMENT,
    IncidentDate TEXT,
    MachineID TEXT,
    Severity TEXT,
    Category TEXT,
    Description TEXT
)
""")

conn.commit()
conn.close()

print("Factory V2 database created.")