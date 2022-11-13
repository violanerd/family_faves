import os
from crypt import methods

from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('family_faves.db')
    conn.row_factory = sqlite3.Row
  
    return conn
app.secret_key = os.getenv("secret_key")




@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
        
       
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    
    return render_template("index.html", new_recipe=recipes)
    # else:
    #     # return render_template("index.html", name = "name")
    #     return render_template("index.html", name = cursor.fetchall()) this was a test.... 

@app.route("/new-recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        recipe_title = request.form.get("recipe-title")
        url = request.form.get("recipe-url")
        description = request.form.get('recipe-description')
        name = request.form.get('user')
        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (recipe_title, url, description, name) VALUES (?, ?, ?, ?)',
                         (recipe_title, url, description, name))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("new-recipe.html")

@app.route("/login")
def login():
    return render_template("login.html")

# if __name__ == '__main__':
#     app.run()

