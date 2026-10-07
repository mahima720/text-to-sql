import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop existing table to prevent 'table already exists' errors on re-runs
cursor.execute("DROP TABLE IF EXISTS STUDENT")

table_info = """
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert records
records = [
    ('Mahima', 'Data Science', 'A', 90),
    ('Nima', 'Information Technology', 'B', 100),
    ('Harini', 'Computer Science', 'A', 86),
    ('Vikash', 'DEVOPS', 'A', 50),
    ('Dipesh', 'Software Engineer', 'A', 35),
]

cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", records)

print("Inserted records:")
for row in cursor.execute("SELECT * FROM STUDENT"):
    print(row)

connection.commit()
connection.close()