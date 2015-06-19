import web
import sqlite3
import DBManager

def getCharacterRequest():
	pass

def getStoryRequest():
	pass

def getStepCorrectRequest():
	pass

def getStepIncorrectRequest():
	pass

class WebpyServer:
	def __init__(self):
		"""
		The WebpyServer class is the blueprint for the server which will be called whenever a client begins a session.
		This is how the server is initialized and how it is able to react to the client.
		"""
		self.urls = ('/', 'WebpyServer') #The structure of the url and the name of the class to send the request to.
		self.app = web.application(self.urls, globals()) #The application object that needs to be created for the app to run.
		self.render = web.template.render('templates/') #The file path for HTML templates.


	def gameStart(self):
		"""
		This function contains all of the start up code necessary for GET().
		This function constructs a PlayerState object and assigns it to a variable in order to track the players place 
		in the story. Additionally, this function also renders the initial web page the player sees.

		Parameters: 
		None

		Returns:
		Rendered HTML page
		"""
		DBManager.insertPlayerData(web.ctx.ip)
		playerStateObject = PlayerState()
		return playerStateObject

	#def PlayerIsReturning():
		#if None != playerStateObject.player_current_action:
			#return True

	def pageToRender(self, playerStateObject):
		if None != playerStateObject.player_current_character_id:
			if None != playerStateObject.player_current_story_id:
				return self.render.gameScreen()
			else:
				return self.render.storyScreen()
		else:
			return self.render.homeScreen()
		

	def GET(self):
		"""
		The GET function is a HTTP method which will help create the initial server/client session.
		This is the initial handshake.
		This specific GET function will check to see if the player has played before via IP.
		If not then the player will be given a 'new player' path.

		Examples:
		Player enters the URL for the game. This begins the GET function which will serve up the player the correct HTML page.

		Parameters:
		None

		Returns:
		Rendered HTML page
		"""
		playerStateObject = self.gameStart()
		return self.pageToRender(playerStateObject) #Uses the template path that was defined earlier to find the correct HTML template. In this case, it is 'main.'

	def POST(self):
		"""
		The POST function is a HTTP method which allows for data to be sent from the client to the server.
		The main purpose of this POST is to make sure that the player's input will have an appropriate response.
		
		Examples:
		Player inputs an incorrect accession number. Receives the hint screen template with the correct information.
		Player inputs a correct accession number. Receives next part of the correct story.

		Parameters:
		None

		Returns:
		Rendered HTML page
		"""

		#return "post" #This is just a test for the moment.

		"""
		Lines 70 through 76 are an example of taking user input, comparing it to the DB, and finally generating an HTML page that is populated with data from the DB.
		"""
		playerStateObject = PlayerState()
		postData=web.input()
		DBManager.insertPlayerAction(playerStateObject.player_id, playerStateObject.player_current_story_id, playerStateObject.player_current_character_id,postData)
		#print postData
		self.pageToRender(playerStateObject)
			#if DBManager.checkPlayerInput(postData['homeMenu'],playerStateObject.player_current_action()[2]):
				#stepText = DBManager.getStepDataFromDB(playerStateObject.player_current_action()[2])[5]
				#return self.render.StepPrototype(stepText)
			#elif postData['homeMenu'] == "home":
				#return self.render.homeScreen()
				
		if DBManager.getAccessionAssociationFromDB(postData['user']):
			aa=DBManager.getAccessionAssociationFromDB(postData.user0
			return self.render.main(aa)
			
		'''
		if action.main=="home":
		action=web.input()
		if action=="home":
			return render.home()
		elif action=="navigation":
			return render.incorrect()
		elif readdata(action.accession)==True:
			return render.correct()
		'''

class PlayerState:
	def __init__(self):
		"""
		The player state class is initialized for each player which keeps a record of the player within the DB.
		This allows for easy access to the player's information through DBManager.

		Parameters:
		Character: The player's chosen character.
		Story: The player's chosen story.

		Returns:
		Something.
		"""

		self.player_data = DBManager.getPlayerFromDB(web.ctx.ip)

		self.player_id = self.player_data[0]

		self.player_current_action = DBManager.getCurrentPlayerActionFromDB(self.player_data[2])

		if None != self.player_current_action:

			self.player_current_story_id = self.player_current_action[4]

			self.player_current_character_id = self.player_current_action[5]

			self.player_current_step_id = self.player_current_action[2]

		else:

			self.player_current_story_id = None

			self.player_current_character_id = None

			self.player_current_step_id = None

