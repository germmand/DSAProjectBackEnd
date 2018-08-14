from dsabackend.src.handlers import db

class RevokeTokenModel(db.Model):
    __tablename__ = "Revoke_Tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(250))

    def __init__(self, jti_token):
        self.jti = jti_token

    def add(self):
        try: 
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise e

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()

        return bool(query)
