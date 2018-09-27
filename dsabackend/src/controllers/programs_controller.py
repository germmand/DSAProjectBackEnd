from flask import Blueprint, request, jsonify
from dsabackend.src.models import (
    GraduateProgramModel
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

ProgramsController = Blueprint('ProgramsController', __name__)

@ProgramsController.route('/<int:program_id>', methods=['GET'])
@jwt_required
def get_program_by_id(program_id):
    program = GraduateProgramModel.query.get(program_id)
    
    if program is None:
        return jsonify({
            "error": "El programa '" + str(program_id) + "' no existe."
        }), 404

    # Getting program's subject and making sure that the subjects
    # are sorted by semester ascendantly.
    subjects_program = [subject.serialized for subject in program.subjects]
    subjects_program.sort(key=lambda x: x['subject_semester'], reverse=False)

    # Adding the subjects to the program's serialized dictionary.
    result = program.serialized
    result.update({'subjects': subjects_program})

    return jsonify({
        "program": result
    }), 200
