import web
# import sqlite3

urls = (
    '/','index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

# connection=sqlite3.connect('test.db')
# c=connection.cursor()
# sql="SELECT * FROM nameoftable WHERE ascension=?"

# def readdata(x):
#   for row in c.execute(sql, [(x)]):
#       return True
#   else:
#       return False

class index:
    def GET(self):
        $def with (name)
        #renders the html file
        # return render.mainScreen()
        # return render.charScreen()
        # return render.storyScreen()
        return render.gameScreen(name = "Hello World!")
        


#   def POST(self):
        # form =  web.input()
        # form = form.user

 
if __name__ == "__main__": 
    app.run()