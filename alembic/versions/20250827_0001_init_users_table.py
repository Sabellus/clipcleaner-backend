"""init users table"""

from alembic import op
import sqlalchemy as sa

# ревизии
revision = "20250827_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("uid", sa.String(), primary_key=True, nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_seen",  sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

def downgrade():
    op.drop_table("users")