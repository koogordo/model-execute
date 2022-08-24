"""create model table

Revision ID: f3b1ccf09396
Revises:
Create Date: 2022-08-16 13:40:40.891266

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'f3b1ccf09396'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'model',
        sa.Column('id', UUID(as_uuid=True),
                  primary_key=True, default=uuid.uuid4, unique=True),
        sa.Column('name', sa.String(150), unique=True, nullable=False),
        sa.Column('artifacts', sa.String(250), nullable=False),
        sa.Column('file_name', sa.String(75), nullable=False),
        sa.Column('predict_method', sa.String(50), nullable=False),
        sa.Column('status', sa.Enum('ONLINE', 'OFFLINE',
                  name='model_status'), nullable=False),
        sa.Column('created_at', sa.DateTime(
            timezone=False), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(
            timezone=False), onupdate=func.now())
    )


def downgrade() -> None:
    op.drop_table('model')
    op.execute('DROP TYPE model_status')
