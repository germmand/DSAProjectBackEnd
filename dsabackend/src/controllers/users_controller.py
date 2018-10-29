from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256
from re import search
from dsabackend.src.models import UserModel, RoleModel
from dsabackend.src.handlers import db

from sqlalchemy.exc import (
    IntegrityError
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

UsersController = Blueprint('UsersController', __name__)

@UsersController.route('/', methods=['GET'])
@jwt_required
def get_users():
    page = request.args.get('page', default=0, type=int)
    size = request.args.get('size', default=0, type=int)
  
    users = UserModel.query.order_by(UserModel.id)
    users = users.all() if page <= 0 or size <= 0 else users.paginate(page, size, False).items

    return jsonify(users = [user.serialized for user in users]), 200

@UsersController.route('/<string:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id):
    user = UserModel.query.get(user_id)

    if user is None:
        return jsonify({
            "error": "El usuario '" + str(user_id) + "' no existe."
        }), 404

    return jsonify(user.serialized), 200

@UsersController.route('/<string:user_id>', methods=['DELETE'])
@jwt_required
def delete_user_by_id(user_id):
    if get_jwt_identity()["role"] != "Administrador":
        return jsonify({
            "error": "Sólo administradores tienen acceso a este recurso." 
        }), 401

    user = UserModel.query.get(user_id)

    if user is None:
        return jsonify({
            "error": "El usuario '" + str(user_id) + "' no existe."
        }), 404

    db.session.delete(user)
    db.sesion.commit()

    return jsonify({
        "message": "Usuario eliminado con éxito.",
        "user_deleted": user.serialized
    }), 200

# Éste endpoint no lleva el decorador jwt_required porque es el que se usa para signup.
@UsersController.route('/', methods=['POST'])
def create_new_user():
    data = request.get_json()
    
    try: 
        if search('^V-\d+$', data["id"]) is None:
            return jsonify({"error": "La cédula tiene que seguir el siguiente formato: V-12345678"}), 400

        role = RoleModel.query.get(data["role_id"])
        if role is None:
            return jsonify({
                "error": "El rol '" + str(data["role_id"]) + "' no existe."
            }), 404

        user = UserModel(data["id"],
                         data["email"], 
                         pbkdf2_sha256.hash(data["password"]), 
                         data["fullname"], 
                         role)

        db.session.add(user)
        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: " + str(ke) + " no fue enviado."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 409
    except Exception as e:
        db.session.rollback() # In case anything was tried to be committed into the database.

        return jsonify({
            "message": "¡Ha ocurrido un error!",
            "error": str(e)
        }), 500
    
    return jsonify({
        "message": "¡Usuario creado con éxito!",
        "user_created": user.serialized
    }), 201

@UsersController.route('/<string:user_id>', methods=['PUT'])
@jwt_required
def update_user_data(user_id):
    user = UserModel.query.get(user_id)
    data = request.get_json()

    if user is None:
        return jsonify({
            "error": "El usuario '" + str(user_id) + "' no existe."
        }), 404

    try:
        if not pbkdf2_sha256.verify(data["password"], user.password):
            return jsonify({
                "error": "La contraseña es incorrecta."
            }), 401 

        user.fullname = data["fullname"]
        user.email = data["email"]
        if "new_password" in data:
            user.password = pbkdf2_sha256.hash(data["new_password"]) 

        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: '" + str(ke) + "' es requerido."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
       
    return jsonify({
        "message": "Datos del usuario actualizados correctamente.",
        "user_updated": user.serialized
    }), 200 
