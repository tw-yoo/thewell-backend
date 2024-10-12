"""Auto revision

Revision ID: 5c2c4490af4f
Revises: 640fd2a84f43
Create Date: 2024-09-11 12:36:10.258921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5c2c4490af4f'
down_revision: Union[str, None] = '640fd2a84f43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('questions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('answer', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('student', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.Column('image_small', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='questions_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    # ### end Alembic commands ###
