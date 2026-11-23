"""Crear tabla de tareas por evento."""

from alembic import op
import sqlalchemy as sa


revision = "c4d5e6f7a801"
down_revision = "b303d9dbf5e5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tareas",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "evento_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "titulo",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "descripcion",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "completada",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "length(trim(titulo)) > 0",
            name="ck_tareas_titulo_no_vacio",
        ),
        sa.ForeignKeyConstraint(
            ["evento_id"],
            ["eventos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_tareas_evento_id",
        "tareas",
        ["evento_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        "ix_tareas_evento_id",
        table_name="tareas",
    )
    op.drop_table("tareas")