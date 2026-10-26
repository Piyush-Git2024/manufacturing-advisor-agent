import sqlite3

conn = sqlite3.connect("factory_v2.db")
cursor = conn.cursor()

tables = [
    "Plants",
    "ProductionLines",
    "Machines"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(table, ":", count)

conn.close()