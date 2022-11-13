import sqlite3

connection = sqlite3.connect('family_faves.db')


with open('model/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("maddy", "password"))
cur.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("rachel", "password"))
            

cur.execute("INSERT INTO recipes (recipe_title, url, description, name) VALUES (?, ?, ?, ?)",
            ("Banana Bread", "http://www.google.com", "Better than mom's, don't tell!", "the kids")
            )
cur.execute("INSERT INTO recipes (recipe_title, url, description, name) VALUES (?, ?, ?, ?)",
            ("Pizza", "http://www.google.com", "Mushroom, sausage and cheese", "Dad"))

cur.execute("INSERT INTO recipes (recipe_title, url, description, name) VALUES (?, ?, ?, ?)",
            ("Enchiladas", "http://www.google.com", "Vegan, sweet potato and black bean", "Stacy"))

connection.commit()
connection.close()