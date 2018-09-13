from flask import Blueprint, jsonify
from dsabackend.src.models import RoleModel
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

RolesController = Blueprint('RolesController', __name__)

# This action will return all roles except the role regarding to admins
@RolesController.route('/', methods=['GET'])
@jwt_required
def get_all_roles():
    db_roles = RoleModel.query.order_by(RoleModel.id) 
    
    roles = [
        role.serialized 
        for role in db_roles.all() 
        if ("admin" not in role.role_name.lower() 
            or
            get_jwt_identity()["role"] is "Administrador" )
    ]

    return jsonify({
        "roles": roles
    }), 200

@RolesController.route('/<string:role_name>', methods=['GET'])
@jwt_required
def get_role_by_name(role_name):
    role = RoleModel.query.filter_by(role_name=role_name).first()

    if role is None:
        return jsonify({
            "error": "El rol '" + role_name + "' no existe."
        }), 404

    return jsonify({
        "role": role.serialized
    }), 200

# Éste endpoint es para el signup.
# Ya que sólo se pueden registrar estudiantes desde ese form.
# Por ende, no contiene jwt_required.
@RolesController.route('/student', methods=['GET'])
def get_student_role():
    role = RoleModel.query.filter_by(role_name='Estudiante').first()

    return jsonify({
        "role": role.serialized
    }), 200

@RolesController.route('/<int:role_id>', methods=['GET'])
@jwt_required
def get_all_users_by_role(role_id):
    db_role = RoleModel.query.filter_by(id=role_id).first()

    if db_role is None:
        return jsonify({
            "error": "El rol '" + str(role_id) + "' no existe."
        }), 404

    users = [user.serialized for user in db_role.users]

    return jsonify({
        "users": users
    }), 200
