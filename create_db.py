"""This file is to create the database should only be run once"""
import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='Team32', port=3306)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE Inventory")
