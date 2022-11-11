import os
from crypt import methods

from flask import Flask, render_template, request, url_for

from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("mysql_password")
app.config['MYSQL_DATABASE_DB'] = os.getenv("db")
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()




with cursor:
    cursor.execute("SELECT * FROM user WHERE id = 1")
    print(cursor.fetchall())
url_for('static', filename='styles.css')

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
        # return render_template("index.html", name = "name")
        return render_template("index.html", name = cursor.fetchall())

@app.route("/new-recipe")
def new_recipe():
    return render_template("new-recipe.html")

@app.route("/login")
def login():
    return render_template("login.html")

# if __name__ == '__main__':
#     app.run()