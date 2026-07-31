from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Create Database

#Create Routes
@app.route("/")      # Home page route
def home():
    return "Home page root url connected."



if __name__ == "__main__":
    app.run(debug = True)