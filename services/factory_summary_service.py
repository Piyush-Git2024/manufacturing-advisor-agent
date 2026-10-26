import sqlite3


DB_NAME = "factory_v2.db"


def get_factory_summary():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    findings = []

    # =====================================================
    # PRODUCTION ANALYSIS
    # =====================================================

    cursor.execute("""
    SELECT
        LineID,
        AVG(TargetProduction),
        AVG(ActualProduction)
    FROM ProductionHistory
    GROUP BY LineID
    """)

    production_results = cursor.fetchall()

    biggest_gap_line = None
    biggest_gap = -9999

    for line, target, actual in production_results:

        gap = target - actual

        if gap > biggest_gap:
            biggest_gap = gap
            biggest_gap_line = line

    findings.append(
        f"Worst production line: {biggest_gap_line} "
        f"(average shortfall {biggest_gap:.0f} units)"
    )

    # =====================================================
    # QUALITY ANALYSIS
    # =====================================================

    cursor.execute("""
    SELECT
        LineID,
        AVG(DefectRate)
    FROM QualityHistory
    GROUP BY LineID
    ORDER BY AVG(DefectRate) DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    if row:

        line_id, defect_rate = row

        findings.append(
            f"Highest defect rate observed on "
            f"{line_id} ({defect_rate:.2f}%)"
        )

    # =====================================================
    # MACHINE HEALTH ANALYSIS
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        AVG(Temperature),
        AVG(Vibration)
    FROM MachineHealthHistory
    GROUP BY MachineID
    ORDER BY AVG(Temperature) DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    if row:

        machine, temp, vib = row

        findings.append(
            f"Highest machine stress detected on "
            f"{machine} "
            f"(Temp={temp:.1f}, Vibration={vib:.1f})"
        )

    # =====================================================
    # INCIDENT ANALYSIS
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        COUNT(*)
    FROM OperationalIncidents
    GROUP BY MachineID
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    if row:

        machine, count = row

        findings.append(
            f"Most incidents recorded for "
            f"{machine} ({count} incidents)"
        )

    # =====================================================
    # MAINTENANCE ANALYSIS
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        SUM(Cost)
    FROM MaintenanceHistory
    GROUP BY MachineID
    ORDER BY SUM(Cost) DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    if row:

        machine, cost = row

        findings.append(
            f"Highest maintenance spend on "
            f"{machine} "
            f"(${cost:.0f})"
        )

    conn.close()

    return "\n".join(findings)
def get_executive_risk_summary():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    summary = []

    # =====================================================
    # HIGHEST RISK MACHINE
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        AVG(Temperature),
        AVG(Vibration)
    FROM MachineHealthHistory
    GROUP BY MachineID
    ORDER BY AVG(Temperature) DESC,
             AVG(Vibration) DESC
    LIMIT 1
    """)

    machine, temp, vib = cursor.fetchone()

    summary.append("EXECUTIVE RISK SUMMARY")
    summary.append("")
    summary.append("HIGH RISK MACHINE")
    summary.append("-----------------")
    summary.append(
        f"{machine} "
        f"(Temperature={temp:.1f}, "
        f"Vibration={vib:.1f})"
    )

    # =====================================================
    # PRODUCTION CONCERN
    # =====================================================

    cursor.execute("""
    SELECT
        LineID,
        AVG(TargetProduction) - AVG(ActualProduction) AS Gap
    FROM ProductionHistory
    GROUP BY LineID
    ORDER BY Gap DESC
    LIMIT 1
    """)

    line, gap = cursor.fetchone()

    summary.append("")
    summary.append("PRODUCTION CONCERN")
    summary.append("------------------")
    summary.append(
        f"{line} "
        f"(Average shortfall={gap:.0f} units)"
    )

    # =====================================================
    # QUALITY CONCERN
    # =====================================================

    cursor.execute("""
    SELECT
        LineID,
        AVG(DefectRate)
    FROM QualityHistory
    GROUP BY LineID
    ORDER BY AVG(DefectRate) DESC
    LIMIT 1
    """)

    line, defect_rate = cursor.fetchone()

    summary.append("")
    summary.append("QUALITY CONCERN")
    summary.append("----------------")
    summary.append(
        f"{line} "
        f"(Average defect rate={defect_rate:.2f}%)"
    )

    # =====================================================
    # INCIDENT CONCERN
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        COUNT(*)
    FROM OperationalIncidents
    GROUP BY MachineID
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """)

    machine, incidents = cursor.fetchone()

    summary.append("")
    summary.append("INCIDENT CONCERN")
    summary.append("----------------")
    summary.append(
        f"{machine} "
        f"({incidents} incidents)"
    )

    # =====================================================
    # MAINTENANCE CONCERN
    # =====================================================

    cursor.execute("""
    SELECT
        MachineID,
        SUM(Cost)
    FROM MaintenanceHistory
    GROUP BY MachineID
    ORDER BY SUM(Cost) DESC
    LIMIT 1
    """)

    machine, cost = cursor.fetchone()

    summary.append("")
    summary.append("MAINTENANCE CONCERN")
    summary.append("-------------------")
    summary.append(
        f"{machine} "
        f"(Maintenance spend=${cost:.0f})"
    )

    # =====================================================
    # RECOMMENDED ACTIONS
    # =====================================================

    summary.append("")
    summary.append("RECOMMENDED ACTIONS")
    summary.append("-------------------")
    summary.append(
        "1. Schedule immediate maintenance for CNC101."
    )

    summary.append(
        "2. Investigate increasing defects on HYD-LINE-A."
    )

    summary.append(
        "3. Recover production performance on PUN-LINE-B."
    )

    summary.append(
        "4. Review recurring incidents on PRESS201."
    )

    conn.close()

    return "\n".join(summary)