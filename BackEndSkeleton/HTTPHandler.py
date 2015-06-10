import web
import sqlite3
import DBManager

class WebpyServer:
	def __init__(self):

		self.urls = ('/', 'WebpyServer')
		self.app = web.application(self.urls, globals())
		self.render = web.template.render('templates/')

	def GET(self):
		return self.render.main()

	def POST(self):
		return "post"

class PlayerState:
	def __init__(self, character = None, story = None):

		player_ip = DBManager.getIP()

		player_character = DBManager.getCharacter()

		player_story = DBManager.getStory()

		player_current_step = DBManager.getStep()