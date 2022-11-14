import os
from crypt import methods

from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
import sqlite3
from helpers import login_required


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('family_faves.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?',
                        (username,)).fetchone()
    conn.close()
    # if user is None:
    #     flash("Something went wrong")
    return user

app.secret_key = os.getenv("secret_key")




@app.route("/")
@login_required
def index():      
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    
    return render_template("index.html", new_recipe=recipes)

@app.route("/new-recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        recipe_title = request.form.get("recipe-title")
        url = request.form.get("recipe-url")
        description = request.form.get('recipe-description')
        name = request.form.get('user')
        if not recipe_title:
            flash("Make sure to enter a title")
        elif not description:
            flash("Make sure to describe your recipe!")
        elif not name:
            flash("Please enter your name")
        else:  
            conn = get_db_connection()
            conn.execute('INSERT INTO recipes (recipe_title, url, description, name) VALUES (?, ?, ?, ?)',
                            (recipe_title, url, description, name))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    return render_template("new-recipe.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not request.form.get("username"):
            flash("Please enter a username")
        elif not request.form.get("password"):
            flash("Please enter a password")
        else: 
            user = get_user(username)
            if user:
                for row in user:
                    print(row)
                session["user_id"] = user["id"]
                print(session)
                return redirect("/")
            else:
                flash("Something went wrong")
    return render_template("login.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():



    return render_template("signup.html")
@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")
# if __name__ == '__main__':
#     app.run()

