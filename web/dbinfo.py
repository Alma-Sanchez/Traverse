"""
I've uploaded the db needed to run the server I've created. However since we'll likely
want to create a different table and enter in actual data, it might be helpful to easily 
be able to do so. Below is how I created and then added in data to my db.
"""

import sqlite3

connection=sqlite3.connect('test.db')
c=connection.cursor()

def createtable():
	c.execute("CREATE TABLE nameoftable(ascension REAL, title TEXT, artist TEXT)")
	  """
	  Please note that sql commands are in all caps. Also I have acension number, 
	  title, and artist in as filler currently until we decide what we want our 
	  framework to be.
	  """

#createtable()

def dataentry():
	c.execute("INSERT INTO nameoftable VALUES(111.1, 'Title 1', 'Artist 1')")
	c.execute("INSERT INTO nameoftable VALUES(222.2, 'Title 2', 'Artist 2')")
	c.execute("INSERT INTO nameoftable VALUES(333.3, 'Title 3', 'Artist 3')")
	connection.commit()
	"""
	The values correspond to the labels in createtable (ascension, title, and artist
	respectively). 
	"""

#dataentry()
