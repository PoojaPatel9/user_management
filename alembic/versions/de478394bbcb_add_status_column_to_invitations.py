"""Add status column to invitations

Revision ID: de478394bbcb
Revises: 9fc5eb4c2b88
Create Date: 2025-05-05 03:37:09.216993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de478394bbcb'
down_revision: Union[str, None] = '9fc5eb4c2b88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations', sa.Column('status', sa.String(), nullable=True))
    op.alter_column('invitations', 'inviter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('invitations', 'qr_code_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('invitations', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('invitations', 'accepted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations', sa.Column('accepted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('invitations', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitations', 'qr_code_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('invitations', 'inviter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_column('invitations', 'status')
    # ### end Alembic commands ###
