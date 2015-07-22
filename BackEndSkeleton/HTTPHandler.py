import web
import sqlite3
import DBManager


#THIS IS A CHANGE

class homeScreen:
	def __init__(self):
		"""
		The WebpyServer class is the blueprint for the server which will be called whenever a client begins a session.
		This is how the server is initialized and how it is able to react to the client.
		"""
		self.urls = (

			#self.urls is a tuple that contains all of the various urls for the webpage. Those urls are listed below with the name of the corresponding html pages that will generate.

			'/', "homeScreen",
			'/char',"charScreen",
			'/story',"storyScreen",
			'/game',"gameScreen",
			'/end',"endScreen",
			'/home', "homeScreen",
			'/hint', "hintScreen",
			'/about','aboutScreen',
			'/help','helpScreen',
			'/last', "lastScreen"

		) #The structure of the url and the name of the class to send the request to.
		self.render = web.template.render('templates/') #The file path for HTML templates.

		self.app = web.application(self.urls, globals()) #The application object that needs to be created for the app to run.

	def GET(self):
		"""
		This function renders homeScreen.html and checks to see if player data exists in the database. If not, this is a new player and new data is inserted into the database.
		If there is player data then the existing player state is updated.

		Parameters:
		None

		Returns:
		None
		"""
		if not DBManager.checkforExistingPlayer(web.ctx.ip): #Checking to see if current player has played before
			DBManager.insertPlayerData(web.ctx.ip) #If the above is true save the players ip address in the database
		playerStateObject = PlayerState() #Updating the player state
		return self.render.homeScreen() #Render homeScreen.html
	def POST(self):
		"""
		This function generates different html pages based on the buttons pressed by the user. From this screen, the player can choose to load a previous game or start a new one.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Update the player state
		action = web.input() #Create web.input() to save any information the user 
		if action['new'] == 'charScreen': #Checks to see if the user pressed the button to send them to the character selection screen
			raise web.seeother('/char') #If the above is true this line renders charScreen.html
		elif action['new'] == 'loadScreen': #Checks to see if the user pressed the button to load a previous game 
			if None != DBManager.getPlayerCharacterActionFromDB(playerStateObject.player_id): #If the above is true this line checks to see if the player has chosen a character in their previous game
				if None != DBManager.getPlayerStoryActionFromDB(playerStateObject.player_id): #If the above is true this line checks to see if the player has chosen a story in their previous game
					raise web.seeother('/game') #If the above is true this line renders gameScreen.html 
				else: 
					raise web.seeother('/story') #If the conditional on line 65 is false then the story selection screen for the players chosen character is rendered
			else:
				raise web.seeother('/char') #If the conditional on line 64 is false then the character selection screen is rendered
		elif action['new'] == 'aboutScreen': #This conditional checks to see if the user pressed the button to go to the about screen
			raise web.seeother('/about') #If the above conditional is true this line renders aboutScreen.html
		elif action['new'] == 'helpScreen': #This conditional checks to see if the user pressed the button to go to the help screen
			raise web.seeother('/help') #If the above is true then helpScreen.html is rendered

class charScreen:
	def __init__(self):
		"""
		This function contains the logic for dynamically rendering the character selection screen as well as saving the player's character choice in the database.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #This if the file path for all of the .html files so the renderer can find them
	def GET(self):
		"""
		This function renders charScreen.html when the user either types in the appropriate url or navigates to this page by interacting with the website.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		character_ids = DBManager.getCharacterData() #Pulls character data from the database and saves it to a variable
		character_names = DBManager.getCharacterNames() #Pulls character names from the database and saves it to a variable
		return self.render.charScreen(character_ids, character_names) #Dynamically renders charScreen.html using character_ids and character_names variables above
	def POST(self):
		"""
		This function handles saving the players chosen character and saving that information in the database.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating player state
		action = web.input() #Creating a web.input() object to hold any information that the user enters
		if action['Character']== "back": #Checks to see if the player pressed the back button
			raise web.seeother('/home') #Renders homeScreen.html
		else: 
			character=DBManager.getCharacterIDFromName(action['Character'])
			if DBManager.checkPlayerCharacterInput(character):
				DBManager.insertPlayerCharacterAction(playerStateObject.player_id,character)
				raise web.seeother('/story')


class storyScreen:
	def __init__(self):
		"""
		This class contains the logic for dynamically generating the story selection screen based on the players chosen character and saving the players story selection.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining the file path to all of the .html templates for the renderer
	def GET(self):
		"""
		This function dynamically renders storyScreen.html when the user types in the appropriate url or navigates to the page by interacting with the website.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		story_ids = DBManager.getStoriesFromDB(playerStateObject.player_id) #Getting story data from the database and saving it to a variable
		story_titles=DBManager.getStoryTitles(playerStateObject.player_id) #Getting story titles from the database and saving it to a variable
		return self.render.storyScreen(story_ids, story_titles) #Using the above two variables to dynamically generate storyScreen.html
	def POST(self):
		"""
		

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState()
		action = web.input()
		if action['story']== "back":
			raise web.seeother('/char')
		else:
			story_id= DBManager.getStoryIDFromTitle(action['story'])
			if DBManager.checkPlayerStoryInput(story_id):
				DBManager.insertPlayerStoryAction(playerStateObject.player_id,story_id)
				raise web.seeother('/game')

class gameScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		title, text, hint1, hint2, hint3, progress = DBManager.getDataFromDBForGameScreen(playerStateObject.player_id)
		if DBManager.needLastScreen(playerStateObject.player_id):
			raise web.seeother('/last')
		return self.render.gameScreen(title, text, hint1, hint2, hint3, progress)
	def POST(self):
		playerStateObject = PlayerState()
		if web.input()['home']=='home':
			raise web.seeother('/home')
		else:
			accession= web.input()['home']
			DBManager.insertPlayerStepAction(playerStateObject.player_id,accession)
			raise web.seeother('/game')

class lastScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		title,text,hint = DBManager.getDataFromDBForGameScreen(playerStateObject.player_id)
		return self.render.lastScreen(text,title)
	def POST(self):
		playerStateObject = PlayerState()
		if web.input()['home']=='home':
			raise web.seeother('/home')
		else:
			DBManager.insertPlayerStepAction(playerStateObject.player_id)
			raise web.seeother('/end')

class endScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		return self.render.endScreen()
	def POST(self):
		playerStateObject = PlayerState()
		if web.input()['home']=='home':
			raise web.seeother('/home')

class aboutScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		return self.render.aboutScreen()
	def POST(self):
		action = web.input()
		if action['back'] == 'backButton':
			raise web.seeother('/')

class helpScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		return self.render.helpScreen()
	def POST(self):
		action = web.input()
		if action['back'] == 'backButton':
			raise web.seeother('/')

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
