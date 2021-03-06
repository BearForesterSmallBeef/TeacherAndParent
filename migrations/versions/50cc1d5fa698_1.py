"""1

Revision ID: 50cc1d5fa698
Revises: 
Create Date: 2022-03-22 23:52:43.487160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50cc1d5fa698'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classes_id'), 'classes', ['id'], unique=False)
    op.create_table('objects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objects_id'), 'objects', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_hashed_password'), 'users', ['hashed_password'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index(op.f('ix_users_role_id'), 'users', ['role_id'], unique=False)
    op.create_index(op.f('ix_users_surname'), 'users', ['surname'], unique=False)
    op.create_table('consultations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('consultation_start_time', sa.DateTime(), nullable=True),
    sa.Column('consultation_finish_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consultations_id'), 'consultations', ['id'], unique=False)
    op.create_index(op.f('ix_consultations_parent_id'), 'consultations', ['parent_id'], unique=False)
    op.create_index(op.f('ix_consultations_teacher_id'), 'consultations', ['teacher_id'], unique=False)
    op.create_table('parents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parents_class_id'), 'parents', ['class_id'], unique=False)
    op.create_index(op.f('ix_parents_id'), 'parents', ['id'], unique=False)
    op.create_index(op.f('ix_parents_parent_id'), 'parents', ['parent_id'], unique=False)
    op.create_table('teachers&objects&classes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('object_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['object_id'], ['objects.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers&objects&classes_class_id'), 'teachers&objects&classes', ['class_id'], unique=False)
    op.create_index(op.f('ix_teachers&objects&classes_id'), 'teachers&objects&classes', ['id'], unique=False)
    op.create_index(op.f('ix_teachers&objects&classes_object_id'), 'teachers&objects&classes', ['object_id'], unique=False)
    op.create_index(op.f('ix_teachers&objects&classes_teacher_id'), 'teachers&objects&classes', ['teacher_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_teachers&objects&classes_teacher_id'), table_name='teachers&objects&classes')
    op.drop_index(op.f('ix_teachers&objects&classes_object_id'), table_name='teachers&objects&classes')
    op.drop_index(op.f('ix_teachers&objects&classes_id'), table_name='teachers&objects&classes')
    op.drop_index(op.f('ix_teachers&objects&classes_class_id'), table_name='teachers&objects&classes')
    op.drop_table('teachers&objects&classes')
    op.drop_index(op.f('ix_parents_parent_id'), table_name='parents')
    op.drop_index(op.f('ix_parents_id'), table_name='parents')
    op.drop_index(op.f('ix_parents_class_id'), table_name='parents')
    op.drop_table('parents')
    op.drop_index(op.f('ix_consultations_teacher_id'), table_name='consultations')
    op.drop_index(op.f('ix_consultations_parent_id'), table_name='consultations')
    op.drop_index(op.f('ix_consultations_id'), table_name='consultations')
    op.drop_table('consultations')
    op.drop_index(op.f('ix_users_surname'), table_name='users')
    op.drop_index(op.f('ix_users_role_id'), table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_hashed_password'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_objects_id'), table_name='objects')
    op.drop_table('objects')
    op.drop_index(op.f('ix_classes_id'), table_name='classes')
    op.drop_table('classes')
    # ### end Alembic commands ###
