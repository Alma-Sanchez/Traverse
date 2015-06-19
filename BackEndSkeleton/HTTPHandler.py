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

class homeScreen:
	def __init__(self):
		"""
		The WebpyServer class is the blueprint for the server which will be called whenever a client begins a session.
		This is how the server is initialized and how it is able to react to the client.
		"""
		self.urls = (

			'/', "homeScreen",
			'/char',"charScreen",
			'/char/story',"storyScreen",
			'/char/story/game',"gameScreen",
			'/char/story/game/end',"endScreen"

		) #The structure of the url and the name of the class to send the request to.
		self.render = web.template.render('templates/') #The file path for HTML templates.

		self.app = web.application(self.urls, globals()) #The application object that needs to be created for the app to run.

	def GET(self):
		return self.render.homeScreen()
	def POST(self):
		action = web.input()
		if action['new'] == 'charScreen':
			raise web.seeother('/char')

class charScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		return self.render.charScreen()
	def POST(self):
		action1 = web.input()
		if action1['Character'] == '1':
			raise web.seeother('/char/story')
		elif action1['Character'] == '2':
			raise web.seeother('/char/story')
		elif action1['Character'] == '3':
			raise web.seeother('/char/story')

class storyScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		return self.render.storyScreen()
	def POST(self):
		pass
		action = web.input()

class gameScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		return self.render.gameScreen()
	def POST(self):
		pass
		action = web.input()

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

