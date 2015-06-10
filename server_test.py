from http.server import *
import time
import urllib.request

hostName = "localhost"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):

    def get_html(self):
        #I was testing some html files inside of this code. I added the html to the repository, if you wanted to try it out
        '''html_file = open("server_text_test.html", "r")
        page = urllib.request.urlopen('http://www.w3schools.com/html/tryit.asp?filename=tryhtml_basic_document')
        text = page.read().decode("utf8")
        for line in html_file:
            self.wfile.write(bytes("%s" % line, "utf-8"))
        html_file.close()'''
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.get_html()
        self.wfile.write(bytes("<html><head><title></title>HELLO</head>", "utf-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<form action=server_text_test.html>","utf-8"))
        self.wfile.write(bytes("<input type=\"text\" name=\"FirstName\"> <br>", "utf-8"))
        self.wfile.write(bytes("<input type=\"submit\" value=\"Submit\">", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))