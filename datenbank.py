import sqlite3

def connect_to_database(datenbankname):  
    # Verbindung zur Datenbank herstellen (erstellt die Datenbank, falls sie nicht existiert)
    conn = sqlite3.connect(f'{datenbankname}.db')

    # Cursor erstellen
    cur = conn.cursor()
    return conn,cur

columns =[("Id", "INTEGER PRIMARY KEY"), ("title", "TEXT"), ("promt", "TEXT")]
table_name = ""

def create_table(cur, table_name, columns):    
    # SQL-Anweisung dynamisch zusammenstellen
    columns_def = ", ".join([f"{name} {dtype}" for name, dtype in columns])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"

    # Tabelle erstellen
    cur.execute(create_table_sql)

def print_table(cur, table_name):
    # SQL-Anweisung dynamisch zusammenstellen    
    sql = f"SELECT * FROM {table_name}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

id = "1"
title = "Coaching" 
promt = "Du bist ein Klient"

def insert_in_table(cur, table_name, id, title, promt):
    # Define the columns you want to insert into
    columns_def = "id, title, prompt"
    # SQL-Anweisung dynamisch zusammenstellen    
    sql = f'''INSERT INTO {table_name} ({columns_def}) VALUES (?, ?, ?)'''
    cur.execute(sql, (id, title, promt))

conn, cur = connect_to_database("Hallo")   
columns =[("Id", "INTEGER PRIMARY KEY"), ("title", "TEXT"), ("promt", "TEXT")]
table_name = "Gespraeche"
create_table(cur, table_name, columns)
title = "Coaching" 
promt = "Du bist ein Klient"
insert_in_table(cur, table_name, id, title, promt)
print_table(cur, table_name)