import sqlite3
from datetime import datetime

def get_maintenance_analysis():

    conn = sqlite3.connect("factory.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM MachineHealth
    """)

    row = cursor.fetchone()

    conn.close()

    machine = row[0]
    temperature = row[1]
    vibration = row[2]
    runtime = row[3]
    last_maintenance = row[4]

    last_date = datetime.strptime(
        last_maintenance,
        "%Y-%m-%d"
    )

    days_since_maintenance = (
        datetime.now() - last_date
    ).days

    return {
        "machine": machine,
        "temperature": temperature,
        "vibration": vibration,
        "runtime": runtime,
        "days_since_maintenance": days_since_maintenance
    }