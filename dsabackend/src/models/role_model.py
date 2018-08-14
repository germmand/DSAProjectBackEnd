from dsabackend.src.handlers import db

class RoleModel(db.Model):
    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('UserModel', lazy='select', backref=db.backref('role', lazy='joined'))

    def __init__(self, name):
        self.role_name = name

    def __repr__(self):
        return '<RoleModel %r>' % (self.role_name)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.role_name
        }
