# wsgi.py
import os
import logging
from flask import Flask, jsonify, request

from config import Config

#logging.warn(os.environ["DUMMY"])

app = Flask(__name__)

app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products', methods=['GET'])
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<id>', methods=['GET'])
def product_read(id):
    product = db.session.query(Product).get(id)
    print(type(product), flush=True)
    return product_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def product_create():
    #json = request.get_json("name")
    product_name = request.form.get('name')
    product_desc = request.form.get('description')
    product = Product(name=product_name, description=product_desc)
    db.session.add(product)
    db.session.commit()
    return "", 201

@app.route('/products/<id>', methods=['PATCH'])
def product_update(id):
    #json = request.get_json("name")
    product_name = request.form.get('name')
    product_desc = request.form.get('description')
    product = db.session.query(Product).filter_by(id=id).first()
    print(product, flush=True)
    product.name = product_name
    product.description = product_desc
    db.session.commit()
    return "", 201

@app.route('/products/<id>', methods=['DELETE'])
def product_delete(id):
    #json = request.get_json("name")
    product = db.session.query(Product).filter_by(id=id).first()
    print(product, flush=True)
    db.session.delete(product)
    db.session.commit()
    return "", 201

