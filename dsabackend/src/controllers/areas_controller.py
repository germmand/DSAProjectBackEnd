from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from dsabackend.src.handlers import db
from dsabackend.src.models import (
    AreaModel,
    GraduateProgramModel,
    SubjectModel,
    ProgramTypeModel,
    DegreeModel
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

AreasController = Blueprint('AreasController', __name__)

@AreasController.route('/', methods=['GET'])
@jwt_required
def get_areas():
    page = request.args.get('page', default=0, type=int)
    size = request.args.get('size', default=0, type=int)

    areas = AreaModel.query.order_by(AreaModel.id) 
    areas = areas.all() if page <= 0 or size <= 0 else areas.paginate(page, size, False).items

    return jsonify({
        "areas": [area.serialized for area in areas]
    }), 200

@AreasController.route('/<int:area_id>', methods=['GET'])
@jwt_required
def get_areas_by_id(area_id):
    area = AreaModel.query.get(area_id)
    if area is None:
        return jsonify({
            "error": "El area '" + str(area_id) + "' no existe."
        }), 404

    return jsonify({
        "area": area.serialized
    }), 200

@AreasController.route('/', methods=['POST'])
@jwt_required
def create_new_area():
    if get_jwt_identity()["role"] != "Administrador":
        return jsonify({
            "error": "Sólo administradores tienen acceso a este recurso."
        }), 401

    try:
        new_area = AreaModel(request.get_json()["area_name"])

        db.session.add(new_area)
        db.session.commit()
    except KeyError as ke:
        return jsonify({
            "error": "El campo: " + str(ke) + " no fue enviado."
        }), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({
            "error": detailed_extracted_message
        }), 409
    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "¡Ha ocurrido un error!",
            "error": str(e)
        }), 500 

    return jsonify({
        "message": "¡Área creada satisfactoriamente!",
        "area": new_area.serialized
    }), 201

@AreasController.route('/<int:area_id>', methods=['PATCH'])
@jwt_required
def add_program_to_area(area_id):
    if get_jwt_identity()["role"] != "Administrador":
        return jsonify({
            "error": "Sólo administradores tienen acceso a este recurso."
        }), 401

    area = AreaModel.query.get(area_id)
    if area is None:
        return jsonify({
            "error": "El área '" + str(area_id) + "' no existe."
        }), 404

    try:
        programs = request.get_json()["area_programs"]
        for program in programs:
            program_type = ProgramTypeModel.query.get(program["program_type"])
            program_degree = DegreeModel.query.get(program["program_degree"])

            new_program = GraduateProgramModel(program["program_name"], 
                                               program_type,
                                               program_degree)
            subjects = program["program_subjects"]
            
            for subject in subjects:
                new_program.subjects.append(
                    SubjectModel(subject["subject_name"],
                                 subject["subject_credits"],
                                 subject["subject_hours"],
                                 subject["subject_weeks"],
                                 subject["subject_semester"]))

            new_program.area = area
        
        db.session.commit()
    except KeyError as ke:
        return jsonify({
            "error": "El campo: " + str(ke) + " no fue enviado."
        }), 400
    except IntegrityError as ie:
        db.session.rollback()

        detail_msg_index = str(ie).find("DETAIL:")
        detailed_extracted_message = str(ie)[detail_msg_index + 9:str(ie).find("\n", detail_msg_index)]

        return jsonify({
            "error": detailed_extracted_message
        }), 409
    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "¡Ha ocurrido un error!",
            "error": str(e)
        }), 500 

    return jsonify({
        "message": "El área '" + str(area_id) + " fue actualizada con éxito."
    }), 200
