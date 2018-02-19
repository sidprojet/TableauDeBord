import sqlite3


class Database():
	"""
		This class is responsible for handling all tasks concerning the
		database.
	"""
	def create_articles():
		"""
			Create table articles in the database if it doesn't exist.
		"""
		db = sqlite3.connect('newspaper_db')
		cursor = db.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			url TEXT, newspaper TEXT, author TEXT, title TEXT, theme TEXT, description TEXT,
			date_published DATE, body TEXT)
		''')
		cursor.close()
		db.commit()
		db.close()

	def insert(url, site, author, title, theme, description, date_published, body):
		"""
			Take in parameters informations about an article that we want to
			insert in the database and insert it.
		"""
		db = sqlite3.connect('newspaper_db')
		cursor = db.cursor()
		cursor.execute('''INSERT INTO articles(url, newspaper, author, title, theme,
			description, date_published, body) VALUES(?,?,?,?,?,?,?, ?)''', [url, site, author,
			title, theme, description, date_published, body])
		cursor.close()
		db.commit()
		db.close()

	def get_id():
		"""
			Return the next id value for the next article that will be created.
		"""
		db = sqlite3.connect('newspaper_db')
		cursor = db.cursor()
		cursor.execute('''SELECT max(id)+1 FROM articles''')
		row = cursor.fetchone()
		cursor.close()
		db.close()
		if row[0] != None:
			return row[0]
		else:
			return 1


Database.create_articles()