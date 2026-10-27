from flask import jsonify, request

from db import db
from models.category import Categories
from models.company import Companies
from models.product import Products, product_schema, products_schema
from util.reflection import populate_object


def add_product():
    post_data = request.form if request.form else request.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201

def create_product_category():
    post_data = request.form if request.form else request.json

    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query and category_query:
        product_query.categories.append(category_query)
        db.session.commit()

    return jsonify({"message": "category added to product", "result": product_schema.dump(product_query)}), 200

def get_all_products():
    products_query = db.session.query(Products).all()

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200

def get_active_products():
    products_query = db.session.query(Products).filter(Products.active == True).all()

    return jsonify({"message": "active products found", "results": products_schema.dump(products_query)}), 200

def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_query:
        populate_object(product_query, post_data)

        db.session.commit()
        return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200

    return jsonify({"message": "product not found"}), 404

def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "result": product_schema.dump(product_query)}), 200

def get_products_by_company(company_id):
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200

def delete_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product does not exist"}), 404

    try:
        db.session.delete(product_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete product"}), 400

    return jsonify({"message": "product deleted"}), 200



  
