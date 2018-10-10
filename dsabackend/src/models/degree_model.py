from dsabackend.src.handlers import db

class DegreeModel(db.Model):
    __tablename__ = 'Degree_Types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree_name = db.Column(db.String(200), nullable=False, unique=True)

    programs = db.relationship('GraduateProgramModel',
                               lazy='select',
                               backref=db.backref('degree', lazy='joined'))

    def __init__(self, name):
        self.degree_name = name

    def appendPrograms(self, new_programs):
        for program in new_programs:
            self.programs.append(program)

    def __repr__(self):
        return '<DegreeModel %r>' % (self.degree_name)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "degree_name": self.degree_name
        }
