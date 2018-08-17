from flask import Blueprint, request, jsonify
from dsabackend.src.handlers import db
from sqlalchemy.exc import IntegrityError
from dsabackend.src.models import (
    AdmissionModel,
    UserModel,
    AdmissionSubjectRelation
)

AdmissionsController = Blueprint('AdmissionsController', __name__)

@AdmissionsController.route('/', methods=['POST'])
def create_admission():
    data = request.get_json()

    try:
        # The '1' as the third argument means the admission is under review...
        # user_id has to be taken from the token; meanwhile, it's done like this for testing...
        admission = AdmissionModel(data["user_id"], data["program_id"], 1)

        db.session.add(admission)
        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": str(ke) + " field is missing."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({
        "message": "User has submitted his program application successfully!",
        "admission_submitted": admission.serialized
    }), 201

@AdmissionsController.route('/', methods=['PATCH'])
def accept_or_decline_application():
    # Add token validation here...
    # Only administrators can access this endpoint...

    data = request.get_json()

    try:
        admission_id = data['admission_id']
        status_id = data['status_id']

        admission = AdmissionModel.query.get(admission_id)
        if admission is None:
            return jsonify({"error": "admission '" + str(admission_id) + "' does not exist."}), 404

        admission.status_id = status_id
        if status_id == 2:
            admission.current_semester = 1  

        db.session.commit()

        if admission.current_semester == 1:
            for subject in admission.program.subjects:
                db.session.add(AdmissionSubjectRelation(subject.id, admission.id, 3))

        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": str(ke) + " field is missing."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Admission has been updated successfully!"})

@AdmissionsController.route('/users/<int:user_id>', methods=['GET'])
def get_admissions_by_user(user_id):
    # user_id must be taken from the token; but it'll be done like this for testing purposes
    # in the mean time...
    user = UserModel.query.get(user_id)
    if user is None:
        return jsonify({"error": "User '" + user_id + "' does not exist."}), 404

    admissions = [admission.serialized for admission in user.admissions]

    return jsonify({
        "admissions": admissions
    }), 200
