from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from dsabackend.src.handlers import db
from dsabackend.src.models import (
    AdmissionSubjectRelation,
    AdmissionModel,
    SubjectStatusModel
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from dsabackend.src.helpers import get_subjects_from_status

SubjectsController = Blueprint('SubjectsController', __name__)

@SubjectsController.route('/', methods=['PUT'])
@jwt_required
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
                "error": "La asignatura '" + str(subject_id) + "' en la admissión '" + str(admission_id) + "' no existe."
            }), 404
        
        subject_admission.status_id = status_id

        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: " + str(ke) + " no fue enviado."}), 400        
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "La asignatura para la admissión '" + str(admission_id) + "' se ha actualizado con éxito."}), 200

@SubjectsController.route('/all/<int:admission_id>', methods=['GET'])
@jwt_required
def get_all_subjects(admission_id):
    taken_status = SubjectStatusModel.query.filter_by(status_name='Cursada').first()
    taking_status = SubjectStatusModel.query.filter_by(status_name='Cursando').first()
    willtake_status = SubjectStatusModel.query.filter_by(status_name='Por cursar').first()

    taken_subjects = get_subjects_from_status(admission_id, taken_status)
    taking_subjects = get_subjects_from_status(admission_id, taking_status)
    willtake_subjects = get_subjects_from_status(admission_id, willtake_status)
      
    taken_subjects_serialized = [subject.serialized for subject in taken_subjects]
    taking_subjects_serialized = [subject.serialized for subject in taking_subjects]
    willtake_subjects_serialized = [subject.serialized for subject in willtake_subjects]

    subjects = {
        "taken_subjects": taken_subjects_serialized,
        "taking_subjects": taking_subjects_serialized,
        "willtake_subjects": willtake_subjects_serialized
    }

    return jsonify(subjects), 200

@SubjectsController.route('/', methods=['GET'])
@jwt_required
def get_subjects_by_status():
    admission_id = request.args.get('admission', default=0, type=int)
    status_id = request.args.get('status', default=0, type=int)

    if status_id != 0:
        subjects = AdmissionSubjectRelation.query.filter(
            and_(AdmissionSubjectRelation.admission_id == admission_id,
                 AdmissionSubjectRelation.status_id == status_id)).all()
    else:
        subjects = AdmissionSubjectRelation.query.filter_by(admission_id=admission_id).all()
    
    serialized_result = [subject.serialized for subject in subjects]

    return jsonify({"subjects": serialized_result}), 200 

@SubjectsController.route('/<int:admission_id>', methods=['GET'])
@jwt_required
def get_subjects_to_signup(admission_id):
    admission = AdmissionModel.query.get(admission_id)

    if admission is None:
        return jsonify({"error": "La admissión '" + str(admission_id) + "' no existe."}), 404

    status_id = SubjectStatusModel.query.filter_by(status_name="Por cursar").first().id

    subjects = [
        subject_admission.subject.serialized 
        for subject_admission in admission.subjects 
            if (subject_admission.subject.subject_semester == admission.current_semester 
                and
                subject_admission.status_id == status_id)
    ]
    
    return jsonify({"subjects": subjects}), 200
