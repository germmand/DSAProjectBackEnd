from dsabackend.src.handlers import db

class ProgramTypeModel(db.Model):
    __tablename__ = 'Program_Types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    
    programs = db.relationship('GraduateProgramModel',
        lazy='select',
        backref=db.backref('type', lazy='joined'))

    def __init__(self, name):
        self.type_name = name
