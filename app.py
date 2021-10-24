from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODEIFICATIONS'] = False


# Init Database
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity



# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# Init Schema
Product_schema = ProductSchema()
Products_schema = ProductSchema(many=True)


# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)

    db.session.add(new_product)
    db.session.commit()

    return Product_schema.jsonify(new_product)


# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = Products_schema.dump(all_products)
    return jsonify(result)


# Get Single Product
@app.route('/product/<id>', methods=['GET'])
def single_product(id):
    product = Product.query.get(id)
    return Product_schema.jsonify(product)


# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return Product_schema.jsonify(product)


# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return Product_schema.jsonify(product)




@app.route('/', methods=['GET','POST'])
def get():
    return jsonify({'msg': 'Hello AI World!'})




# Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)




