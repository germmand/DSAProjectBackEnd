from flask import Blueprint, request, jsonify
from dsabackend.src.models import UserModel, RoleModel
from dsabackend.src.handlers import db

from sqlalchemy.exc import (
    IntegrityError
)

UsersController = Blueprint('UsersController', __name__)

@UsersController.route('/', methods=['GET'])
def get_users():
    page = request.args.get('page', default=0, type=int)
    size = request.args.get('size', default=0, type=int)
  
    users = UserModel.query.order_by(UserModel.id)
    users = users.all() if page <= 0 or size <= 0 else users.paginate(page, size, False).items

    return jsonify(users = [user.serialized for user in users]), 200

@UsersController.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserModel.query.get(user_id)

    if user is None:
        return jsonify({
            "error": "User '" + str(user_id) + "' does not exist."
        }), 404

    return jsonify(user.serialized), 200

@UsersController.route('/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = UserModel.query.get(user_id)

    if user is None:
        return jsonify({
            "error": "User '" + str(user_id) + "' does not exist."
        }), 404

    db.session.delete(user)
    db.sesion.commit()

    return jsonify({
        "message": "User deleted successfully.",
        "user_deleted": user.serialized
    }), 200

@UsersController.route('/', methods=['POST'])
def create_new_user():
    data = request.get_json()
    
    try: 
        user = UserModel(data["email"], data["password"], data["fullname"], data["role_id"])

        db.session.add(user)
        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": str(ke) + " field is missing."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 409
    except Exception as e:
        db.session.rollback() # In case anything was tried to be committed into the database.

        return jsonify({
            "message": "Uh oh! Something went terribly wrong.",
            "error": str(e)
        }), 500
    
    return jsonify({
        "message": "User created successfully.",
        "user_created": user.serialized
    }), 201

@UsersController.route('/<int:user_id>', methods=['PUT'])
def update_user_data(user_id):
    user = UserModel.query.get(user_id)
    data = request.get_json()

    if user is None:
        return jsonify({
            "error": "User '" + str(user_id) + "' does not exist."
        }), 400

    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    if "fullname" in data:
        user.fullname = data["fullname"]

    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
       
    return jsonify({
        "message": "User updated successfully.",
        "user_updated": user.serialized
    }), 200 
