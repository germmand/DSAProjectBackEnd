from dsabackend.src.models import (
    AdmissionStatusModel
)

def get_admission_quantity_by_status(status_name, user):
    try:
        given_status = AdmissionStatusModel.query.filter_by(status_name=status_name).first()
        
        admission_status_quantity = sum([
            1
            for admission in user.admissions
                if admission.status_id == given_status.id
        ])
    except Exception as e:
        raise e

    return admission_status_quantity
