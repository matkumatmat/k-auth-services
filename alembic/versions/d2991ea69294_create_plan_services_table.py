"""create_plan_services_table

Revision ID: d2991ea69294
Revises: b8352b457691
Create Date: 2026-01-20 16:09:54.091233

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd2991ea69294'
down_revision: str | Sequence[str] | None = 'b8352b457691'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'plan_services',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('plan_id', UUID(as_uuid=True), sa.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False),
        sa.Column('service_id', UUID(as_uuid=True), sa.ForeignKey('services.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("(now() AT TIME ZONE 'utc')"), nullable=False),
        sa.UniqueConstraint('plan_id', 'service_id', name='uq_plan_service')
    )
    op.create_index('idx_plan_services_plan_id', 'plan_services', ['plan_id'])
    op.create_index('idx_plan_services_service_id', 'plan_services', ['service_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_plan_services_service_id', table_name='plan_services')
    op.drop_index('idx_plan_services_plan_id', table_name='plan_services')
    op.drop_table('plan_services')
