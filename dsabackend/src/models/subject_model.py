from dsabackend.src.handlers import db

class SubjectModel(db.Model):
    __tablename__ = "Subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(200), nullable=False, unique=True)
    subject_credits = db.Column(db.Integer, nullable=False)
    hours_per_week = db.Column(db.Integer, nullable=False)
    amount_of_weeks = db.Column(db.Integer, nullable=False)
    subject_semester = db.Column(db.Integer, nullable=False)

    program_id = db.Column(db.Integer, db.ForeignKey('Graduate_Programs.id'), nullable=False)

    admissions = db.relationship('AdmissionSubjectRelation',
        lazy='select',
        backref=db.backref('subject', lazy='joined'))

    def __init__(self, name, credits, hours, weeks, semester):
        self.subject_name = name
        self.subject_credits = credits
        self.hours_per_week = hours
        self.amount_of_weeks = weeks
        self.subject_semester = semester
