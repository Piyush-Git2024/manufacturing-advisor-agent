import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("factory_v2.db")
cursor = conn.cursor()

# ====================================================
# CONFIG
# ====================================================

today = datetime.today()

lines = [
    "HYD-LINE-A",
    "HYD-LINE-B",
    "HYD-LINE-C",
    "PUN-LINE-A",
    "PUN-LINE-B",
    "PUN-LINE-C",
    "BLR-LINE-A",
    "BLR-LINE-B",
    "BLR-LINE-C"
]

machines = [
    "CNC101",
    "CNC102",
    "CNC103",
    "PRESS201",
    "PRESS202",
    "ROBOT301",
    "ROBOT302",
    "ROBOT303",
    "PACK401",
    "PACK402"
]

line_to_plant = {
    "HYD-LINE-A": "HYD",
    "HYD-LINE-B": "HYD",
    "HYD-LINE-C": "HYD",
    "PUN-LINE-A": "PUN",
    "PUN-LINE-B": "PUN",
    "PUN-LINE-C": "PUN",
    "BLR-LINE-A": "BLR",
    "BLR-LINE-B": "BLR",
    "BLR-LINE-C": "BLR",
}

# ====================================================
# CLEAN TABLES
# ====================================================

cursor.execute("DELETE FROM ProductionHistory")
cursor.execute("DELETE FROM QualityHistory")
cursor.execute("DELETE FROM MachineHealthHistory")
cursor.execute("DELETE FROM MaintenanceHistory")
cursor.execute("DELETE FROM OperationalIncidents")

# ====================================================
# PRODUCTION HISTORY
# ====================================================

for day in range(30):

    production_date = (
        today - timedelta(days=29-day)
    ).strftime("%Y-%m-%d")

    for line in lines:

        plant = line_to_plant[line]

        target = 1500

        # ------------------------------------------------
        # PUN-LINE-B = Underperforming
        # ------------------------------------------------
        if line == "PUN-LINE-B":

            actual = 1490 - (day * 5)

            utilization = 88 - (day * 0.5)

            downtime = random.randint(30, 90)

        # ------------------------------------------------
        # BLR-LINE-C = Best Performer
        # ------------------------------------------------
        elif line == "BLR-LINE-C":

            actual = random.randint(1490, 1520)

            utilization = random.randint(94, 98)

            downtime = random.randint(0, 10)

        else:

            actual = random.randint(1400, 1510)

            utilization = random.randint(85, 95)

            downtime = random.randint(5, 30)

        cursor.execute("""
        INSERT INTO ProductionHistory
        (
            ProductionDate,
            PlantID,
            LineID,
            Shift,
            TargetProduction,
            ActualProduction,
            DowntimeMinutes,
            MachineUtilization
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            production_date,
            plant,
            line,
            random.choice(["A", "B", "C"]),
            target,
            actual,
            downtime,
            utilization
        ))

# ====================================================
# QUALITY HISTORY
# ====================================================

for day in range(30):

    inspection_date = (
        today - timedelta(days=29-day)
    ).strftime("%Y-%m-%d")

    for line in lines:

        plant = line_to_plant[line]

        # ------------------------------------------------
        # HYD-LINE-A = Quality Deterioration
        # ------------------------------------------------
        if line == "HYD-LINE-A":

            defect_rate = 2 + (day * 0.15)

            scrap_rate = 1 + (day * 0.07)

            rework_rate = 0.5 + (day * 0.04)

        # ------------------------------------------------
        # BLR-LINE-C = Best Quality
        # ------------------------------------------------
        elif line == "BLR-LINE-C":

            defect_rate = round(
                random.uniform(0.5, 1.5),
                2
            )

            scrap_rate = round(
                random.uniform(0.2, 0.8),
                2
            )

            rework_rate = round(
                random.uniform(0.2, 0.6),
                2
            )

        else:

            defect_rate = round(
                random.uniform(1.5, 3.5),
                2
            )

            scrap_rate = round(
                random.uniform(0.5, 2.0),
                2
            )

            rework_rate = round(
                random.uniform(0.5, 2.0),
                2
            )

        total_defects = int(defect_rate * 10)

        cursor.execute("""
        INSERT INTO QualityHistory
        (
            InspectionDate,
            PlantID,
            LineID,
            DefectRate,
            ScrapRate,
            ReworkRate,
            TotalDefects
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            inspection_date,
            plant,
            line,
            defect_rate,
            scrap_rate,
            rework_rate,
            total_defects
        ))

# ====================================================
# MACHINE HEALTH HISTORY
# ====================================================

for day in range(30):

    reading_time = (
        today - timedelta(days=29-day)
    ).strftime("%Y-%m-%d %H:%M:%S")

    for machine in machines:

        # --------------------------------------------
        # CNC101 = Highest Risk
        # --------------------------------------------
        if machine == "CNC101":

            temperature = 75 + (day * 0.6)

            vibration = 2 + (day * 0.25)

            runtime = 500 + (day * 12)

            load = 70 + (day * 0.4)

        # --------------------------------------------
        # ROBOT302 = Healthy
        # --------------------------------------------
        elif machine == "ROBOT302":

            temperature = random.randint(60, 70)

            vibration = round(
                random.uniform(1, 2),
                2
            )

            runtime = 400 + day

            load = random.randint(55, 70)

        else:

            temperature = random.randint(65, 85)

            vibration = round(
                random.uniform(2, 6),
                2
            )

            runtime = random.randint(300, 800)

            load = random.randint(60, 90)

        cursor.execute("""
        INSERT INTO MachineHealthHistory
        (
            ReadingTime,
            MachineID,
            Temperature,
            Vibration,
            RuntimeHours,
            LoadPercentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            reading_time,
            machine,
            round(temperature, 2),
            round(vibration, 2),
            runtime,
            round(load, 2)
        ))

# ====================================================
# MAINTENANCE HISTORY
# ====================================================

maintenance_records = [

    (
        "CNC101",
        "Preventive",
        "2026-09-10",
        "John",
        5000,
        2,
        "Routine maintenance"
    ),

    (
        "PRESS201",
        "Corrective",
        "2026-09-05",
        "Mike",
        12000,
        5,
        "Hydraulic leak repair"
    ),

    (
        "PRESS201",
        "Corrective",
        "2026-09-25",
        "Mike",
        15000,
        6,
        "Motor overheating"
    ),

    (
        "ROBOT302",
        "Preventive",
        "2026-09-20",
        "David",
        3000,
        1,
        "Routine check"
    )
]

for record in maintenance_records:

    cursor.execute("""
    INSERT INTO MaintenanceHistory
    (
        MachineID,
        MaintenanceType,
        MaintenanceDate,
        Technician,
        Cost,
        DowntimeHours,
        Notes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, record)

# ====================================================
# INCIDENTS
# ====================================================

incidents = [

    (
        "2026-09-05",
        "PRESS201",
        "High",
        "Motor",
        "Motor overheating"
    ),

    (
        "2026-09-11",
        "PRESS201",
        "Medium",
        "Hydraulics",
        "Hydraulic leak"
    ),

    (
        "2026-09-21",
        "PRESS201",
        "High",
        "Motor",
        "Motor overheating"
    ),

    (
        "2026-09-28",
        "PRESS201",
        "Medium",
        "Pressure",
        "Pressure drop"
    ),

    (
        "2026-10-05",
        "CNC101",
        "High",
        "Vibration",
        "High vibration alert"
    )
]

for incident in incidents:

    cursor.execute("""
    INSERT INTO OperationalIncidents
    (
        IncidentDate,
        MachineID,
        Severity,
        Category,
        Description
    )
    VALUES (?, ?, ?, ?, ?)
    """, incident)

# ====================================================
# COMMIT
# ====================================================

conn.commit()

# Verification counts

tables = [
    "ProductionHistory",
    "QualityHistory",
    "MachineHealthHistory",
    "MaintenanceHistory",
    "OperationalIncidents"
]

print("\nData Generated:\n")

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count}")

conn.close()

print("\nFactory history data loaded successfully.")