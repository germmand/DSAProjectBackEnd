"""empty message

Revision ID: dd4143402e5f
Revises: 
Create Date: 2018-10-10 19:28:58.398477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd4143402e5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Admission_Statuses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status_name')
    )
    op.create_table('Areas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('area_name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('area_name')
    )
    op.create_table('Degree_Types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('degree_name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('degree_name')
    )
    op.create_table('Program_Types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('Revoke_Tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role_name')
    )
    op.create_table('Subject_Statuses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status_name')
    )
    op.create_table('Graduate_Programs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('program_name', sa.String(length=200), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('degree_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['Areas.id'], ),
    sa.ForeignKeyConstraint(['degree_id'], ['Degree_Types.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['Program_Types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Users',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('fullname', sa.String(length=200), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['Roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Admissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('current_semester', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['program_id'], ['Graduate_Programs.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['Admission_Statuses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Subjects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subject_name', sa.String(length=200), nullable=False),
    sa.Column('subject_credits', sa.Integer(), nullable=False),
    sa.Column('hours_per_week', sa.Integer(), nullable=False),
    sa.Column('amount_of_weeks', sa.Integer(), nullable=False),
    sa.Column('subject_semester', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['program_id'], ['Graduate_Programs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subject_name')
    )
    op.create_table('Admission_Subject_Relations',
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admission_id'], ['Admissions.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['Subject_Statuses.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['Subjects.id'], ),
    sa.PrimaryKeyConstraint('subject_id', 'admission_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Admission_Subject_Relations')
    op.drop_table('Subjects')
    op.drop_table('Admissions')
    op.drop_table('Users')
    op.drop_table('Graduate_Programs')
    op.drop_table('Subject_Statuses')
    op.drop_table('Roles')
    op.drop_table('Revoke_Tokens')
    op.drop_table('Program_Types')
    op.drop_table('Degree_Types')
    op.drop_table('Areas')
    op.drop_table('Admission_Statuses')
    # ### end Alembic commands ###
