import sqlite3

def get_production_analysis():

    conn = sqlite3.connect("factory.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM ProductionStatus
    """)

    row = cursor.fetchone()

    conn.close()

    line_id = row[0]
    target = row[1]
    current = row[2]
    hours_elapsed = row[3]
    hours_remaining = row[4]

    current_rate = current / hours_elapsed

    projected_output = int(
        current + (current_rate * hours_remaining)
    )

    gap = target - projected_output

    return {
        "line": line_id,
        "target": target,
        "current": current,
        "projected_output": projected_output,
        "gap": gap
    }