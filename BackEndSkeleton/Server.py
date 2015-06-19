#Python version 2.7.9
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
	player = HTTPHandler.PlayerState()
	player.playerUpdate()

if __name__=="__main__": #Checks to see if server.py is the main file that is being called. 
	setupServer() #runs a Webpy server

'''
while True:
	#Need to update player on a loop here.
	#Problem here is that we will constantly be overwriting the player variable with a new PlayerState construction.
	#Need to be able to update player member variables without overwriting the player variable everytime we update.
	#We cannot define player outside of the loop because we need to create a new player variable everytime a new player joins the game.
	#Therefore, creating an instance of the PlayerState object must happen in some sort of loop or some other dynamic construct.
	setupPlayer()
'''