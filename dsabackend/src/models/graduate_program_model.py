from dsabackend.src.handlers import db

class GraduateProgramModel(db.Model):
    __tablename__ = 'Graduate_Programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_name = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('Areas.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('Program_Types.id'), nullable=False)

    subjects = db.relationship('SubjectModel',
        lazy='select',
        backref=db.backref('program', lazy='joined'))

    admissions = db.relationship('AdmissionModel',
        lazy='select',
        backref=db.backref('program', lazy='joined'))

    def __init__(self, name, type):
        self.program_name = name
        self.type_id = type

    @property
    def serialized(self):
        return {
            "program_id": self.id,
            "program_name": self.program_name,
            "area_id": self.area_id,
            "type_name": self.type.type_name
        }

    def __repr__(self):
        return '<GraduateProgramModel %r>' % (self.program_name)
