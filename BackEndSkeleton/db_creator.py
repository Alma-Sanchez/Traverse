#Python version 2.7.9

import csv
import sqlite3

def dropTables(connection):
	"""
	This function drops all the tables that should be in the SAAM database.

	Parameters:
	None

	Returns:
	None
	"""
	conn = connection
	c = conn.cursor() #Cursor for querying the database.

	c.execute("DROP TABLE IF EXISTS Player_Data") #Drops (deletes) table named Player_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Player_Character_Action") #Drops (deletes) table named Player_Action if it exists.
	c.execute("DROP TABLE IF EXISTS Player_Story_Action")
	c.execute("DROP TABLE IF EXISTS Player_Step_Action")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Data") #Drops (deletes) table named Archived_Player_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Archived_Player_Character_Action") #Drops (deletes) table named Archived_Player_Action if it exists.
	c.execute("DROP TABLE IF EXISTS Archived_Player_Story_Action")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Step_Action")
	c.execute("DROP TABLE IF EXISTS Story_Data") #Drops (deletes) table named Story_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Character_Data") #Drops (deletes) table named Character_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Step_Data") #Drops (deletes) table named Step_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Accession_Association") #Drops (deletes) table named Accession_Association if it exists.

def createTables(connection):
	"""
	This function creates the tables that will be used for the SAAM database. 
	If this function is executed while these tables exist, an error will appear. 
	In order to change the schema, call dropTables() and call createTables().

	Parameters:
	None

	Returns:
	None
	"""
	conn = connection
	c = conn.cursor() #Cursor for querying database.

	c.execute("CREATE TABLE Player_Data (Player_ID Integer primary key autoincrement, IP Text, Current_Action_ID INT)") #Creates new table named Player_Data with hardcoded parameters.
	c.execute("CREATE TABLE Player_Character_Action (Character_Action_ID Integer primary key autoincrement, Player_ID INT, Current_Character_ID INT, Player_Input Text)") #Creates new table named Player_Action with hardcoded parameters.
	c.execute("CREATE TABLE Player_Story_Action (Story_Action_ID Integer primary key autoincrement, Player_ID INT, Current_Story_ID INT, Player_Input Text)")
	c.execute("CREATE TABLE Player_Step_Action (Step_Action_ID Integer primary key autoincrement, Previous_Step_ID INT, Current_Step_ID INT, Next_Step_ID INT, Player_Input Text)")
	c.execute("CREATE TABLE Archived_Player_Data (Player_ID INT, Player_name TEXT, Current_step_ID INT)") #Creates new table named Archived_Player_Data with hardcoded parameters.
	c.execute("CREATE TABLE Archived_Player_Character_Action (Character_Action_ID Int, Player_ID INT, Current_Character_ID INT, Player_Input Text)") #Creates new table named Player_Action with hardcoded parameters.
	c.execute("CREATE TABLE Archived_Player_Story_Action (Story_Action_ID Int, Player_ID INT, Current_Story_ID INT, Player_Input Text)")
	c.execute("CREATE TABLE Archived_Player_Step_Action (Step_Action_ID Int, Previous_Step_ID INT, Current_Step_ID INT, Next_Step_ID INT, Player_Input Text)")
	c.execute("CREATE TABLE Story_Data (Story_ID INT, Character_ID INT, Title_Of_Story TEXT, Number_Of_Steps INT)") #Creates new table named Story_Data with hardcoded parameters.
	c.execute("CREATE TABLE Character_Data(Character_ID INT, Character_Name TEXT, Accession_Number TEXT)") #Creates new table named Character_Data with hardcoded parameters.
	c.execute("CREATE TABLE Step_Data(Story_ID INT, Step_ID INT, Previous_step_ID INT, Next_Step_ID INT, Accession_Association TEXT, Step_Text TEXT, Step_Art TEXT, Step_Hint TEXT)") #Creates new table named Step_Data with hardcoded parameters.
	c.execute("CREATE TABLE Accession_Association(Accession_Association TEXT, Accession_Number TEXT)") #Creates new table named Accession_Association with hardcoded parameters.

def populateTables(connection):
	"""
	This function will populate tables within the SAAM database using CSV files.
	The file names and the path for the file open should be the same. If it is not then the reader will break.

	Parameters:
	None 

	Returns:
	None
	"""
	conn = connection
	c = conn.cursor() #Cursor for querying database.

	with open('CSV_file\Accession.csv','rb') as accession_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(accession_data_file) #Reads the csv file and sets it as a new variable
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Accession_Association VALUES (?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	accession_data_file.close() #Closes the csv file.

	with open('CSV_file\Character_Data.csv','rb') as character_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(character_data_file) #Reads the csv file and sets ut as a new variable.
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Character_Data VALUES (?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	character_data_file.close() #Closes the csv file.

	with open('CSV_file\Story_Data.csv', 'rb') as story_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(story_data_file) #Reads the csv file and sets it as a new variable.
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Story_Data VALUES (?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	story_data_file.close() #Closes the csv file.

	with open('CSV_file\Step_Data.csv', 'rb') as step_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(step_data_file) #Reads the csv file and sets it a new variable.
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Step_Data VALUES (?,?,?,?,?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8"),unicode(row[4], "utf-8"),unicode(row[5], "utf-8"),unicode(row[6], "utf-8"),unicode(row[7], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	step_data_file.close() #Closes the csv file.