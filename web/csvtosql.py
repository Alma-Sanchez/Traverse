import sqlite3
import csv 

def csv_to_sql():
    connection = sqlite3.connect("test.db") 
    c = connection.cursor()
    c.executescript(""" DROP TABLE IF EXISTS nameoftable; CREATE TABLE nameoftable (ascension REAL, title TEXT, artist TEXT);""") 
    	# So the executescript checks if the table already exists. If it does the old one will be deleted and you'll be able to get a fresh table so you can just push your most recent csv file without ending up with duplicates.
    with open("data.csv") as f: 
        reader = csv.reader(f, delimiter=',') #I'm doing this where there is no header in the csv 
        for row in reader:
            db = [unicode(row[0], "utf8"), unicode(row[1], "utf8"),unicode(row[2], "utf8")]
            c.execute("INSERT INTO nameoftable (ascension, title, artist) VALUES(?, ?, ?)", db)
            connection.commit()
    connection.close()

csv_to_sql()

