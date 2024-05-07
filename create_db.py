import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user="root", passwd= "Team32")

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE Inventory")

