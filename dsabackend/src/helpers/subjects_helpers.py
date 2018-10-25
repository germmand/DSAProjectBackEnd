from dsabackend.src.models import AdmissionSubjectRelation
from sqlalchemy import and_

def get_subjects_from_status(admission_id, status):
    subjects = AdmissionSubjectRelation.query.filter(
        and_(AdmissionSubjectRelation.admission_id == admission_id,
             AdmissionSubjectRelation.status_id == status.id)).all()

    return subjects
