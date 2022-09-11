from crypt import methods
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

#url_for('static', filename='styles.css')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        new_recipe = {
            "name" : request.form.get("recipe-title"),
            "url" : request.form.get("recipe-url"),
            "description" : request.form.get("recipe-description"),
            "user" : request.form.get("user")
        }
        #name = request.form.get("recipe-title")
        #url = request.form.get("recipe-url")
        #description = request.form.get("recipe-description")
        #user = request.form.get("user")
        return render_template("index.html", new_recipe=new_recipe)
    else:
        return render_template("index.html", name = "not post")

@app.route("/new-recipe")
def new_recipe():
    return render_template("new-recipe.html")

