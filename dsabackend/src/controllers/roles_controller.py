from flask import Blueprint, jsonify
from dsabackend.src.models import RoleModel

RolesController = Blueprint('RolesController', __name__)

# This action will return all roles except the role regarding to admins
@RolesController.route('/', methods=['GET'])
def get_all_roles():
    db_roles = RoleModel.query.order_by(RoleModel.id) 
    
    roles = [role.serialized for role in db_roles.all() if "admin" not in role.role_name.lower()]

    return jsonify({
        "roles": roles
    }), 200

@RolesController.route('/<int:user_id>', methods=['GET'])
def get_all_users_by_role(user_id):
    db_role = RoleModel.query.filter_by(id=user_id).first()

    if db_role is None:
        return jsonify({
            "error": "User '" + str(user_id) + "' does not exist."
        }), 404

    users = [user.serialized for user in db_role.users]

    return jsonify({
        "users": users
    }), 200
