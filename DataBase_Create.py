import sqlite3

conn = sqlite3.connect("SAAM_database_test2.db")

c = conn.cursor()

def tableCreate():
	c.execute("CREATE TABLE Player_Data (Player_ID INT, Player_name TEXT, e_mail TEXT, Password TEXT)")
	c.execute("CREATE TABLE Player_Action (Action_ID INT, Player_ID INT, Current_step_ID INT, Previous_step_ID INT, Story_ID INT)")
	c.execute("CREATE TABLE Archived_Player_Data (Player_ID INT, Player_name TEXT, e_mail, TEXT, Password TEXT)")
	c.execute("CREATE TABLE Archived_Player_Action (Action_ID INT, Player_ID INT, Current_step_ID INT, Previous_step_ID INT, Story_ID INT)")
	c.execute("CREATE TABLE Story_Data (Story_ID INT, Character_ID INT, Title_of_Story TEXT, Number_of_steps INT)")
	c.execute("CREATE TABLE Character_Data(Character_ID INT, Character_name TEXT, Accession_number TEXT)")
	c.execute("CREATE TABLE Step_Data(Step_ID INT, Story_ID INT, Previous_step_ID INT, Next_Step_ID INT, Accession_association TEXT, Hint TEXT, Art TEXT, Step_Text TEXT)")
	c.execute("CREATE TABLE Accession(Accession_association TEXT, Accession_number TEXT)")




tableCreate()
