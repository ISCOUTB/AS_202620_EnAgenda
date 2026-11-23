"""Agregar preferencia de color por cuenta, conservando usuarios existentes."""
from alembic import op
import sqlalchemy as sa
revision = "d91f6a2c804e"
down_revision = "b303d9dbf5e5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("usuarios", sa.Column("tema", sa.String(16), nullable=False, server_default="violeta"))


def downgrade():
    op.drop_column("usuarios", "tema")
