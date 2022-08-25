"""create run table

Revision ID: b9b654b23fa4
Revises: f3b1ccf09396
Create Date: 2022-08-16 13:54:33.441580

"""

import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b9b654b23fa4'
down_revision = 'f3b1ccf09396'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'run',
        sa.Column('id', UUID(as_uuid=True),
                  primary_key=True, default=uuid.uuid4, unique=True),
        sa.Column('model_name', sa.String(150), sa.ForeignKey(
            'model.name'), nullable=False),
        sa.Column('input', sa.String(500), nullable=False),
        sa.Column('max_partition_size', sa.BigInteger, nullable=False),
        sa.Column('created_at', sa.DateTime(
            timezone=False), server_default=func.now()),
        sa.Column('status', sa.Enum('STARTED', 'RUNNING', 'FAILED',
                  'SUCCESS', name='run_status'), nullable=True),
        sa.Column('updated_at', sa.DateTime(
            timezone=False), onupdate=func.now())
    )


def downgrade() -> None:
    op.drop_table('run')
    op.execute('DROP TYPE run_status')
