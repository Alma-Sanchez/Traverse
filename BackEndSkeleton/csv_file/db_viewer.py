#Python version 2.7.9
#A_Sandhu
import sqlite3

con = sqlite3.connect('SAAM_database_test2.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM Character_Data")

print(cursor.fetchall())