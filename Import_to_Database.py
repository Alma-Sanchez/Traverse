#used Python 2.7.9

import sqlite3
import csv


conn = sqlite3.connect("SAAM_database_test6.db")

c = conn.cursor()

def import_Story_ID():
	with open('Story_Data.csv', 'r') as Story_Data:
		reader = csv.DictReader(Story_Data)
		for row in reader:
			return row['Story_ID']
	conn.close()

def import_Character_ID():
	with open('Story_Data.csv', 'r') as Story_Data:
		reader = csv.DictReader(Story_Data)
		for row in reader:
			return row['Character_ID']
	conn.close()

def import_Title_of_Story():
	with open('Story_Data.csv', 'r') as Story_Data:
		reader = csv.DictReader(Story_Data)
		for row in reader:
			return row['Title_of_story']
	conn.close()

def import_Number_or_Steps():
	with open('Story_Data.csv', 'r') as Story_Data:
		reader = csv.DictReader(Story_Data)
		for row in reader:
			return row['Number_or_Steps']
	conn.close()
		

def import_to_database():
	c.execute("INSERT INTO Character_Data (Story_ID, Character_ID, Number_or_Steps, Title_of_story) VALUES (?,?,?,?)", 
		(import_Story_ID(), import_Character_ID(), import_Title_of_Story(), import_Number_or_Steps()))
	conn.commit()


import_to_database()








with open('Story_Data.csv') as Story_Data:
	reader = csv.DictReader(Story_Data)
	for row in reader:
		print row['Story_ID'], row['Character_ID'], row['Title_of_story'], row['Number_or_Steps']

def read_cell(x,y):
	with open('Story_Data.csv', 'r') as Story_Data:
		reader = csv.reader(Story_Data)
		y_count = 0
		for n in reader:
			if y_count == y:
				cell = n[x]
				return cell
			y_count += 1