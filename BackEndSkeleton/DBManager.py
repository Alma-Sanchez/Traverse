#Python version 2.7.9

import sqlite3 #Imports sqlite3 module. Needed to work with the Database.

conn = sqlite3.connect("SAAM_database_test2.db") #Connects database 

def getPlayerFromDB(ip):
	"""
	This function will get the player's IP address from the database and returns the player's IP.

	Parameters:
		ip (int): The IP address of the player connecting to the web.py server.

	Returns:
		string: Player's IP
	"""
	pass

def getPlayerActionFromDB(currentStepID):
	"""
	This function returns a row from the Player_Action table that corresponds 
	to the current player action.

	Parameters:
		currentStepID (int): The ID of the current step taken from the Player_Data table.

	Returns:
		tuple: The tuple containing the row information.

	Examples:
		getPlayerActionFromDB(playerInfo.currentStepID) => (4 50, 22, 21, 2, 1)
	"""
	pass

def getCharacterFromDB():
	"""
	This function will get the correct character for the correct player and return the appropriate character.
	
	Parameters:
	None

	Returns:
	tuple: character fields
	"""
	pass

def getStoryFromDB():
	"""
	This function will query the database and return the correct story associated with the player.

	Parameters:
	None

	Returns:
	tuple: Story fields
	"""
	pass

def getStepFromDB():
	"""
	This function will query the database and return the correct step that the player is on.

	Parameters:
	None

	Returns:
	tuple: Step fields
	"""
	pass

def getAccessionNumberFromDB():
	pass