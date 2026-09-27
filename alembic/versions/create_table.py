"""create emails table

Revision ID: 0001
Revises:
Create Date: 2026-09-27
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "emails",
        sa.Column("gmail_id", sa.String(), primary_key=True),
        sa.Column("sender", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=True),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("urgency_score", sa.String(), nullable=True),
        sa.Column("needs_reply", sa.Boolean(), nullable=True),
        sa.Column("draft_reply", sa.Text(), nullable=True),
        sa.Column(
            "fetched_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade():
    op.drop_table("emails")