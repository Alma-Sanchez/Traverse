import web
import sqlite3

urls = ('/','main')
app = web.application(urls, globals(), True)
render=web.template.render('templates/')

connection=sqlite3.connect('test.db')
c=connection.cursor()
sql="SELECT * FROM nameoftable WHERE ascension=?"

def readdata(x):
  for row in c.execute(sql, [(x)]):
		return True
	else:
		return False

class main:
	def GET(self):
		return render.main()

	def POST(self):
		form =  web.input()
		form = form.user
		if readdata(form) == True:
			return "That's correct"
		else:
			return render.incorrect()

 
if __name__ == "__main__":
    app.run()
