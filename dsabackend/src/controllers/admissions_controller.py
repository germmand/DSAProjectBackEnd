from flask import Blueprint, request, jsonify
from dsabackend.src.handlers import db
from sqlalchemy.exc import IntegrityError
from dsabackend.src.helpers import get_admission_quantity_by_status
from sqlalchemy import and_

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from dsabackend.src.models import (
    AdmissionModel,
    UserModel,
    AdmissionSubjectRelation,
    AdmissionStatusModel,
    SubjectStatusModel
)

AdmissionsController = Blueprint('AdmissionsController', __name__)

@AdmissionsController.route('/', methods=['POST'])
@jwt_required
def create_admission():
    data = request.get_json()

    try:
        admission_review_id = AdmissionStatusModel.query.filter_by(status_name="En revisión").first().id
        admission_accepted_id = AdmissionStatusModel.query.filter_by(status_name="Aceptada").first().id

        existent_admission = AdmissionModel.query.filter(
            and_(AdmissionModel.user_id==data["user_id"],
                 AdmissionModel.program_id==data["program_id"])).first()

        if existent_admission is not None:
            if (existent_admission.status_id == admission_review_id or
                existent_admission.status_id == admission_accepted_id):
                return jsonify({
                    "error": "El usuario '" + data["user_id"] + "' ya está en el programa '" + str(data["program_id"])
                }), 403

        admission = AdmissionModel(data["user_id"], data["program_id"], admission_review_id)

        db.session.add(admission)
        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: " + str(ke) + " no fue definido."}), 400
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
        "message": "¡El usuario ha cargado su admissión satisfactoriamente!",
        "admission_submitted": admission.serialized
    }), 201

@AdmissionsController.route('/<int:admission_id>/update-subjects', methods=['PATCH'])
@jwt_required
def update_subjects_on_admission(admission_id):
    data = request.get_json()

    try:
        subjects_id = data['subjects_id']
        status_name = data['status_name']

        subject_status = SubjectStatusModel.query.filter_by(status_name=status_name).first()
        if subject_status is None:
            return jsonify({
                "error": "El estado '" + status_name + "' no existe."
            }), 404

        for subject_id in subjects_id:
            admission_subject = AdmissionSubjectRelation.query.filter(
                and_(AdmissionSubjectRelation.subject_id==subject_id,
                     AdmissionSubjectRelation.admission_id==admission_id)).first()
            if admission_subject is None:
                return jsonify({
                    "error": "La asignatura: '" + str(subject_id) + 
                             "' no existe en la admission: '" + str(admission_id) + "'."
                })
            admission_subject.status = subject_status
 
        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: " + str(ke) + " no fue definido."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "Las asignaturas se actualizaron correctamente."
    }), 200
         

@AdmissionsController.route('/', methods=['PATCH'])
@jwt_required
def accept_or_decline_application():
    data = request.get_json()
    user = get_jwt_identity()

    if user["role"] != "Administrador":
        return jsonify({
            "error": "Sólo administradores tienen acceso a este recurso."
        }), 401

    try:
        admission_id = data['admission_id']
        status_name = data['status_name']

        admission = AdmissionModel.query.get(admission_id)
        admission_status = AdmissionStatusModel.query.filter_by(status_name=status_name).first()
        if admission is None:
            return jsonify({"error": "La admissión '" + str(admission_id) + "' no existe."}), 404
        elif admission_status is None:
            return jsonify({"error": "El status '" + status_name + "' no existe."}), 404

        admission.status = admission_status
        if admission_status.status_name == "Aceptada":
            for subject in admission.program.subjects:
                db.session.add(AdmissionSubjectRelation(subject.id, admission.id, 3))

            if (admission.program.type.type_name == "Semestral" and
                admission.current_semester == 0):
                admission.current_semester = 1

        db.session.commit()
    except KeyError as ke:
        return jsonify({"error": "El campo: " + str(ke) + " no fue definido."}), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "¡La admissión se actualizó con éxito!"})

@AdmissionsController.route('/users/<string:user_id>', methods=['GET'])
@jwt_required
def get_admissions_by_user(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return jsonify({"error": "El usuario '" + str(user_id) + "' no existe."}), 404

    admissions = [admission.serialized for admission in user.admissions]

    return jsonify({
        "admissions": admissions
    }), 200

@AdmissionsController.route('/new', methods=['GET'])
@jwt_required
def get_new_admissions():
    user = get_jwt_identity()

    if user["role"] != "Administrador":
        return jsonify({
            "error": "Sólo administradores tienen acceso a este recurso."
        }), 401

    pending_status = AdmissionStatusModel.query.filter_by(status_name="En revisión").first()
    admissions = [{**admission.serialized, **admission.user.serialized, "area": admission.program.area.area_name} 
                  for admission in pending_status.admissions]

    return jsonify({
        "admissions": admissions
    }), 200

@AdmissionsController.route('/statuses/<string:user_id>', methods=['GET'])
@jwt_required
def get_admissions_category(user_id):
    try: 
        user = UserModel.query.get(user_id)
        if user is None:
            return jsonify({
                "error": "El usuario '" + str(user_id) + "' no existe."
            }), 404

        review_status = get_admission_quantity_by_status('En revisión', user)
        accepted_status = get_admission_quantity_by_status('Aceptada', user)
        declined_status = get_admission_quantity_by_status('Declinada', user)
    except IntegrityError as ie:
        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({"error": detailed_extracted_message}), 400
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({
        "review": review_status,
        "accepted": accepted_status,
        "declined": declined_status
    }), 200

@AdmissionsController.route('/update', methods=['PATCH'])
@jwt_required
def update_semesters():
    admissions = AdmissionModel.query.all()

    approved_id = SubjectStatusModel.query.filter_by(status_name="Cursada").first().id

    for admission in admissions:
        # We first find the subjects that the student has approved
        # on his current semester.
        approved_subjects = [
            subject_rel
            for subject_rel in admission.subjects
                if (subject_rel.subject.subject_semester == admission.current_semester
                    and
                    subject_rel.status_id == approved_id)
        ]

        # Then we find how many subjects the program has on the same semester.
        program_semester_subjects = [
            subject
            for subject in admission.program.subjects
                if subject.subject_semester == admission.current_semester
        ]

        # If the quantity of approved subjects by the student on his current semester
        # is equal to the quantity of subjects within the program on that same semester,
        # it means the student has approved all of the subjects, we sum up one to his current semester.
        if len(approved_subjects) == len(program_semester_subjects):
            admission.current_semester += 1

    db.session.commit()
    
    return jsonify({
        "message": "¡Las admissiones se actualizaron correctamente!"
    }), 200
