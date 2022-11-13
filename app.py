import os
from crypt import methods

from flask import Flask, render_template, request, url_for
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('family_faves.db')
    conn.row_factory = sqlite3.Row
  
    return conn
#app.secret_key = os.getenv("secret_key")




@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
        
       
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    print(recipes)
    return render_template("index.html", new_recipe=recipes)
    # else:
    #     # return render_template("index.html", name = "name")
    #     return render_template("index.html", name = cursor.fetchall()) this was a test.... 

@app.route("/new-recipe")
def new_recipe():
    return render_template("new-recipe.html")

@app.route("/login")
def login():
    return render_template("login.html")

# if __name__ == '__main__':
#     app.run()

