
import mysql.connector
db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'root', port = 3306)

my_cursor = db.cursor()

my_cursor.execute("CREATE DATABASE Inventory")

