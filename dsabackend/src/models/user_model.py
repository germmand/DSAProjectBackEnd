from dsabackend.src.handlers import db

class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    fullname = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)

    admissions = db.relationship('AdmissionModel',
        lazy='select',
        backref=db.backref('user', lazy='joined'))

    def __init__(self, id, email, password, fullname, user_role):
        self.id = id
        self.email = email
        self.password = password
        self.fullname = fullname

        # This field exist because of the backref of its relational table.
        self.role = user_role

    def __repr__(self):
        return '<UserModel %r>' % (self.email)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "role": self.role.role_name
        }
