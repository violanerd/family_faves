import os

from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session
import sqlite3
from helpers import login_required, random
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect('family_faves.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?',
                        (username,)).fetchone()
    conn.close()
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
        password = request.form.get("password")
        if not username:
            flash("Please enter a username")
        elif not password:
            flash("Please enter a password")
        else: 
            user = get_user(username)
            
            if user:
                #check password
                if user["password"] != password:
                    flash("Incorrect password")
                else:
                    session["user_id"] = user["id"]
                    return redirect("/")
            else:
                flash("Something went wrong")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not request.form.get("username"):
            flash("Please enter a username")
        elif not request.form.get("password"):
            flash("Please enter a password")
        else: 
            #check if user is in db already
            user = get_user(username)
            if user:
                flash("Username exists already, pick something else")
            else: 
                conn = get_db_connection()
                user = conn.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, password))
                conn.commit()
                conn.close()
                # wanted user to go to dashboard without having to login, call db again to get user id
                user = get_user(username)
                session["user_id"] = user["id"]

                return redirect("/")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/random", methods=["GET", "POST"])
def get_random():
    if request.method=="POST":
        data = random() 
        #error handling
        if data == None:
            flash("Something went wrong on our end")
        else: 
            return render_template("randomdata.html", data=data)
    return render_template("random.html")


