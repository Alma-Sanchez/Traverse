import HTTPHandler
import DBManager

server = HTTPHandler.WebpyServer()

if __name__=="__main__":
	server.app.run()