from dsabackend.src.handlers import db

class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    fullname = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)

    def __init__(self, email, password, fullname, role_identifier):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.role_id = role_identifier

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
