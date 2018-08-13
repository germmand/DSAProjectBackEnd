from dsabackend.src.handlers import db

class AdmissionStatusModel(db.Model):
    __tablename__ = 'Admission_Statuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(50), nullable=False, unique=True)

    admissions = db.relationship('AdmissionModel',
        lazy='select',
        backref=db.backref('status', lazy='joined'))

    def __init__(self, name):
        self.status_name = name
