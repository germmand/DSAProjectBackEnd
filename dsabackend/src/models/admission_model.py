from dsabackend.src.handlers import db

class AdmissionModel(db.Model):
    __tablename__ = 'Admissions'

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)    
    program_id = db.Column(db.Integer, db.ForeignKey('Graduate_Programs.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('Admission_Statuses.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('Admission_Types.id'), nullable=False)

    def __init__(self, userid, programid, statusid, typeid):
        self.user_id = userid
        self.program_id = programid
        self.status_id = statusid
        self.type_id = typeid
