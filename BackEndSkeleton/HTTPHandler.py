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

			'/', "homeScreen",
			'/char',"charScreen",
			'/story',"storyScreen",
			'/game',"gameScreen",
			'/end',"endScreen",
			'/home', "homeScreen",
			'/hint', "hintScreen"

		) #The structure of the url and the name of the class to send the request to.
		self.render = web.template.render('templates/') #The file path for HTML templates.

		self.app = web.application(self.urls, globals()) #The application object that needs to be created for the app to run.

	def GET(self):
		DBManager.insertPlayerData(web.ctx.ip)
		playerStateObject = PlayerState()
		return self.render.homeScreen()
	def POST(self):
		playerStateObject = PlayerState()
		action = web.input()
		if action['new'] == 'charScreen':
			raise web.seeother('/char')

class charScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		return self.render.charScreen()
	def POST(self):
		playerStateObject = PlayerState()
		action = web.input()
		if action['Character'] == '1':
			DBManager.insertPlayerCharacterAction(playerStateObject.player_id,action['Character'])
			raise web.seeother('/story')
		elif action['Character'] == '2':
			DBManager.insertPlayerCharacterAction(playerStateObject.player_id,action['Character'])
			raise web.seeother('/story')
		elif action['Character'] == '3':
			DBManager.insertPlayerCharacterAction(playerStateObject.player_id,action['Character'])
			raise web.seeother('/story')

class storyScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		story1,story2,story3 = DBManager.getStoryIDFromDB(playerStateObject.player_id)
		return self.render.storyScreen(DBManager.getCharacterData(playerStateObject.player_id),story1,story2,story3)
	def POST(self):
		playerStateObject = PlayerState()
		action = web.input()
		story1,story2,story3 = DBManager.getStoryIDFromDB(playerStateObject.player_id)
		if action['story'] == story1:
			DBManager.insertPlayerStoryAction(playerStateObject.player_id,action['story'])
			raise web.seeother('/game')
		if action['story'] == story2:
			DBManager.insertPlayerStoryAction(playerStateObject.player_id,action['story'])
			raise web.seeother('/game')
		if action['story'] == story3:
			DBManager.insertPlayerStoryAction(playerStateObject.player_id,action['story'])
			raise web.seeother('/game')

class gameScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		title,text,art,hint = DBManager.getDataFromDBForGameScreen(playerStateObject.player_id)
		return self.render.gameScreen(text,art,"",title)
	def POST(self):
		playerStateObject = PlayerState()
		print web.input()
		if web.input()['home']=='home':
			raise web.seeother('/home')
		else:
			accession= web.input()['home']
			if DBManager.shouldGameEnd(playerStateObject.player_id):
				raise web.seeother('/end')
			else:
				DBManager.insertPlayerStepAction(playerStateObject.player_id,accession)
				if DBManager.checkPlayerStepInput(accession) is True:
					raise web.seeother('/game')
				else:
					raise web.seeother('/hint')

class hintScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		title,text,art,hint = DBManager.getDataFromDBForGameScreen(playerStateObject.player_id)
		return self.render.gameScreen("",art,hint,title)
	def POST(self):
		playerStateObject = PlayerState()
		print web.input()
		if web.input()['home']=='home':
			raise web.seeother('/homeScreen')
		else:
			accession= web.input()['home']
			if DBManager.shouldGameEnd(playerStateObject.player_id):
				raise web.seeother('/end')
			else:
				DBManager.insertPlayerStepAction(playerStateObject.player_id,accession)
				raise web.seeother('/game')

class endScreen:
	def __init__(self):
		self.render = web.template.render('templates/')
	def GET(self):
		playerStateObject = PlayerState()
		return self.render.endScreen()
	def POST(self):
		playerStateObject = PlayerState()
		pass

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
