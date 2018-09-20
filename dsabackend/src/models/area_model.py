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

    @property
    def serialized(self):
        return {
            "area_id": self.id,
            "area_name": self.area_name,
            "area_programs": [program.serialized for program in self.graduate_programs]
        }

    def __repr__(self):
        return '<AreaModel %r>' % (self.area_name)
