import csv
import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

with open("stocks.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        symbol = row["Symbol"]
        security_name = row["Security Name"]

        sql_statement = f"""INSERT INTO screener_stock (symbol, security_name)
                            VALUES (?, ?)"""
        cursor.execute(sql_statement, (symbol, security_name))

results = cursor.fetchall()
print(results)

connection.commit()
connection.close()
