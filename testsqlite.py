import sqlite3
db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute(f"""CREATE TABLE IF NOT EXISTS users (
    id TEXT
)""")
db.commit()

user_id = input()

sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
if sql.fetchone() is None:
    sql.execute(f"INSERT INTO users VALUES (?)", [user_id])
    db.commit()
    print("registerd")
else:
    print("id EXISTS")
    for value in sql.execute("SELECT * FROM users"):
        print(value)
