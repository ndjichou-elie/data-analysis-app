import sqlite3
from pathlib import Path

# Path to your SQLite database file
db_path = Path('db.sqlite3')

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Drop the old tables
cursor.execute("DROP TABLE IF EXISTS api_customuser;")
cursor.execute("DROP TABLE IF EXISTS api_customuser_groups;")
cursor.execute("DROP TABLE IF EXISTS api_customuser_user_permissions;")

# Commit changes and close the connection
connection.commit()
connection.close()

print("Old tables removed successfully.")
