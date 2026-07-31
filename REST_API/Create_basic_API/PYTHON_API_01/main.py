from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable = False)
    country = db.Column(db.String(50), nullable = False)
    rating = db.Column(db.Float, nullable = False)

    def to_dict(self):
        return{
            "id": self.id,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating
        }

with app.app_context():    # create a db context manager
    db.create_all()

#Create Routes
@app.route("/")      # Home page route
def home():
    return "Home page root url connected."



if __name__ == "__main__":
    app.run(debug = True)