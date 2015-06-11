#Python version 2.7.9
import HTTPHandler #Imports modules needed to run server.py
import DBManager

server = HTTPHandler.WebpyServer() #Creates a new instance of the server.

if __name__=="__main__": #Checks to see if server.py is the main file that is being called. 
	server.app.run() #Runs the server if server.py is the file being called. WILL NOT WORK IF SERVER.PY IS BEING CALLED AS A MODULE.