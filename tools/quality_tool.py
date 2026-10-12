import sqlite3

def get_quality_analysis():

    conn = sqlite3.connect("factory.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM QualityMetrics
    """)

    row = cursor.fetchone()

    conn.close()

    return {
        "line": row[0],
        "defect_rate": row[1],
        "scrap_rate": row[2],
        "rework_rate": row[3]
    }