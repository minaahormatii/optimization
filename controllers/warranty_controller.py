from flask import jsonify, request

from db import db
from models.product import Products
from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object

def add_warranty():
    post_data = request.form if request.form else request.json

    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)

    db.session.add(new_warranty)
    db.session.commit()

    return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201

def get_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200

def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if warranty_query:
        populate_object(warranty_query, post_data)

        db.session.commit()
        return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200

    return jsonify({"message": "warranty not found"}), 404

def delete_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    try:
        db.session.delete(warranty_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400

    return jsonify({"message": "warranty deleted"}), 200