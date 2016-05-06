"""Python version 2.7.9"""
import HTTPHandler #Imports modules needed to run server.py
import DBManager

def setupServer():
	"""
	This function creates a Webpy server obect and begins to run that server.

	Parameters:
	None

	Returns:
	None
	"""
	server = HTTPHandler.homeScreen() #Creates a new instance of the server.
	server.app.run() #Runs the server if server.py is the file being called. WILL NOT WORK IF SERVER.PY IS BEING CALLED AS A MODULE.

def setupPlayer():
	"""
	This function instantiates the playerState class and saves that instance to a variable named player.
	The player state class is initialized for each player which keeps a record of the player within the DB.
	This allows for easy access to the player's information through DBManager.

	Parameters:
	None

	Returns:
	None
	"""
	player = HTTPHandler.PlayerState() #Creating instance of playerState class and assigning that value to the variable player.

if __name__=="__main__": #Checks to see if server.py is the main file that is being called. 
	setupServer() #if the above is true, an instance of the webpy server under the variable name server will run 