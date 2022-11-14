import os
from crypt import methods

from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session
import sqlite3
from helpers import login_required, random


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
                    print(session)
                    for row in session:
                        print(row)
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
        dummy_data = {'url': 'https://familystylefood.com/wheat-berries-tomato-arugula-ricotta/', 'name': 'Wheat Berry Salad with Charred Tomato', 'img': 'https://edamam-product-images.s3.amazonaws.com/web-img/241/2410460e8b1301fa2bd2992c39b1ef8f.jpg?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDVf7v1%2BCvYetkQdvfuaufWLeSYor9lJosdgmw1AasUDwIhAIPeZJ5eklUr7yc6pyG6CJdPShTp6tM2fzX33pwAHPNGKtUECN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMMTg3MDE3MTUwOTg2IgzThLhbXg7dOzMaVyoqqQT33aPc65fSYEKn83okk736%2FSNfJtkwViBbpplBuFrGTvyB1sUlDQwM9ApFGNwecO8eXfY%2FCtnuLrKC4M%2ByKdEknsyKccXPrDE7QZ3WNijIuPMwmQMlfhrzkTjLZaFIl2T7ZBpvb84D8sNZrHrkmwK0hL4dzJTS6k1pQg6LhL%2FUj9GSjB%2BAydH28n4G1C69D1GH6xrehVfvfzpP39euagOMCwupvpHD%2B78Qi%2FF9S1Q2apxPmLYhVyofLwgAxLsM1BDjTJ%2FA33rZoIcngwWeX9RzsF1esBpF12cd%2FDPg%2FiAdgM0Br%2F45ag%2FAlwpA5WmTx7geiplG9mHMPxrG9QCuUgpKaLwMfowpxcZ9NARbchYBHbUtYu8q%2BGPBYBEQV31dLoJW9bE9CXgBG5dxLvoPE1F9i46QzqAP%2FqYYLAqADCLEvcPmoZtXEBbRNUo%2FL3dNroKWU%2FcpfVHKBj4Pr2ug65DLFdfaIagfGsmnWpLPtXW0YCYXiR8ErWZmDW%2FYfomEuyQ%2FcCuFhfwPoLHbDqwhY1zRSftrge9gQu%2F00eD%2Ff3dXz0bxzlTxFHuuSClXDY68lODYlFQycfeBgYe8AdCBTJDKuD4xWcW5y0EuN1aWpOb04u6p4eRTh2QYywnVJeLcMqwG7X2NR%2BnlHnfzBqFclG%2F8SqPcUoXrAEYIMXpXOMQ3aKnqnYI3B2vHcZeML%2BK8P6Dr%2Frsw4BIAIQviXqUtag4sLz4QVpxXcbPsMLjHypsGOqgBOwYfwzaHvYGoFCQYeNI592eOD12IS70W15O4pQNEIuol1Isnud%2B0aqHS3IxFGJK8L1o5zAGmquzdkvgT6mafjQ8ino1kg9iikXbkIwrh2RD2U%2BZn5O9QvM2tMzfMM90RHMAXHJ9WzloIkNV5foBi4yYMdnVPkNHqpyC62fqmmBtRcHZ9XtcW%2BrKiTgTd9%2B86IOHUNJinWFqrkC8S%2FLOuP4AlPoYB5BhA&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221114T213508Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=ASIASXCYXIIFBCE23GPX%2F20221114%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=be352c570d5f6069a4473c4d30c9cdc694bb5f48449cd9574d631edfd67e3ef8'}

        #data=random()
        #print("made it here")
        #print(data)
        return render_template("randomdata.html", data=dummy_data)
    return render_template("random.html")


