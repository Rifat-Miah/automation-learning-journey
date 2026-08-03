from flask import Flask, jsonify, request
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
    return jsonify({"message": "Welcome to the RIFAT Travel API."})

@app.route("/destinations", methods = ["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

@app.route("/destinations/<int:destination_id>", methods = ["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination Not Found!"}), 404

#POST
@app.route("/destinations", methods = "POST")
def add_destination():
    data = request.get_json()  # parse

    new_destination = Destination(destination = data["destination"],
                                  contry = data["country"],
                                  rating = data["rating"])
    db.session.add(new_destination)    # insert new object
    db.session.commit()

    return jsonify(new_destination.to_dict()), 201

# PUT (Update)
@app.route("destinations/<int:destination_id>", methods = ["PUT"])
def update_destination(destination_id):
    data = request.get_json()

    destination = Destination.query.get(destination_id)
    if destination:
        destination.destination = data.get("destination", destination.destination)   # create properties use dot ( . )
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)

        db.session.commit()
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination  not Found."}), 404

if __name__ == "__main__":
    app.run(debug = True)