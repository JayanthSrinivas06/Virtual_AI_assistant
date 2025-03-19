import csv
import sqlite3

connection = sqlite3.connect("neils.db")
cursor = connection.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(ID integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "insert INTO sys_command VALUES (null, 'pictures', 'C:\\Users\\B_Jayanth\\OneDrive\\Pictures')"
# cursor.execute(query)
# connection.commit()

# query = "DELETE FROM sys_command WHERE name = 'vs code'"
# cursor.execute(query)
# connection.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(ID integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "insert INTO web_command VALUES (null,'gmail', 'https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox')"
# cursor.execute(query)
# connection.commit()

# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

query = "INSERT INTO contacts VALUES (null,'mama', '99856 00182', 'null')"
cursor.execute(query)
connection.commit()

# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# connection.commit()
# connection.close()