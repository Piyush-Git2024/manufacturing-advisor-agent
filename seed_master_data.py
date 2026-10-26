import sqlite3

conn = sqlite3.connect("factory_v2.db")
cursor = conn.cursor()

# =====================================
# Plants
# =====================================

plants = [
    ("HYD", "Hyderabad Plant", "Hyderabad"),
    ("PUN", "Pune Plant", "Pune"),
    ("BLR", "Bangalore Plant", "Bangalore")
]

cursor.executemany(
    "INSERT INTO Plants VALUES (?, ?, ?)",
    plants
)

# =====================================
# Production Lines
# =====================================

lines = [
    ("HYD-LINE-A", "HYD", "Line A", "Engine Components"),
    ("HYD-LINE-B", "HYD", "Line B", "Engine Components"),
    ("HYD-LINE-C", "HYD", "Line C", "Final Assembly"),

    ("PUN-LINE-A", "PUN", "Line A", "Body Panels"),
    ("PUN-LINE-B", "PUN", "Line B", "Body Panels"),
    ("PUN-LINE-C", "PUN", "Line C", "Paint Shop"),

    ("BLR-LINE-A", "BLR", "Line A", "Electronics"),
    ("BLR-LINE-B", "BLR", "Line B", "Electronics"),
    ("BLR-LINE-C", "BLR", "Line C", "Final Testing")
]

cursor.executemany(
    "INSERT INTO ProductionLines VALUES (?, ?, ?, ?)",
    lines
)

# =====================================
# Machines
# =====================================

machines = [
    ("CNC101", "HYD-LINE-A", "CNC", "Siemens", "2021-01-10"),
    ("CNC102", "HYD-LINE-A", "CNC", "Siemens", "2021-04-15"),
    ("CNC103", "HYD-LINE-B", "CNC", "Fanuc", "2022-01-20"),

    ("PRESS201", "PUN-LINE-A", "Press", "Bosch", "2019-11-10"),
    ("PRESS202", "PUN-LINE-B", "Press", "Bosch", "2020-07-11"),

    ("ROBOT301", "BLR-LINE-A", "Robot", "ABB", "2023-01-01"),
    ("ROBOT302", "BLR-LINE-B", "Robot", "ABB", "2023-01-05"),
    ("ROBOT303", "BLR-LINE-C", "Robot", "ABB", "2023-01-08"),

    ("PACK401", "HYD-LINE-C", "Packaging", "TetraPak", "2022-03-01"),
    ("PACK402", "PUN-LINE-C", "Packaging", "TetraPak", "2022-06-01")
]

cursor.executemany(
    "INSERT INTO Machines VALUES (?, ?, ?, ?, ?)",
    machines
)

conn.commit()
conn.close()

print("Master data loaded.")