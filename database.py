import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (name text, password text, type text)'

cursor.execute(create_table)

query1 = "INSERT INTO users VALUES ('r2app181@mailinator.com', 'Nttdata@123', 'PAYM')"
cursor.execute(query1)
query2 = "INSERT INTO users VALUES ('v4payg34@yopmail.com', 'Nttdata@1', 'PAYG')"
cursor.execute(query2)
query3 = "INSERT INTO users VALUES ('santosh_somani@thbs.com', 'Thbs123!', 'PAYG')"
cursor.execute(query3)
query4 = "INSERT INTO users VALUES ('r2app381@mailinator.com', 'Nttdata@123', 'PAYM')"
cursor.execute(query4)

select = 'SELECT * FROM users'
result = cursor.execute(select)
rows = result.fetchall()

for row in rows:
    print(row)

connection.commit()
connection.close()
