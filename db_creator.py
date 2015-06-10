#Python version 2.7.9
#A_Sandhu

import csv
import sqlite3

conn = sqlite3.connect("SAAM_database_test2.db")

def dropTables():
	"""
	This function drops all the tables that should be in the SAAM database.

	Parameters:
	None

	Returns:
	None
	"""
	c = conn.cursor()

	c.execute("DROP TABLE IF EXISTS Player_Data")
	c.execute("DROP TABLE IF EXISTS Player_Action")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Data")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Action")
	c.execute("DROP TABLE IF EXISTS Story_Data")
	c.execute("DROP TABLE IF EXISTS Character_Data")
	c.execute("DROP TABLE IF EXISTS Step_Data")
	c.execute("DROP TABLE IF EXISTS Accession")

def createTables():
	"""This function creates the tables that will be used for the SAAM database. 
	If this function is executed while these tables exist, an error will appear. 
	In order to change the schema, call dropTables() and call createTables().

	Parameters:
	None

	Returns:
	None
	"""
	c = conn.cursor()

	c.execute("CREATE TABLE Player_Data (Player_ID INT, Player_name TEXT, e_mail TEXT, Password TEXT)")
	c.execute("CREATE TABLE Player_Action (Action_ID INT, Player_ID INT, Current_step_ID INT, Previous_step_ID INT, Story_ID INT)")
	c.execute("CREATE TABLE Archived_Player_Data (Player_ID INT, Player_name TEXT, e_mail, TEXT, Password TEXT)")
	c.execute("CREATE TABLE Archived_Player_Action (Action_ID INT, Player_ID INT, Current_step_ID INT, Previous_step_ID INT, Story_ID INT)")
	c.execute("CREATE TABLE Story_Data (Story_ID INT, Character_ID INT, Title_of_Story TEXT, Number_of_steps INT)")
	c.execute("CREATE TABLE Character_Data(Character_ID INT, Character_name TEXT, Accession_number TEXT)")
	c.execute("CREATE TABLE Step_Data(Step_ID INT, Story_ID INT, Previous_step_ID INT, Next_Step_ID INT, Accession_association TEXT, Hint TEXT, Art TEXT, Step_Text TEXT)")
	c.execute("CREATE TABLE Accession(Accession_association TEXT, Accession_number TEXT)")

def populateTables():
	"""
	This function will populate tables within the SAAM database using CSV files.
	The file names and the path for the file open should be the same. If it is not then the reader will break.

	Parameters:
	None 

	Returns:
	None
	"""
	c = conn.cursor()

	with open('CSV_file\Accession.csv','rb') as accession_data_file:
		spamreader = csv.reader(accession_data_file)
		for row in spamreader:
			#Adds the information from the csv file into the correct database table.
			c.execute("INSERT INTO Accession VALUES (?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8")))
	conn.commit()
	accession_data_file.close()

	with open('CSV_file\Character_Data.csv','rb') as character_data_file:
		spamreader = csv.reader(character_data_file)
		for row in spamreader:
			#Adds the information from the csv file into the correct database table.
			c.execute("INSERT INTO Character_Data VALUES (?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8")))
	conn.commit()
	character_data_file.close()

	with open('CSV_file\Story_Data.csv', 'rb') as story_data_file:
		spamreader = csv.reader(story_data_file)
		for row in spamreader:
			#Adds the information from the csv file into the correct database table.
			c.execute("INSERT INTO Story_Data VALUES (?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8")))
	conn.commit()
	story_data_file.close()

	with open('CSV_file\Step_Data.csv', 'rb') as step_data_file:
		spamreader = csv.reader(step_data_file)
		for row in spamreader:
			#Adds the information from the csv file into the correct database table.
			c.execute("INSERT INTO Step_Data VALUES (?,?,?,?,?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8"),unicode(row[4], "utf-8"),unicode(row[5], "utf-8"),unicode(row[6], "utf-8"),unicode(row[7], "utf-8")))
	conn.commit()
	step_data_file.close()

dropTables()
createTables()
populateTables()