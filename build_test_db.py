"""
To get webpy_server.py working you'll need to create your db and then add
in the info you'd like. Here's the code below. Please note that once you only
need to create the table once.
""" 

import sqlite3

connection=sqlite3.connect('test.db')
c=connection.cursor()

def createtable():
	c.execute("CREATE TABLE nameoftable(ascension REAL, title TEXT, artist TEXT)")
		#sql commands are in all caps, acension number, title, artist

#createtable()

def dataentry():
	c.execute("INSERT INTO nameoftable VALUES(111.1, 'Title 1', 'Artist 1')")
	c.execute("INSERT INTO nameoftable VALUES(222.2, 'Title 2', 'Artist 2')")
	c.execute("INSERT INTO nameoftable VALUES(333.3, 'Title 3', 'Artist 3')")
	connection.commit()

#dataentry()
