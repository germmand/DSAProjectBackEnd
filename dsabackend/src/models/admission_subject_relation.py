from dsabackend.src.handlers import db

class AdmissionSubjectRelation(db.Model):
    __tablename__ = 'Admission_Subject_Relations'

    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id'), primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('Admissions.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('Subject_Statuses.id'), nullable=False)

    def __init__(self, subjectid, admissionid, statusid):
        self.subject_id = subjectid
        self.admission_id = admissionid
        self.status_id = statusid
