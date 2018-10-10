from dsabackend.src.handlers import db

class GraduateProgramModel(db.Model):
    __tablename__ = 'Graduate_Programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_name = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('Areas.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('Program_Types.id'), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('Degree_Types.id'), nullable=False)

    subjects = db.relationship('SubjectModel',
        lazy='select',
        backref=db.backref('program', lazy='joined'))

    admissions = db.relationship('AdmissionModel',
        lazy='select',
        backref=db.backref('program', lazy='joined'))

    def __init__(self, name, program_type, program_degree):
        self.program_name = name
        
        # These variables exist because of the backref of their relational tables.
        self.type = program_type
        self.degree = program_degree

    def appendSubjects(self, new_subjects):
        for subject in new_subjects:
            self.subjects.append(subject) 

    @property
    def serialized(self):
        return {
            "program_id": self.id,
            "program_name": self.program_name,
            "area_id": self.area_id,
            "area_name": self.area.area_name,
            "type_name": self.type.type_name,
            "degree_type": self.degree.degree_name
        }

    def __repr__(self):
        return '<GraduateProgramModel %r>' % (self.program_name)
