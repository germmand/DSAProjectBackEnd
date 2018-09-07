from dsabackend.src.handlers import db

class SubjectStatusModel(db.Model):
    __tablename__ = "Subject_Statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(50), unique=True, nullable=False)

    admission_subjects = db.relationship('AdmissionSubjectRelation',
        lazy='select',
        backref=db.backref('status', lazy='joined'))

    def __init__(self, name):
        self.status_name = name

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.status_name
        }
