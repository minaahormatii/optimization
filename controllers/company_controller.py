from flask import jsonify, request

from db import db
from models.product import Products, product_schema, products_schema
from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object


def add_company():
    post_data = request.form if request.form else request.get_json()

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201

def get_all_companies():
    company_query = db.session.query(Companies).all()

    return jsonify({"message": "companies found", "results": companies_schema.dump(company_query)}), 200

def update_company_by_id(company_id):
    post_data = request.form if request.form else request.get_json()
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company_query:
        populate_object(company_query, post_data)

        db.session.commit()
        return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200
    
    return jsonify({"message": "company not found"}), 404

def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(company_query)}), 200

def delete_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    try:
        db.session.delete(company_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete company"}), 400

    return jsonify({"message": "company deleted"}), 200