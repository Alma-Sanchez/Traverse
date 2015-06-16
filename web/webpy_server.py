import web
import sqlite3

urls = ('/','main')
app = web.application(urls, globals(), True)
render=web.template.render('templates')

def readdata(x):
	connection=sqlite3.connect('test.db',check_same_thread=False)
	c=connection.cursor()
	sql="SELECT * FROM nameoftable WHERE ascension=?"
	for row in c.execute(sql, [(x)]):
		return True
	else:
		return False
		
def checkip(x):
	ipcon=sqlite3.connect('ip.db',  check_same_thread=False)
	ipc=ipcon.cursor()
	ipsql="SELECT * FROM iptable WHERE ip=?"
	for row in ipc.execute(ipsql, [(x)]):
		return True
	else:
		ipc.execute("INSERT INTO iptable VALUES('127.0.0.1')")
		ipcon.commit()
		return True

class main:
	def GET(self):
		if checkip(web.ctx.environ['REMOTE_ADDR'])==True:
			return render.home()
		else:
			return render.home()

	def POST(self):
		action=web.input()
		if action.home=="new":
			return render.character()
		elif action.character=="character1":
			return render.story()
		else:
			pass
		#	characteraction=web.input()
		#	if characteraction.character=="character1":
		#		return render.story()
		#		storyaction=web.input()
		#		if storyaction=="story1" or "story2" or "story3":
		#			return render.test()
		#	else:
		#		pass
		#else:
		#	pass
#		if action.home=="load":
#			pass
#		if action.home=="about":
#			pass
#		if action.home=="help":
#			pass
#		if action.main=="home":
#			return render.home()
#		elif action.main=="navigation":
#			return render.incorrect()
#		elif readdata(action.accession)==True:
#			return render.correct()
#		else:
#			pass

 
if __name__ == "__main__":
    app.run()
