from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import and_

from dsabackend.src.handlers import db
from dsabackend.config import DbConfig

from dsabackend.src.controllers import (
    DefaultController,
    UsersController
)

# Creating Flask Application
app = Flask(__name__)

# Registering Application's Blueprints
app.register_blueprint(DefaultController, url_prefix='/')
app.register_blueprint(UsersController, url_prefix='/api/users')

# Adding SQLAlchemy support
app.config['SQLALCHEMY_DATABASE_URI'] = DbConfig.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DbConfig.TRACK_MODIFICATIONS
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Importing models in order for Alembic to be able to detect upcoming changes to the database's schema when creating migrations.
# DO NOT remove this line.
from dsabackend.src.models import *

@manager.command
def seed(): 
    try:
        print("Creating roles...")
     
        roles = [
            RoleModel("Administrador"),
            RoleModel("Estudiante"),
            RoleModel("Profesor")
        ]

        for role in roles:
            if RoleModel.query.filter_by(role_name=role.role_name).first() is None:
                db.session.add(role)

        print("Roles were staged and are ready to go into the database...")
        print("----------")
        print("Creating areas, graduate programs and subjects...")

        postgrado_fisica = GraduateProgramModel("Postgrado en Física")
        postgrado_matematica = GraduateProgramModel("Postgrado en Matemáticas (Maestría)")
        postgrado_biologia = GraduateProgramModel("Postgrado en Biología Aplicada (Maestría)")

        cs_exactas = AreaModel("Ciencias Exactas y Naturales", [
            postgrado_fisica,
            postgrado_matematica,
            postgrado_biologia
        ])

        postgrado_comp = GraduateProgramModel("Postgrado en Ingeniería en Computación (Maestría)")
        postgrado_electrica = GraduateProgramModel("Postgrado en Ingeniería Eléctrica (Maestría)")
        postgrado_mecanica = GraduateProgramModel("Postgrado en Ingeniería Mecánica (Maestría)")

        cs_ingenieria = AreaModel("Tecnología y Ciencias de la Ingeniería", [
            postgrado_comp,
            postgrado_electrica,
            postgrado_mecanica
        ])

        postgrado_cirugia = GraduateProgramModel("Postgrado en Cirugía General (Especialización)")
        postgrado_dermatologia = GraduateProgramModel("Postgrado en Dermatología (Especialización)") 
        postgrado_cardiologia = GraduateProgramModel("Postgrado en Cardiología (Especialización)")

        cs_medicas = AreaModel("Tecnología y Ciencias Médicas", [
            postgrado_cirugia,
            postgrado_dermatologia,
            postgrado_cardiologia
        ])

        areas = [
            cs_exactas, 
            cs_ingenieria, 
            cs_medicas
        ]

        for area in areas:
            if AreaModel.query.filter_by(area_name=area.area_name).first() is None:
                db.session.add(area)
        
        print("Areas, programs and subjects were staged and are ready to go into the database...")
        print("----------")
        
        # Here will go the rest of the database seeding while it keeps being developed...

        db.session.commit()
    
        print("----------")
        print("All changes were committed into the database successfully!")
    except Exception as e:
        db.session.rollback()
        
        print("An exception has occurred while seeding the database: \n" + str(e))
