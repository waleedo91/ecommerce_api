import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, String, Column, select, DateTime
from typing import List

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:mypassword1234@localhost/ecommerce_api"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("product_id", ForeignKey('products.id'))
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    customer: Mapped[int] = mapped_column(ForeignKey("users.id"))
    products: Mapped[List['Product']] = relationship(
        secondary=order_product, back_populates='orders')


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] = mapped_column()

    orders: Mapped[List["Order"]] = relationship(
        secondary=order_product, back_populates="products"
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# TODO:  User Endpoints

# GET /users: Retrieve all users

@app.route('/users', method=['GET'])
def get_users():
    pass

# GET /users/<id>: Retrieve a user by ID


@app.route('/users/<int:user_id>', method=['GET'])
def get_single_user(user_id):
    pass

# POST /users: Create a new user


@app.route('/users', method=['POST'])
def create_user():
    pass

# PUT /users/<id>: Update a user by ID


@app.route('/users/<int:user_id>', method=['PUT'])
def update_user(user_id):
    pass

# DELETE /users/<id>: Delete a user by ID


@app.route('/user/<int:user_id>', method=['DELETE'])
def delete_user(user_id):
    pass


# ===================================================

# TODO: Product Endpoints
# GET /products: Retrieve all products
# GET /products/<id>: Retrieve a product by ID
# POST /products: Create a new product
# PUT /products/<id>: Update a product by ID
# DELETE /products/<id>: Delete a product by ID

# ======================================================

# TODO: Order Endpoints
# POST /orders: Create a new order (requires user ID and order date)
# GET /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)
# DELETE /orders/<order_id>/remove_product: Remove a product from an order
# GET /orders/user/<user_id>: Get all orders for a user
# GET /orders/<order_id>/products: Get all products for an order


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
