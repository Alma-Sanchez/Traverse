#Python version 2.7.9

import sqlite3 #Imports sqlite3 module. Needed to work with the Database.

conn = sqlite3.connect("SAAM_database_test2.db") #Connects database 

def getIPFromDB():
	"""
	This function will get the player's IP address from the database and returns the player's IP.

	Parameters:
	None

	Returns:
	string: Player's IP
	"""
	pass

def getCharacterFromDB():
	"""
	This function will get the correct character for the correct player and return the appropriate character.
	
	Parameters:
	None

	Returns:
	number: character ID (OR CAN RETURN STRING: CHARACTER NAME. TAYLOR DECIDE.)
	"""
	pass

def getStoryFromDB():
	"""
	This function will query the database and return the correct story associated with the player.

	Parameters:
	None

	Returns:
	number: Story ID (OR CAN RETURN STRING: STORY NAME. TAYLOR DECIDE THIS.)
	"""
	pass

def getStepFromDB():
	"""
	This function will query the database and return the correct step that the player is on.

	Parameters:
	None

	Returns:
	number: Step ID
	"""
	pass

def getStepTextFromDB():
	"""
	This function will query the database and return the text associated with the step the player is on

	Parameters: Step ID

	Returns:
	text: the text associated with the step in the story
	"""
	pass

def getStepArtFromDB():
	"""
	This function will query the database and return the art associated with the step the player is on (if such art exists)

	Parameter: Step ID

	Returns:
	text: the key word associated with the particular art for that step
	"""
	pass

def getHintFromDB():
	"""
	This function will query the database and return the hint associated with the particular ste the play is on

	Parameter: Step ID

	Returns:
	text: the hint asociated with that step in the story
	"""
	pass
