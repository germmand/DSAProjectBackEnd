from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager

from dsabackend.src.handlers import db
from dsabackend.config import (
    DbConfig,
    JWTConfig
)
from dsabackend.src.controllers import (
    DefaultController,
    UsersController,
    AuthController,
    RolesController
)

# Creating Flask Application
app = Flask(__name__)

# Registering Application's Blueprints
app.register_blueprint(DefaultController, url_prefix='/')
app.register_blueprint(UsersController, url_prefix='/api/users')
app.register_blueprint(AuthController, url_prefix='/api/auth')
app.register_blueprint(RolesController, url_prefix='/api/roles')

# Adding SQLAlchemy support
app.config['SQLALCHEMY_DATABASE_URI'] = DbConfig.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DbConfig.TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWTConfig.JWT_SECRET
app.config['JWT_BLACKLIST_ENABLED'] = JWTConfig.JWT_BLACKLIST_ENABLED
app.config['JWT_BLACKLIST_TOKENS_CHECKS'] = JWTConfig.JWT_BLACKLIST_TOKENS

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

jwt = JWTManager(app)

# Importing models in order for Alembic to be able to detect upcoming changes to the database's schema when creating migrations.
# DO NOT remove this line.
from dsabackend.src.models import *

# This is done in order to prevent previously invalidated tokens to gain access to protected endpoints.
@jwt.token_in_blacklist_loader
def check_blacklisted_tokens(decrypted_token):
    jti = decrypted_token['jti']
    
    return RevokeTokenModel.is_jti_blacklisted(jti) 

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
        print("Creating types and statuses for admissions and programs...")

        tipo_modular = ProgramTypeModel("Modular")
        tipo_semestral = ProgramTypeModel("Semestral")

        types = [
            tipo_modular,
            tipo_semestral
        ]

        statuses = [
            AdmissionStatusModel("En revisión"),
            AdmissionStatusModel("Aceptada"),
            AdmissionStatusModel("Declinada")
        ]

        subject_statuses = [
            SubjectStatusModel("Cursada"),
            SubjectStatusModel("Cursando"),
            SubjectStatusModel("Por cursar")
        ]

        for type in types:
            if ProgramTypeModel.query.filter_by(type_name=type.type_name).first() is None:
                db.session.add(type)

        for status in statuses:
            if AdmissionStatusModel.query.filter_by(status_name=status.status_name).first() is None:
                db.session.add(status)

        for subject_status in subject_statuses:
            if SubjectStatusModel.query.filter_by(status_name=subject_status.status_name).first() is None:
                db.session.add(subject_status)
        
        print("Types and statuses were starged and are ready to go into the database...")
        print("----------")
        print("Creating areas, graduate programs and subjects...")

        mec_cuantica = SubjectModel("Mecánica Cuántica", 4, 12, 4, 1)
        mec_estadistica = SubjectModel("Mecánica Estadística", 4, 12, 4, 2)
        teoria_dielectricos = SubjectModel("Teoría de Dieléctricos", 4, 12, 4, 3)

        teoria_probabilidad = SubjectModel("Teoría de Probabilidad", 4, 12, 4, 1)
        algebra_lineal = SubjectModel("Álgebra Lineal", 4, 12, 4, 2)
        algebra_multilineal = SubjectModel("Álgebra Multilineal", 4, 12, 4, 3)

        bioquimica = SubjectModel("Bioquímica Avanzada", 4, 12, 4, 1)
        biologia_molecular = SubjectModel("Biología Molecular", 4, 12, 4, 2)
        inmunologia_avanzada = SubjectModel("Inmunología Avanzada", 4, 12, 4, 3)

        postgrado_fisica = GraduateProgramModel("Postgrado en Física", tipo_semestral, [
            mec_cuantica, 
            mec_estadistica, 
            teoria_dielectricos
        ])
        postgrado_matematica = GraduateProgramModel("Postgrado en Matemáticas (Maestría)", tipo_semestral, [
            teoria_probabilidad,
            algebra_lineal,
            algebra_multilineal
        ])
        postgrado_biologia = GraduateProgramModel("Postgrado en Biología Aplicada (Maestría)", tipo_modular, [
            bioquimica,
            biologia_molecular,
            inmunologia_avanzada
        ])

        cs_exactas = AreaModel("Ciencias Exactas y Naturales", [
            postgrado_fisica,
            postgrado_matematica,
            postgrado_biologia
        ])

        teoria_grafos = SubjectModel("Teoría de Grafos", 4, 12, 4, 1)
        redes_neuronales = SubjectModel("Redes Neuronales Artificiales", 4, 12, 4, 2)
        criptografia = SubjectModel("Criptografía", 4, 12, 4, 3)

        robotica = SubjectModel("Robótica", 4, 12, 4, 1)
        sistemas_control = SubjectModel("Sistemas de Control Distribuido", 4, 12, 4, 2)
        instrumentacion = SubjectModel("Instrumentación Inteligente", 4, 12, 4, 3)

        dinamica = SubjectModel("Dinámica Avanzada", 4, 12, 4, 1)
        elasticidad = SubjectModel("Elasticidad", 4, 12, 4, 2)
        ing_materiales = SubjectModel("Ingeniería de Materiales", 4, 12, 4, 3)

        postgrado_comp = GraduateProgramModel("Postgrado en Ingeniería en Computación (Maestría)", tipo_semestral, [
            teoria_grafos,
            redes_neuronales,
            criptografia
        ])
        postgrado_electrica = GraduateProgramModel("Postgrado en Ingeniería Eléctrica (Maestría)", tipo_semestral, [
            robotica,
            sistemas_control,
            instrumentacion
        ])
        postgrado_mecanica = GraduateProgramModel("Postgrado en Ingeniería Mecánica (Maestría)", tipo_semestral, [
            dinamica,
            elasticidad,
            ing_materiales
        ])

        cs_ingenieria = AreaModel("Tecnología y Ciencias de la Ingeniería", [
            postgrado_comp,
            postgrado_electrica,
            postgrado_mecanica
        ])

        cirugia_i = SubjectModel("Cirugía I", 4, 12, 4, 1)
        cirugia_ii = SubjectModel("Cirugía II", 4, 12, 4, 2)
        cirugia_iii = SubjectModel("Cirugía III", 4, 12, 4, 3)

        dermatologia_i = SubjectModel("Dermatología I", 4, 12, 4, 1)
        dermatologia_ii = SubjectModel("Dermatología II", 4, 12, 4, 2)
        dermatologia_iii = SubjectModel("Dermatología III", 4, 12, 4, 3)

        cardiologia_i = SubjectModel("Cardiología I", 4, 12, 4, 1)
        cardiologia_ii = SubjectModel("Cardiología II", 4, 12, 4, 2)
        cardiologia_iii = SubjectModel("Cardiología III", 4, 12, 4, 3)

        postgrado_cirugia = GraduateProgramModel("Postgrado en Cirugía General (Especialización)", tipo_modular, [
            cirugia_i,
            cirugia_ii,
            cirugia_iii,
        ])
        postgrado_dermatologia = GraduateProgramModel("Postgrado en Dermatología (Especialización)", tipo_modular, [
            dermatologia_i,
            dermatologia_ii,
            dermatologia_iii,
        ]) 
        postgrado_cardiologia = GraduateProgramModel("Postgrado en Cardiología (Especialización)", tipo_modular, [
            cardiologia_i,
            cardiologia_ii,
            cardiologia_iii,
        ])

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
        # Here will go the rest of the database seeding while it keeps being developed...

        db.session.commit()
    
        print("----------")
        print("All changes were committed into the database successfully!")
    except Exception as e:
        db.session.rollback()
        
        print("An exception has occurred while seeding the database: \n" + str(e))
