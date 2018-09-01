from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from dsabackend.src.models import (
    UserModel, 
    RevokeTokenModel
)

AuthController = Blueprint('AuthController', __name__)

@AuthController.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    try:
        email = data["email"]
        password = data["password"] 

        user = UserModel.query.filter_by(email=email).first()
        if user is None:
            return jsonify({"error": "Credentials provided are incorrect."}), 401
        
        if not pbkdf2_sha256.verify(password, user.password):
            return jsonify({"error": "Credentials provided are incorrect."}), 401 

        access_token = create_access_token(identity=user.serialized)
        refresh_token = create_refresh_token(identity=user.serialized)
    except KeyError as ke:
        return jsonify({"error": str(ke) + " field is missing."}), 400

    return jsonify({
        "message": "Logged in successfully!",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.serialized
    })

@AuthController.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh_access_token():
    current_user = get_jwt_identity()
    jti = get_raw_jwt()['jti']

    # We revoke refresh token, since it can only be used once.
    # And then we generate a new one along with an access token.
    try:
        revoke_token = RevokeTokenModel(jti)
        revoke_token.add()
    except Exception as e:
        return jsonify({ 
            "message": "An error has occurred!",
            "error": str(e)
        })

    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)

    return jsonify({
        "message": "Both access token and refresh token has been refreshed.",
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@AuthController.route('/access/logout', methods=['GET'])
@jwt_required
def access_token_logout():
    jti = get_raw_jwt()['jti']
    
    try:
        revoke_token = RevokeTokenModel(jti)
        revoke_token.add()
    except Exception as e:
        return jsonify({
            "message": "An error has occurred!",
            "error": str(e)
        })

    return jsonify({
        "message": "Access token has been revoked successfully!"
    })

@AuthController.route('/refresh/logout', methods=['GET'])
@jwt_refresh_token_required
def refresh_token_logout():
    jti = get_raw_jwt()['jti']
    
    try:
        revoke_token = RevokeTokenModel(jti)
        revoke_token.add() 
    except Exception as e:
        return jsonify({
            "message": "An error has occurred!",
            "error": str(e)
        })

    return jsonify({
        "message": "Refresh token has been revoked successfully!"
    })
