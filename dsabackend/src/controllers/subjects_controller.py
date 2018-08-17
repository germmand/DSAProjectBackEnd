from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from dsabackend.src.handlers import db
from dsabackend.src.models import (
    AdmissionSubjectRelation
)

SubjectsController = Blueprint('SubjectsController', __name__)

@SubjectsController.route('/', methods=['PUT'])
def update_subject_on_admission():
    data = request.get_json()

    try:
        admission_id = data["admission_id"]
        subject_id = data["subject_id"]
        status_id = data["status_id"]

        subject_admission = AdmissionSubjectRelation.query.filter(
            and_(AdmissionSubjectRelation.subject_id == subject_id,
                 AdmissionSubjectRelation.admission_id == admission_id)).first()

        if subject_admission is None:
            return jsonify({
                "error": "Subject '" + str(subject_id) + "' on Admission '" + str(admission_id) + "' does not exist."
            }), 404
        
        subject_admission.status_id = status_id

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

    return jsonify({
        "message": "Subject for admission '" + str(admission_id) + "' has been updated successfully."}), 200

@SubjectsController.route('/', methods=['GET'])
def get_subjects_by_status():
    admission_id = request.args.get('admission', default=0, type=int)
    status_id = request.args.get('status', default=0, type=int)

    subjects = AdmissionSubjectRelation.query.filter(
        and_(AdmissionSubjectRelation.admission_id == admission_id,
             AdmissionSubjectRelation.status_id == status_id)).all()
    
    serialized_result = [subject.serialized for subject in subjects]

    return jsonify({"subjects": serialized_result}), 200 
