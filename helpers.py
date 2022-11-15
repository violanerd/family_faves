import os
import requests
from functools import wraps
from flask import session, redirect, url_for, request
from dotenv import load_dotenv
load_dotenv()

def login_required(f):
   
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def random():
    api_key = os.getenv("api_key")
    app_id = os.getenv("application_id")
    #the f is a string format!
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q=&app_id={app_id}&app_key={api_key}&diet=balanced&random=true"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
    except requests.RequestException:
        return None
    try: 
        recipe = response.json()
        return {
            "url": recipe["hits"][0]['recipe']['url'],
            "name": recipe["hits"][0]['recipe']['label'],
            "img": recipe["hits"][0]['recipe']['image']

        }
    except (KeyError, TypeError, ValueError):
        return None

