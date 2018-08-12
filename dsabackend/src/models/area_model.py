from dsabackend.src.handlers import db

class AreaModel(db.Model):
    __tablename__ = 'Areas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_name = db.Column(db.String(150), unique=True, nullable=False)
    graduate_programs = db.relationship('GraduateProgramModel', 
        lazy='select', 
        backref=db.backref('area', lazy='joined'))

    def __init__(self, name):
        self.area_name = name

    def __init__(self, name, programs):
        self.area_name = name

        for program in programs:
            self.graduate_programs.append(program)

    def __repr__(self):
        return '<AreaModel %r>' % (self.area_name)
