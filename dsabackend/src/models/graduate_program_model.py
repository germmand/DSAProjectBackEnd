from dsabackend.src.handlers import db

class GraduateProgramModel(db.Model):
    __tablename__ = 'Graduate_Programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_name = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('Areas.id'), nullable=False)

    def __init__(self, name):
        self.program_name = name

    def __repr__(self):
        return '<GraduateProgramModel %r>' % (self.program_name)
