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
	conn,c = connection

	c.execute("DROP TABLE IF EXISTS Player_Data") #Drops (deletes) table named Player_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Player_Story_Action")
	c.execute("DROP TABLE IF EXISTS Player_Step_Action")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Data") #Drops (deletes) table named Archived_Player_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Archived_Player_Story_Action")
	c.execute("DROP TABLE IF EXISTS Archived_Player_Step_Action")
	c.execute("DROP TABLE IF EXISTS Story_Data") #Drops (deletes) table named Story_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Step_Data") #Drops (deletes) table named Step_Data if it exists.
	c.execute("DROP TABLE IF EXISTS Accession_Answers") #Drops (deletes) table named Accession_Association if it exists.
	c.execute("DROP TABLE IF EXISTS Answer_Key") #Drops (deletes) table named Answer_Key if it exists.
	c.execute("DROP TABLE IF EXISTS Answer_Type_Numbers") #Drops (deletes) table named Number_Answers if it exists.
	c.execute("DROP TABLE IF EXISTS Answer_Type_Text") #Drops (deletes) table named Text_Answers if it exists.
	c.execute("DROP TABLE IF EXISTS Answer_Type_Multiple_Choice") #Drops (deletes) table named Answer_Type_Multiple_Choice if it exists.
	c.execute("DROP TABLE IF EXISTS Step_Transition_Data") #Drops (deletes) table named Step_Transition_Data.

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
	conn,c = connection

	c.execute("CREATE TABLE Player_Data (Player_ID Integer primary key autoincrement, IP Text, Current_Character_Action_ID INT, Current_Story_Action_ID INT, Current_Step_Action_ID INT)") #Creates new table named Player_Data with hardcoded parameters.
	c.execute("CREATE TABLE Player_Story_Action (Story_Action_ID Integer primary key autoincrement, Player_ID INT, Current_Story_ID INT, Player_Input TEXT)")
	c.execute("CREATE TABLE Player_Step_Action (Step_Action_ID Integer primary key autoincrement, Player_ID INT, Previous_Step_ID INT, Current_Step_ID INT, Next_Step_ID INT, Player_Input TEXT, Misses INT)")
	c.execute("CREATE TABLE Archived_Player_Data (Player_ID INT, IP TEXT, Current_Character_Action_ID INT, Current_Story_Action_ID INT, Current_Step_Action_ID INT)") #Creates new table named Archived_Player_Data with hardcoded parameters.
	c.execute("CREATE TABLE Archived_Player_Story_Action (Story_Action_ID INT, Player_ID INT, Current_Story_ID INT, Player_Input TEXT)")
	c.execute("CREATE TABLE Archived_Player_Step_Action (Step_Action_ID INT, Previous_Step_ID INT, Current_Step_ID INT, Next_Step_ID INT, Player_Input TEXT)")
	c.execute("CREATE TABLE Story_Data (Story_ID INT, Title_Of_Story TEXT, Walk_Level INT, Kid_Friendly TEXT)") #Creates new table named Story_Data with hardcoded parameters.
	c.execute("CREATE TABLE Step_Data(Story_ID INT, Step_ID INT,Actual_Step_Number INT, Step_Text TEXT, Step_Hint_1 TEXT, Step_Hint_2 TEXT, Step_Hint_3 TEXT)") #Creates new table named Step_Data with hardcoded parameters.
	c.execute("CREATE TABLE Answer_Key (Answer_ID INT, Answer_Type INT)")
	c.execute("CREATE TABLE Answer_Type_Numbers(Answer_ID INT, Low_End INT, High_End INT)")
	c.execute("CREATE TABLE Answer_Type_Text(Answer_ID INT, String_Answer TEXT)")
	c.execute("CREATE TABLE Answer_Type_Multiple_Choice(Answer_ID INT, Answer_Text TEXT, Right_Wrong INT, MC_Flag INT)")
	c.execute("CREATE TABLE Step_Transition_Data(Story_ID INT, Step_ID INT, Previous_Step_ID INT, Next_Step_ID INT, Answer_ID INT, MC_Flag INT)")

def populateTables(connection):
	"""
	This function will populate tables within the SAAM database using CSV files.
	The file names and the path for the file open should be the same. If it is not then the reader will break.

	Parameters:
	None

	Returns:
	None
	"""
	conn,c = connection

	with open('CSV_file\Story_Data.csv', 'rb') as story_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(story_data_file) #Reads the csv file and sets it as a new variable.
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Story_Data VALUES (?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"), unicode(row[3], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	story_data_file.close() #Closes the csv file.

	with open('CSV_file\Step_Data.csv', 'rb') as step_data_file: #Opens file and assigns it to a variable.
		spamreader = csv.reader(step_data_file) #Reads the csv file and sets it a new variable.
		for row in spamreader: #Iterates through csv file rows.
			c.execute("INSERT INTO Step_Data VALUES (?,?,?,?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8"),unicode(row[4], "utf-8"),unicode(row[5], "utf-8"),unicode(row[6], "utf-8"))) #Encodes and inserts data from the csv file.
	conn.commit() #Commits (permanently changes) the database.
	step_data_file.close() #Closes the csv file.

	with open('CSV_file\Answer_Key.csv', 'rb') as answer_key_file:
		spamreader = csv.reader(answer_key_file)
		for row in spamreader:
			c.execute("INSERT INTO Answer_Key VALUES (?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8")))
	conn.commit()
	answer_key_file.close()

	with open('CSV_file\Answer_Type_Text.csv', 'rb') as text_answers_file:
		spamreader = csv.reader(text_answers_file)
		for row in spamreader:
			c.execute("INSERT INTO Answer_Type_Text VALUES (?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8")))
	conn.commit()
	text_answers_file.close()

	# with open('CSV_file\Answer_Type_Multiple_Choice.csv', 'rb') as Answer_Type_Multiple_Choice_file:
	# 	spamreader = csv.reader(Answer_Type_Multiple_Choice_file)
	# 	for row in spamreader:
	# 		c.execute("INSERT INTO Answer_Type_Multiple_Choice VALUES (?,?,?,?)", (unicode(row[0], "utf-8", errors='ignore'),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8")))
	# conn.commit()
	# Answer_Type_Multiple_Choice_file.close()

	with open('CSV_file\Step_Transition_Data.csv', 'rb') as step_transition_data_file:
		spamreader = csv.reader(step_transition_data_file)
		for row in spamreader:
			c.execute("INSERT INTO Step_Transition_Data VALUES (?,?,?,?,?,?)", (unicode(row[0], "utf-8"),unicode(row[1], "utf-8"),unicode(row[2], "utf-8"),unicode(row[3], "utf-8"),unicode(row[4], "utf-8"),unicode(row[5], "utf-8")))
	conn.commit()
	step_transition_data_file.close()

	# with open('CSV_file\Answer_Type_Numbers.csv', 'rb') as number_answers_file:
	# 	spamreader = csv.reader(number_answers_file)
	# 	for row in spamreader:
	# 		c.execute("INSERT INTO Answer_Type_Numbers VALUES (?,?,?)", (unicode(row[0], "utf-8"), unicode(row[1], "utf-8"), unicode(row[2], "utf-8")))
	# conn.commit()
	# number_answers_file.close()
