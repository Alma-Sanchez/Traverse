import web
import sqlite3
import DBManager

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
			'/last', "lastScreen",
			'/load', "loadScreen"

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
		#if not DBManager.checkforExistingPlayer(web.ctx.ip): #Checking to see if current player has played before
		DBManager.getPlayerIP(web.ctx.ip) #If the above is true save the players ip address in the database
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
		if action['new'] == 'storyScreen': #Checks to see if the user pressed the button to send them to the character selection screen
			raise web.seeother('/story') #If the above is true this line renders charScreen.html
		elif action['new'] == 'loadScreen': #Checks to see if the user pressed the button to load a previous game
			if None != DBManager.getPlayerCharacterActionFromDB(playerStateObject.player_id): #If the above is true this line checks to see if the player has chosen a character in their previous game
				if None != DBManager.getPlayerStoryActionFromDB(playerStateObject.player_id): #If the above is true this line checks to see if the player has chosen a story in their previous game
					raise web.seeother('/load') #If the above is true this line renders gameScreen.html
				else:
					raise web.seeother('/load') #If the conditional on line 65 is false then the story selection screen for the players chosen character is rendered
			else:
				raise web.seeother('/load') #If the conditional on line 64 is false then the character selection screen is rendered
		elif action['new'] == 'aboutScreen': #This conditional checks to see if the user pressed the button to go to the about screen
			raise web.seeother('/about') #If the above conditional is true this line renders aboutScreen.html
		elif action['new'] == 'helpScreen': #This conditional checks to see if the user pressed the button to go to the help screen
			raise web.seeother('/help') #If the above is true then helpScreen.html is rendered

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
		walk_level=DBManager.getStoryData()[0]
		kid_friendly=DBManager.getStoryData()[1]
		return self.render.storyScreen(story_ids, story_titles, walk_level, kid_friendly) #Using the above two variables to dynamically generate storyScreen.html
	def POST(self):
		"""
		This function checks to see if the player has chosen a story and if they have the story choice is saved.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		action = web.input() #Creating web.input() object to save any from data input by the user
		if action['story']== "back": #Checks to see if the player pressed the back button
			raise web.seeother('/home') #If the above is true then the charScreen.html is rendered
		else:
			title= action['story']
			story_id=DBManager.getStoryIDFromTitle(title)
			print story_id
			DBManager.insertPlayerStoryAction(playerStateObject.player_id,story_id) #If the above is true the story selection is inserted into the database
			raise web.seeother('/game') #Rendering gameScreen.html

class loadScreen:
	def __init__(self):
		"""
		This class contains the logic for dynamically generating the load selection screen based and saving the players story selection.

		Parameters:
		None

		Returns:
		None
		"""
	def GET(self):
		"""
		This function dynamically renders loadScreen.html when the user choses to load past progress by navigating from the home screen.

		Parameters:
		None

		Returns:
		None
		"""
		story_ids= (1,2,3)
		story_titles=("title1", "title2", "title3")
		walk_level= (1,1,3)
		kid_friendly= ("K","","")
		self.render = web.template.render('templates/') #Defining the file path for the renderer to find all of the .html files
		return self.render.loadScreen(story_ids, story_titles, walk_level, kid_friendly)
	def POST(self):
		"""
		This function checks to see if the player has chosen a story and if they have the story choice is saved.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState()
		action = web.input()
		if action['story']=="back":
			raise web.seeother('/')
		else:
			title=action['story']
			story_id=DBManager.getStoryIDFromTitle(title)
			DBManager.insertPlayerStoryAction(playerStateObject.player_id,story_id)
			raise web.seeother('/game')


class gameScreen:
	def __init__(self):
		"""
		This class handles dynamically rendering each step of the game. There is the same basic template, but the text displayed to the user and the answer needed to advance to the
		next step are dynamically generated based on player character/story choice as well as player progress.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining file path to the .html templates for the renderer to find
	def GET(self):
		"""
		This function dynamically generates the steps of the game until there are no more steps. The elements of this webpage change based on the players progress and their
		Character/Story choices.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState()
		if DBManager.needLastScreen(playerStateObject.player_id)==True:
			print "need last"
			raise web.seeother('/last')
		else:
			print "not last"
		title, text, hint1, hint2, hint3, answertext = DBManager.getGameScreenDataFromDB(playerStateObject.player_id) #Assigning several variables by pulling data from the database in order to dynamically generate different bodies of text for the user
		return self.render.gameScreen(title, text, hint1, hint2, hint3, answertext) #Rendering the gameScreen.html

	def POST(self):
		"""
		This function responds to user input and generates the proper game screens. This function ultimately controls game flow.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating player state

		if web.input()['home']=='home': #Checking to see if the player pressed the home button
			raise web.seeother('/home') #If the above is true then homeScreen.html is rendered
		else:
			player_input= web.input()['home'] #Creating web.input() to hold user input information
			player_input= player_input.lower()
			#if DBManager.needLastScreen(playerStateObject.player_id, player_input): #Checks to see if the player has reached the end of the game and the final screen need to be displayed
			#	raise web.seeother('/last') #If the above is true then lastScreen.html is rendered
			DBManager.compareInputToAnswers(playerStateObject.player_id, player_input) #Inserting the action that the player took and inserting that information into the database
			print "compare input run"
			raise web.seeother('/game') #Rendering gameScreen.html



class lastScreen:
	def __init__(self):
		"""
		This class renders the second to last screen of the game.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining the file path for the renderer to find all of the .html files
	def GET(self):
		"""
		This function render lastScreen.html when the player either navigates to it by interacting with the website or typing in the appropriate url.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		title,text = DBManager.getLastScreenDataFromDB(playerStateObject.player_id) #Assigning several variables by pulling data from the database
		return self.render.lastScreen(text,title) #Rendering lastScreen.html using the variables on line 239
	def POST(self):
		"""
		This function checks to see if the home button was pressed and if it was homeScreen.html is rendered. If not, lastScreen.html stays rendered.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		if web.input()['home']=='home': #Checks to see if the player pressed the home button
			raise web.seeother('/end') #If the above is true homeScreen.html is rendered
		else:
			DBManager.insertPlayerStepAction(playerStateObject.player_id) #If the player did not hit the home button this line records the action the player took and saves it in the database
			raise web.seeother('/end') #This line renders endScreen.html

class endScreen:
	def __init__(self):
		"""
		This class renders the final screen of the game after the story is concluded.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining the file path of the .html templates for the renderer to use
	def GET(self):
		"""
		This function renders the end game screen when the player finishes a story.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating the player state
		return self.render.endScreen() #Rendering endScreen.html
	def POST(self):
		"""
		This function waits to see if the player has pressed the home button and if they have homeScreen.html is rendered.

		Parameters:
		None

		Returns:
		None
		"""
		playerStateObject = PlayerState() #Updating player state
		if web.input()['home']=='home': #Checking to see if the player pressed the home button
			raise web.seeother('/home') #If the above is true this line renders homeScreen.html

class aboutScreen:
	def __init__(self):
		"""
		This class renders the about page and also contains the logic to navigate back to the home screen.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining the file path for all of the .html templates
	def GET(self):
		"""
		This function renders aboutScreen.html.

		Parameters:
		None

		Returns:
		None
		"""
		return self.render.aboutScreen() #Rendering aboutScreen.html
	def POST(self):
		"""
		This function defines a web.input() in order to hold any information the user may input. Additionally, it contains the logic to return to the home screen.
		"""
		action = web.input() #Creating web.input() to save user input data
		if action['back'] == 'backButton': #Checking to see if the user pressed the back button
			raise web.seeother('/') #If the above is true then homeScreen.html is rendered.

class helpScreen:
	def __init__(self):
		"""
		This class renders the help screen.

		Parameters:
		None

		Returns:
		None
		"""
		self.render = web.template.render('templates/') #Defining the file path for the .html templates
	def GET(self):
		"""
		This function renders helpScreen.html

		Parameters:
		None

		Returns:
		None
		"""
		return self.render.helpScreen() #Rendering helpScreen.html
	def POST(self):
		"""
		This function creates a web.input() in order to hold any information the user may input as well as containing the logic for a back button.

		Parameters:
		None

		Returns:
		None
		"""
		action = web.input() #Creatig web.input() in order to hold any user input data
		if action['back'] == 'backButton': #Checking to see if the user pressed the back button
			raise web.seeother('/') #If the above is true homeScreen.html is rendered

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

		self.player_data = DBManager.getPlayerFromDB(web.ctx.ip) #Pulling all player data from the database via a unique player ip address

		self.player_id = self.player_data[0] #Pull the first element from the player_data array to obtain a player's unique id
