"""empty message

Revision ID: b33afb6e0097
Revises: 8c1415fbd10c
Create Date: 2021-02-22 15:44:46.884719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b33afb6e0097'
down_revision = '8c1415fbd10c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('member_id', sa.Integer(), nullable=False))
    op.add_column('tasks', sa.Column('project_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tasks', 'members', ['member_id'], ['id'])
    op.create_foreign_key(None, 'tasks', 'projects', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'project_id')
    op.drop_column('tasks', 'member_id')
    # ### end Alembic commands ###
