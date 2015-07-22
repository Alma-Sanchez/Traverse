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
		if not DBManager.checkforExistingPlayer(web.ctx.ip):
			DBManager.insertPlayerData(web.ctx.ip)
		playerStateObject = PlayerState()
		return self.render.homeScreen()
	def POST(self):
		playerStateObject = PlayerState()
		action = web.input()
		if action['new'] == 'charScreen':
			raise web.seeother('/char')
		elif action['new'] == 'loadScreen':
			if None != DBManager.getPlayerCharacterActionFromDB(playerStateObject.player_id):
				if None != DBManager.getPlayerStoryActionFromDB(playerStateObject.player_id):
					raise web.seeother('/game')
				else:
					raise web.seeother('/story')
			else:
				raise web.seeother('/char')
		elif action['new'] == 'aboutScreen':
			raise web.seeother('/about')
		elif action['new'] == 'helpScreen':
			raise web.seeother('/help')

class charScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		character_ids = DBManager.getCharacterData()
		character_names = DBManager.getCharacterNames()
		return self.render.charScreen(character_ids, character_names)
	def POST(self):
		playerStateObject = PlayerState()
		action = web.input()
		if action['Character']== "back":
			raise web.seeother('/home')
		else: 
			character=DBManager.getCharacterIDFromName(action['Character'])
			if DBManager.checkPlayerCharacterInput(character):
				DBManager.insertPlayerCharacterAction(playerStateObject.player_id,character)
				raise web.seeother('/story')

class storyScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		story_ids = DBManager.getStoriesFromDB(playerStateObject.player_id)
		story_titles=DBManager.getStoryTitles(playerStateObject.player_id)
		return self.render.storyScreen(story_ids, story_titles)
	def POST(self):
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
