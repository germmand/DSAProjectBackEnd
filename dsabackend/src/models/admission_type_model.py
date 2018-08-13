from dsabackend.src.handlers import db

class AdmissionTypeModel(db.Model):
    __tablename__ = 'Admission_Types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    
    admissions = db.relationship('AdmissionModel',
        lazy='select',
        backref=db.backref('type', lazy='joined'))

    def __init__(self, name):
        self.type_name = name
