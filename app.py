"""Pet adoption application."""

import os
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

# Application and DB configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Secret key generation for using flash()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# database connection and creation
connect_db(app)
db.create_all()


@app.route("/")
def cupcake_homepage():
    return render_template("home.html")


@app.route("/api/cupcakes")
def show_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:id>")
def show_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=['POST'])
def add_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:id>", methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def delete_cupcake(id):
    Cupcake.query.filter(Cupcake.id == id).delete()
    db.session.commit()

    return jsonify(message="Deleted")
