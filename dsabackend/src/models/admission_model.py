from dsabackend.src.handlers import db

class AdmissionModel(db.Model):
    __tablename__ = 'Admissions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), db.ForeignKey('Users.id'), nullable=False)    
    program_id = db.Column(db.Integer, db.ForeignKey('Graduate_Programs.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('Admission_Statuses.id'), nullable=False)
    current_semester = db.Column(db.Integer, nullable=False)

    subjects = db.relationship('AdmissionSubjectRelation',
                                lazy='select',
                                backref=db.backref('admission', lazy='joined'))

    def __init__(self, userid, programid, statusid):
        self.user_id = userid
        self.program_id = programid
        self.status_id = statusid
        self.current_semester = 0

    @property
    def serialized(self):
        return {
            "admission_id": self.id,
            "user_email": self.user.email,
            "program_name": self.program.program_name,
            "status": self.status.status_name,
            "current_semester": self.current_semester,
            "type": self.program.type.type_name
        }
