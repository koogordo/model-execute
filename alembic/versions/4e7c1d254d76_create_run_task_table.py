"""create run task table

Revision ID: 4e7c1d254d76
Revises: b9b654b23fa4
Create Date: 2022-08-19 15:39:57.467794

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '4e7c1d254d76'
down_revision = 'b9b654b23fa4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'run_task',
        sa.Column('id', UUID(as_uuid=True),
                  primary_key=True, default=uuid.uuid4),
        sa.Column('run_id', UUID(as_uuid=True), sa.ForeignKey(
            'run.id'), nullable=False),
        sa.Column('beginning_offset', sa.BigInteger, nullable=True),
        sa.Column('ending_offset', sa.BigInteger, nullable=True),
        sa.Column('output', sa.String(500), nullable=True),
        sa.Column('partition_num', sa.Integer, nullable=False),
        sa.Column('status', sa.Enum('SCHEDULED', 'RUNNING', 'FAILED',
                  'SUCCESS', 'PARTITIONING', name='task_status'), nullable=True),
        sa.Column('created_at', sa.DateTime(
            timezone=False), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(
            timezone=False), onupdate=func.now())
    )


def downgrade() -> None:
    op.drop_table('run_task')
    op.execute('DROP TYPE task_status')
